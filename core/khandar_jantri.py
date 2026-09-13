"""Published Vijayshwar Jantri Khandar (Marriage) dates.

This edition explicitly lists Khandar Saath dates from April 2026 through
March 2027. It is source data transcribed from the Jantri, not an inferred
astronomical rule or a collection of range-specific exceptions.
"""

from datetime import date, timedelta

JANTRI_COVERAGE_START = date(2026, 4, 16)
JANTRI_COVERAGE_END = date(2027, 3, 12)

def _dates(year: int, month: int, *days: int) -> set[date]:
    return {date(year, month, day) for day in days}

KHANDAR_JANTRI_DATES = frozenset().union(
    _dates(2026, 4, 16, 20, 25, 26, 29, 30),
    _dates(2026, 5, 6, 7, 8, 9, 10),
    _dates(2026, 6, 19, 20, 22, 24, 26, 27, 28),
    _dates(2026, 7, 1, 2, 4, 6, 8, 9, 12),
    _dates(2026, 8, 13),
    _dates(2026, 9, 17, 21, 23),
    _dates(2026, 11, 5, 7, 8, 11, 12, 13, 14, 21),
    _dates(2026, 12, 9, 10, 11, 12),
    _dates(2027, 1, 15, 18, 24, 25, 27, 28, 29, 31),
    _dates(2027, 2, 3, 4, 5, 10, 15, 24, 27, 28),
    _dates(2027, 3, 1, 3, 4, 7, 10, 11, 12),
)

