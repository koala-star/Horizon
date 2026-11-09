from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import initialise, homework_status, update_homework_status
from .models import Availability, ConnectionRequest, Dashboard, Homework, HomeworkStatus, HomeworkStatusUpdate
from .connectors.pronote import PronoteConnector, ConnectorUnavailable

connector = PronoteConnector()

@asynccontextmanager
async def lifespan(_: FastAPI):
    initialise()
    yield

app = FastAPI(title="Horizon API", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "https://koala-star.github.io"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def unavailable() -> Availability:
    return Availability(available=False, reason="Connectez votre compte Pronote pour afficher cette information.")

@app.get("/api/health")
def health():
    return {"status": "ok", "pronote_connected": connector.client is not None}

@app.get("/api/connection/status")
def connection_status():
    return {"connected": connector.client is not None, "provider": "pronote"}

@app.get("/api/dashboard", response_model=Dashboard)
def dashboard():
    if connector.client is None:
        state = unavailable()
        return Dashboard(connection=state, next_class=state, timetable=state, grades=state, homework=state, absences=state, news=state)
    try:
        lessons = connector.upcoming_lessons()
        homework_items = connector.upcoming_homework()
        connected = Availability(available=True)
        return Dashboard(connection=connected, next_class=Availability(available=bool(lessons), count=len(lessons)), timetable=Availability(available=True, count=len(lessons)), grades=Availability(available=True), homework=Availability(available=True, count=len(homework_items)), absences=Availability(available=True), news=Availability(available=True))
    except Exception:
        return Dashboard(connection=Availability(available=True), next_class=Availability(available=False, reason="Données Pronote temporairement indisponibles."), timetable=Availability(available=False, reason="Données Pronote temporairement indisponibles."), grades=Availability(available=False, reason="Données Pronote temporairement indisponibles."), homework=Availability(available=False, reason="Données Pronote temporairement indisponibles."), absences=Availability(available=False, reason="Données Pronote temporairement indisponibles."), news=Availability(available=False, reason="Données Pronote temporairement indisponibles."))

@app.get("/api/homework", response_model=list[Homework])
def homework():
    try:
        return [Homework(id=str(item.id), subject=getattr(getattr(item, "subject", None), "name", None), description=item.description, due_date=item.date, status=HomeworkStatus.DONE if item.done else HomeworkStatus.TODO, source_available=True) for item in connector.upcoming_homework()]
    except ConnectorUnavailable as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=502, detail="Les devoirs Pronote sont temporairement indisponibles.")

@app.patch("/api/homework/{homework_id}", response_model=Homework)
def set_homework_status(homework_id: str, payload: HomeworkStatusUpdate):
    update_homework_status(homework_id, payload.status)
    return Homework(id=homework_id, status=homework_status(homework_id), source_available=False)

@app.post("/api/connection")
def connect(payload: ConnectionRequest):
    try:
        connector.connect(payload.url, payload.username, payload.password)
    except ConnectorUnavailable as exc:
        raise HTTPException(status_code=501, detail=str(exc))
    return {"connected": True}

@app.delete("/api/connection", status_code=204)
def disconnect():
    connector.client = None
