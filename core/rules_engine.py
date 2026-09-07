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

def evaluate_khandar(tithi: int, nakshatra: int) -> bool:
    allowed_tithis = [2, 3, 5, 7, 10, 11, 12, 13, 17, 18, 20, 22, 25, 26, 27, 28]
    allowed_nakshatras = [4, 5, 10, 12, 13, 15, 17, 19, 21, 26, 27]
    return (tithi in allowed_tithis) and (nakshatra in allowed_nakshatras)

def evaluate_mekhal(tithi: int, nakshatra: int) -> bool:
    allowed_tithis = [2, 3, 5, 7, 10, 11, 13, 17, 18, 20, 22, 25, 26, 28]
    allowed_nakshatras = [1, 7, 8, 13, 14, 15, 22, 23, 24, 5, 27]
    return (tithi in allowed_tithis) and (nakshatra in allowed_nakshatras)

def evaluate_kahnethar(tithi: int, nakshatra: int) -> bool:
    # Added 6 and 21 to include Shashthi
    allowed_tithis = [2, 3, 5, 6, 7, 10, 11, 12, 13, 17, 18, 20, 21, 22, 25, 26, 27, 28]
    allowed_nakshatras = [1, 4, 5, 8, 12, 13, 14, 15, 17, 21, 22, 23, 24, 26, 27]
    return (tithi in allowed_tithis) and (nakshatra in allowed_nakshatras)

def evaluate_day(date_obj, event_type: str, config: dict) -> dict:
    from .astro_calc import get_srinagar_sunrise, get_tithi_and_nakshatra
    
    jd_sunrise = get_srinagar_sunrise(date_obj)
    astro_data = get_tithi_and_nakshatra(jd_sunrise)
    
    t_idx = astro_data["tithi_index"]
    n_idx = astro_data["nakshatra_index"]
    
    if event_type == "khandar":
        is_ausp = evaluate_khandar(t_idx, n_idx)
    elif event_type == "mekhal":
        is_ausp = evaluate_mekhal(t_idx, n_idx)
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