from typing import Literal

from pydantic import BaseModel, Field

from .common import Metrics, TrackPoint


class PredictRequest(BaseModel):
    cyclone_id: str
    forecast_horizon_hours: int = Field(24, description="Supported: 24 or 48")


class PredictResponse(BaseModel):
    model: Literal["classical", "hybrid", "persistence"]
    cyclone_id: str
    forecast_horizon_hours: int
    predicted_track: list[TrackPoint]
    actual_track: list[TrackPoint]
    metrics: Metrics
