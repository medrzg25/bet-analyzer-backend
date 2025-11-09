from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Autoriser Vercel Frontend (ton site)
origins = [
    "https://bet-analyzer-frontend.vercel.app",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/programme")
def programme():
    return {
        "programme": [
            {
                "course_id": "C1",
                "hippodrome": "Vincennes",
                "discipline": "Trot",
                "distance_m": 2700,
                "date": "2025-11-09"
            }
        ]
    }

@app.get("/api/valuebets")
def valuebets(top: int = 3):
    return {
        "valuebets": [
            {"horse": "Ninja Star", "course_id": "C1", "score": 9.2, "probability": 0.61, "edge": 0.15}
        ]
    }

