"""Prepare a tiny North Indian Ocean cyclone dataset for CycloneQ demo."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "data" / "samples"
PROCESSED = ROOT / "data" / "processed"


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(SAMPLES / "tracks.csv", parse_dates=["time"])

    df["heading_lat"] = df.groupby("cyclone_id")["lat"].diff().fillna(0.0)
    df["heading_lon"] = df.groupby("cyclone_id")["lon"].diff().fillna(0.0)
    df["speed_proxy"] = (df["heading_lat"].pow(2) + df["heading_lon"].pow(2)).pow(0.5)

    df.to_csv(PROCESSED / "cyclone_tracks_processed.csv", index=False)

    storms = sorted(df["cyclone_id"].unique())
    train, test = train_test_split(storms, test_size=0.33, random_state=42)
    split = {"train": train, "test": test, "val": []}
    with (PROCESSED / "split.json").open("w", encoding="utf-8") as f:
        json.dump(split, f, indent=2)

    print(f"Saved processed data rows={len(df)}")


if __name__ == "__main__":
    main()
