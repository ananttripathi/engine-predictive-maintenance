"""
Model training and experimentation tracking script.

Responsibilities:
- Load prepared train and test datasets (preferably from Hugging Face dataset repo).
- Define a model pipeline (Random Forest by default) and hyperparameter search space.
- Run hyperparameter tuning with cross-validation.
- Log all tuned parameters and evaluation metrics with MLflow.
- Save the best model locally.
- Register/upload the best model to the Hugging Face model hub.
"""

from __future__ import annotations

from typing import Dict, Tuple

import joblib
import mlflow
import mlflow.sklearn  # noqa: F401
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import config
from hf_data_utils import download_dataset_file
from hf_model_utils import upload_model


def _load_train_test_from_hf_or_local() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load train and test data from the HF dataset repo if available,
    otherwise fall back to local CSVs created by data_prep.py.
    """
    if config.HF_TOKEN and config.HF_DATASET_REPO:
        try:
            train_path = download_dataset_file(
                filename="data/train.csv",
                repo_id=config.HF_DATASET_REPO,
                token=config.HF_TOKEN,
                local_dir=config.DATA_DIR,
            )
            test_path = download_dataset_file(
                filename="data/test.csv",
                repo_id=config.HF_DATASET_REPO,
                token=config.HF_TOKEN,
                local_dir=config.DATA_DIR,
            )
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            return train_df, test_df
        except Exception:
            # Fall back to local
            pass

    if not config.TRAIN_FILE.exists() or not config.TEST_FILE.exists():
        raise FileNotFoundError(
            "Train/test files not found locally or in the HF dataset repo. "
            "Run data_prep.py first to generate the splits."
        )

    train_df = pd.read_csv(config.TRAIN_FILE)
    test_df = pd.read_csv(config.TEST_FILE)
    return train_df, test_df


def _build_model_and_search_space() -> Tuple[Pipeline, Dict]:
    """
    Build a sklearn Pipeline and define the hyperparameter search space.

    We use a RandomForestClassifier with a StandardScaler on numeric features.
    """
    clf = RandomForestClassifier(random_state=config.RANDOM_STATE)

    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("clf", clf),
        ]
    )

    param_distributions = {
        "clf__n_estimators": [100, 200, 300, 400],
        "clf__max_depth": [None, 5, 10, 20],
        "clf__min_samples_split": [2, 5, 10],
        "clf__min_samples_leaf": [1, 2, 4],
        # 'auto' is deprecated in recent sklearn versions; use valid options only
        "clf__max_features": ["sqrt", "log2", None],
        "clf__bootstrap": [True, False],
    }

    return pipeline, param_distributions


def _evaluate_model(
    model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series
) -> Dict[str, float]:
    """
    Compute standard binary classification metrics.
    """
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
    }
    return metrics


def main() -> None:
    """
    Execute the training, tuning, logging, and model registration pipeline.
    """
    print("Loading train and test data...")
    train_df, test_df = _load_train_test_from_hf_or_local()

    X_train = train_df[config.FEATURE_COLUMNS]
    y_train = train_df[config.TARGET_COLUMN]
    X_test = test_df[config.FEATURE_COLUMNS]
    y_test = test_df[config.TARGET_COLUMN]

    print("Building model and hyperparameter search space...")
    pipeline, param_distributions = _build_model_and_search_space()

    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=param_distributions,
        n_iter=20,
        cv=5,
        scoring="f1",
        n_jobs=-1,
        verbose=1,
        random_state=config.RANDOM_STATE,
    )

    # Configure MLflow
    mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(config.MLFLOW_EXPERIMENT_NAME)

    print("Starting hyperparameter tuning with MLflow tracking...")
    with mlflow.start_run(run_name="RandomForest_random_search"):
        search.fit(X_train, y_train)

        best_model: Pipeline = search.best_estimator_
        best_params = search.best_params_

        # Log all evaluated parameter combinations as nested runs,
        # similar to the reference notebook pattern.
        results = search.cv_results_
        for i in range(len(results["params"])):
            param_set = results["params"][i]
            mean_score = results["mean_test_score"][i]
            with mlflow.start_run(nested=True):
                mlflow.log_params(param_set)
                mlflow.log_metric("mean_cv_f1", float(mean_score))

        # Evaluation
        metrics = _evaluate_model(best_model, X_test, y_test)

        # Log parameters and metrics
        mlflow.log_params(best_params)
        for name, value in metrics.items():
            mlflow.log_metric(name, float(value))

        # Save model locally
        config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(best_model, config.BEST_MODEL_LOCAL_PATH)
        mlflow.log_artifact(str(config.BEST_MODEL_LOCAL_PATH), artifact_path="artifacts")

        # Also log the model in MLflow's model registry format
        mlflow.sklearn.log_model(best_model, artifact_path="engine_model")

        print("Best parameters found:")
        for k, v in best_params.items():
            print(f"  {k}: {v}")

        print("Evaluation metrics on test set:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")

    # Upload best model to Hugging Face model hub, if configured
    if config.HF_TOKEN and config.HF_MODEL_REPO:
        try:
            print("Uploading best model to Hugging Face model hub...")
            upload_model(
                local_model_path=config.BEST_MODEL_LOCAL_PATH,
                repo_id=config.HF_MODEL_REPO,
                repo_path="model.joblib",
                token=config.HF_TOKEN,
            )
            print("Model upload to Hugging Face completed.")
        except Exception as e:
            print(f"Warning: Failed to upload model to Hugging Face: {e}")


if __name__ == "__main__":
    main()

