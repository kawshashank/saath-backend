import swisseph as swe
import datetime

# Srinagar Coordinates
SRINAGAR_LON = 74.7973
SRINAGAR_LAT = 34.0837
SRINAGAR_ALT = 1585.0
SRINAGAR_UTC_OFFSET_HOURS = 5.5  # India has no daylight-saving adjustment.

def _get_srinagar_solar_event(date_obj: datetime.date, event_flag: int) -> float:
    """Return the UT Julian date of a Srinagar solar event.

    ``rise_trans`` returns ``(status, event_times)``.  The former code passed
    its arguments in the wrong order and then returned the status code rather
    than ``event_times[0]``.  That silently made downstream panchang values
    use an arbitrary instant instead of the local sunrise/sunset.
    """
    # ``rise_trans`` searches forward from its input. Start at local midnight,
    # not 00:00 UTC: Srinagar's summer sunrise can occur on the previous UTC
    # date and would otherwise be incorrectly taken from the next civil day.
    jd_start = (
        swe.julday(date_obj.year, date_obj.month, date_obj.day, 0.0)
        - SRINAGAR_UTC_OFFSET_HOURS / 24
    )
    geopos = (SRINAGAR_LON, SRINAGAR_LAT, SRINAGAR_ALT)
    try:
        status, event_times = swe.rise_trans(
            jd_start,
            swe.SUN,
            event_flag,
            geopos,
            flags=swe.FLG_SWIEPH,
        )
        if status == 0:
            return event_times[0]
        raise RuntimeError("Swiss Ephemeris could not find the solar event")
    except Exception as exc:
        # Srinagar always has a sunrise/sunset, so reaching this path means an
        # infrastructure problem rather than a valid astronomical condition.
        raise RuntimeError(
            f"Unable to calculate Srinagar solar event for {date_obj.isoformat()}"
        ) from exc


def get_srinagar_sunrise(date_obj: datetime.date) -> float:
    return _get_srinagar_solar_event(date_obj, swe.CALC_RISE)


def get_srinagar_sunset(date_obj: datetime.date) -> float:
    return _get_srinagar_solar_event(date_obj, swe.CALC_SET)

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
    # Normalize across the 0°/360° boundary before determining daily motion.
    ven_daily_motion = (ven_pos_tmrw[0] - ven_pos[0] + 180) % 360 - 180
    is_venus_retro = ven_daily_motion < 0
    
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
