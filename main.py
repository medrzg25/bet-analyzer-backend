import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

# ✅ Scraping du PMU via l'API publique JSON
@app.get("/api/programme")
def programme():
    url = "https://online.pmu.fr/rest/client/1/programme/"
    r = requests.get(url)

    if r.status_code != 200:
        return {"programme": []}

    data = r.json()

    courses = []

    # Transforme les données PMU pour ton front
    for item in data.get("programme", []):
        courses.append({
            "course_id": item["idReunion"],
            "hippodrome": item["hippodrome"],
            "discipline": item["specialite"],
            "distance_m": item["distance"],
            "date": item["dateCourse"]
        })

    return {"programme": courses}


@app.get("/api/valuebets")
def valuebets(top: int = 3):
    url = "https://online.pmu.fr/rest/client/1/programme/"
    r = requests.get(url)

    if r.status_code != 200:
        return {"valuebets": []}

    data = r.json()
    valuebets = []

    for item in data.get("programme", [])[:top]:
        valuebets.append({
            "horse": item["hippodrome"],
            "course_id": item["idReunion"],
            "score": 10,           # Placeholder (on améliorera après avec algo)
            "probability": 0.50,   # Placeholder
            "edge": 0.10           # Placeholder
        })

    return {"valuebets": valuebets}
