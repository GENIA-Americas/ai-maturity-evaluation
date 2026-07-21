import os

os.environ["DATABASE_URL"] = "sqlite:///./test_maturity.db"
os.environ["API_KEYS"] = "devkey1:acme_corp,devkey2:globex_inc,devkey3:brandnew_org"

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

ACME_HEADERS = {"X-API-Key": "devkey1"}
GLOBEX_HEADERS = {"X-API-Key": "devkey2"}
BRANDNEW_HEADERS = {"X-API-Key": "devkey3"}

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


def payload(**overrides):
    responses = {**BASE_RESPONSES, **overrides}
    return {"sector": "Manufacturing", "org_size": "51-200", "responses": responses}


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_create_evaluation_requires_api_key():
    resp = client.post("/evaluations", json=payload())
    assert resp.status_code == 401


def test_create_evaluation():
    resp = client.post("/evaluations", json=payload(), headers=ACME_HEADERS)
    assert resp.status_code == 201
    body = resp.json()
    assert body["org_name"] == "acme_corp"
    assert body["maturity_tier"] in {"Initial", "Developing", "Managed", "Optimizing"}


def test_get_evaluation():
    created = client.post("/evaluations", json=payload(), headers=ACME_HEADERS).json()
    resp = client.get(f"/evaluations/{created['id']}", headers=ACME_HEADERS)
    assert resp.status_code == 200


def test_cannot_read_another_orgs_evaluation():
    created = client.post("/evaluations", json=payload(), headers=ACME_HEADERS).json()
    resp = client.get(f"/evaluations/{created['id']}", headers=GLOBEX_HEADERS)
    assert resp.status_code == 404


def test_get_missing_evaluation_404():
    resp = client.get("/evaluations/999999", headers=ACME_HEADERS)
    assert resp.status_code == 404


def test_trend_requires_api_key():
    assert client.get("/organizations/trend").status_code == 401


def test_trend_computes_deltas():
    client.post("/evaluations", json=payload(models_in_production=1), headers=ACME_HEADERS)
    client.post("/evaluations", json=payload(models_in_production=4), headers=ACME_HEADERS)

    resp = client.get("/organizations/trend", headers=ACME_HEADERS)
    assert resp.status_code == 200
    points = resp.json()
    assert len(points) >= 2
    assert points[0]["delta_from_previous"] is None


def test_trend_only_returns_own_org():
    client.post("/evaluations", json=payload(), headers=ACME_HEADERS)
    client.post("/evaluations", json=payload(), headers=GLOBEX_HEADERS)

    acme_trend = client.get("/organizations/trend", headers=ACME_HEADERS).json()
    globex_trend = client.get("/organizations/trend", headers=GLOBEX_HEADERS).json()
    assert len(acme_trend) >= 1
    assert len(globex_trend) >= 1


def test_trend_404_for_org_with_no_evaluations():
    resp = client.get("/organizations/trend", headers=BRANDNEW_HEADERS)
    assert resp.status_code == 404
