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
from core.mekhal_jantri import (
    JANTRI_COVERAGE_END as MEKHAL_END,
    JANTRI_COVERAGE_START as MEKHAL_START,
    get_empty_month_summaries as get_mekhal_empty,
)


from core.shishur_jantri import (
    JANTRI_COVERAGE_END as SHISHUR_END,
    JANTRI_COVERAGE_START as SHISHUR_START,
    get_empty_month_summaries as get_shishur_empty,
)
from core.gandan_jantri import (
    JANTRI_COVERAGE_END as GANDAN_END,
    JANTRI_COVERAGE_START as GANDAN_START,
    get_empty_month_summaries as get_gandan_empty,
)
from core.pravesh_jantri import (
    JANTRI_COVERAGE_END as PRAVESH_END,
    JANTRI_COVERAGE_START as PRAVESH_START,
    get_empty_month_summaries as get_pravesh_empty,
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
    event_type: Literal["kahnethar", "khandar", "mekhal", "shishur", "gandan", "pravesh"]
    start_date: str
    end_date: str
    config: dict = {}

@app.post("/api/v1/calculate")
def calculate_muhurat(request: SaathRequest):
    start = datetime.datetime.strptime(request.start_date, "%Y-%m-%d").date()
    end = datetime.datetime.strptime(request.end_date, "%Y-%m-%d").date()
    if start > end:
        raise HTTPException(status_code=422, detail="Start date must not be after end date.")
        


    if request.event_type == "kahnethar":
        response["empty_months"] = get_kahn_empty(start, end)
    elif request.event_type == "khandar":
        response["empty_months"] = get_khandar_empty(start, end)
    elif request.event_type == "mekhal":
        response["empty_months"] = get_mekhal_empty(start, end)
    elif request.event_type == "shishur":
        response["empty_months"] = get_shishur_empty(start, end)
    elif request.event_type == "gandan":
        response["empty_months"] = get_gandan_empty(start, end)
    elif request.event_type == "pravesh":
        response["empty_months"] = get_pravesh_empty(start, end)

    return response
