from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import initialise, homework_status, update_homework_status
from .models import Availability, ConnectionRequest, Dashboard, Homework, HomeworkStatusUpdate
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
    state = unavailable()
    return Dashboard(connection=Availability(available=connector.client is not None, reason=None if connector.client else state.reason), next_class=state, timetable=state, grades=state, homework=state, absences=state, news=state)

@app.get("/api/homework", response_model=list[Homework])
def homework():
    # No items are fabricated when the provider is not connected.
    return []

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
