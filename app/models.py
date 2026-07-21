from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    org_name: Mapped[str] = mapped_column(String, index=True)
    sector: Mapped[str] = mapped_column(String)
    org_size: Mapped[str] = mapped_column(String)

    responses: Mapped[dict] = mapped_column(JSON)
    category_scores: Mapped[dict] = mapped_column(JSON)
    overall_score: Mapped[float] = mapped_column(Float)
    maturity_tier: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
