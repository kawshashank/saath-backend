"""Published Vijayshwar Jantri Kahnethar (Jatakarma) dates.

This edition explicitly lists Kahnethar Saath dates from March 2026 through
March 2027. It is source data transcribed from the Jantri, not an inferred
astronomical rule or a collection of range-specific exceptions.
"""

from datetime import date, timedelta


JANTRI_COVERAGE_START = date(2026, 3, 1)
JANTRI_COVERAGE_END = date(2027, 3, 31)


def _dates(year: int, month: int, *days: int) -> set[date]:
    return {date(year, month, day) for day in days}


KAHNETHAR_JANTRI_DATES = frozenset().union(
    _dates(2026, 3, 20, 25, 27),
    _dates(2026, 4, 3, 6, 20, 23, 29),
    _dates(2026, 5, 3, 4),
    _dates(2026, 6, 17, 21, 24, 25),
    _dates(2026, 7, 1, 2, 3, 5),
    # August is absent from the printed Jatakarma/Kahnethar Saath list.
    _dates(2026, 9, 17, 21, 23, 24),
    _dates(2026, 10, 30),
    _dates(2026, 11, 11, 20, 22, 25, 26),
    _dates(2026, 12, 13, 14),
    _dates(2027, 1, 15, 20),
    _dates(2027, 2, 8, 11, 18, 19, 22, 25, 26),
    _dates(2027, 3, 10, 11, 17, 18),
)

# Timings transcribed from the published Kahnethar entries.
KAHNETHAR_JANTRI_TIMING_NOTES = {
    date(2026, 3, 25): "Till 1:49 PM",
    date(2026, 4, 3): "From 8:42 AM",
    date(2026, 4, 6): "From 2:10 PM",
    date(2026, 4, 20): "Till 7:27 AM",
    date(2026, 5, 3): "From 7:09 AM",
    date(2026, 5, 4): "Till 9:57 AM",
    date(2026, 6, 21): "From 9:30 AM",
    date(2026, 6, 25): "Till 4:28 PM",
    date(2026, 7, 1): "From 7:38 AM",
    date(2026, 7, 3): "Till 11:20 AM",
    date(2026, 7, 5): "Till 1:30 PM",
    date(2026, 10, 30): "Till 9:03 AM",
    date(2026, 11, 11): "Till 11:37 AM",
    date(2026, 11, 25): "From 4:50 AM",
    date(2026, 12, 13): "From 4:47 AM",
    date(2027, 1, 15): "Till 2:13 PM",
    date(2027, 1, 20): "Till 4:16 PM",
    date(2027, 2, 19): "Till 11:14 AM",
    date(2027, 2, 22): "From 11:54 AM",
    date(2027, 2, 26): "Till 10:13 AM",
    date(2027, 3, 11): "Till 3:37 PM",
    date(2027, 3, 17): "From 6:45 AM",
}

EMPTY_MONTH_REASONS = {
    (2026, 8): "No Kahnethar Saath is listed during Shukra Ash / As-Sang.",
}


def is_covered_by_jantri(date_obj: date) -> bool:
    return JANTRI_COVERAGE_START <= date_obj <= JANTRI_COVERAGE_END


def is_kahnethar_jantri_date(date_obj: date) -> bool:
    return date_obj in KAHNETHAR_JANTRI_DATES


def get_kahnethar_timing(date_obj: date) -> str | None:
    return KAHNETHAR_JANTRI_TIMING_NOTES.get(date_obj)


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
                day for day in KAHNETHAR_JANTRI_DATES
                if cursor <= day <= month_end
            ]
            if not month_dates:
                if is_covered_by_jantri(cursor) and is_covered_by_jantri(month_end):
                    reason = EMPTY_MONTH_REASONS.get(
                        (cursor.year, cursor.month),
                        "No Kahnethar Saath is listed in this Jantri month.",
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
