from collections import namedtuple
import math
from math import floor
import mpmath as mp
mp.mp.dps = 50  # 50 decimal‐digit precision

# --- Supporting classes and stubs ---
class Location:
    """
    Simplified time-zone/location object.
    Only `zone_offset` (hours) is used here.
    """
    def __init__(self, zone_offset):
        self.zone_offset = zone_offset

# Constants for Gregorian conversion
gregorian_epoch = 1

# Convert fixed date to Gregorian year
def gregorian_year_from_fixed(date):
    """
    Gregorian year corresponding to the fixed `date`.
    """
    # Prior days since epoch
    d0 = date - gregorian_epoch
    # Completed 400-year cycles
    n400 = d0 // 146097
    # Days not in completed 400-year cycles
    d1 = d0 % 146097
    # 100-year cycles not in 400-year cycles
    n100 = d1 // 36524
    # Days not in 400-year or 100-year cycles
    d2 = d1 % 36524
    # 4-year cycles not in 100-year cycles
    n4 = d2 // 1461
    # Days not in 400, 100, or 4-year cycles
    d3 = d2 % 1461
    # Years not in 400, 100, or 4-year cycles
    n1 = d3 // 365
    # Compute base year (0-based)
    year = 400 * n400 + 100 * n100 + 4 * n4 + n1
    # If it's the last day of a leap cycle, do not add 1
    if n100 == 4 or n1 == 4:
        return year
    else:
        return year + 1


def fixed_from_gregorian(year: int, month: int, day: int) -> int:
    """
    Convert a (proleptic) Gregorian calendar date to Rata Die fixed date.
    Epoch: 1 Jan 1 CE → fixed‐date 1.
    """
    # 1) days before this year
    y = year - 1
    days = 365 * y
    days += y // 4
    days -= y // 100
    days += y // 400

    # 2) days in prior months
    days += (367 * month - 362) // 12

    # 3) correct for Feb having 28/29 days
    if month > 2:
        days -= 1 if gregorian_leap_year(year) else 2

    # 4) days in current month
    days += day
    # 5) offset so that 1 Jan 1 CE → 1
    return days + (gregorian_epoch - 1)

def gregorian_new_year(g_year: int) -> int:
    """
    Fixed date of January 1 in Gregorian year g_year.
    """
    # Simply delegate to your converter at month=1, day=1
    return fixed_from_gregorian(g_year, 1, 1)

# Named tuple to represent the Chinese date result
ChineseDate = namedtuple("ChineseDate", ["cycle", "year", "month", "is_leap_month", "day", "name"])

# --- Constants (please define these) ---
mean_synodic_month = 29.530588861
mean_tropical_year = 365.242189
chinese_epoch = fixed_from_gregorian(-2636, 2, 15)
winter_solar_longitude = 270.0  # degrees for winter solstice
j2000 = gregorian_new_year(2000) + 12/24.0

# --- Lower-level astronomy/chronology functions still needed: ---

def gregorian_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def julian_centuries(tee):
    return (dynamical_from_universal(tee) - j2000) / 36525.0

def estimate_prior_solar_longitude(lambda_deg, tee):
    rate = mean_tropical_year / 360.0
    tau = tee - rate * ((solar_longitude(tee) - lambda_deg) % 360)
    cap_delta = ((solar_longitude(tau) - lambda_deg + 180) % 360) - 180
    return min(tee, tau - rate * cap_delta)

def midnight_in_china(date):
    return universal_from_standard(date, chinese_location(date))

