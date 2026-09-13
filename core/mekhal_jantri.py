"""Published Vijayshwar Jantri Mekhal (Yagnopavit) dates.

This edition explicitly lists Mekhal Saath dates from March 2026 through
March 2027. It is source data transcribed from the Jantri, not an inferred
astronomical rule or a collection of range-specific exceptions.
"""

from datetime import date, timedelta

JANTRI_COVERAGE_START = date(2026, 3, 1)
JANTRI_COVERAGE_END = date(2027, 3, 31)

def _dates(year: int, month: int, *days: int) -> set[date]:
    return {date(year, month, day) for day in days}

MEKHAL_JANTRI_DATES = frozenset().union(
    _dates(2026, 3, 20, 25, 27),
    _dates(2026, 4, 23),
    _dates(2026, 5, 3, 4),
    _dates(2026, 6, 17, 24),
    _dates(2026, 7, 1, 2),
    _dates(2026, 9, 17, 21, 24),
    _dates(2026, 11, 11, 12, 22, 25, 26),
    _dates(2026, 12, 14),
    _dates(2027, 1, 15),
    _dates(2027, 2, 8, 18),
    _dates(2027, 3, 10, 11, 17, 18),
)

# Timings transcribed from the published Mekhal entries.
MEKHAL_JANTRI_TIMING_NOTES = {
    date(2026, 3, 20): "From 7:43 AM to 9:14 AM (Mesha)\nFrom 9:14 AM to 11:07 AM (Vrishabha)",
    date(2026, 3, 25): "From 7:23 AM to 8:54 AM (Mesha)\nFrom 8:54 AM to 10:41 AM (Vrishabha)",
    date(2026, 3, 27): "From 10:06 AM to 10:40 AM (Vrishabha)\nFrom 10:40 AM to 12:56 PM (Mithuna)",
    date(2026, 4, 23): "From 7:03 AM to 8:57 AM (Vrishabha)\nFrom 11:12 AM to 1:36 PM (Karka)",
    date(2026, 5, 3): "From 8:17 AM to 10:33 AM (Mithuna)\nFrom 10:33 AM to 12:57 PM (Karka)",
    date(2026, 5, 4): "From 8:13 AM to 10:29 AM (Mithuna)\nFrom 10:29 AM to 12:53 PM (Karka)",
    date(2026, 6, 17): "From 7:36 AM to 8:12 AM (Karka)",
    date(2026, 6, 24): "From 7:09 AM to 9:32 AM (Karka)\nFrom 9:32 AM to 11:54 AM (Simha)",
    date(2026, 7, 1): "From 6:50 AM to 9:05 AM (Karka)\nFrom 9:05 AM to 11:27 AM (Simha)",
    date(2026, 7, 2): "From 6:37 AM to 9:01 AM (Karka)\nFrom 9:01 AM to 9:26 AM (Simha)",
    date(2026, 9, 17): "From 1:25 PM to 3:28 PM (Dhanu)",
    date(2026, 9, 21): "From 1:09 PM to 3:12 PM (Dhanu)",
    date(2026, 9, 24): "From 12:53 PM to 3:01 PM (Dhanu)",
    date(2026, 11, 11): "From 11:37 AM to 11:52 AM (Dhanu)\nFrom 11:52 AM to 1:28 PM (Makara)",
    date(2026, 11, 12): "From 9:45 AM to 11:48 AM (Dhanu)\nFrom 11:48 AM to 1:27 PM (Makara)",
    date(2026, 11, 22): "From 9:06 AM to 11:09 AM (Dhanu)\nFrom 11:09 AM to 12:47 PM (Makara)",
    date(2026, 11, 25): "From 8:54 AM to 10:57 AM (Dhanu)\nFrom 10:57 AM to 12:36 PM (Makara)",
    date(2026, 11, 26): "From 8:50 AM to 10:53 AM (Dhanu)\nFrom 10:53 AM to 12:32 PM (Makara)",
    date(2026, 12, 14): "From 7:39 AM to 9:11 AM (Dhanu)",
    date(2027, 1, 15): "From 9:15 AM to 10:38 AM (Kumbha)",
    date(2027, 2, 8): "From 11:55 AM to 1:49 PM (Vrishabha)",
    date(2027, 2, 18): "From 11:16 AM to 1:09 PM (Vrishabha)",
    date(2027, 3, 10): "From 9:53 AM to 10:52 AM (Vrishabha)",
    date(2027, 3, 11): "From 11:19 AM to 11:43 AM (Vrishabha)\nFrom 11:43 AM to 1:58 PM (Mithuna)",
    date(2027, 3, 17): "From 7:55 AM to 9:26 AM (Mesha)\nFrom 9:26 AM to 11:19 AM (Vrishabha)",
    date(2027, 3, 18): "From 7:51 AM to 9:22 AM (Mesha)\nFrom 9:22 AM to 11:15 AM (Vrishabha)\nFrom 11:15 AM to 1:31 PM (Mithuna)",
}

EMPTY_MONTH_REASONS = {
    (2026, 8): "No Mekhal Saath is listed during this Jantri month.",
    (2026, 10): "No Mekhal Saath is listed during this Jantri month.",
}

def is_covered_by_jantri(date_obj: date) -> bool:
    return JANTRI_COVERAGE_START <= date_obj <= JANTRI_COVERAGE_END

def is_mekhal_jantri_date(date_obj: date) -> bool:
    return date_obj in MEKHAL_JANTRI_DATES

def get_mekhal_timing(date_obj: date) -> str | None:
    return MEKHAL_JANTRI_TIMING_NOTES.get(date_obj)

def get_empty_month_summaries(start_date: date, end_date: date) -> list[dict]:
    """Explain only full calendar months covered by the user's query."""
    cursor = date(start_date.year, start_date.month, 1)
    summaries = []

    while cursor <= end_date:
        next_month = (
            date(cursor.year + 1, 1, 1)
            if cursor.month == 12
            else date(cursor.year, cursor.month + 1, 1)
        )
        month_end = next_month - timedelta(days=1)

        if cursor >= start_date and month_end <= end_date:
            month_dates = [
                day for day in MEKHAL_JANTRI_DATES
                if cursor <= day <= month_end
            ]
            if not month_dates:
                if is_covered_by_jantri(cursor) and is_covered_by_jantri(month_end):
                    reason = EMPTY_MONTH_REASONS.get(
                        (cursor.year, cursor.month),
                        "No Mekhal Saath is listed in this Jantri month.",
                    )
                else:
                    reason = "This month is outside the loaded Jantri edition."
                summaries.append({
                    "month": cursor.strftime("%Y-%m"),
                    "label": cursor.strftime("%B %Y"),
                    "reason": reason,
                })
        cursor = next_month

    return summaries
