from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Evaluation
from app.schemas import EvaluationCreate, EvaluationResult, TrendPoint
from app.scoring import score_evaluation

router = APIRouter(tags=["evaluations"])


@router.post("/evaluations", response_model=EvaluationResult, status_code=201)
def create_evaluation(payload: EvaluationCreate, db: Session = Depends(get_db)):
    category_scores, overall_score, maturity_tier = score_evaluation(payload.responses)

    record = Evaluation(
        org_name=payload.org_name,
        sector=payload.sector,
        org_size=payload.org_size,
        responses=payload.responses.model_dump(),
        category_scores=category_scores,
        overall_score=overall_score,
        maturity_tier=maturity_tier,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/evaluations/{evaluation_id}", response_model=EvaluationResult)
def get_evaluation(evaluation_id: int, db: Session = Depends(get_db)):
    record = db.get(Evaluation, evaluation_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return record


@router.get("/organizations/{org_name}/trend", response_model=list[TrendPoint])
def get_trend(org_name: str, db: Session = Depends(get_db)):
    records = (
        db.query(Evaluation)
        .filter(Evaluation.org_name == org_name)
        .order_by(Evaluation.created_at.asc())
        .all()
    )
    if not records:
        raise HTTPException(status_code=404, detail="No evaluations found for this organization")

    points = []
    previous_score = None
    for r in records:
        delta = None if previous_score is None else round(r.overall_score - previous_score, 2)
        points.append(
            TrendPoint(
                id=r.id,
                overall_score=r.overall_score,
                maturity_tier=r.maturity_tier,
                created_at=r.created_at,
                delta_from_previous=delta,
            )
        )
        previous_score = r.overall_score
    return points
