from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import ComplianceEvent
from schemas import EventCreate

app = FastAPI(title="RegulAegis AI")

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "RegulAegis Backend Running"}


@app.post("/event")
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    new_event = ComplianceEvent(
        event_type=event.event_type,
        title=event.title,
        department=event.department,
        severity=event.severity,
        description=event.description,
        status=event.status,
        date=event.date
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {
        "success": True,
        "id": new_event.id
    }


@app.get("/events")
def get_events(
    db: Session = Depends(get_db)
):
    return db.query(ComplianceEvent).all()

@app.get("/dashboard")
def dashboard():

    return {
        "compliance_score": 82,
        "open_findings": 12,
        "critical_risks": 3,
        "missed_deadlines": 4
    }

@app.get("/timeline")
def timeline(
    db: Session = Depends(get_db)
):
    return db.query(
        ComplianceEvent
    ).order_by(
        ComplianceEvent.date
    ).all()

@app.get("/risks")
def get_risks():

    return [
        {
            "id":"RISK001",
            "title":"Firewall Retention Risk",
            "department":"IT",
            "risk_score":89,
            "status":"Critical"
        }
    ]

@app.get("/risk/{risk_id}")
def get_risk(risk_id: str):

    return {
        "id":risk_id,
        "title":"Firewall Retention Risk",
        "department":"IT",
        "risk_score":89,
        "status":"Critical",
        "severity":"High",
        "reasons":[
            "Repeated Findings",
            "Missed Deadline",
            "New Regulation Impact"
        ],
        "ai_analysis":"This issue remained unresolved for 120 days. A remediation deadline was missed and a new regulation impacts the finding."
    }

@app.get("/alerts")
def alerts():

    return [
        {
            "severity":"Critical",
            "message":"Firewall retention issue unresolved"
        }
    ]