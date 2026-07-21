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
6/6 tests pass as of last verified run.

## API
- `POST /evaluations` — submit a maturity questionnaire, get category scores + tier
  (`Initial` / `Developing` / `Managed` / `Optimizing`).
- `GET /evaluations/{id}` — retrieve one evaluation.
- `GET /organizations/{org_name}/trend` — all evaluations for an org, ordered by time,
  with `delta_from_previous` computed between consecutive entries.
- `GET /health`
