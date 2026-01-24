"""
Helper script to push the Streamlit app and deployment files
to a Hugging Face Space.

This script mirrors the behaviour of the notebook's `hosting.py`:
- Ensures the Space exists (creating it if necessary),
- Uploads only the files required for deployment (code, Dockerfile,
  and requirements), excluding data, MLflow artifacts, etc.
"""

from __future__ import annotations

import os

from huggingface_hub import HfApi

import config


def main() -> None:
    token = config.HF_TOKEN or os.getenv("HF_TOKEN")
    if not token:
        raise ValueError(
            "HF_TOKEN is not set. Please export HF_TOKEN or configure it in config.py."
        )

    space_repo = config.HF_SPACE_REPO or os.getenv("HF_SPACE_REPO")
    if not space_repo:
        raise ValueError(
            "HF_SPACE_REPO is not set. Set it as an environment variable or in config.py."
        )

    api = HfApi(token=token)

    # Create the Space if it does not exist
    api.create_repo(
        repo_id=space_repo,
        repo_type="space",
        space_sdk="streamlit",
        exist_ok=True,
    )

    # Upload project files needed for deployment.
    # We ignore large local artifacts like raw data, mlruns, and models,
    # similar to how the reference notebook uploads only the deployment folder.
    api.upload_folder(
        folder_path=str(config.PROJECT_ROOT),
        path_in_repo=".",
        repo_id=space_repo,
        repo_type="space",
        ignore_patterns=[
            "data/*",
            "mlruns/*",
            "models/*",
            ".git/*",
            "__pycache__/*",
            ".github/*",
        ],
    )

    print(f"Deployment files pushed to Hugging Face Space: {space_repo}")


if __name__ == "__main__":
    main()


