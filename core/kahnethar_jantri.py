"""Published Vijayshwar Jantri Kahnethar (Jatakarma) dates.

This edition explicitly lists Kahnethar Saath dates from March 2026 through
March 2027. It is source data transcribed from the Jantri, not an inferred
astronomical rule or a collection of range-specific exceptions.
"""

from datetime import date


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


def is_covered_by_jantri(date_obj: date) -> bool:
    return JANTRI_COVERAGE_START <= date_obj <= JANTRI_COVERAGE_END


def is_kahnethar_jantri_date(date_obj: date) -> bool:
    return date_obj in KAHNETHAR_JANTRI_DATES
