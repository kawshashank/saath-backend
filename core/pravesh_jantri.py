"""Published Vijayshwar Jantri Pravesh Muhurat (Navis Makanas) dates.\n\nThis edition explicitly lists Pravesh Saath dates from March 2026 through\nMarch 2027.\n"""

from datetime import date, timedelta

JANTRI_COVERAGE_START = date(2026, 3, 1)
JANTRI_COVERAGE_END = date(2027, 3, 31)

def _dates(year: int, month: int, *days: int) -> set[date]:
    return {date(year, month, day) for day in days}

PRAVESH_JANTRI_DATES = frozenset().union(
    _dates(2026, 3, 20, 27, 28),
    _dates(2026, 4, 6),
    _dates(2026, 5, 4),
    _dates(2026, 6, 17, 24, 27),
    _dates(2026, 7, 1, 2, 4),
    _dates(2026, 9, 17, 24),
    _dates(2026, 11, 21, 26, 28),
    _dates(2026, 12, 12),
    _dates(2027, 1, 15),
    _dates(2027, 2, 8),
    _dates(2027, 3, 18),
)

PRAVESH_JANTRI_TIMING_NOTES = {
    date(2026, 3, 20): "From 9:14 AM to 11:07 AM (Vrishabha)\nFrom 11:07 AM to 1:23 PM (Mithuna)\nFrom 3:47 PM to 6:09 PM (Simha)",
    date(2026, 3, 27): "From 3:19 PM to 5:41 PM (Simha)",
    date(2026, 3, 28): "From 8:43 AM to 10:36 AM (Vrishabha)\nFrom 10:36 AM to 12:52 PM (Mithuna)",
    date(2026, 4, 6): "From 2:43 PM to 5:05 PM (Simha)",
    date(2026, 5, 4): "From 6:20 AM to 8:13 AM (Vrishabha)\nFrom 8:13 AM to 10:29 AM (Mithuna)",
    date(2026, 6, 17): "From 1:36 PM to 2:42 PM (Tula)",
    date(2026, 6, 24): "From 9:32 AM to 11:54 AM (Simha)\nFrom 11:54 AM to 1:58 PM (Kanya)",
    date(2026, 6, 27): "From 9:21 AM to 11:42 AM (Simha)\nFrom 11:42 AM to 2:03 PM (Kanya)",
    date(2026, 7, 1): "From 9:05 AM to 11:27 AM (Simha)\nFrom 11:27 AM to 1:47 PM (Kanya)",
    date(2026, 7, 2): "From 9:01 AM to 9:26 AM (Simha)",
    date(2026, 7, 4): "From 12:39 PM to 1:36 PM (Kanya)",
    date(2026, 9, 17): "From 3:28 PM to 5:07 PM (Makara)",
    date(2026, 9, 24): "From 3:01 PM to 4:39 PM (Makara)",
    date(2026, 11, 21): "From 11:12 AM to 12:51 PM (Makara)",
    date(2026, 11, 26): "From 10:53 AM to 12:32 PM (Makara)",
    date(2026, 11, 28): "From 10:45 AM to 12:24 PM (Makara)",
    date(2026, 12, 12): "From 11:29 AM to 12:52 PM (Makara)",
    date(2027, 1, 15): "From 9:15 AM to 10:38 AM (Kumbha)",
    date(2027, 2, 8): "From 7:41 AM to 9:04 AM (Kumbha)",
    date(2027, 3, 18): "From 11:15 AM to 1:31 PM (Mithuna)",
}

EMPTY_MONTH_REASONS = {
    (2026, 8): "No Pravesh Saath is listed during this Jantri month.",
    (2026, 10): "No Pravesh Saath is listed during this Jantri month.",
}

def is_covered_by_jantri(date_obj: date) -> bool:
    return JANTRI_COVERAGE_START <= date_obj <= JANTRI_COVERAGE_END

def is_pravesh_jantri_date(date_obj: date) -> bool:
    return date_obj in PRAVESH_JANTRI_DATES

def get_pravesh_timing(date_obj: date) -> str | None:
    return PRAVESH_JANTRI_TIMING_NOTES.get(date_obj)

def get_empty_month_summaries(start_date: date, end_date: date) -> list[dict]:
    cursor = date(start_date.year, start_date.month, 1)
    summaries = []
    while cursor <= end_date:
        next_month = date(cursor.year + 1, 1, 1) if cursor.month == 12 else date(cursor.year, cursor.month + 1, 1)
        month_end = next_month - timedelta(days=1)
        if cursor >= start_date and month_end <= end_date:
            month_dates = [day for day in PRAVESH_JANTRI_DATES if cursor <= day <= month_end]
            if not month_dates:
                if is_covered_by_jantri(cursor) and is_covered_by_jantri(month_end):
                    reason = EMPTY_MONTH_REASONS.get((cursor.year, cursor.month), "No Pravesh Saath is listed in this Jantri month.")
                else:
                    reason = "This month is outside the loaded Jantri edition."
                summaries.append({"month": cursor.strftime("%Y-%m"), "label": cursor.strftime("%B %Y"), "reason": reason})
        cursor = next_month
    return summaries
