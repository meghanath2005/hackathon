from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import StandardScaler


@dataclass
class DatasetBundle:
    x: torch.Tensor
    y: torch.Tensor
    scaler: StandardScaler


def build_training_data(df: pd.DataFrame, seq_len: int = 4) -> DatasetBundle:
    features = ["lat", "lon", "wind_kts", "pressure_hpa"]
    rows_x: list[np.ndarray] = []
    rows_y: list[np.ndarray] = []

    for _, storm in df.groupby("cyclone_id"):
        storm = storm.sort_values("time").copy()
        storm["d_lat"] = storm["lat"].diff().fillna(0)
        storm["d_lon"] = storm["lon"].diff().fillna(0)
        feature_matrix = storm[features + ["d_lat", "d_lon"]].to_numpy(dtype=np.float32)
        target = storm[["lat", "lon"]].to_numpy(dtype=np.float32)
        for i in range(seq_len, len(storm)):
            rows_x.append(feature_matrix[i - seq_len : i])
            rows_y.append(target[i])

    x = np.stack(rows_x)
    y = np.stack(rows_y)
    scaler = StandardScaler()
    x_2d = x.reshape(-1, x.shape[-1])
    x_scaled = scaler.fit_transform(x_2d).reshape(x.shape)

    return DatasetBundle(
        x=torch.tensor(x_scaled, dtype=torch.float32),
        y=torch.tensor(y, dtype=torch.float32),
        scaler=scaler,
    )
