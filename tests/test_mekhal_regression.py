import unittest
import datetime
from fastapi.testclient import TestClient
from main import app
from core.mekhal_jantri import get_empty_month_summaries, get_mekhal_timing

client = TestClient(app)

class MekhalJantriRegressionTests(unittest.TestCase):
    def test_known_jantri_dates_are_returned(self):
        response = client.post(
            "/api/v1/calculate",
            json={
                "event_type": "mekhal",
                "start_date": "2026-03-01",
                "end_date": "2026-05-31",
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        auspicious_dates = [d["date"] for d in data.get("auspicious_days", [])]
        
        expected_dates = [
            "2026-03-20", "2026-03-25", "2026-03-27",
            "2026-04-23",
            "2026-05-03", "2026-05-04"
        ]
        
        for date_str in expected_dates:
            self.assertIn(date_str, auspicious_dates)

    def test_timing_notes_retrieval(self):
        self.assertIn(
            "From 7:43 AM to 9:14 AM (Mesha)",
            get_mekhal_timing(datetime.date(2026, 3, 20))
        )
        self.assertIsNone(get_mekhal_timing(datetime.date(2026, 3, 21)))

if __name__ == "__main__":
    unittest.main()
