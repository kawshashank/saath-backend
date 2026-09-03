def evaluate_khandar(tithi: int, nakshatra: int, config: dict) -> dict:
    """Applies Kashmiri Marriage (Khandar) rules."""
    
    # Allowed Tithis: 2,3,5,7,10,11,12,13 in both Pakshas
    allowed_tithis = [2, 3, 5, 7, 10, 11, 12, 13, 17, 18, 20, 22, 25, 26, 27, 28]
    if config.get("allow_purnima", False):
        allowed_tithis.append(15)
        
    # Allowed Nakshatras: Rohini, Mrigashira, Magha, U.Phal, Hasta, Swati, Anuradha, Mula, U.Ashadha, U.Bhadra, Revati
    allowed_nakshatras = [4, 5, 10, 12, 13, 15, 17, 19, 21, 26, 27]
    
    is_valid_tithi = tithi in allowed_tithis
    is_valid_nak = nakshatra in allowed_nakshatras
    
    return {
        "is_auspicious": is_valid_tithi and is_valid_nak,
        "reason": [] if (is_valid_tithi and is_valid_nak) else ["Invalid Tithi or Nakshatra combination for Khandar."]
    }

def evaluate_day(date_obj, event_type: str, config: dict) -> dict:
    from .astro_calc import get_srinagar_sunrise, get_tithi_and_nakshatra
    
    jd_sunrise = get_srinagar_sunrise(date_obj)
    astro_data = get_tithi_and_nakshatra(jd_sunrise)
    
    if event_type == "khandar":
        result = evaluate_khandar(astro_data["tithi_index"], astro_data["nakshatra_index"], config)
    else:
        result = {"is_auspicious": False, "reason": ["Event type not fully implemented yet."]}
        
    return {
        "date": date_obj.strftime("%Y-%m-%d"),
        "tithi_index": astro_data["tithi_index"],
        "nakshatra_index": astro_data["nakshatra_index"],
        "is_auspicious": result["is_auspicious"],
        "reasons": result["reason"]
    }