# Astronomical solar longitude calculation
def solar_longitude(tee):
    c = julian_centuries(tee)
    coefficients = [403406, 195207, 119433, 112392, 3891, 2819, 1721,
                    660, 350, 334, 314, 268, 242, 234, 158, 132, 129, 114,
                    99, 93, 86, 78, 72, 68, 64, 46, 38, 37, 32, 29, 28, 27, 27,
                    25, 24, 21, 20, 18, 17, 14, 13, 13, 12, 10, 10, 10]
    multipliers = [0.9287892, 35999.1376958, 35999.4089666,
                   35998.7287385, 71998.20261, 71998.4403, 36000.35726,
                   71997.4812, 32964.4678, -19.441, 445267.1117, 45036.884,
                   3.1008, 22518.443, -19.9739, 65928.9345, 9038.0293, 3034.7684,
                   33718.148, 3034.448, -2280.773, 29929.992, 31556.493, 149.588,
                   9037.75, 107997.405, -4444.176, 151.771, 67555.316, 31556.08,
                   -4561.54, 62894.167, 107996.706, 1221.655, 62894.167, 31437.369,
                   14578.298, -31931.757, 34777.243, 1221.999, 62894.511,
                   -4442.039, 107997.909, 119.066, 16859.071, -4.578, 26895.292,
                   -39.127, 12297.536, 90073.778]
    addends = [270.54861, 340.19128, 63.91854, 331.2622, 317.843, 86.631,
               240.052, 310.26, 247.23, 260.87, 297.82, 343.14, 166.79, 81.53,
               3.5, 132.75, 182.95, 162.03, 29.8, 266.4, 249.2, 157.6, 257.8,
               185.1, 69.9, 8.0, 197.1, 250.4, 65.3, 162.7, 341.5, 291.6,
               98.5, 146.7, 110.0, 5.2, 342.6, 230.9, 256.1, 45.3, 242.9,
               115.2, 151.8, 285.3, 53.3, 126.6, 205.7, 85.9, 146.1]
    sigma = sum(a * math.sin(math.radians(b + m_mul * c))
                for a, b, m_mul in zip(coefficients, addends, multipliers))
    lam = (282.7771834 + 36000.76953744 * c
           + 0.000005729577951308232 * sigma)
    lam += aberration(tee) + nutation(tee)
    return lam % 360

# Solar aberration and nutation stubs
def lunar_longitude(tee):
    """
    Longitude of the Moon (in degrees) at moment tee.
    Adapted from "Astronomical Algorithms" by Jean Meeus,
    Willmann-Bell (1998), pp. 338–342.
    """
    c = julian_centuries(tee)

    # Fundamental arguments
    cap_L_prime  = mean_lunar_longitude(c)
    cap_D        = lunar_elongation(c)
    cap_M        = solar_anomaly(c)
    cap_M_prime  = lunar_anomaly(c)
    cap_F        = moon_node(c)

    # Small polynomial correction E
    cap_E = poly(c, [1, -0.002516, -0.0000074])

    # Periodic-term coefficients from Meeus
    sine_coeff = [
        6288774, 1274027, 658314, 213618, -185116, -114332,
        58793, 57066, 53322, 45758, -40923, -34720, -30383,
        15327, -12528, 10980, 10675, 10034, 8548, -7888,
        -6766, -5163, 4987, 4036, 3994, 3861, 3665, -2689,
        -2602, 2390, -2348, 2236, -2120, -2069, 2048, -1773,
        -1595, 1215, -1110, -892, -810, 759, -713, -700, 691,
        596, 549, 537, 520, -487, -399, -381, 351, -340, 330,
        327, -323, 299, 294
    ]
    args_lunar_elongation = [
        0,2,2,0,0,0,2,2,2,0,1,0,2,0,0,4,0,4,2,2,1,
        2,2,4,2,0,2,2,2,2,4,0,3,2,4,0,2,2,4,0,4,1,2,0,1,3,4,2,0,1,2
    ]
    args_solar_anomaly      = [
        0,0,0,0,1,0,0,-1,-1,1,0,1,1,0,0,0,0,0,1,1,
        0,1,-1,0,0,0,1,0,-1,0,-2,1,2,-2,0,0,-1,0,1,
        -1,2,2,1,-1,0,-1,0,1,0,1,0
    ]
    args_lunar_anomaly      = [
        1,-1,0,2,0,0,-2,1,1,0,-1,0,1,0,1,1,-1,3,-2,
        -1,0,-1,0,1,2,0,-3,-2,-1,-2,1,0,2,0,2,-1,2,2,-1,-2,1,0,2,1,4,0,-2,0,2,1,-2,-3,2,1,-1,3
    ]
    args_moon_node          = [
        0,0,0,0,2,0,0,0,0,0,0,-2,2,-2,0,0,0,0,0,
        0,0,0,0,2,0,0,0,0,0,0,-2,2,-2,0,0,0,0,0,0,
        0,0,-2,0,0,0,0,-2,-2,0,0,0,0
    ]

    # Compute the periodic correction ("sigma" in Lisp)
    correction = 0.0
    for v, w, x, y, z in zip(
        sine_coeff,
        args_lunar_elongation,
        args_solar_anomaly,
        args_lunar_anomaly,
        args_moon_node
    ):
        term = v * (cap_E ** abs(x)) * math.sin(math.radians(
            w * cap_D +
            x * cap_M +
            y * cap_M_prime +
            z * cap_F
        ))
        correction += term / 1_000_000.0  # the Lisp used deg(1/1_000_000)

    # Planetary and flat-earth corrections
    venus      = (3958/1_000_000) * math.sin(math.radians(119.75 + 131.849 * c))
    jupiter    = (318/1_000_000)  * math.sin(math.radians(53.09  + 479264.29 * c))
    flat_earth = (1962/1_000_000) * math.sin(math.radians(cap_L_prime - cap_F))

    # Nutation and aberration
    lam = (cap_L_prime + correction + venus + jupiter + flat_earth +
           aberration(tee) + nutation(tee)) % 360.0

    return lam

