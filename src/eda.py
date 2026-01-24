"""
Exploratory Data Analysis (EDA) script for the predictive maintenance project.

This script covers:
- Data overview (shape, types, missing values, basic statistics)
- Univariate analysis (distributions of features, target balance)
- Bivariate/multivariate analysis (correlations and pairwise relationships)

Figures are saved under `notebooks/figures/` for easy inclusion in reports.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

import config
from data_prep import _clean_data, _load_raw_data_from_hf_or_local


FIGURES_DIR = config.PROJECT_ROOT / "notebooks" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def run_eda() -> None:
    # Load and clean data using the same logic as the pipeline
    raw_df = _load_raw_data_from_hf_or_local()
    df = _clean_data(raw_df)

    print("=== DATA OVERVIEW ===")
    print(f"Shape: {df.shape}")
    print("\nData types:")
    print(df.dtypes)
    print("\nMissing values per column:")
    print(df.isna().sum())
    print("\nSummary statistics:")
    print(df.describe())

    # Univariate analysis: target distribution
    plt.figure(figsize=(4, 4))
    sns.countplot(x=config.TARGET_COLUMN, data=df)
    plt.title("Engine Condition Distribution")
    plt.xlabel("Engine Condition (0 = Normal, 1 = Faulty)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "target_distribution.png")
    plt.close()

    # Univariate analysis: histograms for features
    df[config.FEATURE_COLUMNS].hist(bins=30, figsize=(12, 8))
    plt.suptitle("Feature Distributions", y=1.02)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "feature_histograms.png")
    plt.close()

    # Correlation heatmap (multivariate)
    plt.figure(figsize=(8, 6))
    corr = df[config.FEATURE_COLUMNS + [config.TARGET_COLUMN]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "correlation_heatmap.png")
    plt.close()

    # Pairplot for a subset of features (bivariate relationships)
    subset_cols = ["Engine_RPM", "Lub_Oil_Pressure", "Fuel_Pressure", config.TARGET_COLUMN]
    sns.pairplot(
        df[subset_cols],
        hue=config.TARGET_COLUMN,
        diag_kind="hist",
        corner=True,
    )
    plt.suptitle("Pairwise Relationships (subset of features)", y=1.02)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "pairplot_subset.png")
    plt.close()

    print(f"\nEDA figures saved to: {FIGURES_DIR}")


if __name__ == "__main__":
    run_eda()

