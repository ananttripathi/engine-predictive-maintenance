"""
Data registration script for the predictive maintenance project.

This script is the analogue of the notebook's `data_register.py`:
- It ensures the Hugging Face dataset repo exists.
- It uploads the raw engine dataset from the local `data/` folder
  into the dataset repo so it can be consumed by other stages
  (EDA, data preparation, model training) using a consistent source.
"""

from __future__ import annotations

from pathlib import Path

import config
from hf_data_utils import register_raw_engine_data_to_hf


def main() -> None:
    if not config.RAW_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Expected raw data at {config.RAW_DATA_FILE}, "
            "but the file does not exist. Make sure `engine_data.csv` "
            "is placed in the `data/` folder."
        )

    print(f"Registering raw engine dataset from: {config.RAW_DATA_FILE}")
    print(f"Target HF dataset repo: {config.HF_DATASET_REPO}")
    register_raw_engine_data_to_hf()
    print("Dataset registration to Hugging Face completed.")


if __name__ == "__main__":
    main()

