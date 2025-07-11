#!/usr/bin/env python3
# bazi_calc.py

from datetime import datetime
from apps import create_app, db
from apps.config import config_dict
from chinese_calendar import fixed_from_gregorian, chinese_from_fixed
from apps.data.tables import Stems, HiddenStem


def calculate_bazi(year: int,
                   month: int,
                   day: int,
                   hour: int = None,
                   minute: int = 0) -> dict:
    """
    Calculate the Four Pillars (BaZi) for a given date/time.

    Returns a dict:
      - GM     : GanMen for the year's Heavenly Stem (from Stems.gm)
      - Stem   : Heavenly Stem of the year (Jia, Yi, …)
      - Branch : Earthly Branch of the year (Zi, Chou, …)
      - HS     : Hidden Stems for the Earth's Branch (from HiddenStem.hidden)
    """
    # 1) Fixed date (Rata Die) for the given Gregorian date
    fixed = fixed_from_gregorian(year, month, day)

    # 2) Compute ChineseDate → cd.name is "Stem-Branch", e.g. "Jia-Zi"
    cd = chinese_from_fixed(fixed)
    stem, branch = cd.name.split('-')

    # 3) Lookup GanMen (GM) in your Stems table
    rec = db.session.query(Stems).filter_by(name=stem).first()
    gm = rec.gm if rec else None

    # 4) Lookup Hidden Stems for this Earthly Branch
    hs_rec = db.session.query(HiddenStem).filter_by(branch=branch).first()
    hidden_stems = hs_rec.hidden if hs_rec else None

    return {
        "GM": gm,
        "Stem": stem,
        "Branch": branch,
        "HS": hidden_stems
    }


if __name__ == "__main__":
    # Create Flask app with proper configuration
    app = create_app(config_dict['Debug'])
    
    # Simple interactive CLI test
    raw = input("Enter date and optional hour (YYYY MM DD [HH]): ").split()
    try:
        y, mo, d = map(int, raw[:3])
        h = int(raw[3]) if len(raw) >= 4 else None
    except ValueError:
        print("Invalid input. Use: 2025 07 10 14")
        exit(1)

    # Run the calculation within Flask application context
    with app.app_context():
        result = calculate_bazi(y, mo, d, h)
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))