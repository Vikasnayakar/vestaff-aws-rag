import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from backend.database import Base

class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(String, nullable=False)
    answer_text = Column(String, nullable=False)
    latency_seconds = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    no_answer_found = Column(Boolean, default=False)