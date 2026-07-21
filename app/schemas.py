from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

OrgSize = Literal["1-10", "11-50", "51-200", "200+"]


class MaturityResponses(BaseModel):
    """0-5 per question, same shape family as ai-readiness-assessment."""

    model_config = ConfigDict(extra="forbid")

    data_centralized: int = Field(ge=0, le=5)
    data_quality_process: int = Field(ge=0, le=5)
    ai_literate_staff: int = Field(ge=0, le=5)
    dedicated_owner: int = Field(ge=0, le=5)
    has_ai_policy: int = Field(ge=0, le=5)
    risk_review_process: int = Field(ge=0, le=5)
    cloud_or_api_access: int = Field(ge=0, le=5)
    integration_capacity: int = Field(ge=0, le=5)
    leadership_buy_in: int = Field(ge=0, le=5)
    budget_allocated: int = Field(ge=0, le=5)
    models_in_production: int = Field(ge=0, le=5, description="AI/ML models actually running in prod")
    continuous_monitoring: int = Field(ge=0, le=5, description="Monitoring/retraining process in place")


class EvaluationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sector: str = Field(min_length=1, max_length=100)
    org_size: OrgSize
    responses: MaturityResponses


class EvaluationResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    org_name: str
    sector: str
    org_size: str
    category_scores: dict
    overall_score: float
    maturity_tier: str
    created_at: datetime


class TrendPoint(BaseModel):
    id: int
    overall_score: float
    maturity_tier: str
    created_at: datetime
    delta_from_previous: Optional[float] = None
