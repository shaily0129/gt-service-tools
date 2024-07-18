from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import List, Optional
from enum import Enum


class TriageCategory(Enum):
    EXPECTANT = "expectant"
    IMMEDIATE = "immediate"
    DELAYED = "delayed"
    MINOR = "minor"


class Patient(BaseModel):
    id: UUID
    name: str
    triage_score: int
    triage_category: Optional[TriageCategory] = None
    physiology_record: Optional[dict] = None  # Adding the missing attribute


class PatientUpdateRequest(BaseModel):
    name: Optional[str]
    triage_score: Optional[int]
    triage_category: Optional[TriageCategory]
    physiology_record: Optional[dict]  # Include in update request if necessary


class Threshold(BaseModel):
    min_value: int
    max_value: int
