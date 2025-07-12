#!/usr/bin/env python3
# bazi_calc.py

from datetime import datetime
from apps import create_app, db
from apps.config import config_dict
from calculation.chinese_calendar import fixed_from_gregorian, chinese_from_fixed
from apps.data.tables import Stems, HiddenStem, StemOrgan, BranchOrgan


def calculate_bazi(year: int,
                   month: int,
                   day: int,
                   hour: int = None,
                   minute: int = 0) -> dict:
    """
    Calculate the Four Pillars (BaZi) for a given date/time.

    Returns a dict with:
      - year  : { GM, Stem, Branch, HS }
      - month : (to be implemented)
      - day   : (to be implemented)
      - hour  : (to be implemented)
    """
    # Ensure Flask app context for DB
    app = create_app(config_dict['Debug'])
    with app.app_context():
        # 1) Fixed date (Rata Die) for the given Gregorian date
        fixed = fixed_from_gregorian(year, month, day)

        # 2) Compute ChineseDate → cd.name is "Stem-Branch", e.g. "Jia-Zi"
        cd = chinese_from_fixed(fixed)
        stem_pinyin, branch_pinyin = cd.name.split('-')

        # 3) Lookup GanMen (GM) in your Stems table
        gm_rec = db.session.query(Stems).filter_by(name=stem_pinyin).first()
        gm = gm_rec.gm if gm_rec else None

        # 4a) Lookup Stem details from StemOrgan
        def lookup_stem(pinyin):
            rec = db.session.query(StemOrgan).filter_by(pinyin=pinyin).first()
            if rec:
                return {
                    'pinyin': rec.pinyin,
                    'chinese_char': rec.chinese_char,
                    'organ': rec.organ,
                    'phase': rec.phase,
                }
            return {'pinyin': pinyin}

        # 4b) Lookup Branch details from BranchOrgan
        def lookup_branch(pinyin):
            rec = db.session.query(BranchOrgan).filter_by(pinyin=pinyin).first()
            if rec:
                return {
                    'pinyin': rec.pinyin,
                    'chinese_char': rec.chinese_char,
                    'organ': rec.organ,
                    'phase': rec.phase,
                }
            return {'pinyin': pinyin}

        stem_info = lookup_stem(stem_pinyin)
        branch_info = lookup_branch(branch_pinyin)

        # 5) Lookup Hidden Stems for this Earthly Branch (JSON list of pinyin)
        hs_rec = db.session.query(HiddenStem).filter_by(branch=branch_pinyin).first()
        hidden_pinyins = hs_rec.hidden_stems if hs_rec and hs_rec.hidden_stems else []
        hidden_info = [lookup_stem(h) for h in hidden_pinyins]

        # Assemble year pillar under 'year' key
        year_pillar = {
            "GM": gm,
            "Stem": stem_info,
            "Branch": branch_info,
            "HS": hidden_info
        }

        return {
            "year": year_pillar,
            # placeholders for future month/day/hour pillars
            "month": {},
            "day": {},
            "hour": {}
        }

if __name__ == "__main__":
    # Simple interactive CLI test
    raw = input("Enter date and optional hour (YYYY MM DD [HH]): ").split()
    try:
        y, mo, d = map(int, raw[:3])
        h = int(raw[3]) if len(raw) >= 4 else None
    except ValueError:
        print("Invalid input. Use: 2025 07 10 14")
        exit(1)

    result = calculate_bazi(y, mo, d, h)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
