"""
Utility functions for interacting with the Hugging Face Hub for MODELS.

Used to:
- Upload the best trained model to a model repo.
- Download the registered model for inference or deployment.
"""

from pathlib import Path
from typing import Optional

import joblib
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


def create_or_get_model_repo(
    repo_id: str, token: Optional[str] = None, private: bool = False
) -> None:
    """
    Create the model repo on Hugging Face Hub if it does not already exist.
    """
    token = _get_token(token)
    api = HfApi(token=token)
    api.create_repo(
        repo_id=repo_id,
        repo_type="model",
        private=private,
        exist_ok=True,
    )


def upload_model(
    local_model_path: Path,
    repo_id: Optional[str] = None,
    repo_path: str = "model.joblib",
    token: Optional[str] = None,
) -> None:
    """
    Upload the trained model artifact to the Hugging Face model hub.
    """
    token = _get_token(token)
    repo_id = repo_id or config.HF_MODEL_REPO

    api = HfApi(token=token)
    create_or_get_model_repo(repo_id=repo_id, token=token)

    api.upload_file(
        path_or_fileobj=str(local_model_path),
        path_in_repo=repo_path,
        repo_id=repo_id,
        repo_type="model",
    )


def download_model(
    repo_id: Optional[str] = None,
    filename: str = "model.joblib",
    token: Optional[str] = None,
    local_dir: Optional[Path] = None,
):
    """
    Download a model artifact from the Hugging Face model hub and load it.
    """
    token = _get_token(token)
    repo_id = repo_id or config.HF_MODEL_REPO
    local_dir = local_dir or config.MODELS_DIR
    local_dir.mkdir(parents=True, exist_ok=True)

    downloaded_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        repo_type="model",
        token=token,
        local_dir=str(local_dir),
        local_dir_use_symlinks=False,
    )

    return joblib.load(downloaded_path)

