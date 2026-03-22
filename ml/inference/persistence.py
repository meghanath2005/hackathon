from __future__ import annotations

from datetime import timedelta

import pandas as pd


def persistence_forecast(storm: pd.DataFrame, horizon_hours: int = 24) -> pd.DataFrame:
    steps = horizon_hours // 6
    hist = storm.tail(3)
    last = hist.iloc[-1]
    prev = hist.iloc[-2]
    d_lat = last["lat"] - prev["lat"]
    d_lon = last["lon"] - prev["lon"]

    out = []
    for i in range(steps):
        out.append(
            {
                "time": pd.to_datetime(last["time"]) + timedelta(hours=6 * (i + 1)),
                "lat": float(last["lat"] + d_lat * (i + 1)),
                "lon": float(last["lon"] + d_lon * (i + 1)),
            }
        )
    return pd.DataFrame(out)
