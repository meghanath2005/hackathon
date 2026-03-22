# Data Notes

CycloneQ uses a lightweight demo dataset located in `data/samples/tracks.csv` and `data/samples/cyclones.json`.

`python scripts/prepare_data.py` generates:
- `data/processed/cyclone_tracks_processed.csv`
- `data/processed/split.json`

The schema includes timestamped cyclone coordinates plus wind/pressure and derived heading features.
