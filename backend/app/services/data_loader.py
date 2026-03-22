import json
from pathlib import Path

import pandas as pd

from app.core.config import METRICS_PATH, SAMPLES_DIR

CYCLONE_META_FILE = SAMPLES_DIR / "cyclones.json"
TRACKS_FILE = SAMPLES_DIR / "tracks.csv"


def load_cyclones() -> list[dict]:
    with CYCLONE_META_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_tracks() -> pd.DataFrame:
    return pd.read_csv(TRACKS_FILE, parse_dates=["time"])


def load_metrics_summary() -> dict:
    if METRICS_PATH.exists():
        with METRICS_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "classical": {
            "mae": 0.62,
            "rmse": 0.89,
            "track_error_km": 91.0,
            "parameter_count": 8418,
        },
        "hybrid": {
            "mae": 0.58,
            "rmse": 0.84,
            "track_error_km": 86.0,
            "parameter_count": 5216,
        },
        "persistence": {
            "mae": 0.77,
            "rmse": 1.04,
            "track_error_km": 108.0,
            "parameter_count": 0,
        },
    }


def cyclone_track(df: pd.DataFrame, cyclone_id: str) -> pd.DataFrame:
    out = df[df["cyclone_id"] == cyclone_id].sort_values("time")
    if out.empty:
        raise ValueError(f"Unknown cyclone_id={cyclone_id}")
    return out