# Supporting lunar input functions (to implement)
def mean_lunar_longitude(c):
    """
    Mean longitude of moon (degrees) at moment given in Julian centuries c.
    Adapted from Meeus, Astronomical Algorithms (1998), pp. 337–340.
    """
    # Coefficients: [218.3164477, 481267.88123421, -0.0015786, 1/538841, -1/65194000]
    coeffs = [218.3164477, 481267.88123421, -0.0015786, 1.0/538841.0, -1.0/65194000.0]
    return poly(c, coeffs) % 360.0

def lunar_elongation(c):
    """
    Elongation of moon (degrees) at moment given in Julian centuries c.
    Adapted from Meeus, Astronomical Algorithms (1998), p. 338.
    """
    # Coefficients: [297.8501921, 445267.1114034, -0.0018819, 1/545868, -1/11306500]
    coeffs = [297.8501921, 445267.1114034, -0.0018819, 1.0/545868.0, -1.0/11306500.0]
    return poly(c, coeffs) % 360.0

def solar_anomaly(c):
    """
    Mean anomaly of sun (degrees) at moment given in Julian centuries c.
    Adapted from Meeus, Astronomical Algorithms (1998), p. 338.
    """
    # Coefficients: [357.5291092, 35999.0502909, -0.0001536, 1/24490000]
    coeffs = [357.5291092, 35999.0502909, -0.0001536, 1.0/24490000.0]
    return poly(c, coeffs) % 360.0

def lunar_anomaly(c):
    """
    Mean anomaly of moon (degrees) at moment given in Julian centuries c.
    Adapted from Meeus, Astronomical Algorithms (1998), p. 338.
    """
    coeffs = [
        134.9633964,
        477198.8675055,
        0.0087414,
        1.0/69699.0,
        -1.0/14712000.0
    ]
    # Drop the leftover stub string. Just return the angle mod 360:
    return poly(c, coeffs) % 360.0

def moon_node(c):
    """
    Moon's argument of latitude F (degrees) at moment given in Julian centuries c.
    Adapted from Meeus, Astronomical Algorithms (1998), p. 338.
    """
    # Coefficients: [93.2720950, 483202.0175233, -0.0036539, -1/3526000, 1/863310000]
    coeffs = [93.2720950, 483202.0175233, -0.0036539, -1.0/3526000.0, 1.0/863310000.0]
    return poly(c, coeffs) % 360.0

def poly(x, coeffs):
    """
    Evaluate polynomial with coefficients `coeffs` at `x`.
    coeffs[0] + coeffs[1]*x + coeffs[2]*x^2 + ...
    """
    return sum(coef * (x ** i) for i, coef in enumerate(coeffs))

# Aberration and nutation
def aberration(tee):
    c = julian_centuries(tee)
    angle = 177.63 + 35999.01848 * c + 0.005575
    return -0.0000974 * math.cos(math.radians(angle))

def nutation(tee):
    """
    Longitudinal nutation (degrees) at moment `tee`.
    Adapted from Bretagnon & Simon.
    """
    c = julian_centuries(tee)
    # Compute A = 124.90° - 1934.134° * c + 0.002063° * c^2
    A = math.radians(124.90 + (-1934.134) * c + 0.002063 * c * c)
    # Compute B = 201.11° + 72001.5377° * c + 0.00057° * c^2
    B = math.radians(201.11 + 72001.5377 * c + 0.00057 * c * c)
    # Nutation: -0.004778° * sin(A) + -0.0003667° * sin(B)
    return -0.004778 * math.sin(A) + -0.0003667 * math.sin(B)

