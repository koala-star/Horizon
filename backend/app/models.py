from datetime import date
from enum import Enum
from pydantic import BaseModel, Field

class Availability(BaseModel):
    available: bool
    reason: str | None = None
    count: int | None = None

class HomeworkStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class HomeworkStatusUpdate(BaseModel):
    status: HomeworkStatus

class Homework(BaseModel):
    id: str
    subject: str | None = None
    description: str | None = None
    due_date: date | None = None
    status: HomeworkStatus = HomeworkStatus.TODO
    source_available: bool = False

class Dashboard(BaseModel):
    connection: Availability
    next_class: Availability
    timetable: Availability
    grades: Availability
    homework: Availability
    absences: Availability
    news: Availability

class ConnectionRequest(BaseModel):
    url: str = Field(min_length=8, max_length=500)
    username: str = Field(min_length=1, max_length=200)
    password: str = Field(min_length=1, max_length=500)
