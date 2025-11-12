from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

origins = [
    "https://bet-analyzer-frontend.vercel.app",
    "http://localhost:3000",
    "https://orange-scene-bc30.med-rzg.workers.dev"  # ton proxy Cloudflare
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/programme")
def get_programme():
    try:
        pmu_url = "https://online.pmu.fr/rest/client/1/programme"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
            "Referer": "https://www.pmu.fr/",
        }
        res = requests.get(pmu_url, headers=headers, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"status": "✅ Backend Render opérationnel"}
