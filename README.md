# ai-maturity-evaluation

Part of the GENIA Americas AI Toolkit — repo #2. Longitudinal AI maturity benchmarking,
reusing the scoring pattern from `ai-readiness-assessment`.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run
```bash
uvicorn app.main:app --reload
```
Docs at http://127.0.0.1:8000/docs

## Test
```bash
pytest tests/ -v
```
10/10 tests pass as of last verified run.

## Auth
All endpoints require an `X-API-Key` header. Keys are configured via the `API_KEYS`
env var as `key1:org_one,key2:org_two` — each key authenticates its caller as exactly
one org, and reads/writes are scoped to that org.

## API
- `POST /evaluations` — submit a maturity questionnaire, get category scores + tier
  (`Initial` / `Developing` / `Managed` / `Optimizing`). Org name is derived from your
  API key, not sent in the request body.
- `GET /evaluations/{id}` — retrieve one evaluation belonging to your org.
- `GET /organizations/trend` — all evaluations for *your* org (the one your API key
  belongs to), ordered by time, with `delta_from_previous` computed between consecutive
  entries. Takes no org parameter — there is no way to request another org's trend.
- `GET /health`
