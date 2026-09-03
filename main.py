from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import swisseph as swe
from datetime import datetime

app = FastAPI(title="Saath Calculator Engine")

# Allow your future Vercel frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # We will lock this down to your Vercel URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SaathRequest(BaseModel):
    event_type: str
    start_date: str
    end_date: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "Saath Engine is listening."}

@app.post("/api/calculate")
def calculate_saath(req: SaathRequest):
    try:
        # Prove the engine works by calculating the Moon's longitude for the start date
        dt = datetime.strptime(req.start_date, "%Y-%m-%d")
        jd = swe.julday(dt.year, dt.month, dt.day, 12.0)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        moon_pos, _ = swe.calc_ut(jd, swe.MOON)
        
        return {
            "event": req.event_type,
            "julian_day": jd,
            "moon_longitude_proof": round(moon_pos[0], 2),
            "results": [
                {
                    "date": req.start_date,
                    "tithi": "Dummy Tithi (Engine Alive)",
                    "nakshatra": "Dummy Nakshatra",
                    "score": "Excellent"
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))