from sqlalchemy import Column, Integer, String
from database import Base

class ComplianceEvent(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String)
    title = Column(String)
    department = Column(String)
    severity = Column(String)
    description = Column(String)
    status = Column(String)
    date = Column(String)