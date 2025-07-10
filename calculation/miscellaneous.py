#!/usr/bin/env python3
"""
season.py

Provides:
 - calculate_season(date) → str
 - CLI entrypoint for testing
 - Optional Flask blueprint if Flask is installed
"""
# season.py

from datetime import datetime, date
from flask import Blueprint, request, jsonify

season_bp = Blueprint('season_bp', __name__)

def get_western_season(d: date) -> str:
    """
    Return the astronomical season name for Northern Hemisphere:
      - Spring:  March 20 – June 20
      - Summer:  June 21 – September 22
      - Autumn:  September 23 – December 20
      - Winter:  December 21 – March 19
    """
    Y = d.year
    # define season start dates
    spring_start = date(Y,  3, 20)
    summer_start = date(Y,  6, 21)
    autumn_start = date(Y,  9, 23)
    winter_start = date(Y, 12, 21)

    if spring_start <= d < summer_start:
        return "Spring"
    if summer_start <= d < autumn_start:
        return "Summer"
    if autumn_start <= d < winter_start:
        return "Autumn"
    # covers Winter (end of year) and Jan–Mar
    return "Winter"

def get_chinese_season_by_month(month: int) -> str:
    """
    Map lunar month (1–12) to one of the four Chinese seasons,
    via its Earthly Branch association:

      1→Yin, 2→Mao, 3→Chen  → Spring
      4→Si, 5→Wu, 6→Wei     → Summer
      7→Shen, 8→You, 9→Xu   → Autumn
      10→Hai,11→Zi,12→Chou  → Winter
    """
    # Earthly Branches in order starting at index 0 for Zi:
    branches = ["Zi","Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"]
    # lunar month 1 is Yin → branches[ (1+1) % 12 == 2 ]
    branch = branches[(month + 1) % 12]

    season_map = {
      "Yin":"Spring",   "Mao":"Spring",   "Chen":"Spring",
      "Si":"Summer",    "Wu":"Summer",    "Wei":"Summer",
      "Shen":"Autumn",  "You":"Autumn",   "Xu":"Autumn",
      "Hai":"Winter",   "Zi":"Winter",    "Chou":"Winter"
    }
    return season_map[branch]



if __name__ == "__main__":
    """
    Interactive CLI:
      Prompt: Enter date (YYYY MM DD)
      Example: 2025 07 10
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

    season = calculate_westernseason(dt)
    print(f"Date: {dt} → Season: {season}")
