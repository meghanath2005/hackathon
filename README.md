# CycloneQ — Hybrid Quantum–Classical Indian Cyclone Track Forecasting Dashboard

CycloneQ is a hackathon-focused MVP for **trajectory forecasting of North Indian Ocean cyclones**. It compares a classical baseline against a compact hybrid quantum-classical model and visualizes predicted vs observed storm tracks on an interactive map.

> **Honesty note:** this is a prototype for demonstration and experimentation, not an operational disaster warning system.

## 1) Hackathon Problem Statement
Cyclone-prone regions around the Bay of Bengal and Arabian Sea need fast, interpretable forecast tooling. CycloneQ demonstrates a compact full-stack pipeline that can:
- select a known historical cyclone,
- forecast next 24h/48h trajectory,
- compare classical vs hybrid quantum-classical predictions,
- explain where a quantum layer fits in a realistic workflow.

## 2) Architecture Overview
- **Frontend (React + Vite + Tailwind + React Leaflet)**
  - Landing page
  - Forecast dashboard with map overlays and metric cards
  - Quantum explainer page
- **Backend (FastAPI)**
  - `GET /health`
  - `GET /cyclones`
  - `POST /predict/classical`
  - `POST /predict/hybrid`
  - `GET /metrics`
- **ML stack**
  - Persistence baseline
  - GRU baseline (PyTorch)
  - Hybrid GRU + 4-qubit variational layer (PennyLane)

See `docs/architecture.md` for the implementation plan and structure rationale.

## 3) Data Pipeline
Data is intentionally lightweight and demo-safe:
- Source sample: `data/samples/tracks.csv`, `data/samples/cyclones.json`
- Preprocess script: `python scripts/prepare_data.py`
- Output: `data/processed/cyclone_tracks_processed.csv`, `data/processed/split.json`

Feature set includes lat/lon history, wind, pressure, and derived motion features (`heading_lat`, `heading_lon`, `speed_proxy`).

## 4) Models
### Persistence baseline
Projects future points by extending latest displacement vector.

### Classical GRU baseline
A compact GRU encoder and dense head predict next coordinate.

### Hybrid quantum-classical model
`sequence -> GRU encoder -> 4-qubit variational circuit -> dense head`
- Quantum block uses angle embedding + entangler layers.
- Runs on simulator (`default.qubit`) for reproducibility.
- Intended as exploratory quantum feature transform.

## 5) Run Locally
## Prerequisites
- Python 3.11+
- Node.js 20+

### Backend setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend setup
```bash
cd frontend
npm install
npm run dev
```
Frontend defaults to `http://localhost:8000` backend.

## 6) Training & Evaluation Commands
From repo root:
```bash
python scripts/prepare_data.py
python scripts/train_classical.py
python scripts/train_hybrid.py
python scripts/evaluate_models.py
python scripts/generate_demo_assets.py
```

If training is skipped, the API still runs with deterministic forecast logic and fallback metrics (`ml/saved_models/metrics_summary.json`).

## 7) API Response Shape
`POST /predict/classical` and `POST /predict/hybrid` return:
- model name
- cyclone id
- horizon hours
- predicted track points
- actual track points
- metrics (MAE, RMSE, track error km, parameter count)

## 8) Project Structure
```
backend/         FastAPI app and API routes
frontend/        React app with map + metrics dashboard
data/            raw/processed/sample datasets
ml/              classical + quantum model modules
scripts/         prepare/train/evaluate helper scripts
docs/            architecture/data/modeling/demo docs
notebooks/       notebook placeholders for exploratory work
```

## 9) Limitations
- Uses compact demo dataset (not full IBTrACS production ingestion).
- Forecast objective is simplified to short-horizon track continuation.
- Hybrid model uses simulator; no hardware execution.
- No claim of quantum advantage or deployment readiness.

## 10) Future Improvements
- ingest larger IBTrACS subset and richer environmental predictors,
- multi-step direct sequence forecasting,
- uncertainty cones and ensemble methods,
- stronger validation splits by year/storm regime,
- deployment packaging and monitoring.
