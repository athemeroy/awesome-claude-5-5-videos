#!/usr/bin/env python3
"""Record dated engagement observations from the public X post interface.

The primary pass reads the rendered post and hovers its view counter to expose
X's exact view-count tooltip. An optional second pass fills incomplete rows
from the same public post page's HTML response, validating the primary post ID,
creation time, and compact UI displays. Neither pass logs in or calls private
or mirror APIs. Compact like counts remain non-exact until the optional HTML
pass verifies an exact count; otherwise conservative display-derived bounds
are stored separately.

Collection uses an existing Chrome DevTools endpoint and Playwright. Checking
an exported CSV needs only the Python standard library. One row is retained
for every reviewed case, including failures and unattempted posts.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import tempfile
import time
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "data/cases.csv"
BASELINE = ROOT / "data/case-engagement-observed.csv"
POST_URL = re.compile(r"^https://x\.com/[^/]+/status/(\d+)$")
EXACT = re.compile(r"^(?:\d{1,3}(?:,\d{3})+|\d+)$")
COMPACT = re.compile(r"^(\d+(?:\.\d+)?)(万|亿|[KMB])$", re.IGNORECASE)
METHOD = "x_public_post_ui_hover"
HTML_METHOD = "x_public_post_html"
FIELDS = (
    "post_id", "source_url", "post_created_at_utc", "likes", "views",
    "likes_display", "views_display", "likes_lower_bound", "likes_upper_bound",
    "observed_at_utc", "source_method", "page_http_status", "page_url",
    "status", "error",
)


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def parse_utc(value: str) -> dt.datetime:
    value = value.replace("Z", "+00:00")
    result = dt.datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError(f"Timestamp has no offset: {value}")
    return result.astimezone(dt.timezone.utc)


def load_inputs() -> list[dict[str, str]]:
    with CASES.open(encoding="utf-8-sig", newline="") as stream:
        cases = list(csv.DictReader(stream))
    with BASELINE.open(encoding="utf-8-sig", newline="") as stream:
        baseline = list(csv.DictReader(stream))
    if len(cases) != 168 or len(baseline) != 168:
        raise ValueError("Expected 168 reviewed cases and 168 baseline observations")
    old = {row["post_id"]: row for row in baseline}
    if len(old) != 168:
        raise ValueError("Duplicate baseline post ID")
    result = []
    for case in cases:
        url = case["source_url"]
        match = POST_URL.fullmatch(url)
        if not match:
            raise ValueError(f"Unexpected case URL: {url}")
        post_id = match.group(1)
        if post_id not in old or old[post_id]["source_url"] != url:
            raise ValueError(f"Case/baseline mismatch: {url}")
        parse_utc(old[post_id]["post_created_at_utc"])
        result.append({field: "" for field in FIELDS} | {
            "post_id": post_id,
            "source_url": url,
            "post_created_at_utc": old[post_id]["post_created_at_utc"],
            "status": "not_attempted",
        })
    if len({row["post_id"] for row in result}) != 168:
        raise ValueError("Duplicate case post ID")
    return result


def count_and_bounds(display: str) -> tuple[str, str, str]:
    """Return exact, lower, upper; bounds include rounding and truncation.

    For example, `1.6万` is represented by [15,500, 16,999]. The interval is
    deliberately broad because X does not disclose the compacting rule here.
    It is an interval inferred from a display string, not an X count.
    """
    display = re.sub(r"\s+", "", display)
    if EXACT.fullmatch(display):
        number = str(int(display.replace(",", "")))
        return number, number, number
    match = COMPACT.fullmatch(display)
    if not match:
        return "", "", ""
    mantissa = Decimal(match.group(1))
    scale = {"万": 10_000, "亿": 100_000_000, "K": 1_000,
             "M": 1_000_000, "B": 1_000_000_000}[match.group(2).upper()]
    places = len(match.group(1).partition(".")[2])
    step = Decimal(scale) / (Decimal(10) ** places)
    nominal = mantissa * scale
    lower = max(0, int(nominal - step / 2))
    upper = int(nominal + step - 1)
    return "", str(lower), str(upper)


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="",
                                     dir=path.parent, prefix=f".{path.name}.",
                                     delete=False) as stream:
        tmp = Path(stream.name)
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    os.chmod(tmp, 0o644)
    os.replace(tmp, path)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError(f"Unexpected columns: {path}")
        return list(reader)


def validate(path: Path, require_complete: bool = False) -> dict[str, int]:
    expected = load_inputs()
    rows = read_rows(path)
    if len(rows) != len(expected):
        raise ValueError(f"Expected {len(expected)} rows, found {len(rows)}")
    counts = {key: 0 for key in ("ok", "partial", "failed", "not_attempted")}
    for row, source in zip(rows, expected, strict=True):
        for field in ("post_id", "source_url", "post_created_at_utc"):
            if row[field] != source[field]:
                raise ValueError(f"Input key mismatch: {field} {row['post_id']}")
        state = row["status"]
        if state not in counts:
            raise ValueError(f"Unknown status {state!r}: {row['post_id']}")
        counts[state] += 1
        if state == "not_attempted":
            if any(row[field] for field in FIELDS[3:-2]):
                raise ValueError(f"Unattempted row has observations: {row['post_id']}")
            continue
        if row["source_method"] not in {METHOD, HTML_METHOD} or not row["observed_at_utc"]:
            raise ValueError(f"Attempt lacks method/time: {row['post_id']}")
        if parse_utc(row["observed_at_utc"]) < parse_utc(row["post_created_at_utc"]):
            raise ValueError(f"Observation predates post: {row['post_id']}")
        for field in ("likes", "views", "likes_lower_bound", "likes_upper_bound"):
            if row[field] and (not row[field].isdigit() or int(row[field]) < 0):
                raise ValueError(f"Invalid {field}: {row['post_id']}")
        if any(row[field] for field in ("likes", "views", "likes_lower_bound")):
            landed = POST_URL.fullmatch(row["page_url"].split("?")[0].rstrip("/"))
            if not landed or landed.group(1) != row["post_id"]:
                raise ValueError(f"Metric-bearing page URL mismatches ID: {row['post_id']}")
        if row["source_method"] == METHOD and not row["views_display"] and any(
            row[field] for field in ("likes", "likes_display", "likes_lower_bound", "likes_upper_bound")
        ):
            raise ValueError(f"UI likes lack a verified target-post view link: {row['post_id']}")
        exact, lower, upper = count_and_bounds(row["likes_display"])
        if row["source_method"] == METHOD:
            if (row["likes"], row["likes_lower_bound"], row["likes_upper_bound"]) != (exact, lower, upper):
                raise ValueError(f"Like display/bounds mismatch: {row['post_id']}")
        elif row["likes"]:
            if row["likes_lower_bound"] != row["likes"] or row["likes_upper_bound"] != row["likes"]:
                raise ValueError(f"HTML exact likes need equal bounds: {row['post_id']}")
            if exact and row["likes"] != exact:
                raise ValueError(f"HTML likes conflict with exact UI display: {row['post_id']}")
            if not exact and lower and upper and not int(lower) <= int(row["likes"]) <= int(upper):
                raise ValueError(f"HTML likes conflict with compact UI display: {row['post_id']}")
        if row["views"] and not row["views_display"] and row["source_method"] == METHOD:
            raise ValueError(f"Exact views lack displayed counter: {row['post_id']}")
        if row["views"]:
            shown_exact, shown_lower, shown_upper = count_and_bounds(row["views_display"])
            if shown_exact and row["views"] != shown_exact:
                raise ValueError(f"Exact view display conflicts with count: {row['post_id']}")
            if shown_lower and shown_upper:
                margin = max(10, int(shown_upper) // 10)
                if not max(0, int(shown_lower) - margin) <= int(row["views"]) <= int(shown_upper) + margin:
                    raise ValueError(f"View tooltip conflicts with displayed counter: {row['post_id']}")
        expected_state = ("ok" if row["likes"] and row["views"] else
                          "partial" if row["likes"] or row["views"] else "failed")
        if state != expected_state:
            raise ValueError(f"Metrics/status mismatch: {row['post_id']}")
    if require_complete and counts["not_attempted"]:
        raise ValueError(f"Unattempted cases remain: {counts['not_attempted']}")
    return counts


def capture(page, row: dict[str, str]) -> dict[str, str]:
    """Read one post. A failed field is left blank rather than estimated."""
    result = row.copy()
    result.update({field: "" for field in FIELDS[3:-2]})
    result["status"] = "failed"
    result["error"] = ""
    issues = []
    try:
        response = page.goto(row["source_url"], wait_until="domcontentloaded", timeout=25_000)
        result["page_http_status"] = str(response.status) if response else ""
        result["page_url"] = page.url
        landed = POST_URL.fullmatch(page.url.split("?")[0].rstrip("/"))
        if not landed or landed.group(1) != row["post_id"]:
            raise ValueError(f"Post ID changed at {page.url}")
        if response and response.status != 200:
            raise ValueError(f"HTTP {response.status}")
        view_link = page.locator(
            f'a[data-base-ui-tooltip-trigger][href$="/status/{row["post_id"]}"]:has(> div)'
        ).first
        view_link.wait_for(state="visible", timeout=7_000)
        article = view_link.locator("xpath=ancestor::article[1]")
        like = article.locator('button[aria-label="Like"], button[aria-label="Unlike"]').first
        try:
            result["likes_display"] = like.inner_text(timeout=4_000).strip()
            exact, lower, upper = count_and_bounds(result["likes_display"])
            result["likes"], result["likes_lower_bound"], result["likes_upper_bound"] = exact, lower, upper
            if not exact:
                issues.append("like_count_compact_or_unrecognized")
        except Exception as exc:
            issues.append(f"like_button_unavailable:{type(exc).__name__}")

        try:
            text = view_link.inner_text(timeout=4_000).strip()
            result["views_display"] = text.splitlines()[0].strip()
            if not result["views_display"]:
                issues.append("view_display_empty")
            # A real pointer move is required: synthetic DOM events do not
            # reliably open the Base UI tooltip on X.
            page.mouse.move(1, 1)
            page.wait_for_timeout(300)
            view_link.hover(timeout=6_000)
            page.wait_for_function(
                """() => [...document.querySelectorAll('[data-base-ui-portal]')]
                  .some(e => /^(?:\\d{1,3}(?:,\\d{3})+|\\d+)$/.test(e.innerText.trim()))""",
                timeout=7_000,
            )
            tips = page.locator("[data-base-ui-portal]").all_inner_texts()
            exact_views = next((text.strip() for text in tips if EXACT.fullmatch(text.strip())), "")
            if not exact_views:
                raise ValueError("numeric view tooltip absent")
            result["views"] = str(int(exact_views.replace(",", "")))
        except Exception as exc:
            issues.append(f"view_tooltip_unavailable:{type(exc).__name__}")
    except Exception as exc:
        issues.append(f"page_unavailable:{type(exc).__name__}:{str(exc)[:110]}")
    result["observed_at_utc"] = now_utc()
    result["source_method"] = METHOD
    result["status"] = ("ok" if result["likes"] and result["views"] else
                        "partial" if result["likes"] or result["views"] else "failed")
    result["error"] = re.sub(r"\s+", " ", ";".join(issues)).strip()[:300]
    return result


def html_counts(document: str, row: dict[str, str]) -> tuple[int, int]:
    """Find the primary post in X's public page response, not a quote/reply.

    The response can contain the target ID repeatedly, including reply links.
    The direct ``tweet_result_by_rest_id`` result identifies the primary post.
    Its first ``counts`` block and a matching legacy ``rest_id``/``views`` block
    supply counts. A matching creation time checks the association once more.
    An unrecognized response shape raises rather than guessing from neighbors.
    """
    post_id = row["post_id"]
    wrapper = re.search(
        r'tweet_result_by_rest_id:\$R\[\d+\]=\{id:"[^"]+",rest_id:"' +
        re.escape(post_id) + r'",result:\$R\[\d+\]=\{',
        document,
    )
    if not wrapper:
        raise ValueError("Primary post result absent from public HTML")
    section = document[wrapper.end():wrapper.end() + 25_000]
    quote = section.find("quoted_status_result:")
    root_prefix = section[:min(8_000, quote if quote >= 0 else 8_000)]
    likes_match = re.search(
        r'counts:\$R\[\d+\]=\{[^}]{0,500}favorite_count:(\d+)', root_prefix
    )
    created_match = re.search(r'created_at_ms:(\d+)', root_prefix)
    if not likes_match or not created_match:
        raise ValueError("Primary post count/creation fields missing")
    expected_ms = int(parse_utc(row["post_created_at_utc"]).timestamp() * 1000)
    if abs(int(created_match.group(1)) - expected_ms) > 1000:
        raise ValueError("Primary post creation time disagrees with archived case")
    # Legacy rest_id followed by url_entities and views refers to the post
    # itself. Mere proximity to the ID can instead select a quoted/reply post.
    view_candidates = []
    for match in re.finditer(r'rest_id:"' + re.escape(post_id) + r'",url_entities:', section):
        following = section[match.end():match.end() + 3_000]
        view = re.search(r'views:\$R\[\d+\]=\{count:"(\d+)"', following)
        if not view:
            continue
        if re.search(r'rest_id:"\d+"', following[:view.start()]):
            continue
        view_candidates.append(int(view.group(1)))
    if not view_candidates:
        raise ValueError("Primary post exact views missing")
    if len(set(view_candidates)) != 1:
        raise ValueError("Conflicting primary-post views in one response")
    return int(likes_match.group(1)), view_candidates[0]


def capture_html(page, row: dict[str, str]) -> dict[str, str]:
    """Replace an incomplete row only when both exact HTML counts validate."""
    response = page.goto(row["source_url"], wait_until="domcontentloaded", timeout=25_000)
    if not response or response.status != 200:
        raise ValueError(f"Public post page HTTP {response.status if response else 'none'}")
    landed = POST_URL.fullmatch(page.url.split("?")[0].rstrip("/"))
    if not landed or landed.group(1) != row["post_id"]:
        raise ValueError(f"Post ID changed at {page.url}")
    likes, views = html_counts(response.text(), row)
    updated = row.copy()
    updated.update({
        "likes": str(likes), "views": str(views),
        "likes_lower_bound": str(likes), "likes_upper_bound": str(likes),
        "likes_display": "", "views_display": "",
        "observed_at_utc": now_utc(), "source_method": HTML_METHOD,
        "page_http_status": "200", "page_url": page.url,
        "status": "ok", "error": "",
    })
    # A reply's page can show its parent first. Only the article containing
    # the target post's own view counter may supply display strings.
    view = page.locator(
        f'a[data-base-ui-tooltip-trigger][href$="/status/{row["post_id"]}"]:has(> div)'
    ).first
    if view.count():
        article = view.locator("xpath=ancestor::article[1]")
        like = article.locator('button[aria-label="Like"], button[aria-label="Unlike"]').first
        if like.count():
            updated["likes_display"] = like.inner_text(timeout=3_000).strip()
        updated["views_display"] = view.inner_text(timeout=3_000).strip().splitlines()[0].strip()
    return updated


def collect(path: Path, rows: list[dict[str, str]], ids: set[str] | None,
            limit: int | None, cdp: str, interval: float,
            retry_missing_views: bool, fill_from_html: bool) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Collection needs Playwright; --check uses only Python stdlib") from exc
    if fill_from_html and any(row["status"] == "not_attempted" for row in rows):
        raise ValueError("Finish the UI pass before HTML supplementation")
    pending = [row for row in rows if
               ((fill_from_html and row["status"] in {"partial", "failed"}) or
                (not fill_from_html and
                 (row["status"] == "not_attempted" or
                  (retry_missing_views and row["status"] in {"partial", "failed"} and
                   not row["views"])))) and
               (ids is None or row["post_id"] in ids)]
    if limit is not None:
        pending = pending[:limit]
    if not pending:
        print(json.dumps({"message": "No unattempted matching posts", "path": str(path)}))
        return
    by_id = {row["post_id"]: index for index, row in enumerate(rows)}
    consecutive_failures = 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(cdp)
        if not browser.contexts:
            raise RuntimeError("CDP browser has no existing context")
        page = browser.contexts[0].new_page()
        page.set_default_timeout(7_000)
        try:
            for number, row in enumerate(pending, 1):
                started = time.monotonic()
                if fill_from_html:
                    try:
                        captured = capture_html(page, row)
                        trial = rows.copy()
                        trial[by_id[row["post_id"]]] = captured
                        write_rows(path, trial)
                        try:
                            validate(path)
                        except Exception:
                            write_rows(path, rows)
                            raise
                        rows[:] = trial
                        html_error = ""
                    except Exception as exc:
                        captured = row
                        html_error = re.sub(r"\s+", " ", str(exc)).strip()[:200]
                else:
                    captured = capture(page, row)
                    rows[by_id[row["post_id"]]] = captured
                    write_rows(path, rows)
                    html_error = ""
                print(json.dumps({"number": number, "post_id": row["post_id"],
                                  "status": captured["status"], "likes": captured["likes"],
                                  "views": captured["views"], "likes_display": captured["likes_display"],
                                  "error": html_error or captured["error"]}, ensure_ascii=False), flush=True)
                unsuccessful = bool(html_error) if fill_from_html else captured["status"] == "failed"
                consecutive_failures = consecutive_failures + 1 if unsuccessful else 0
                if consecutive_failures >= 3:
                    print("Stopped after three consecutive complete failures; remaining rows stay not_attempted.",
                          file=sys.stderr)
                    break
                time.sleep(max(0, interval - (time.monotonic() - started)))
        finally:
            page.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).date().isoformat(),
                        help="Date label for the output file in UTC")
    parser.add_argument("--output", type=Path, help="Override the dated CSV output path")
    parser.add_argument("--check", action="store_true", help="Validate an existing CSV without browser access")
    parser.add_argument("--require-complete", action="store_true",
                        help="With --check, fail if any row is not_attempted")
    parser.add_argument("--resume", action="store_true", help="Continue rows marked not_attempted")
    parser.add_argument("--retry-missing-views", action="store_true",
                        help="With --resume, also re-read attempted rows lacking exact views")
    parser.add_argument("--fill-from-html", action="store_true",
                        help="With --resume, fill only incomplete rows from X's public post HTML")
    parser.add_argument("--ids", help="Comma-separated post IDs for a bounded pilot")
    parser.add_argument("--limit", type=int, help="Maximum unattempted posts in this invocation")
    parser.add_argument("--cdp", default="http://127.0.0.1:9333", help="Existing Chrome CDP endpoint")
    parser.add_argument("--min-interval", type=float, default=1.0,
                        help="Minimum seconds between post reads (default: 1)")
    args = parser.parse_args()
    dt.date.fromisoformat(args.date)
    if args.limit is not None and args.limit <= 0:
        parser.error("--limit must be positive")
    if args.min_interval < 1:
        parser.error("--min-interval must be at least 1 second")
    path = args.output or ROOT / "data" / f"case-engagement-refresh-{args.date}.csv"
    if args.check:
        print(json.dumps({"path": str(path),
                          "status_counts": validate(path, args.require_complete)}, ensure_ascii=False))
        return
    if args.retry_missing_views and not args.resume:
        parser.error("--retry-missing-views needs --resume")
    if args.fill_from_html and not args.resume:
        parser.error("--fill-from-html needs --resume")
    if args.fill_from_html and args.retry_missing_views:
        parser.error("Choose one incomplete-row method at a time")
    if path.exists():
        if not args.resume:
            parser.error(f"Output already exists: {path}; use --resume to continue unattempted rows")
        rows = read_rows(path)
        validate(path)
    else:
        rows = load_inputs()
        write_rows(path, rows)
    ids = set(args.ids.split(",")) if args.ids else None
    if ids is not None and not ids <= {row["post_id"] for row in rows}:
        parser.error("--ids includes a post ID outside the reviewed cases")
    collect(path, rows, ids, args.limit, args.cdp, args.min_interval,
            args.retry_missing_views, args.fill_from_html)
    print(json.dumps({"path": str(path), "status_counts": validate(path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
