"""
Inference utilities for the predictive maintenance model.

These functions are used both by scripts and by the Streamlit app
to load a trained model (from local storage or Hugging Face) and
generate predictions from raw sensor values.
"""

from __future__ import annotations

from typing import Dict, Iterable, Optional

import joblib
import numpy as np
import pandas as pd

import config
from hf_model_utils import download_model


def load_local_model() -> object:
    """
    Load the best trained model from the local models directory.
    """
    if not config.BEST_MODEL_LOCAL_PATH.exists():
        raise FileNotFoundError(
            f"Local model not found at {config.BEST_MODEL_LOCAL_PATH}. "
            "Run train.py to create it, or configure HF model loading."
        )
    return joblib.load(config.BEST_MODEL_LOCAL_PATH)


def load_hf_model() -> object:
    """
    Load the model directly from the Hugging Face model hub.
    """
    return download_model()


def build_input_dataframe(
    inputs: Dict[str, float],
) -> pd.DataFrame:
    """
    Convert a dictionary of feature values into a single-row DataFrame
    with columns ordered according to config.FEATURE_COLUMNS.
    """
    data = {col: float(inputs.get(col, 0.0)) for col in config.FEATURE_COLUMNS}
    return pd.DataFrame([data])


def predict_engine_condition(
    inputs: Dict[str, float],
    model: Optional[object] = None,
    source: str = "local",
) -> Dict[str, float]:
    """
    Predict whether the engine requires maintenance.

    Parameters
    ----------
    inputs : dict
        Keys correspond to feature names in config.FEATURE_COLUMNS.
    model : object, optional
        Pre-loaded sklearn Pipeline model. If None, it will be loaded
        from `source`.
    source : {'local', 'hf'}
        If model is None, determines where to load it from.

    Returns
    -------
    dict
        Contains the predicted class label (0/1) and the probability
        of the positive class.
    """
    if model is None:
        if source == "hf":
            model = load_hf_model()
        else:
            model = load_local_model()

    df = build_input_dataframe(inputs)
    proba = model.predict_proba(df)[0, 1]
    pred = int(proba >= 0.5)

    return {
        "prediction": pred,
        "probability_faulty": float(proba),
    }


__all__ = [
    "load_local_model",
    "load_hf_model",
    "build_input_dataframe",
    "predict_engine_condition",
]

