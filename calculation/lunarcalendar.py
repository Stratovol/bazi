from datetime import date, datetime
import math

# pip install lunardate
from lunardate import LunarDate

def julian_day(y, m, d):
    """Convert a Gregorian date to Julian Day Number."""
    if m <= 2:
        y, m = y - 1, m + 12
    A = y // 100
    B = 2 - A + A // 4
    jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524.5
    return jd

def moon_phase(given_date):
    """Return the moon age (days since new moon) and a phase name."""
    # Known new moon reference: Jan 6, 2000 → JD 2451550.1
    jd = julian_day(given_date.year, given_date.month, given_date.day)
    synodic_month = 29.530588853
    age = (jd - 2451550.1) % synodic_month

    # Determine phase
    if age < 1:
        phase = "New Moon"
    elif age < 7.38:
        phase = "Waxing Crescent"
    elif age < 8.38:
        phase = "First Quarter"
    elif age < 14.77:
        phase = "Waxing Gibbous"
    elif age < 15.77:
        phase = "Full Moon"
    elif age < 22.15:
        phase = "Waning Gibbous"
    elif age < 23.15:
        phase = "Last Quarter"
    else:
        phase = "Waning Crescent"

    return age, phase

def lunar_calendar_date(given_date):
    """Convert to Chinese lunar calendar date."""
    lunar = LunarDate.fromSolarDate(
        given_date.year,
        given_date.month,
        given_date.day
    )
    return lunar.year, lunar.month, lunar.day

def moon_age_to_date(given_date):
    age, phase_name = moon_phase(given_date)
    ly, lm, ld = lunar_calendar_date(given_date)
    return f"Moon age: {ld} → Phase: {phase_name}"


if __name__ == "__main__":
    # Example for today (2025-06-27)
    today = date(2025, 6, 10)

    age, phase_name = moon_phase(today)
    ly, lm, ld = lunar_calendar_date(today)

    print(f"Gregorian date: {today}")
    print(f"Moon age: {ld} → Phase: {phase_name}")