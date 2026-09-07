import datetime
import unittest

from core.rules_engine import evaluate_day


class KahnetharJantriRegressionTests(unittest.TestCase):
    """Published Vijayshwar Jantri dates; never use these as runtime data."""

    def test_known_jantri_windows(self):
        cases = {
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

    @staticmethod
    def _is_valid_date(year, month, day):
        try:
            datetime.date(year, month, day)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    unittest.main()
