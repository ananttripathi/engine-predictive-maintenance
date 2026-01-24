import os
from pathlib import Path

"""
Central configuration for the predictive maintenance project.

Update the Hugging Face repo IDs to match your own account, or
set them via environment variables.
"""

# Handle both local execution and GitHub Actions
if Path(__file__).resolve().name == "config.py":
    # Running from src/ directory
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
else:
    # Running as module
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------------
# Data paths
# -------------------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_FILE = DATA_DIR / "engine_data.csv"
PROCESSED_DIR = DATA_DIR / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

TRAIN_FILE = PROCESSED_DIR / "train.csv"
TEST_FILE = PROCESSED_DIR / "test.csv"

# -------------------------------------------------------------------------
# Target and feature configuration
# -------------------------------------------------------------------------
# Raw CSV column names (as they appear in engine_data.csv)
RAW_COLUMN_RENAME_MAP = {
    "Engine rpm": "Engine_RPM",
    "Lub oil pressure": "Lub_Oil_Pressure",
    "Fuel pressure": "Fuel_Pressure",
    "Coolant pressure": "Coolant_Pressure",
    "lub oil temp": "Lub_Oil_Temperature",
    "Coolant temp": "Coolant_Temperature",
    "Engine Condition": "Engine_Condition",
}

TARGET_COLUMN = "Engine_Condition"

FEATURE_COLUMNS = [
    "Engine_RPM",
    "Lub_Oil_Pressure",
    "Fuel_Pressure",
    "Coolant_Pressure",
    "Lub_Oil_Temperature",
    "Coolant_Temperature",
]

RANDOM_STATE = 42
TEST_SIZE = float(os.getenv("TEST_SIZE", "0.2"))

# -------------------------------------------------------------------------
# Hugging Face configuration
# -------------------------------------------------------------------------
HF_TOKEN = os.getenv("HF_TOKEN")  # set this in your environment or GitHub secrets

# Default repo IDs can be overridden via environment variables
# Hugging Face username: ananttripathiak
# GitHub username: ananttripathi
HF_DATASET_REPO = os.getenv(
    "HF_DATASET_REPO", "ananttripathiak/engine-maintenance-dataset"
)
HF_MODEL_REPO = os.getenv("HF_MODEL_REPO", "ananttripathiak/engine-maintenance-model")
HF_SPACE_REPO = os.getenv("HF_SPACE_REPO", "ananttripathiak/engine-maintenance-space")

# -------------------------------------------------------------------------
# MLflow configuration
# -------------------------------------------------------------------------
MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI", (PROJECT_ROOT / "mlruns").as_uri()
)
MLFLOW_EXPERIMENT_NAME = os.getenv(
    "MLFLOW_EXPERIMENT_NAME", "engine_predictive_maintenance"
)

# -------------------------------------------------------------------------
# Model artifacts
# -------------------------------------------------------------------------
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

BEST_MODEL_LOCAL_PATH = MODELS_DIR / "best_model.joblib"

