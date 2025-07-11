#!/usr/bin/env python3
"""
season.py

Provides:
  - get_chinese_season_by_month(month) → str
  - CLI entrypoint for testing Chinese season with branch
"""
from datetime import date

def get_chinese_season_by_month(month: int) -> (str, str):
    """
    Map lunar month (1–12) to Chinese season and its Earthly Branch:
      1→Yin, 2→Mao, 3→Chen  → Spring
      4→Si, 5→Wu, 6→Wei     → Summer
      7→Shen,8→You,9→Xu     → Autumn
      10→Hai,11→Zi,12→Chou  → Winter

    Returns a tuple (season, branch).
    """
    branches = ["Zi","Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"]
    season_map = {
      "Yin":"Spring",   "Mao":"Spring",   "Chen":"Spring",
      "Si":"Summer",    "Wu":"Summer",    "Wei":"Summer",
      "Shen":"Autumn",  "You":"Autumn",   "Xu":"Autumn",
      "Hai":"Winter",   "Zi":"Winter",    "Chou":"Winter"
    }
    # lunar month 1 maps to branches[2] == "Yin"
    branch = branches[(month + 1) % 12]
    season = season_map[branch]
    return season, branch

if __name__ == "__main__":
    """
    Interactive CLI:
      Prompt: Enter date (YYYY MM DD)
      Example: 2025 07 10
    Prints: Date: 2025-07-10 → Chinese season: Summer (Wu)
    """
    raw = input("Enter date (YYYY MM DD): ").split()
    try:
        y, mo, d = map(int, raw[:3])
    except ValueError:
        print("Invalid input. Use: YYYY MM DD, e.g. 2025 07 10")
        exit(1)

    try:
        dt = date(y, mo, d)
    except ValueError as e:
        print(f"Invalid date: {e}")
        exit(1)

    season, branch = get_chinese_season_by_month(dt.month)
    print(f"Date: {dt} → Chinese season: {season} ({branch})")

