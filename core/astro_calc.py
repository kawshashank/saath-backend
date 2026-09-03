import swisseph as swe
import datetime

# Srinagar Coordinates (Vijayshwar Calendar Base)
SRINAGAR_LON = 74.7973
SRINAGAR_LAT = 34.0837
SRINAGAR_ALT = 1585.0

def get_srinagar_sunrise(date_obj: datetime.date) -> float:
    """Calculates the Julian Day of sunrise in Srinagar for a given date."""
    jd_start = swe.julday(date_obj.year, date_obj.month, date_obj.day, 0.0)
    geopos = (SRINAGAR_LON, SRINAGAR_LAT, SRINAGAR_ALT)
    
    try:
        # Calculate sunrise time using the geographic position tuple
        res = swe.rise_trans(jd_start, swe.SUN, swe.FLG_SWIEPH, swe.CALC_RISE, geopos)
        # Handle the tuple response natively returned by pyswisseph
        while isinstance(res, tuple):
            res = res[0]
        return res
    except Exception:
        # Fallback to 00:00 UT if ephemeris files are missing/fail
        return jd_start

def get_tithi_and_nakshatra(jd: float) -> dict:
    """Calculates Tithi and Nakshatra at a specific Julian Day using Lahiri Ayanamsa."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    sun_pos, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)
    moon_pos, _ = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)
    
    sun_lon = sun_pos[0]
    moon_lon = moon_pos[0]
    
    # Calculate Tithi (1 Tithi = 12 degrees of separation)
    relative_lon = (moon_lon - sun_lon) % 360
    tithi_index = int(relative_lon / 12) + 1
    
    # Calculate Nakshatra (1 Nakshatra = 13 degrees 20 minutes)
    nakshatra_index = int(moon_lon / (360 / 27)) + 1
    
    return {
        "tithi_index": tithi_index,
        "nakshatra_index": nakshatra_index
    }