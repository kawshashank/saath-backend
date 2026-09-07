import swisseph as swe
import datetime

# Srinagar Coordinates
SRINAGAR_LON = 74.7973
SRINAGAR_LAT = 34.0837
SRINAGAR_ALT = 1585.0

def get_srinagar_sunrise(date_obj: datetime.date) -> float:
    jd_start = swe.julday(date_obj.year, date_obj.month, date_obj.day, 0.0)
    geopos = (SRINAGAR_LON, SRINAGAR_LAT, SRINAGAR_ALT)
    try:
        res = swe.rise_trans(jd_start, swe.SUN, swe.FLG_SWIEPH, swe.CALC_RISE, geopos)
        while isinstance(res, tuple): res = res[0]
        return res
    except Exception: return jd_start

def get_srinagar_sunset(date_obj: datetime.date) -> float:
    jd_start = swe.julday(date_obj.year, date_obj.month, date_obj.day, 0.0)
    geopos = (SRINAGAR_LON, SRINAGAR_LAT, SRINAGAR_ALT)
    try:
        res = swe.rise_trans(jd_start, swe.SUN, swe.FLG_SWIEPH, swe.CALC_SET, geopos)
        while isinstance(res, tuple): res = res[0]
        return res
    except Exception: return jd_start + 0.5

def get_astro_data(date_obj: datetime.date) -> dict:
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    jd_sunrise = get_srinagar_sunrise(date_obj)
    jd_sunset = get_srinagar_sunset(date_obj)
    
    # SUNRISE CALCULATIONS
    sun_pos, _ = swe.calc_ut(jd_sunrise, swe.SUN, swe.FLG_SIDEREAL)
    moon_pos, _ = swe.calc_ut(jd_sunrise, swe.MOON, swe.FLG_SIDEREAL)
    jup_pos, _ = swe.calc_ut(jd_sunrise, swe.JUPITER, swe.FLG_SIDEREAL)
    ven_pos, _ = swe.calc_ut(jd_sunrise, swe.VENUS, swe.FLG_SIDEREAL)
    
    sun_lon = sun_pos[0]
    moon_lon = moon_pos[0]
    
    rel_lon_rise = (moon_lon - sun_lon) % 360
    tithi_rise = int(rel_lon_rise / 12) + 1
    nakshatra_rise = int(moon_lon / (360 / 27)) + 1
    karana_rise = int(rel_lon_rise / 6) + 1
    
    combined_lon = (moon_lon + sun_lon) % 360
    yoga_rise = int(combined_lon / (40 / 3)) + 1
    sun_rashi = int(sun_lon / 30) + 1
    
    # SUNSET CALCULATIONS (To prevent mid-day Rikta Tithi overlaps)
    sun_pos_set, _ = swe.calc_ut(jd_sunset, swe.SUN, swe.FLG_SIDEREAL)
    moon_pos_set, _ = swe.calc_ut(jd_sunset, swe.MOON, swe.FLG_SIDEREAL)
    rel_lon_set = (moon_pos_set[0] - sun_pos_set[0]) % 360
    tithi_set = int(rel_lon_set / 12) + 1
    
    # SANKRANTI & RETROGRADE CHECKS
    sun_pos_yest, _ = swe.calc_ut(jd_sunrise - 1.0, swe.SUN, swe.FLG_SIDEREAL)
    is_sankranti = sun_rashi != (int(sun_pos_yest[0] / 30) + 1)
    
    ven_pos_tmrw, _ = swe.calc_ut(jd_sunrise + 1.0, swe.VENUS, swe.FLG_SIDEREAL)
    is_venus_retro = ven_pos_tmrw[0] < ven_pos[0]
    
    return {
        "tithi_sunrise": tithi_rise,
        "tithi_sunset": tithi_set,
        "nakshatra_index": nakshatra_rise,
        "karana_index": karana_rise,
        "yoga_index": yoga_rise,
        "sun_lon": sun_lon,
        "sun_rashi": sun_rashi,
        "is_sankranti": is_sankranti,
        "jup_lon": jup_pos[0],
        "ven_lon": ven_pos[0],
        "is_venus_retro": is_venus_retro
    }