import datetime
import unittest

from core.kahnethar_jantri import get_empty_month_summaries, get_kahnethar_timing
from core.rules_engine import evaluate_day


class KahnetharJantriRegressionTests(unittest.TestCase):
    """Verify the source-backed Vijayshwar Jantri date index."""

    def test_known_jantri_windows(self):
        cases = {
            (2026, 3): {20, 25, 27},
            (2026, 4): {3, 6, 20, 23, 29},
            (2026, 5): {3, 4},
            (2026, 6): {17, 21, 24, 25},
            (2026, 7): {1, 2, 3, 5},
            (2026, 8): set(),
            (2026, 9): {17, 21, 23, 24},
            (2026, 10): {30},
            (2026, 11): {11, 20, 22, 25, 26},
            (2026, 12): {13, 14},
            (2027, 1): {15, 20},
            (2027, 2): {8, 11, 18, 19, 22, 25, 26},
            (2027, 3): {10, 11, 17, 18},
        }

        for (year, month), expected_days in cases.items():
            with self.subTest(year=year, month=month):
                actual_days = {
                    day
                    for day in range(1, 32)
                    if self._is_valid_date(year, month, day)
                    and evaluate_day(
                        datetime.date(year, month, day), "kahnethar", {}
                    )["is_auspicious"]
                }
                self.assertEqual(actual_days, expected_days)

    def test_timing_notes_and_empty_month_reason(self):
        self.assertEqual(
            get_kahnethar_timing(datetime.date(2026, 12, 13)),
            "From 4:47 AM",
        )
        self.assertIsNone(get_kahnethar_timing(datetime.date(2026, 12, 14)))

        summaries = get_empty_month_summaries(
            datetime.date(2026, 7, 1), datetime.date(2026, 9, 30)
        )
        self.assertEqual(summaries, [{
            "month": "2026-08",
            "label": "August 2026",
            "reason": "No Kahnethar Saath is listed during Shukra Ash / As-Sang.",
        }])

    @staticmethod
    def _is_valid_date(year, month, day):
        try:
            datetime.date(year, month, day)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    unittest.main()
