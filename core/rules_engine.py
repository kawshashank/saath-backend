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

def check_global_blockers(astro_data: dict, date_obj) -> bool:
    """Returns True if the day is BLOCKED by any overarching Jantri constraint."""
    sun_lon = astro_data["sun_lon"]
    tithi = astro_data["tithi_index"]
    sun_rashi = astro_data["sun_rashi"]
    jup_lon = astro_data["jup_lon"]
    ven_lon = astro_data["ven_lon"]
    karana = astro_data["karana_index"]
    yoga = astro_data["yoga_index"]
    is_sankranti = astro_data["is_sankranti"]

    # 1. Vaar (Day of Week): Block Tuesday (1) and Saturday (5)
    if date_obj.weekday() in [1, 5]:
        return True
        
    # 2. Sankranti: Block days where the Sun shifts to a new Rashi
    if is_sankranti:
        return True
        
    # 3. Nithya Yogas: Block Vyatipata (17) and Vaidhriti (27)
    if yoga in [17, 27]:
        return True
        
    # 4. Karana (Bhadra / Vishti): Block destructive Karana alignments
    # Vishti aligns at specific mathematical intervals between karana 2 and 57
    if 2 <= karana <= 57 and (karana - 1) % 7 == 0:
        return True

    # 5. Pitra Paksha (Mahalaya Paksha)
    if 16 <= tithi <= 30 and 135 <= sun_lon <= 180:
        return True
        
    # 6. Kharmas / Malamas (Strictly prohibited when Sun is in Dhanu or Meena)
    if sun_rashi == 9 or sun_rashi == 12:
        return True
        
    # 7. Guru Astha (Jupiter Combust)
    if get_angular_distance(sun_lon, jup_lon) < 11:
        return True
        
    # 8. Shukra Astha (Venus Combust)
    if get_angular_distance(sun_lon, ven_lon) < 10:
        return True

    return False

def evaluate_khandar(tithi: int, nakshatra: int) -> bool:
    allowed_tithis = [2, 3, 5, 7, 10, 11, 12, 13, 17, 18, 20, 22, 25, 26, 27, 28]
    allowed_nakshatras = [4, 5, 10, 12, 13, 15, 17, 19, 21, 26, 27]
    return (tithi in allowed_tithis) and (nakshatra in allowed_nakshatras)

def evaluate_mekhal(tithi: int, nakshatra: int, sun_rashi: int) -> bool:
    allowed_tithis = [2, 3, 5, 7, 10, 11, 13, 17, 18, 20, 22, 25, 26, 28]
    allowed_nakshatras = [1, 7, 8, 13, 14, 15, 22, 23, 24, 5, 27]
    # Mekhal is strictly performed during Uttarayana (Sun moving North: Capricorn to Gemini)
    is_uttarayana = sun_rashi in [10, 11, 12, 1, 2, 3]
    return (tithi in allowed_tithis) and (nakshatra in allowed_nakshatras) and is_uttarayana

def evaluate_kahnethar(tithi: int, nakshatra: int) -> bool:
    # Including 6 and 21 to ensure Shashthi is mapped properly
    allowed_tithis = [2, 3, 5, 6, 7, 10, 11, 12, 13, 17, 18, 20, 21, 22, 25, 26, 27, 28]
    allowed_nakshatras = [1, 4, 5, 8, 12, 13, 14, 15, 17, 21, 22, 23, 24, 26, 27]
    return (tithi in allowed_tithis) and (nakshatra in allowed_nakshatras)

def evaluate_day(date_obj, event_type: str, config: dict) -> dict:
    from .astro_calc import get_srinagar_sunrise, get_tithi_and_nakshatra
    
    jd_sunrise = get_srinagar_sunrise(date_obj)
    astro_data = get_tithi_and_nakshatra(jd_sunrise)
    
    t_idx = astro_data["tithi_index"]
    n_idx = astro_data["nakshatra_index"]
    sun_rashi = astro_data["sun_rashi"]
    
    # Run the strict global Panchang filters first
    is_blocked = check_global_blockers(astro_data, date_obj)
    
    if is_blocked:
        is_ausp = False
    elif event_type == "khandar":
        is_ausp = evaluate_khandar(t_idx, n_idx)
    elif event_type == "mekhal":
        is_ausp = evaluate_mekhal(t_idx, n_idx, sun_rashi)
    elif event_type == "kahnethar":
        is_ausp = evaluate_kahnethar(t_idx, n_idx)
    else:
        is_ausp = False

    return {
        "date": date_obj.strftime("%Y-%m-%d"),
        "tithi": TITHI_NAMES[t_idx - 1] if 1 <= t_idx <= 30 else "Unknown",
        "nakshatra": NAKSHATRA_NAMES[n_idx - 1] if 1 <= n_idx <= 27 else "Unknown",
        "is_auspicious": is_ausp
    }