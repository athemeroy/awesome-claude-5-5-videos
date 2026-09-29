#!/usr/bin/env python3
"""Compatibility entry point for the unified public statistical charts.

Use generate_stat_charts.py for generation and --check; this entry point shares
that renderer so it cannot overwrite the domain chart with an older design.
"""

from generate_stat_charts import main


if __name__ == "__main__":
    raise SystemExit(main())
