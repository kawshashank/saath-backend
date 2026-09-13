import unittest
import datetime
from fastapi.testclient import TestClient
from main import app
from core.khandar_jantri import get_empty_month_summaries, get_khandar_timing

client = TestClient(app)

class KhandarJantriRegressionTests(unittest.TestCase):
    def test_known_jantri_dates_are_returned(self):
        # Request a few months covered by the Khandar Jantri
        response = client.post(
            "/api/v1/calculate",
            json={
                "event_type": "khandar",
                "start_date": "2026-04-01",
                "end_date": "2026-06-30",
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Extract returned dates
        auspicious_dates = [d["date"] for d in data.get("auspicious_days", [])]
        
        # Some dates transcribed from screenshots:
        expected_dates = [
            "2026-04-16", "2026-04-20", "2026-04-25", "2026-04-26",
            "2026-04-29", "2026-04-30", "2026-05-06", "2026-05-07",
            "2026-05-08", "2026-05-09", "2026-05-10", "2026-06-19",
            "2026-06-20", "2026-06-22", "2026-06-24", "2026-06-26",
            "2026-06-27", "2026-06-28"
        ]
        
        for date_str in expected_dates:
            self.assertIn(date_str, auspicious_dates)

    def test_timing_notes_retrieval(self):
        # 2026-04-25 has specific timings
        self.assertEqual(
            get_khandar_timing(datetime.date(2026, 4, 25)),
            "From 10:55 PM to 1:02 AM (Dhanu), From 1:02 AM to 2:41 AM (Makara)"
        )
        # 2026-04-27 has NO Khandar
        self.assertIsNone(get_khandar_timing(datetime.date(2026, 4, 27)))

    def test_empty_months_reporting(self):
        # August 2026 and October 2026 have specific reasons in the mock data
        # Actually October is not in our transcribed dates for 2026!
        # Let's test the endpoint logic
        response = client.post(
            "/api/v1/calculate",
            json={
                "event_type": "khandar",
                "start_date": "2026-08-01",
                "end_date": "2026-10-31",
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        empty_months = {m["month"]: m["reason"] for m in data.get("empty_months", [])}
        
        # August has 13th August, so it is NOT empty!
        # October should be empty because we transcribed no dates in Oct 2026
        self.assertIn("2026-10", empty_months)
        self.assertEqual(
            empty_months["2026-10"],
            "No Khandar Saath is listed during this Jantri month."
        )

if __name__ == "__main__":
    unittest.main()
