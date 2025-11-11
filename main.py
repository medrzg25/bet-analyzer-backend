from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

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

PMU_API = "https://online.turfinfo.api.pmu.fr/rest/client/infosForMeeting/programme/FR"


@app.get("/api/programme")
def programme():
    # 👉 au lieu de renvoyer du mock, on récupère les vraies courses du jour
    import datetime
    today = datetime.date.today().strftime("%Y-%m-%d")

    url = f"{PMU_API}/{today}"

    response = requests.get(url)
    data = response.json()

    programme = []
    for meeting in data.get("meetings", []):
        for race in meeting.get("races", []):
            programme.append({
                "course_id": race["id"],
                "hippodrome": meeting["name"],
                "discipline": race.get("discipline"),
                "distance_m": race.get("distance"),
                "date": race.get("startTime")
            })

    return {"programme": programme}


@app.get("/api/valuebets")
def valuebets(top: int = 3):
    # 👉 Exemple simple de calcul de valuebet à partir des cotes
    url = "https://online.turfinfo.api.pmu.fr/rest/client/odd/currentOdd/FR"
    data = requests.get(url).json()

    valuebets_list = []

    for meeting in data.get("meetings", []):
        for race in meeting.get("races", []):
            for runner in race.get("runners", []):
                if "odds" in runner:
                    cote = runner["odds"]["value"]
                    if cote > 0:
                        implied_prob = 1 / cote
                        expected = (1 / cote) - implied_prob

                        valuebets_list.append({
                            "horse": runner["name"],
                            "course_id": race["id"],
                            "score": round(10 * expected, 2),
                            "probability": round(implied_prob, 2),
                            "edge": round(expected, 2),
                        })

    # tri des meilleurs valuebets
    valuebets_list = sorted(valuebets_list, key=lambda x: x["edge"], reverse=True)

    return {"valuebets": valuebets_list[:top]}
