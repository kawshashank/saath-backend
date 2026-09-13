from fastapi.testclient import TestClient
from main import app
import traceback

client = TestClient(app)

try:
    response = client.post(
        "/api/v1/calculate",
        json={
            "event_type": "kahnethar",
            "start_date": "2026-03-01",
            "end_date": "2026-03-31",
        },
    )
    print("Status:", response.status_code)
    print("JSON:", response.json())
except Exception as e:
    traceback.print_exc()
