from fastapi import APIRouter, HTTPException

from app.schemas.cyclone import CyclonesResponse
from app.schemas.prediction import PredictRequest, PredictResponse
from app.services.data_loader import load_cyclones
from app.services.predictor import PredictionService

router = APIRouter()
predictor = PredictionService.build()


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "CycloneQ API"}


@router.get("/cyclones", response_model=CyclonesResponse)
def cyclones() -> CyclonesResponse:
    return CyclonesResponse(cyclones=load_cyclones())


@router.post("/predict/classical", response_model=PredictResponse)
def predict_classical(payload: PredictRequest) -> PredictResponse:
    try:
        return predictor.predict(payload.cyclone_id, payload.forecast_horizon_hours, model="classical")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/predict/hybrid", response_model=PredictResponse)
def predict_hybrid(payload: PredictRequest) -> PredictResponse:
    try:
        return predictor.predict(payload.cyclone_id, payload.forecast_horizon_hours, model="hybrid")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/metrics")
def metrics() -> dict:
    return predictor.summary_metrics