# Ephemeris correction (ΔT)
def ephemeris_correction(tee):
    """
    Dynamical Time minus Universal Time (days) for moment `tee`.
    Adapted from "Astronomical Algorithms" by Jean Meeus (1991) and NASA polynomials.
    """
    # Gregorian year at this date
    year = gregorian_year_from_fixed(math.floor(tee))
    # Fixed dates for 1900-01-01 and July 1 of year
    d0 = fixed_from_gregorian(1900, 1, 1)
    d1 = fixed_from_gregorian(year, 7, 1)
    c = (d1 - d0) / 36525.0
    y = year - 2000
    # Polynomial segments (ΔT in days)
    c2051 = (-20 + 32 * ((year - 1820)/100)**2 + 0.5628 * (2150 - year)) / 86400
    c2000 = poly(y, [62.92, 0.32217, 0.005589]) / 86400
    c1987 = poly(y, [63.86, 0.3345, -0.060374, 0.0017275, 0.0000651814, 0.00002373599]) / 86400
    c1900 = poly(c, [-0.00002, 0.000297, 0.025184, -0.181133, 0.55304, -0.861938, 0.677066, -0.212591])
    c1800 = poly(c, [-0.000009, 0.003844, 0.083563, 0.865736, 4.867575, 15.845535,
                     31.332267, 38.291999, 28.316289, 11.636204, 2.043794])
    c1700 = poly(year-1700, [8.118780842, -0.005092142, 0.003336121, -0.0000266484]) / 86400
    c1600 = poly(c, [120, -0.9808, -0.01532, 0.000140272128]) / 86400
    c500  = c1600
    c0    = poly(year/100, [10583.6, -1014.41, 33.78311, -5.952053, -0.1798452, 0.0221741, 0.0090316521]) / 86400
    # Select segment
    if 2051 <= year <= 2150:
        dt = c2051
    elif 2006 <= year <= 2050:
        dt = c2000
    elif 1987 <= year <= 2005:
        dt = c1987
    elif 1900 <= year <= 1986:
        dt = c1900
    elif 1800 <= year <= 1899:
        dt = c1800
    elif 1700 <= year <= 1799:
        dt = c1700
    elif 1600 <= year <= 1699:
        dt = c1600
    elif 500  <= year <= 1599:
        dt = c500
    elif -500 < year < 500:
        dt = c0
    else:
        dt = poly(year/100, [1574.2, -556.01, 71.23472, -0.8503463,
                              -0.005050998, 0.0083572073]) / 86400
    return dt

# New moon stubs
def lunar_phase(tee):
    """
    Lunar phase angle (degrees) at moment `tee`.
    0 = new moon, 90 = first quarter, 180 = full moon, 270 = last quarter.
    """
    # Angle between lunar and solar longitude
    phi = (lunar_longitude(tee) - solar_longitude(tee)) % 360.0
    # Find nearest new moon index
    t0 = nth_new_moon(0)
    n = round((tee - t0) / mean_synodic_month)
    # Phase approximation based on time since nth new moon
    phi_prime = 360.0 * (((tee - nth_new_moon(n)) / mean_synodic_month) % 1.0)
    # If the two estimates differ by more than 180°, use 180° to avoid ambiguity
    if abs(phi - phi_prime) > 180.0:
        return 180.0
    return phi_prime

