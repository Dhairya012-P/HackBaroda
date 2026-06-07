from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from services.risk_engine import calculate_risk
from services.ai_analysis import generate_analysis

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
def get_risks(
    db: Session = Depends(get_db)
):

    events = db.query(
        ComplianceEvent
    ).all()

    risk = calculate_risk(events)

    return [
        {
            "id": "RISK001",
            "title": "Compliance Risk",
            "department": "IT",
            "risk_score": risk["score"],
            "status": risk["level"]
        }
    ]


@app.get("/risk/{risk_id}")
def get_risk(
    risk_id: str,
    db: Session = Depends(get_db)
):

    events = db.query(
        ComplianceEvent
    ).all()

    risk = calculate_risk(events)

    analysis = generate_analysis(risk)

    return {
        "id": risk_id,
        "title": "Compliance Risk",
        "department": "IT",
        "risk_score": risk["score"],
        "status": risk["level"],
        "severity": "High",
        "reasons": risk["reasons"],
        "ai_analysis": analysis
    }


@app.get("/alerts")
def alerts():

    return [
        {
            "severity": "Critical",
            "message": "Firewall retention issue unresolved"
        }
    ]


@app.get("/relationships")
def relationships(
    db: Session = Depends(get_db)
):

    events = db.query(
        ComplianceEvent
    ).all()

    relationships = []

    audit = False
    remediation = False
    deadline = False
    regulation = False

    for event in events:

        if event.event_type == "Audit Finding":
            audit = True

        if event.event_type == "Remediation Assigned":
            remediation = True

        if event.event_type == "Missed Deadline":
            deadline = True

        if event.event_type == "Regulation Update":
            regulation = True

    if audit:
        relationships.append(
            "Audit Finding Detected"
        )

    if audit and remediation:
        relationships.append(
            "Remediation Assigned"
        )

    if remediation and deadline:
        relationships.append(
            "Remediation Failed"
        )

    if deadline and regulation:
        relationships.append(
            "Risk Increased Due To New Regulation"
        )

    return {
        "relationships": relationships
    }


@app.get("/reset")
def reset(
    db: Session = Depends(get_db)
):
    db.query(
        ComplianceEvent
    ).delete()

    db.commit()

    return {
        "message": "All events deleted"
    }