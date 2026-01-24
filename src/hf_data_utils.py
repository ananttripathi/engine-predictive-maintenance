"""
Utility functions for interacting with the Hugging Face Hub for DATASETS.

These helpers are used to:
- Register the raw engine dataset as a Hugging Face dataset repo.
- Upload processed train/test splits back to the dataset repo.
- Download files from the dataset repo for use in data preparation and modeling.

All functions expect a valid HF token to be available, typically via:
- The HF_TOKEN environment variable, or
- An explicit argument.
"""

from pathlib import Path
from typing import Optional

from huggingface_hub import HfApi, hf_hub_download

import config


def _get_token(explicit_token: Optional[str] = None) -> str:
    token = explicit_token or config.HF_TOKEN
    if not token:
        raise ValueError(
            "Hugging Face token is not set. "
            "Set HF_TOKEN in the environment or pass token explicitly."
        )
    return token


def create_or_get_dataset_repo(
    repo_id: str, token: Optional[str] = None, private: bool = False
) -> None:
    """
    Create the dataset repo on Hugging Face Hub if it does not already exist.
    """
    token = _get_token(token)
    api = HfApi(token=token)
    api.create_repo(
        repo_id=repo_id,
        repo_type="dataset",
        private=private,
        exist_ok=True,
    )


def upload_dataset_file(
    local_path: Path,
    repo_id: Optional[str] = None,
    repo_path: Optional[str] = None,
    token: Optional[str] = None,
) -> None:
    """
    Upload a single file to the Hugging Face dataset repo.

    Parameters
    ----------
    local_path : Path
        The local file to upload.
    repo_id : str, optional
        The dataset repo ID (e.g., 'username/engine-maintenance-dataset').
        Defaults to config.HF_DATASET_REPO.
    repo_path : str, optional
        The path inside the repo (e.g., 'data/train.csv'). Defaults to the
        file name if not provided.
    token : str, optional
        Hugging Face token. Defaults to config.HF_TOKEN.
    """
    token = _get_token(token)
    repo_id = repo_id or config.HF_DATASET_REPO
    repo_path = repo_path or local_path.name

    api = HfApi(token=token)
    create_or_get_dataset_repo(repo_id=repo_id, token=token)

    api.upload_file(
        path_or_fileobj=str(local_path),
        path_in_repo=repo_path,
        repo_id=repo_id,
        repo_type="dataset",
    )


def download_dataset_file(
    filename: str,
    repo_id: Optional[str] = None,
    token: Optional[str] = None,
    local_dir: Optional[Path] = None,
) -> Path:
    """
    Download a file from the Hugging Face dataset repo and return its local path.

    Parameters
    ----------
    filename : str
        The filename inside the dataset repo (e.g., 'data/engine_data.csv').
    repo_id : str, optional
        The dataset repo ID. Defaults to config.HF_DATASET_REPO.
    token : str, optional
        Hugging Face token.
    local_dir : Path, optional
        Directory to place the downloaded file. Defaults to config.DATA_DIR.
    """
    token = _get_token(token)
    repo_id = repo_id or config.HF_DATASET_REPO
    local_dir = local_dir or config.DATA_DIR
    local_dir.mkdir(parents=True, exist_ok=True)

    downloaded_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        repo_type="dataset",
        token=token,
        local_dir=str(local_dir),
        local_dir_use_symlinks=False,
    )
    return Path(downloaded_path)


def register_raw_engine_data_to_hf(
    token: Optional[str] = None,
    repo_id: Optional[str] = None,
) -> None:
    """
    Convenience function to register the original engine_data.csv
    in the dataset repo under 'data/engine_data.csv'.
    """
    repo_id = repo_id or config.HF_DATASET_REPO
    local_path = config.RAW_DATA_FILE
    if not local_path.exists():
        raise FileNotFoundError(
            f"Raw data file not found at {local_path}. "
            "Ensure engine_data.csv is present in the data/ folder."
        )

    upload_dataset_file(
        local_path=local_path,
        repo_id=repo_id,
        repo_path="data/engine_data.csv",
        token=token,
    )

