#!/usr/bin/env python3
# bazi_calc.py
from sqlalchemy import nullsfirst

from apps import create_app, db
from apps.config import config_dict
from calculation.chinese_calendar import fixed_from_gregorian, chinese_from_fixed, ChineseDate
from apps.data.tables import Stems, HiddenStem, StemOrgan, BranchOrgan


def lookup_stem(pinyin: str) -> dict:
    rec = db.session.query(StemOrgan).filter_by(pinyin=pinyin).first()
    if rec:
        return {
            'pinyin': rec.pinyin,
            'chinese_char': rec.chinese_char,
            'organ': rec.organ,
            'phase': rec.phase,
        }
    return {'pinyin': pinyin}


def lookup_branch(pinyin: str) -> dict:
    rec = db.session.query(BranchOrgan).filter_by(pinyin=pinyin).first()
    if rec:
        return {
            'pinyin': rec.pinyin,
            'chinese_char': rec.chinese_char,
            'organ': rec.organ,
            'phase': rec.phase,
        }
    return {'pinyin': pinyin}


def calculate_year_pillar(date: ChineseDate) -> dict:
    """
    Return the 'year' pillar dict for the given Gregorian date.
    """

    cd = chinese_from_fixed(date)                # ChineseDate
    stem_pinyin, branch_pinyin = cd.name.split('-')

    # Great Movement (GM)
    gm_rec = db.session.query(Stems).filter_by(name=stem_pinyin).first()
    gm = gm_rec.gm if gm_rec else None

    # Stem & Branch info
    stem_info   = lookup_stem(stem_pinyin)
    branch_info = lookup_branch(branch_pinyin)

    # Hidden stems
    hs_rec = db.session.query(HiddenStem).filter_by(branch=branch_pinyin).first()
    hidden_pinyins = hs_rec.hidden_stems if hs_rec and hs_rec.hidden_stems else []
    hidden_info = [lookup_stem(h) for h in hidden_pinyins]

    return {
        "GM": gm,
        "Stem": stem_info,
        "Branch": branch_info,
        "HS": hidden_info
    }

def calculate_month_pillar(date: ChineseDate) -> dict:



    return {}


def calculate_bazi(year: int,
                   month: int,
                   day: int,
                   hour: int = None,
                   minute: int = 0) -> dict:
    """
    Calculate the Four Pillars (BaZi) for a given date/time.
    Currently only implements the year pillar.
    """
    # Ensure Flask app context for DB lookups
    app = create_app(config_dict['Debug'])
    with app.app_context():
        # Rata Die for this date
        fixed = fixed_from_gregorian(year, month, day)
        year_pillar = calculate_year_pillar(fixed)

        return {
            "year":  year_pillar,
            "month": {},  # TODO: call calculate_month_pillar(...)
            "day":   {},  # TODO: call calculate_day_pillar(...)
            "hour":  {}   # TODO: call calculate_hour_pillar(...)
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
