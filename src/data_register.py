"""
Data registration script for the predictive maintenance project.

This script is the analogue of the notebook's `data_register.py`:
- It ensures the Hugging Face dataset repo exists.
- It uploads the raw engine dataset from the local `data/` folder
  into the dataset repo so it can be consumed by other stages
  (EDA, data preparation, model training) using a consistent source.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import config
    from hf_data_utils import register_raw_engine_data_to_hf
except ImportError as e:
    print(f"ERROR: Failed to import modules: {e}", file=sys.stderr)
    print(f"Python path: {sys.path}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    try:
        print(f"PROJECT_ROOT: {config.PROJECT_ROOT}")
        print(f"RAW_DATA_FILE: {config.RAW_DATA_FILE}")
        print(f"RAW_DATA_FILE exists: {config.RAW_DATA_FILE.exists()}")
        print(f"HF_DATASET_REPO: {config.HF_DATASET_REPO}")
        print(f"HF_TOKEN is set: {bool(config.HF_TOKEN)}")
        
        if not config.RAW_DATA_FILE.exists():
            raise FileNotFoundError(
                f"Expected raw data at {config.RAW_DATA_FILE}, "
                "but the file does not exist. Make sure `engine_data.csv` "
                "is placed in the `data/` folder."
            )

        if not config.HF_TOKEN:
            raise ValueError(
                "HF_TOKEN is not set. Please set it as an environment variable "
                "or in GitHub Secrets."
            )

        print(f"Registering raw engine dataset from: {config.RAW_DATA_FILE}")
        print(f"Target HF dataset repo: {config.HF_DATASET_REPO}")
        register_raw_engine_data_to_hf()
        print("✅ Dataset registration to Hugging Face completed.")
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

