import os
import datetime
from typing import Literal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.rules_engine import evaluate_day
from core.kahnethar_jantri import get_empty_month_summaries

app = FastAPI(title="Vijayshwar Saath Calculator Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, 
    allow_methods=["*"],
    allow_headers=["*"],
)

class SaathRequest(BaseModel):
    event_type: Literal["kahnethar"]
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
        response["empty_months"] = get_empty_month_summaries(start, end)
    return response
