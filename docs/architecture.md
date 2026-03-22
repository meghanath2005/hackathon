# CycloneQ Architecture & Implementation Plan

## Phase Plan (MVP-first)
1. **Scaffold full-stack app**: FastAPI + React/Vite + Tailwind + Leaflet pages with mock-capable endpoints.
2. **Data pipeline**: build compact processed dataset from sample North Indian Ocean tracks and persist split artifacts.
3. **Classical baseline**: persistence baseline + GRU model, quick-train scripts, saved artifacts.
4. **Hybrid quantum model**: GRU encoder + PennyLane quantum layer + dense head, simulator training script.
5. **Demo polish**: metrics comparison endpoint, map overlays, quantum explainer, reproducible runbook.

## System Design
- **Frontend (React)**
  - Home page, dashboard, and quantum explainer page.
  - Dashboard fetches cyclones and predictions from backend.
  - Leaflet map overlays actual/classical/hybrid tracks.
- **Backend (FastAPI)**
  - Endpoints: `/health`, `/cyclones`, `/predict/classical`, `/predict/hybrid`, `/metrics`.
  - Service layer loads local sample/processed data and metrics artifacts.
  - Consistent Pydantic schemas for requests/responses.
- **ML layer**
  - Classical: persistence + GRU regressor.
  - Hybrid: GRU encoder + 4-qubit variational circuit + MLP head (PennyLane).
  - Scripts support data preparation, training, evaluation, and demo asset generation.

## Practical Hackathon Choices
- Local files instead of DB to keep deployment simple.
- Small fixed demo dataset for guaranteed offline demo reliability.
- Honest claims: exploratory hybrid architecture, not operational cyclone warning system.
