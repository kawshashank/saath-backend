import os
import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.rules_engine import evaluate_day
from core.kahnethar_jantri import JANTRI_COVERAGE_END, JANTRI_COVERAGE_START

app = FastAPI(title="Vijayshwar Saath Calculator Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, 
    allow_methods=["*"],
    allow_headers=["*"],
)

class SaathRequest(BaseModel):
    event_type: str
    start_date: str
    end_date: str
    config: dict = {}

@app.post("/api/v1/calculate")
def calculate_muhurat(request: SaathRequest):
    start = datetime.datetime.strptime(request.start_date, "%Y-%m-%d").date()
    end = datetime.datetime.strptime(request.end_date, "%Y-%m-%d").date()
    
    results = []
    current_date = start
    
    while current_date <= end:
        day_eval = evaluate_day(current_date, request.event_type, request.config)
        if day_eval["is_auspicious"]:
            results.append(day_eval)
        current_date += datetime.timedelta(days=1)
        
    response = {
        "event": request.event_type,
        "range": f"{request.start_date} to {request.end_date}",
        "auspicious_days": results
    }
    if request.event_type == "kahnethar":
        response["source"] = "Vijayshwar Jantri (published Jatakarma/Kahnethar Saath)"
        response["coverage"] = (
            f"{JANTRI_COVERAGE_START.isoformat()} to "
            f"{JANTRI_COVERAGE_END.isoformat()}"
        )
    return response
