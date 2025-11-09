"""
FastAPI backend for the Bet‑Analyzer prototype.

This application exposes a minimal set of JSON endpoints to support
the front‑end prototype. It serves mock data so that the front end
can be developed and tested without a full database or scraping
pipeline. The structure of the responses mirrors the final API
design: each course has an identifier, discipline, top picks and
value bet metadata, and the API can filter and aggregate across
courses.

To run the application locally use::

    uvicorn main:app --host 0.0.0.0 --port 8000

The API will then be available at ``http://localhost:8000`` and
the interactive documentation at ``http://localhost:8000/docs``.
"""

from fastapi import FastAPI, HTTPException, Query
from typing import Dict, List, Optional

app = FastAPI(title="Bet Analyzer API", version="0.1.0")

# ---------------------------------------------------------------------------
# Mock data. In a production application this would be generated on the fly
# from real race data, odds and scoring models. Here we provide two example
# courses to demonstrate the API shape. You can adjust or extend this
# dictionary to include more races or different disciplines.
mock_courses: Dict[str, Dict] = {
    "2025-11-06-R1-C4": {
        "course_id": "2025-11-06-R1-C4",
        "date": "2025-11-06",
        "hippodrome": "Vincennes",
        "discipline": "TROT",
        "top": [
            {
                "cheval": "Kemio du Chêne",
                "note": 87.5,
                "probabilite": 0.30,
                "cote": 4.2,
                "value_edge": 0.08,
            },
            {
                "cheval": "Kazachok",
                "note": 78.0,
                "probabilite": 0.20,
                "cote": 6.7,
                "value_edge": 0.04,
            },
            {
                "cheval": "Kaline du Locher",
                "note": 71.2,
                "probabilite": 0.15,
                "cote": 15.0,
                "value_edge": 0.02,
            },
        ],
    },
    "2025-11-06-R3-C2": {
        "course_id": "2025-11-06-R3-C2",
        "date": "2025-11-06",
        "hippodrome": "Chantilly",
        "discipline": "GALOP",
        "top": [
            {
                "cheval": "Galactique",
                "note": 91.3,
                "probabilite": 0.32,
                "cote": 3.5,
                "value_edge": 0.10,
            },
            {
                "cheval": "Belle Étoile",
                "note": 80.1,
                "probabilite": 0.24,
                "cote": 5.0,
                "value_edge": 0.05,
            },
            {
                "cheval": "Duc de Paris",
                "note": 73.0,
                "probabilite": 0.18,
                "cote": 8.0,
                "value_edge": 0.03,
            },
        ],
    },
}


def _filter_by_discipline(courses: Dict[str, Dict], discipline: Optional[str]) -> Dict[str, Dict]:
    """Return only courses matching the requested discipline.

    Discipline can be 'GALOP' or 'TROT'. If None, all courses are returned.
    """
    if discipline is None:
        return courses
    discipline = discipline.upper()
    return {cid: c for cid, c in courses.items() if c.get("discipline") == discipline}


@app.get("/api/programme")
def get_programme(
    discipline: Optional[str] = Query(
        None, description="Filtrer par discipline (GALOP ou TROT)."),
    value_only: bool = Query(
        False, description="Si vrai, ne renvoie que le meilleur cheval pour chaque course."),
    top: int = Query(
        3, ge=1, le=10, description="Nombre de chevaux à renvoyer pour chaque course."),
) -> List[Dict]:
    """Liste les courses du jour avec leurs meilleurs chevaux.

    - **discipline**: optionnel, filtre GALOP/TROT.
    - **value_only**: si vrai, renvoie uniquement le meilleur cheval de chaque course.
    - **top**: nombre maximum de chevaux à renvoyer par course.
    """
    filtered = _filter_by_discipline(mock_courses, discipline)
    results: List[Dict] = []
    for course in filtered.values():
        entry = {
            "course_id": course["course_id"],
            "date": course["date"],
            "hippodrome": course["hippodrome"],
            "discipline": course["discipline"],
        }
        horses = course["top"][:top]
        if value_only and horses:
            entry["best_pick"] = horses[0]
        else:
            entry["top"] = horses
        results.append(entry)
    return results


@app.get("/api/valuebets")
def get_valuebets(top: int = Query(3, ge=1, le=10)) -> List[Dict]:
    """Retourne les meilleurs value bets parmi toutes les courses.

    Les chevaux sont triés par valeur (edge) décroissant, puis par note.
    - **top**: nombre maximum de chevaux à renvoyer.
    """
    all_horses: List[Dict] = []
    for course_id, course in mock_courses.items():
        for h in course["top"]:
            # Annotate with course_id for context
            all_horses.append({"course_id": course_id, **h})
    # Sort by value_edge desc then note desc
    all_horses.sort(key=lambda x: (x["value_edge"], x["note"]), reverse=True)
    return all_horses[:top]


@app.get("/api/course/{course_id}")
def get_course(course_id: str) -> Dict:
    """Retourne les détails et le classement d'une course donnée.

    - **course_id**: identifiant unique de la course (ex: "2025-11-06-R1-C4").
    """
    course = mock_courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course inconnue")
    return course