def nth_new_moon(n):
    """
    Astronomical instant (UT) of the n-th new moon since the epoch.
    Adapted from Meeus, Astronomical Algorithms (2005).
    """
    # Months since epoch offset for J2000
    n0 = 24724
    # Number of synodic months since J2000
    k = n - n0
    # Julian centuries from J2000
    c = k / 1236.85
    # Mean time of new moon (dynamical time)
    # Approximation polynomial coefficients
    approx = j2000 + poly(c, [
        5.09766,
        mean_synodic_month * 1236.85,
        0.00015437,
        -0.000000150,
        0.0000000073
    ])
    # Phase correction factor E
    cap_E = poly(c, [1, -0.002516, -0.0000074])
    # Solar anomaly M
    sol_anom = poly(c, [
        2.5534,
        29.10535670 * 1236.85,
        -0.0000014,
        -0.00000011
    ])
    # Lunar anomaly M'
    lun_anom = poly(c, [
        201.5643,
        385.81693528 * 1236.85,
        0.0107582,
        0.00001238,
        -0.00000058
    ])
    # Moon's argument of latitude F
    moon_arg = poly(c, [
        160.7108,
        390.67050284 * 1236.85,
        -0.0016118,
        -0.00000227,
        0.00000011
    ])
    # Longitude of ascending node Ω
    cap_omega = poly(c, [
        124.7746,
        -1.56375588 * 1236.85,
        0.0020672,
        0.00000215
    ])
    # Series coefficients
    E_factor    = [0,1,0,0,1,1,2,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0]
    solar_coeff = [0,1,0,0,-1,1,2,0,0,1,0,1,1,-1,1,0,0,3,1,0,1,-1,-1,1,0]
    lunar_coeff = [1,0,2,0,1,1,0,1,1,2,3,0,0,2,1,2,0,1,2,1,1,1,3,4]
    moon_coeff  = [0,0,0,2,0,0,0,-2,2,0,0,2,-2,0,0,-2,0,0]
    sine_coeff  = [
        -0.40720, 0.17241, 0.01608, 0.01039, 0.00739, -0.00514, 0.00208,
        -0.00111, -0.00057, 0.00056, -0.00042, 0.00042, 0.00038, -0.00024,
        -0.00007, 0.00004, 0.00003, 0.00003, -0.00003, 0.00003, -0.00002,
        0.00002
    ]
    # Compute periodic correction term
    correction = 0.0
    for v, w, x, y, z in zip(sine_coeff, E_factor, solar_coeff, lunar_coeff, moon_coeff):
        correction += v * (cap_E ** w) * math.sin(math.radians(
            x * sol_anom + y * lun_anom + z * moon_arg
        ))
    # Add constant, coefficient, and factor arrays
    add_const  = [251.88, 251.83, 349.42, 84.66, 141.74, 207.14, 154.84, 34.52,
                  207.19, 291.34, 161.72, 239.56, 331.55]
    add_coeff  = [0.016321, 26.651886, 36.412478, 18.206239, 53.303771, 2.453732,
                  7.306860, 27.261239, 0.121824, 1.844379, 24.198154, 25.513099,
                  3.592518]
    add_factor = [0.000165, 0.000164, 0.000126, 0.000110, 0.000062, 0.000060,
                  0.000056, 0.000047, 0.000042, 0.000040, 0.000037, 0.000035,
                  0.000023]
    extra = 0.000325 * math.sin(math.radians(poly(c, [299.77, 132.8475848, -0.009173])))
    additional = 0.0
    for i, j, l in zip(add_const, add_coeff, add_factor):
        additional += l * math.sin(math.radians(i + j * k))
    # Dynamical time of true new moon
    true_time = approx + correction + extra + additional
    # Convert from dynamical to universal time
    return true_time - ephemeris_correction(true_time)

def new_moon_at_or_after(tee):
    """
    Astronomical instant of the first new moon at or after `tee` (UT).
    """
    t0 = nth_new_moon(0)
    phi = lunar_phase(tee)
    n = round((tee - t0) / mean_synodic_month - (phi / 360.0))
    k = n
    while True:
        t = nth_new_moon(k)
        if t >= tee:
            return t
        k += 1

def new_moon_before(tee):
    """
    Astronomical instant of the last new moon before `tee` (UT),
    translated directly from CC-2 fig. 14.46.
    """
    # 1) Base epoch new moon
    t0 = nth_new_moon(0)

    # 2) Phase correction
    phi = lunar_phase(tee)

    # 3) Estimate month index
    p = (tee - t0) / mean_synodic_month - (phi / 360.0)
    n = round(p)

    # Seed at n-1, then step k *up* until nth_new_moon(k) < tee
    k = n - 1
    while True:
        k += 1
        t = nth_new_moon(k)
        if t < tee:
            return t

# Time conversions
def standard_from_universal(tee, location):
    """
    Standard-time instant `tee` in universal time at given `location`, converted to local standard time.
    """
    # Local standard time = Universal time + time zone offset
    return tee + (location.zone_offset / 24.0)

def universal_from_standard(tee_rom_s, location):
    return tee_rom_s - (location.zone_offset / 24.0)

# Chinese location (Beijing) with historical timezone changes
def chinese_location(tee):
    date = math.floor(tee)
    year = gregorian_year_from_fixed(date)
    if year < 1929:
        offset = 1397 / 180.0  # hours (7.7611...)
    else:
        offset = 8.0
    return Location(offset)

