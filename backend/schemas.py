from pydantic import BaseModel

class EventCreate(BaseModel):
    event_type: str
    title: str
    department: str
    severity: str
    description: str
    status: str
    date: str


class EventResponse(EventCreate):
    id: int

    class Config:
        from_attributes = True