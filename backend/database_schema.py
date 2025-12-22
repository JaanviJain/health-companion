from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class HealthRecord(BaseModel):
    record_id: str
    user_id: str
    record_type: str  # lab_report, prescription, imaging, consultation
    date: Optional[datetime]
    raw_text: str
    structured_data: dict
    created_at: datetime

class TimelineEvent(BaseModel):
    event_id: str
    user_id: str
    event_type: str
    date: Optional[datetime]
    title: str
    description: str
    related_records: List[str]