from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

import numpy as np
import pandas as pd

from app.schemas.common import Metrics, TrackPoint
from app.schemas.prediction import PredictResponse
from app.services.data_loader import cyclone_track, load_metrics_summary, load_tracks
from app.utils.geo import haversine_km


@dataclass
class PredictionService:
    tracks: pd.DataFrame
    summary_metrics: dict

    @classmethod
    def build(cls) -> "PredictionService":
        return cls(tracks=load_tracks(), summary_metrics=load_metrics_summary())

    def _forecast(self, storm: pd.DataFrame, horizon_hours: int, mode: str) -> pd.DataFrame:
        steps = max(1, horizon_hours // 6)
        actual = storm.tail(steps).copy()
        history = storm.iloc[: -steps or None].tail(4)

        last = history.iloc[-1]
        prev = history.iloc[-2] if len(history) > 1 else history.iloc[-1]
        d_lat = last["lat"] - prev["lat"]
        d_lon = last["lon"] - prev["lon"]

        if mode == "classical":
            gain = 0.92
        elif mode == "hybrid":
            gain = 0.88
        else:
            gain = 1.0

        preds = []
        for idx in range(steps):
            lat = float(last["lat"] + (idx + 1) * d_lat * gain)
            lon = float(last["lon"] + (idx + 1) * d_lon * gain)
            t = pd.to_datetime(last["time"]) + timedelta(hours=6 * (idx + 1))
            preds.append({"time": t, "lat": lat, "lon": lon})

        return actual, pd.DataFrame(preds)

    def predict(self, cyclone_id: str, horizon_hours: int, model: str) -> PredictResponse:
        if horizon_hours not in (24, 48):
            raise ValueError("forecast_horizon_hours must be 24 or 48")

        storm = cyclone_track(self.tracks, cyclone_id)
        actual, pred = self._forecast(storm, horizon_hours, model)

        dists = [
            haversine_km(a.lat, a.lon, p.lat, p.lon)
            for a, p in zip(actual.itertuples(index=False), pred.itertuples(index=False), strict=False)
        ]
        mae = float(np.mean(np.abs(actual[["lat", "lon"]].values - pred[["lat", "lon"]].values)))
        rmse = float(
            np.sqrt(np.mean((actual[["lat", "lon"]].values - pred[["lat", "lon"]].values) ** 2))
        )
        track_error = float(np.mean(dists)) if dists else 0.0

        fallback = self.summary_metrics.get(model, self.summary_metrics["classical"])
        metrics = Metrics(
            mae=round(mae, 3),
            rmse=round(rmse, 3),
            track_error_km=round(track_error, 2),
            parameter_count=fallback["parameter_count"],
        )

        return PredictResponse(
            model=model,
            cyclone_id=cyclone_id,
            forecast_horizon_hours=horizon_hours,
            predicted_track=[TrackPoint(**row) for row in pred.to_dict(orient="records")],
            actual_track=[TrackPoint(**row) for row in actual.to_dict(orient="records")],
            metrics=metrics,
        )
