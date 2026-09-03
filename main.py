import os
import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.rules_engine import evaluate_day

app = FastAPI(title="Saath Calculator API (Vijayshwar Tradition)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Keep open for now, lock to Vercel URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SaathRequest(BaseModel):
    event_type: str
    start_date: str
    end_date: str
    config: dict = {
        "allow_purnima": False,
        "strict_chaturmas": True
    }

@app.get("/")
def read_root():
    return {"status": "online", "message": "Upgraded Saath Engine is running."}

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
        
    return {
        "event": request.event_type,
        "range_evaluated": f"{request.start_date} to {request.end_date}",
        "auspicious_days": results
    }