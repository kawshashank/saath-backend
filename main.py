import os
import datetime
from typing import Literal
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.rules_engine import evaluate_day
from core.kahnethar_jantri import (
    JANTRI_COVERAGE_END as KAHN_END,
    JANTRI_COVERAGE_START as KAHN_START,
    get_empty_month_summaries as get_kahn_empty,
)
from core.khandar_jantri import (
    JANTRI_COVERAGE_END as KHANDAR_END,
    JANTRI_COVERAGE_START as KHANDAR_START,
    get_empty_month_summaries as get_khandar_empty,
)

app = FastAPI(title="Vijayshwar Saath Calculator Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, 
    allow_methods=["*"],
    allow_headers=["*"],
)

class SaathRequest(BaseModel):
    event_type: Literal["kahnethar", "khandar"]
    start_date: str
    end_date: str
    config: dict = {}

@app.post("/api/v1/calculate")
def calculate_muhurat(request: SaathRequest):
    start = datetime.datetime.strptime(request.start_date, "%Y-%m-%d").date()
    end = datetime.datetime.strptime(request.end_date, "%Y-%m-%d").date()
    if start > end:
        raise HTTPException(status_code=422, detail="Start date must not be after end date.")
        
    c_start = KAHN_START if request.event_type == "kahnethar" else KHANDAR_START
    c_end = KAHN_END if request.event_type == "kahnethar" else KHANDAR_END
    
    if start < c_start or end > c_end:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Dates for {request.event_type} are available from "
                f"{c_start.isoformat()} to {c_end.isoformat()}."
            ),
        )
    
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
        response["empty_months"] = get_kahn_empty(start, end)
    elif request.event_type == "khandar":
        response["empty_months"] = get_khandar_empty(start, end)
    return response
