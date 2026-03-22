from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
SAMPLES_DIR = DATA_DIR / "samples"
MODEL_DIR = ROOT_DIR / "ml" / "saved_models"
METRICS_PATH = MODEL_DIR / "metrics_summary.json"