# Timings transcribed from the published Khandar entries.
KHANDAR_JANTRI_TIMING_NOTES = {
    date(2026, 4, 16): "From 9:10 PM to 11:31 PM (Vrishchika), From 11:31 PM to 1:37 AM (Dhanu)",
    date(2026, 4, 20): "From 9:08 AM to 11:24 AM (Mithuna), From 11:24 AM to 1:43 PM (Karka), From 11:15 PM to 1:22 AM (Dhanu), From 1:22 AM to 3:01 AM (Makara)",
    date(2026, 4, 25): "From 10:55 PM to 1:02 AM (Dhanu), From 1:02 AM to 2:41 AM (Makara)",
    date(2026, 4, 26): "From 10:51 PM to 12:58 AM (Dhanu), From 12:58 AM to 2:37 AM (Makara)",
    date(2026, 4, 29): "From 12:43 AM to 2:25 AM (Makara)",
    date(2026, 4, 30): "From 8:29 AM to 10:45 AM (Mithuna), From 10:45 AM to 11:09 AM (Karka), From 10:35 PM to 12:42 AM (Dhanu), From 12:42 AM to 2:16 AM (Makara)",
    date(2026, 5, 6): "From 8:06 AM to 10:21 AM (Mithuna), From 10:21 AM to 12:45 PM (Karka)",
    date(2026, 5, 7): "From 7:47 PM to 10:03 PM (Vrishchika), From 12:15 AM to 1:54 AM (Makara)",
    date(2026, 5, 8): "From 7:52 AM to 10:13 AM (Mithuna), From 10:13 AM to 12:28 PM (Karka), From 7:43 PM to 10:04 PM (Vrishchika), From 10:04 PM to 12:11 AM (Dhanu)",
    date(2026, 5, 9): "From 7:54 AM to 10:09 AM (Mithuna), From 10:09 AM to 12:33 PM (Karka), From 7:39 PM to 10:00 PM (Vrishchika), From 10:00 PM to 12:07 AM (Dhanu)",
    date(2026, 5, 10): "From 7:50 AM to 10:05 AM (Mithuna), From 10:05 AM to 12:29 PM (Karka), From 9:56 PM to 12:03 AM (Dhanu), From 12:03 AM to 12:49 AM (Makara)",
    date(2026, 6, 19): "From 4:58 PM to 7:07 PM (Vrishchika), From 7:07 PM to 9:10 PM (Dhanu), From 10:49 PM to 1:36 AM (Makara), From 3:07 AM to 4:46 AM (Vrishabha)",
    date(2026, 6, 20): "From 7:24 AM to 9:25 AM (Karka)",
    date(2026, 6, 22): "From 2:23 PM to 4:46 PM (Tula)",
    date(2026, 6, 24): "From 7:09 AM to 9:32 AM (Karka), From 2:03 PM to 4:27 PM (Tula), From 8:50 PM to 10:10 PM (Makara)",
    date(2026, 6, 26): "From 8:54 PM to 10:33 PM (Makara), From 1:20 AM to 2:52 AM (Mesha)",
    date(2026, 6, 27): "From 6:57 AM to 9:21 AM (Karka)",
    date(2026, 6, 28): "From 1:13 AM to 2:44 AM (Mesha)",
    date(2026, 7, 1): "From 6:41 AM to 9:05 AM (Karka), From 1:47 PM to 4:11 PM (Tula), From 1:01 AM to 2:32 AM (Mesha)",
    date(2026, 7, 2): "From 6:37 AM to 9:01 AM (Karka)",
    date(2026, 7, 4): "From 6:29 AM to 8:53 AM (Karka)",
    date(2026, 7, 6): "From 8:15 PM to 9:54 PM (Makara), From 12:41 AM to 2:12 AM (Mesha)",
    date(2026, 7, 8): "From 8:07 PM to 9:46 PM (Makara)",
    date(2026, 7, 9): "From 6:10 AM to 8:33 AM (Karka), From 1:16 PM to 2:55 PM (Tula)",
    date(2026, 7, 12): "From 1:04 PM to 3:28 PM (Tula), From 7:51 PM to 9:30 PM (Makara), From 12:18 AM to 1:49 AM (Mesha)",
    date(2026, 8, 13): "From 10:53 AM to 1:22 PM (Tula), From 1:22 PM to 3:43 PM (Vrishchika), From 10:03 PM to 11:39 PM (Mesha), From 11:39 PM to 1:36 AM (Vrishabha)",
    date(2026, 9, 17): "From 8:41 AM to 11:04 AM (Tula)",
    date(2026, 9, 21): "From 8:25 AM to 10:49 AM (Tula), From 10:49 AM to 1:09 PM (Vrishchika), From 1:09 PM to 3:12 PM (Dhanu), From 7:43 PM to 9:06 PM (Mesha), From 9:06 PM to 10:59 PM (Vrishabha), From 10:59 PM to 1:19 AM (Mithuna)",
    date(2026, 9, 23): "From 8:17 AM to 9:08 AM (Tula)",
    date(2026, 11, 5): "From 7:52 AM to 10:12 AM (Vrishchika), From 10:12 AM to 12:15 PM (Dhanu), From 8:02 PM to 10:13 PM (Mithuna)",
    date(2026, 11, 7): "From 7:44 AM to 10:05 AM (Vrishchika), From 10:05 AM to 12:03 PM (Dhanu), From 7:54 PM to 10:10 PM (Mithuna)",
    date(2026, 11, 8): "From 7:40 AM to 10:01 AM (Vrishchika), From 10:01 AM to 11:27 AM (Dhanu), From 7:50 PM to 10:06 PM (Mithuna)",
    date(2026, 11, 11): "From 9:49 AM to 11:37 AM (Dhanu)",
    date(2026, 11, 12): "From 5:41 PM to 7:35 PM (Vrishabha), From 7:35 PM to 9:50 PM (Mithuna)",
    date(2026, 11, 13): "From 7:24 AM to 9:41 AM (Vrishchika), From 11:44 AM to 1:23 PM (Makara)",
    date(2026, 11, 14): "From 8:23 PM to 9:42 PM (Mithuna), From 9:42 PM to 12:10 AM (Karka)",
    date(2026, 11, 21): "From 9:09 AM to 11:12 AM (Dhanu), From 11:12 AM to 12:51 PM (Makara), From 3:35 PM to 5:06 PM (Mesha), From 6:59 PM to 8:30 PM (Mithuna)",
    date(2026, 12, 9): "From 3:14 AM to 5:38 AM (Tula)",
    date(2026, 12, 10): "From 2:20 PM to 3:51 PM (Mesha), From 5:45 PM to 8:00 PM (Mithuna)",
    date(2026, 12, 11): "From 3:07 AM to 5:30 AM (Tula)",
    date(2026, 12, 12): "From 2:12 PM to 3:43 PM (Mesha), From 5:37 PM to 7:52 PM (Mithuna), From 3:03 AM to 5:26 AM (Tula)",
    date(2027, 1, 15): "From 11:55 AM to 1:30 PM (Mesha), From 1:30 PM to 3:23 PM (Vrishabha)",
    date(2027, 1, 18): "From 12:37 AM to 3:01 AM (Tula), From 3:01 AM to 5:21 AM (Vrishchika)",
    date(2027, 1, 24): "From 11:23 AM to 12:54 PM (Mesha), From 12:54 PM to 2:48 PM (Vrishabha), From 2:48 PM to 5:03 PM (Mithuna), From 12:14 AM to 2:37 AM (Tula)",
    date(2027, 1, 25): "From 1:02 AM to 2:33 AM (Tula), From 2:33 AM to 4:54 AM (Vrishchika)",
    date(2027, 1, 27): "From 12:02 AM to 2:25 AM (Tula), From 2:25 AM to 4:46 AM (Vrishchika)",
    date(2027, 1, 28): "From 11:07 AM to 12:33 PM (Mesha), From 12:33 PM to 2:32 PM (Vrishabha), From 2:32 PM to 4:48 PM (Mithuna), From 2:21 AM to 4:42 AM (Vrishchika)",
    date(2027, 1, 29): "From 11:03 AM to 12:35 PM (Mesha), From 12:35 PM to 2:28 PM (Vrishabha), From 2:28 PM to 4:44 PM (Mithuna)",
    date(2027, 1, 31): "From 10:55 AM to 12:27 PM (Mesha), From 12:27 PM to 2:20 PM (Vrishabha), From 2:20 PM to 4:36 PM (Mithuna), From 11:42 PM to 2:10 AM (Tula)",
    date(2027, 2, 3): "From 10:44 AM to 12:15 PM (Mesha)",
    date(2027, 2, 4): "From 3:31 PM to 4:20 PM (Mithuna), From 11:26 PM to 1:54 AM (Tula), From 1:54 AM to 4:15 AM (Vrishchika)",
    date(2027, 2, 5): "From 10:36 AM to 12:07 PM (Mesha), From 12:07 PM to 2:00 PM (Vrishabha), From 2:00 PM to 4:16 PM (Mithuna)",
    date(2027, 2, 10): "From 10:16 AM to 11:47 AM (Mesha), From 11:47 AM to 1:41 PM (Vrishabha), From 1:41 PM to 3:56 PM (Mithuna), From 11:03 PM to 1:30 AM (Tula), From 1:30 AM to 3:51 AM (Vrishchika)",
    date(2027, 2, 15): "From 9:57 AM to 11:23 AM (Mesha), From 1:21 PM to 3:37 PM (Mithuna), From 10:43 PM to 1:11 AM (Tula), From 1:11 AM to 3:25 AM (Vrishchika)",
    date(2027, 2, 24): "From 9:21 AM to 10:52 AM (Mesha), From 10:52 AM to 12:46 PM (Vrishabha), From 12:46 PM to 3:01 PM (Mithuna), From 12:35 AM to 2:56 AM (Vrishchika)",
    date(2027, 2, 27): "From 11:39 AM to 12:34 PM (Vrishabha), From 12:34 PM to 2:50 PM (Mithuna), From 9:56 PM to 12:23 AM (Tula), From 2:44 AM to 4:47 AM (Dhanu)",
    date(2027, 2, 28): "From 9:05 AM to 10:37 AM (Mesha), From 10:37 AM to 12:30 PM (Vrishabha), From 12:30 PM to 1:46 PM (Mithuna)",
    date(2027, 3, 1): "From 9:44 PM to 12:12 AM (Tula), From 12:12 AM to 2:32 AM (Vrishchika)",
    date(2027, 3, 3): "From 10:33 PM to 12:04 AM (Vrishchika), From 12:04 AM to 2:25 AM (Vrishchika)",
    date(2027, 3, 4): "From 8:46 AM to 10:17 AM (Mesha), From 10:17 AM to 12:10 PM (Vrishabha), From 12:10 PM to 2:26 PM (Mithuna), From 9:32 PM to 12:00 AM (Tula), From 12:00 AM to 1:35 AM (Vrishchika)",
    date(2027, 3, 7): "From 8:34 AM to 10:05 AM (Mesha), From 10:05 AM to 11:59 AM (Vrishabha), From 11:59 AM to 1:46 PM (Mithuna)",
    date(2027, 3, 10): "From 8:22 AM to 9:53 AM (Mesha), From 9:53 AM to 10:52 AM (Vrishabha)",
    date(2027, 3, 11): "From 9:49 AM to 11:43 AM (Vrishabha), From 11:43 AM to 1:58 PM (Mithuna), From 9:05 PM to 11:28 PM (Tula), From 11:28 PM to 1:53 AM (Vrishchika)",
    date(2027, 3, 12): "From 9:45 AM to 11:22 AM (Vrishabha)",
}

EMPTY_MONTH_REASONS = {
    (2026, 8): "Only one Khandar Saath is listed during this period.",
    (2026, 10): "No Khandar Saath is listed during this Jantri month.",
}

def is_covered_by_jantri(date_obj: date) -> bool:
    return JANTRI_COVERAGE_START <= date_obj <= JANTRI_COVERAGE_END

def is_khandar_jantri_date(date_obj: date) -> bool:
    return date_obj in KHANDAR_JANTRI_DATES

def get_khandar_timing(date_obj: date) -> str | None:
    return KHANDAR_JANTRI_TIMING_NOTES.get(date_obj)

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
                day for day in KHANDAR_JANTRI_DATES
                if cursor <= day <= month_end
            ]
            if not month_dates:
                if is_covered_by_jantri(cursor) and is_covered_by_jantri(month_end):
                    reason = EMPTY_MONTH_REASONS.get(
                        (cursor.year, cursor.month),
                        "No Khandar Saath is listed in this Jantri month.",
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
