#!/usr/bin/env python3
# moon_phase.py
#
# Compute the lunar phase for any civil date/time,
# using Jean Meeus’s 24-term low-precision series for lunar longitude,
# but with “correct” illumination thresholds for phase names.

import math
import json
from datetime import datetime, timezone

# mean synodic month (days)
_SYNODIC_MONTH = 29.530588861

def _julian_day(dt: datetime) -> float:
    """
    Convert a UTC-aware (or naive UTC) datetime to Julian Day (JD).
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt = dt.astimezone(timezone.utc)

    y, m = dt.year, dt.month
    # fractional day
    d = dt.day + (dt.hour + dt.minute/60 + dt.second/3600) / 24.0

    if m <= 2:
        y -= 1
        m += 12

    A = y // 100
    B = 2 - A + A // 4

    jd = (int(365.25 * (y + 4716))
          + int(30.6001 * (m + 1))
          + d + B - 1524.5)
    return jd

def _phase_name(illum: float) -> str:
    """
    Return one of the eight phase names based purely on illuminated fraction.
    """
    # Tolerances around exact quarters
    tol = 0.13

    if illum <= tol:
        return "New Moon"
    if illum < 0.5 - tol:
        return "Waxing Crescent"
    if abs(illum - 0.5) <= tol:
        return "First Quarter"
    if illum < 1.0 - tol:
        return "Waxing Gibbous"
    if illum >= 1.0 - tol:
        return "Full Moon"
    # Waning half
    if illum > 0.5 + tol:
        return "Waning Gibbous"
    if abs(illum - 0.5) <= tol:
        return "Last Quarter"
    return "Waning Crescent"

def moon_phase(dt: datetime) -> dict:
    """
    Given a datetime (UTC or naive=UTC), return:
      - 'julian_day'   : JD at dt
      - 'age_days'     : days since last New Moon
      - 'illumination' : lit fraction [0..1]
      - 'phase_name'   : one of eight human-readable labels
    """
    jd = _julian_day(dt)
    T = (jd - 2451545.0) / 36525.0
    rad = math.radians

    # Sun’s true longitude (λ☉)
    L0 = 280.46646 + T*(36000.76983 + 0.0003032*T)
    M  = 357.52911 + T*(35999.05029 - 0.0001537*T)
    C  = ((1.914602 - T*(0.004817 + 0.000014*T))*math.sin(rad(M))
          + (0.019993 - 0.000101*T)*math.sin(rad(2*M))
          + 0.000289*math.sin(rad(3*M)))
    lam_sun = (L0 + C) % 360

    # Moon’s longitude series (Jean Meeus, ch. 47)
    Lp = 218.3164591 + 481267.88134236*T - 0.0013268*T**2 + T**3/538841 - T**4/65194000
    D  = 297.8502042 + 445267.1115168*T - 0.0016300*T**2 + T**3/545868 - T**4/113065000
    Mp = 134.9634114 + 477198.8676313*T + 0.0089970*T**2 + T**3/69699  - T**4/14712000
    F  =  93.2720993 + 483202.0175273*T - 0.0034029*T**2 - T**3/3526000 + T**4/863310000

    TERMS = (
        (0,0,1,0,6288774), (2,0,-1,0,1274027), (2,0,0,0,658314),
        (0,0,2,0,213618), (0,1,0,0,-185116),(0,0,0,2,-114332),
        (2,0,-2,0,58793),(2,-1,-1,0,57066),(2,0,1,0,53322),
        (2,-1,0,0,45758),(0,1,-1,0,-40923),(1,0,0,0,-34720),
        (0,1,1,0,-30383),(2,0,0,-2,15327),(0,0,1,2,-12528),
        (0,0,1,-2,10980),(4,0,-1,0,10675),(0,0,3,0,10034),
        (4,0,-2,0,8548),(2,1,-1,0,-7888),(2,1,0,0,-6766),
        (1,0,-1,0,-5163),(1,1,0,0,4987),(2,-1,1,0,4036),
    )

    sigma_l = sum(c * math.sin(rad(d*D + m*M + mp*Mp + f*F))
                  for d,m,mp,f,c in TERMS)
    # extra Meeus terms:
    sigma_l += 3958*math.sin(rad(F + lam_sun - 180))
    sigma_l += 1962*math.sin(rad(L0 - lam_sun))

    lam_moon = (Lp + sigma_l/1_000_000.0) % 360

    delta_l = math.radians((lam_moon - lam_sun) % 360)
    age     = delta_l / (2*math.pi) * _SYNODIC_MONTH
    illum   = (1 - math.cos(delta_l)) / 2

    return {
        "julian_day":   jd,
        "age_days":     age,
        "illumination": illum,
        "phase_name":   _phase_name(illum),
    }

if __name__ == "__main__":
    raw = input("Enter UTC date and time (YYYY MM DD [HH MM SS], time optional): ").split()
    try:
        y, mo, d = map(int, raw[:3])
        if len(raw) >= 6:
            h, mi, s = map(int, raw[3:6])
        else:
            h = mi = s = 0
    except ValueError:
        print("Invalid input. Use: 2025 07 30 12 00 00")
        exit(1)

    dt = datetime(y, mo, d, h, mi, s, tzinfo=timezone.utc)
    result = moon_phase(dt)
    print(json.dumps(result, indent=2))
