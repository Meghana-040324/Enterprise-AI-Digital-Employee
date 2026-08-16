from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AITaskRequest(BaseModel):
    prompt: str = Field(min_length=1)
    session_id: str = "default"
    persona: str = "enterprise"


class AITaskResponse(BaseModel):
    status: str
    response: str
    executionTimeMs: float
    action: Optional[str] = None
    incident_number: Optional[str] = None


class IncidentRequest(BaseModel):
    short_description: str
    description: Optional[str] = None
    urgency: str = "2"
    impact: str = "2"


class IncidentResponse(BaseModel):
    success: bool
    number: Optional[str] = None
    sys_id: Optional[str] = None
    message: str


class DocumentResponse(BaseModel):
    success: bool
    filename: str
    document_id: str
    characters: int
    message: str


class DocumentQuestionRequest(BaseModel):
    question: str
    session_id: str = "default"


class AnalyticsResponse(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    incidents_created: int
    documents_uploaded: int
    average_response_time_ms: float
    action_counts: Dict[str, int]