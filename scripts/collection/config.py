"""Configuration, model taxonomy, and repository paths."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

START_MARKER = "<!-- collection-summary:start -->"
END_MARKER = "<!-- collection-summary:end -->"

POST_URL_RE = re.compile(r"https://x\.com/([^/]+)/status/(\d+)")
LEGACY_LEDGER_RE = re.compile(r"claude55-source-review-(\d{4}-\d{2}-\d{2})(-[a-z0-9-]+)?\.csv")
MODERN_LEDGER_RE = re.compile(r"source-review-(\d{4}-\d{2}-\d{2})(-[a-z0-9-]+)?\.csv")


@dataclass(frozen=True)
class ModelGroup:
    key: str
    slug: str
    label_en: str
    label_zh: str
    pattern: re.Pattern[str]


MODEL_GROUPS: tuple[ModelGroup, ...] = (
    ModelGroup(
        key="Fable 5.2",
        slug="fable-5-2",
        label_en="Fable 5.2",
        label_zh="Fable 5.2",
        pattern=re.compile(r"\bFable\s+5\.2\b", re.I),
    ),
    ModelGroup(
        key="Opus 5.5",
        slug="opus-5-5",
        label_en="Opus 5.5",
        label_zh="Opus 5.5",
        pattern=re.compile(r"\bOpus\s+5\.5\b", re.I),
    ),
    ModelGroup(
        key="Sonnet 5.5",
        slug="sonnet-5-5",
        label_en="Sonnet 5.5",
        label_zh="Sonnet 5.5",
        pattern=re.compile(r"\bSonnet\s+5\.5\b", re.I),
    ),
    ModelGroup(
        key="Haiku 5.5",
        slug="haiku-5-5",
        label_en="Haiku 5.5",
        label_zh="Haiku 5.5",
        pattern=re.compile(r"\bHaiku\s+5\.5\b", re.I),
    ),
    ModelGroup(
        key="Fable (pre-release)",
        slug="fable-pre-release",
        label_en="Fable (pre-release / suspected 5.5)",
        label_zh="Fable（早期灰度 / 疑似 5.5）",
        pattern=re.compile(r"\bFable\b(?!\s+5\.2\b)", re.I),
    ),
)

MODEL_KEYS: tuple[str, ...] = tuple(m.key for m in MODEL_GROUPS)

NEW_CASES_2026_09_27: dict[str, tuple[str, str, str]] = {
    "2104131805175844923": ("Handmade launch film versus code remake", "手工发布片与代码改编", "Opus 5.5"),
    "2104009748874141941": ("Green-screen clip and edited version", "绿幕原片与编辑版本", "Opus 5.5 + Grok footage"),
    "2103923067277733943": ("Wear OS product film with real assets", "使用真实素材的 Wear OS 产品片", "Opus 5.5 + Fable 5.1"),
    "2104039075175182487": ("Personal story with ClaudeAnimationBase", "复用 ClaudeAnimationBase 的个人故事", "Opus 5.5"),
    "2104021764863078697": ("Supplied draft, images and external audio", "提供草稿、图像与外部音频", "Opus 5.5 + GPT-6 Astra + ElevenLabs"),
    "2103869704955900023": ("Multi-tool anime music video", "多工具动漫音乐视频", "Opus 5.5 + external media models"),
    "2104011150471917838": ("Video with checked data slots", "带数据槽校验的视频", "Opus 5.5"),
}
