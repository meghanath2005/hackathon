from datetime import datetime
from pydantic import BaseModel, Field


class TrackPoint(BaseModel):
    time: datetime
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)


class Metrics(BaseModel):
    mae: float
    rmse: float
    track_error_km: float
    parameter_count: int
