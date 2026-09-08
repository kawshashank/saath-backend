TITHI_NAMES = [
    "Shukla Pratipada", "Shukla Dwitiya", "Shukla Tritiya", "Shukla Chaturthi", "Shukla Panchami",
    "Shukla Shashthi", "Shukla Saptami", "Shukla Ashtami", "Shukla Navami", "Shukla Dashami",
    "Shukla Ekadashi", "Shukla Dwadashi", "Shukla Trayodashi", "Shukla Chaturdashi", "Purnima",
    "Krishna Pratipada", "Krishna Dwitiya", "Krishna Tritiya", "Krishna Chaturthi", "Krishna Panchami",
    "Krishna Shashthi", "Krishna Saptami", "Krishna Ashtami", "Krishna Navami", "Krishna Dashami",
    "Krishna Ekadashi", "Krishna Dwadashi", "Krishna Trayodashi", "Krishna Chaturdashi", "Amavasya"
]

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya",
    "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def get_angular_distance(lon1: float, lon2: float) -> float:
    diff = abs(lon1 - lon2)
    return min(diff, 360 - diff)

def check_global_blockers(astro, date_obj, event_type: str) -> bool:
    # Kahnethar is assessed by Udaya Panchang.  The Jantri includes dates on
    # which Sankranti, Vishti, or Vyatipata/Vaidhriti occurs, so these cannot
    # be used as unconditional whole-day rejections for that ceremony.
    if event_type != "kahnethar":
        if astro["is_sankranti"]: return True
        if astro["yoga_index"] in [17, 27]: return True
        if 2 <= astro["karana_index"] <= 57 and (astro["karana_index"] - 1) % 7 == 0: return True

    # 2. Pitra Paksha & Kharmas
    if 16 <= astro["tithi_sunrise"] <= 30 and 135 <= astro["sun_lon"] <= 180: return True
    # The Kahnethar Jantri includes Meena solar-month dates.  Kharmas remains
    # a blocker for Khandar and Mekhal, but is not a blanket Kahnethar ban.
    if event_type != "kahnethar" and astro["sun_rashi"] in [9, 12]: return True
        
    # 3. Shukra/Guru Asta, calculated from the actual day's longitudes.
    ven_threshold = 8 if astro["is_venus_retro"] else 10
    if get_angular_distance(astro["sun_lon"], astro["ven_lon"]) < ven_threshold: return True
    if get_angular_distance(astro["sun_lon"], astro["jup_lon"]) < 11: return True

    return False

def evaluate_khandar(astro, date_obj) -> bool:
    # Khandar strictly blocks Tuesday (1) and Saturday (5)
    if date_obj.weekday() in [1, 5]: return False
    
    allowed_tithis = [2, 3, 5, 7, 10, 11, 12, 13, 17, 18, 20, 22, 25, 26, 27, 28]
    allowed_nakshatras = [4, 5, 10, 12, 13, 15, 17, 19, 21, 26, 27]
    
    # Tithi must be auspicious from sunrise through sunset
    if astro["tithi_sunrise"] not in allowed_tithis or astro["tithi_sunset"] not in allowed_tithis: return False
    if astro["nakshatra_index"] not in allowed_nakshatras: return False
    return True

def evaluate_mekhal(astro, date_obj) -> bool:
    if date_obj.weekday() in [1, 5]: return False
    if astro["sun_rashi"] not in [10, 11, 12, 1, 2, 3]: return False # Uttarayana only
    
    allowed_tithis = [2, 3, 5, 7, 10, 11, 13, 17, 18, 20, 22, 25, 26, 28]
    allowed_nakshatras = [1, 7, 8, 13, 14, 15, 22, 23, 24, 5, 27]
    
    if astro["tithi_sunrise"] not in allowed_tithis or astro["tithi_sunset"] not in allowed_tithis: return False
    if astro["nakshatra_index"] not in allowed_nakshatras: return False
    return True

def evaluate_kahnethar(astro, date_obj) -> bool:
    # The Jantri publishes Kahnethar Saath directly. Its listed dates are
    # authoritative over reverse-engineered generic Panchang rules.
    from .kahnethar_jantri import is_kahnethar_jantri_date
    return is_kahnethar_jantri_date(date_obj)

def evaluate_day(date_obj, event_type: str, config: dict) -> dict:
    from .astro_calc import get_astro_data
    astro_data = get_astro_data(date_obj)
    
    if event_type == "kahnethar":
        # Do not eliminate a printed Jantri date using incomplete generic
        # rules for combustion, yoga, karana, or weekday.
        is_ausp = evaluate_kahnethar(astro_data, date_obj)
    elif check_global_blockers(astro_data, date_obj, event_type): is_ausp = False
    elif event_type == "khandar": is_ausp = evaluate_khandar(astro_data, date_obj)
    elif event_type == "mekhal": is_ausp = evaluate_mekhal(astro_data, date_obj)
    else: is_ausp = False

    t_idx = astro_data["tithi_sunrise"]
    n_idx = astro_data["nakshatra_index"]
    result = {
        "date": date_obj.strftime("%Y-%m-%d"),
        "tithi": TITHI_NAMES[t_idx - 1] if 1 <= t_idx <= 30 else "Unknown",
        "nakshatra": NAKSHATRA_NAMES[n_idx - 1] if 1 <= n_idx <= 27 else "Unknown",
        "is_auspicious": is_ausp
    }
    if event_type == "kahnethar" and is_ausp:
        from .kahnethar_jantri import get_kahnethar_timing_note
        timing_note = get_kahnethar_timing_note(date_obj)
        if timing_note:
            result["jantri_timing"] = timing_note
    return result
