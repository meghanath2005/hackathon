from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "data" / "samples" / "tracks.csv"
OUT = ROOT / "docs" / "assets"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(TRACKS)
    plt.figure(figsize=(6, 4))
    for cid, storm in df.groupby("cyclone_id"):
        plt.plot(storm["lon"], storm["lat"], marker="o", label=cid)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("CycloneQ Demo Storm Tracks")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(OUT / "demo_tracks.png", dpi=160)
    print(f"Saved {OUT / 'demo_tracks.png'}")


if __name__ == "__main__":
    main()
