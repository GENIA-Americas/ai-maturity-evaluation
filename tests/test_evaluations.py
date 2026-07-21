import os

os.environ["DATABASE_URL"] = "sqlite:///./test_maturity.db"

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

BASE_RESPONSES = {
    "data_centralized": 3,
    "data_quality_process": 3,
    "ai_literate_staff": 2,
    "dedicated_owner": 3,
    "has_ai_policy": 2,
    "risk_review_process": 2,
    "cloud_or_api_access": 4,
    "integration_capacity": 3,
    "leadership_buy_in": 4,
    "budget_allocated": 3,
    "models_in_production": 1,
    "continuous_monitoring": 1,
}


def payload(org_name="Acme Test Co", **overrides):
    responses = {**BASE_RESPONSES, **overrides}
    return {"org_name": org_name, "sector": "Manufacturing", "org_size": "51-200", "responses": responses}


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_create_evaluation():
    resp = client.post("/evaluations", json=payload())
    assert resp.status_code == 201
    body = resp.json()
    assert body["maturity_tier"] in {"Initial", "Developing", "Managed", "Optimizing"}


def test_get_evaluation():
    created = client.post("/evaluations", json=payload()).json()
    resp = client.get(f"/evaluations/{created['id']}")
    assert resp.status_code == 200


def test_get_missing_evaluation_404():
    assert client.get("/evaluations/999999").status_code == 404


def test_trend_computes_deltas():
    org = "Trend Test Org"
    client.post("/evaluations", json=payload(org_name=org, models_in_production=1))
    client.post("/evaluations", json=payload(org_name=org, models_in_production=4))

    resp = client.get(f"/organizations/{org}/trend")
    assert resp.status_code == 200
    points = resp.json()
    assert len(points) == 2
    assert points[0]["delta_from_previous"] is None
    assert points[1]["delta_from_previous"] is not None


def test_trend_missing_org_404():
    assert client.get("/organizations/Nonexistent Org/trend").status_code == 404
