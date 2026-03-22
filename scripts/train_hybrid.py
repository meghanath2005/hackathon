from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from ml.quantum.models import HybridQuantumForecaster
from ml.training.dataset import build_training_data

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed" / "cyclone_tracks_processed.csv"
SAVE_DIR = ROOT / "ml" / "saved_models"


def main() -> None:
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(PROCESSED, parse_dates=["time"])
    bundle = build_training_data(df)

    model = HybridQuantumForecaster(input_size=bundle.x.shape[-1])
    loader = DataLoader(TensorDataset(bundle.x, bundle.y), batch_size=6, shuffle=True)
    opt = torch.optim.Adam(model.parameters(), lr=2e-3)
    loss_fn = nn.MSELoss()

    for _ in range(20):
        for xb, yb in loader:
            pred = model(xb)
            loss = loss_fn(pred, yb)
            opt.zero_grad()
            loss.backward()
            opt.step()

    torch.save(model.state_dict(), SAVE_DIR / "hybrid_quantum.pt")
    meta = {"parameter_count": sum(p.numel() for p in model.parameters()), "n_qubits": 4}
    (SAVE_DIR / "hybrid_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print("Saved hybrid model", meta)


if __name__ == "__main__":
    main()
