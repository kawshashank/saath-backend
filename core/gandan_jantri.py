"""Published Vijayshwar Jantri Gandan Saath dates.\n\nThis edition explicitly lists Gandan Saath dates from March 2026 through\nMarch 2027.\n"""

from datetime import date, timedelta

JANTRI_COVERAGE_START = date(2026, 3, 1)
JANTRI_COVERAGE_END = date(2027, 3, 31)

def _dates(year: int, month: int, *days: int) -> set[date]:
    return {date(year, month, day) for day in days}

GANDAN_JANTRI_DATES = frozenset().union(
    _dates(2026, 3, 19, 20, 23, 25, 29, 30, 3, 4, 5, 8, 10, 11, 21),
    _dates(2026, 4, 1, 2, 6, 8, 9, 12, 15, 20, 26, 27, 29),
    _dates(2026, 5, 1, 3, 4, 6, 8, 13),
    _dates(2026, 6, 19, 21, 24, 25, 29),
    _dates(2026, 7, 1, 2, 3, 5, 6, 10, 12),
    _dates(2026, 8, 13, 14),
    _dates(2026, 9, 17, 20, 21, 23, 24),
    _dates(2026, 10, 30),
    _dates(2026, 11, 4, 5, 6, 11, 12, 19, 20, 25, 30),
    _dates(2026, 12, 3, 6, 10, 11, 13, 14),
    _dates(2027, 1, 15, 18, 20, 24, 25, 27, 31),
    _dates(2027, 2, 3, 4, 7, 11, 14, 21, 22, 25, 26),
)

GANDAN_JANTRI_TIMING_NOTES = {
    date(2026, 3, 19): "From 6:52 AM",
    date(2026, 3, 25): "Up to 1:49 PM",
    date(2026, 3, 29): "From 2:37 PM",
    date(2026, 4, 1): "From 7:06 AM",
    date(2026, 4, 2): "Up to 5:38 PM",
    date(2026, 4, 6): "From 2:10 PM",
    date(2026, 4, 20): "Up to 7:27 AM",
    date(2026, 5, 3): "From 7:09 AM",
    date(2026, 5, 4): "Up to 9:57 AM",
    date(2026, 5, 6): "From 7:51 AM",
    date(2026, 6, 19): "From 10:06 AM",
    date(2026, 6, 21): "Up to 3:20 PM",
    date(2026, 6, 24): "From 1:58 PM",
    date(2026, 6, 25): "Up to 4:28 PM",
    date(2026, 7, 3): "Up to 11:20 AM",
    date(2026, 7, 5): "From 3:12 PM",
    date(2026, 7, 10): "From 1:14 PM",
    date(2026, 7, 12): "Up to 10:29 PM",
    date(2026, 9, 17): "Up to 7:53 PM",
    date(2026, 9, 20): "From 5:51 PM",
    date(2026, 9, 24): "Up to 10:34 AM",
    date(2026, 10, 30): "Up to 9:03 AM",
    date(2026, 11, 11): "Up to 11:37 AM",
    date(2026, 11, 12): "From 2:18 PM to 6:09 PM",
    date(2026, 11, 25): "Up to 5:46 PM",
    date(2026, 11, 30): "From 9:41 AM",
    date(2026, 12, 3): "Up to 10:22 AM",
    date(2026, 12, 6): "Up to 1:37 PM",
    date(2026, 12, 13): "From 4:47 PM",
    date(2027, 1, 15): "Up to 2:13 PM",
    date(2027, 1, 20): "Up to 4:16 PM",
    date(2027, 1, 25): "Up to 8:10 AM",
    date(2027, 2, 4): "From 4:31 PM",
    date(2027, 2, 22): "Up to 3:37 PM",
    date(2027, 2, 26): "Up to 10:13 AM",
    date(2026, 3, 8): "From 2:58 PM",
    date(2026, 3, 11): "Up to 11:19 AM",
    date(2026, 3, 21): "From 6:21 PM",
}

EMPTY_MONTH_REASONS = {}

def is_covered_by_jantri(date_obj: date) -> bool:
    return JANTRI_COVERAGE_START <= date_obj <= JANTRI_COVERAGE_END

def is_gandan_jantri_date(date_obj: date) -> bool:
    return date_obj in GANDAN_JANTRI_DATES

def get_gandan_timing(date_obj: date) -> str | None:
    return GANDAN_JANTRI_TIMING_NOTES.get(date_obj)

def get_empty_month_summaries(start_date: date, end_date: date) -> list[dict]:
    cursor = date(start_date.year, start_date.month, 1)
    summaries = []
    while cursor <= end_date:
        next_month = date(cursor.year + 1, 1, 1) if cursor.month == 12 else date(cursor.year, cursor.month + 1, 1)
        month_end = next_month - timedelta(days=1)
        if cursor >= start_date and month_end <= end_date:
            month_dates = [day for day in GANDAN_JANTRI_DATES if cursor <= day <= month_end]
            if not month_dates:
                if is_covered_by_jantri(cursor) and is_covered_by_jantri(month_end):
                    reason = EMPTY_MONTH_REASONS.get((cursor.year, cursor.month), "No Gandan Saath is listed in this Jantri month.")
                else:
                    reason = "This month is outside the loaded Jantri edition."
                summaries.append({"month": cursor.strftime("%Y-%m"), "label": cursor.strftime("%B %Y"), "reason": reason})
        cursor = next_month
    return summaries
