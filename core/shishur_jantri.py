"""Published Vijayshwar Jantri Shishur Laganuk Saath dates.\n\nThis edition explicitly lists Shishur Saath dates from March 2026 through\nMarch 2027.\n"""

from datetime import date, timedelta

JANTRI_COVERAGE_START = date(2026, 3, 1)
JANTRI_COVERAGE_END = date(2027, 3, 31)

def _dates(year: int, month: int, *days: int) -> set[date]:
    return {date(year, month, day) for day in days}

SHISHUR_JANTRI_DATES = frozenset().union(
    _dates(2026, 11, 25, 29),
    _dates(2026, 12, 3, 4, 6, 17, 20, 25, 30, 31),
    _dates(2027, 1, 1, 3, 8, 10),
)

SHISHUR_JANTRI_TIMING_NOTES = {
    date(2026, 11, 29): "Up to 10:59 AM",
    date(2026, 12, 17): "From 3:30 PM",
    date(2026, 12, 20): "Up to 2:55 PM",
    date(2026, 12, 31): "Up to 12:32 PM",
    date(2027, 1, 1): "From 1:09 PM",
    date(2027, 1, 8): "From 9:12 AM",
    date(2027, 1, 10): "From 3:11 PM",
}

EMPTY_MONTH_REASONS = {
    (2026, 3): "Shishur Laganuk occurs primarily in the winter months.",
    (2026, 4): "Shishur Laganuk occurs primarily in the winter months.",
    (2026, 5): "Shishur Laganuk occurs primarily in the winter months.",
    (2026, 6): "Shishur Laganuk occurs primarily in the winter months.",
    (2026, 7): "Shishur Laganuk occurs primarily in the winter months.",
    (2026, 8): "Shishur Laganuk occurs primarily in the winter months.",
    (2026, 9): "Shishur Laganuk occurs primarily in the winter months.",
    (2026, 10): "Shishur Laganuk occurs primarily in the winter months.",
    (2027, 2): "Shishur Laganuk occurs primarily in the winter months.",
    (2027, 3): "Shishur Laganuk occurs primarily in the winter months.",
}

def is_covered_by_jantri(date_obj: date) -> bool:
    return JANTRI_COVERAGE_START <= date_obj <= JANTRI_COVERAGE_END

def is_shishur_jantri_date(date_obj: date) -> bool:
    return date_obj in SHISHUR_JANTRI_DATES

def get_shishur_timing(date_obj: date) -> str | None:
    return SHISHUR_JANTRI_TIMING_NOTES.get(date_obj)

def get_empty_month_summaries(start_date: date, end_date: date) -> list[dict]:
    cursor = date(start_date.year, start_date.month, 1)
    summaries = []
    while cursor <= end_date:
        next_month = date(cursor.year + 1, 1, 1) if cursor.month == 12 else date(cursor.year, cursor.month + 1, 1)
        month_end = next_month - timedelta(days=1)
        if cursor >= start_date and month_end <= end_date:
            month_dates = [day for day in SHISHUR_JANTRI_DATES if cursor <= day <= month_end]
            if not month_dates:
                if is_covered_by_jantri(cursor) and is_covered_by_jantri(month_end):
                    reason = EMPTY_MONTH_REASONS.get((cursor.year, cursor.month), "No Shishur Saath is listed in this Jantri month.")
                else:
                    reason = "This month is outside the loaded Jantri edition."
                summaries.append({"month": cursor.strftime("%Y-%m"), "label": cursor.strftime("%B %Y"), "reason": reason})
        cursor = next_month
    return summaries
