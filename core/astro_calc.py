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
        while isinstance(res, tuple):
            res = res[0]
        return res
    except Exception:
        return jd_start

def get_tithi_and_nakshatra(jd: float) -> dict:
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    # Calculate today's planetary longitudes
    sun_pos, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)
    moon_pos, _ = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)
    jup_pos, _ = swe.calc_ut(jd, swe.JUPITER, swe.FLG_SIDEREAL)
    ven_pos, _ = swe.calc_ut(jd, swe.VENUS, swe.FLG_SIDEREAL)
    
    sun_lon = sun_pos[0]
    moon_lon = moon_pos[0]
    
    # 1. Tithi (12 degrees) & Nakshatra (13.33 degrees)
    relative_lon = (moon_lon - sun_lon) % 360
    tithi_index = int(relative_lon / 12) + 1
    nakshatra_index = int(moon_lon / (360 / 27)) + 1
    
    # 2. Karana (6 degrees)
    karana_index = int(relative_lon / 6) + 1
    
    # 3. Nithya Yoga (Sun + Moon / 13.3333 degrees)
    combined_lon = (moon_lon + sun_lon) % 360
    yoga_index = int(combined_lon / (40 / 3)) + 1
    
    # 4. Solar Transit (Sankranti)
    sun_rashi = int(sun_lon / 30) + 1
    
    # Calculate yesterday's solar position to check for transits
    sun_pos_yest, _ = swe.calc_ut(jd - 1.0, swe.SUN, swe.FLG_SIDEREAL)
    sun_rashi_yest = int(sun_pos_yest[0] / 30) + 1
    is_sankranti = sun_rashi != sun_rashi_yest
    
    return {
        "tithi_index": tithi_index,
        "nakshatra_index": nakshatra_index,
        "karana_index": karana_index,
        "yoga_index": yoga_index,
        "sun_lon": sun_lon,
        "sun_rashi": sun_rashi,
        "is_sankranti": is_sankranti,
        "jup_lon": jup_pos[0],
        "ven_lon": ven_pos[0]
    }