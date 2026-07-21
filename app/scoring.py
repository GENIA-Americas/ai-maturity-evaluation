from app.schemas import MaturityResponses

CATEGORY_WEIGHTS = {
    "data_readiness": 0.20,
    "talent": 0.15,
    "governance": 0.15,
    "infrastructure": 0.15,
    "leadership": 0.10,
    "production_maturity": 0.25,
}

MAX_CATEGORY_SCORE = 5.0


def score_evaluation(responses: MaturityResponses) -> tuple[dict, float, str]:
    category_raw = {
        "data_readiness": (responses.data_centralized + responses.data_quality_process) / 2,
        "talent": (responses.ai_literate_staff + responses.dedicated_owner) / 2,
        "governance": (responses.has_ai_policy + responses.risk_review_process) / 2,
        "infrastructure": (responses.cloud_or_api_access + responses.integration_capacity) / 2,
        "leadership": (responses.leadership_buy_in + responses.budget_allocated) / 2,
        "production_maturity": (responses.models_in_production + responses.continuous_monitoring) / 2,
    }

    category_scores = {
        cat: {"score": round(raw, 2), "max_score": MAX_CATEGORY_SCORE, "weight": CATEGORY_WEIGHTS[cat]}
        for cat, raw in category_raw.items()
    }

    weighted_sum = sum(category_raw[cat] * CATEGORY_WEIGHTS[cat] for cat in CATEGORY_WEIGHTS)
    overall_score = round((weighted_sum / MAX_CATEGORY_SCORE) * 100, 2)

    return category_scores, overall_score, tier_for_score(overall_score)


def tier_for_score(overall_score: float) -> str:
    if overall_score >= 80:
        return "Optimizing"
    if overall_score >= 60:
        return "Managed"
    if overall_score >= 35:
        return "Developing"
    return "Initial"