# Major solar term stub
def current_major_solar_term(date):
    """
    Last Chinese major solar term (zhongqi) before fixed `date`.
    Returns an integer from 1 to 12.
    Adapted from the Lisp algorithm: AMOD(+2, floor(solar_longitude/30)) mod 12.
    """
    # Compute solar longitude at local standard time for Beijing on this date
    tee_univ = universal_from_standard(date, chinese_location(date))
    s = solar_longitude(tee_univ)
    # Determine term index: s/30 gives 0–11; add 2 then wrap into 1–12
    term_index = amod(int(math.floor(s / 30.0)) + 2, 12)
    return term_index

# Dynamical/ephemeris time
def dynamical_from_universal(tee_rom_u):
    return tee_rom_u + ephemeris_correction(tee_rom_u)
    return dt

# Helper arithmetic
def amod(x, y):
    return ((x - 1) % y) + 1

# Chinese calendar conversion
def chinese_winter_solstice_on_or_before(date):
    approx = estimate_prior_solar_longitude(
        winter_solar_longitude, midnight_in_china(date + 1)
    )
    test = midnight_in_china(date + 1)
    day = floor(approx) - 1
    test1 = solar_longitude(midnight_in_china(day + 1))
    while solar_longitude(midnight_in_china(day + 1)) < winter_solar_longitude:
        test2 = solar_longitude(midnight_in_china(day + 1))
        day += 1
    return day

def chinese_new_moon_on_or_after(date):
    tee = new_moon_at_or_after(midnight_in_china(date))
    return floor(standard_from_universal(tee, chinese_location(tee)))

def chinese_new_moon_before(date):
    tee = new_moon_before(midnight_in_china(date))
    return floor(standard_from_universal(tee, chinese_location(tee)))

def chinese_prior_leap_month(m12, m):
    if m < m12:
        return False
    if chinese_no_major_solar_term(m):
        return True
    return chinese_prior_leap_month(m12, chinese_new_moon_before(m))

def chinese_no_major_solar_term(date):
    first_term = current_major_solar_term(date)
    next_date = chinese_new_moon_on_or_after(date + 1)
    return first_term == current_major_solar_term(next_date)

def sexagenary_name(year_in_cycle: int) -> str:
    stems    = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
    branches = ["Zi", "Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"]
    s = stems   [(year_in_cycle - 1) % 10]
    b = branches[(year_in_cycle - 1) % 12]
    return f"{s}-{b}"

def chinese_from_fixed(date):
    s1 = chinese_winter_solstice_on_or_before(date)
    s2 = chinese_winter_solstice_on_or_before(s1 + 370)
    m12 = chinese_new_moon_on_or_after(s1 + 1)
    next_m11 = chinese_new_moon_before(s2 + 1)
    m = chinese_new_moon_before(date + 1)
    leap_year = round((next_m11 - m12) / mean_synodic_month) == 12
    month = amod(
        round((m - m12) / mean_synodic_month)
        - (1 if (leap_year and chinese_prior_leap_month(m12, m)) else 0),
        12
    )
    leap_month = (
        leap_year
        and chinese_no_major_solar_term(m)
        and not chinese_prior_leap_month(m12, m)
        and (m12 == chinese_new_moon_before(m))
    )

    elapsed_years = floor(1.5 - (month / 12) + (date - chinese_epoch) / mean_tropical_year)
    cycle = (elapsed_years - 1) // 60 + 1
    year  = amod(elapsed_years, 60)
    day = (date - m) + 1
    name = sexagenary_name(year)
    return ChineseDate(cycle, year, month, leap_month, day, name)


def main():
    """
    Prompt for a Gregorian date (YYYY MM DD), convert to fixed,
    then compute and display the Chinese date.
    """
    try:
        y, m, d = map(int, input("Enter date (YYYY MM DD): ").split())
    except ValueError:
        print("Invalid input. Please enter three integers, e.g. 2025 7 7")
        return

    fixed = fixed_from_gregorian(y, m, d)
    cycle, year, month, is_leap, day, name = chinese_from_fixed(fixed)

    leap_str = " (leap month)" if is_leap else ""
    print(
        f"Gregorian {y}-{m:02d}-{d:02d} → fixed date {fixed}\n"
        f"Chinese date: cycle {cycle}, year {year} “{name}”, "
        f"month {month}{leap_str}, day {day}"
    )


if __name__ == "__main__":
    main()
