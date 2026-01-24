## Predictive Maintenance – Engine Failure Classification (MLOps Project)

![GitHub](https://img.shields.io/github/license/ananttripathi/engine-predictive-maintenance)
![GitHub last commit](https://img.shields.io/github/last-commit/ananttripathi/engine-predictive-maintenance)
![GitHub repo size](https://img.shields.io/github/repo-size/ananttripathi/engine-predictive-maintenance)
![GitHub stars](https://img.shields.io/github/stars/ananttripathi/engine-predictive-maintenance?style=social)
![GitHub forks](https://img.shields.io/github/forks/ananttripathi/engine-predictive-maintenance?style=social)
![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.43.2-red.svg)
![MLflow](https://img.shields.io/badge/mlflow-2.x-orange.svg)
![Hugging Face](https://img.shields.io/badge/huggingface-spaces-yellow.svg)
![GitHub Actions](https://img.shields.io/github/actions/workflow/status/ananttripathi/engine-predictive-maintenance/pipeline.yml?branch=main&label=CI/CD)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.0-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

This project builds an end‑to‑end **predictive maintenance system** for small and large engines using sensor data (RPM, pressures, temperatures) to classify whether an engine is **healthy** or **requires maintenance**.

The work is organized to satisfy the provided **interim and final report rubrics**, including:

- **Data registration on Hugging Face**
- **Exploratory Data Analysis (EDA)**
- **Data preparation and dataset versioning**
- **Model building with experimentation tracking**
- **Model deployment with Docker + Streamlit on Hugging Face Spaces**
- **Automated GitHub Actions workflow**

### Repository Structure

- `data/` – Raw and processed data (local copies).
  - `engine_data.csv` – Original engine sensor dataset.
- `notebooks/`
  - EDA and experimentation notebooks (you can connect these to your report).
- `src/`
  - `config.py` – Central configuration (paths, Hugging Face repo names, MLflow config).
  - `data_prep.py` – Loads data (from Hugging Face dataset/local), cleans it, and creates train/test splits.
  - `hf_data_utils.py` – Helper functions for uploading/downloading datasets to/from Hugging Face.
  - `train.py` – Model training, hyperparameter tuning, MLflow logging, and best‑model saving.
  - `hf_model_utils.py` – Register and load the best model from the Hugging Face model hub.
  - `inference.py` – Simple Python API for making predictions from the trained model.
  - `app.py` – Streamlit app used for deployment on Hugging Face Spaces.
  - `deploy_to_hf.py` – Script to push deployment files (app, Dockerfile, requirements) to a Hugging Face Space.
- `.github/workflows/pipeline.yml` – Automated CI/CD workflow for data prep, training, and deployment.
- `requirements.txt` – Python dependencies (for local use, CI, Docker, and HF Spaces).
- `Dockerfile` – Container definition for running the Streamlit app.

### High‑Level Pipeline (aligned with template notebook)

1. **Data Registration**
   - Script: `src/data_register.py`
   - Behaviour similar to `data_register.py` in the reference notebook:
     - Creates/uses a **Hugging Face dataset repo** (`HF_DATASET_REPO`),
     - Uploads `data/engine_data.csv` as the canonical raw dataset.
2. **EDA**
   - Script: `src/eda.py` (or use a separate notebook) to perform:
     - Data overview,
     - Univariate, bivariate, multivariate analysis,
     - Business insights about engine health and failure patterns.
3. **Data Preparation**
   - Script: `src/data_prep.py`
   - Loads the raw data from the HF dataset (or local fallback), cleans it, creates train/test splits, and uploads `data/train.csv` and `data/test.csv` back to the dataset repo.
4. **Model Building + Experiment Tracking**
   - Script: `src/train.py`
   - Loads train/test from the HF dataset or local files, trains and tunes a Random Forest classifier, logs all tuned parameters and metrics with **MLflow**, saves the best model locally, and registers it to a **Hugging Face model hub** repo.
5. **Deployment & Hosting**
   - Streamlit app: `src/app.py` (used by Docker / HF Space) loads the best model from HF (or local) and serves predictions.
   - Containerisation: `Dockerfile` and `requirements.txt` define the runtime image and dependencies, matching the “deployment” section of the notebook.
   - Hosting script: `src/deploy_to_hf.py` plays the role of `hosting.py` in the notebook, pushing the app, Dockerfile, and dependencies to a **Hugging Face Space**.
6. **GitHub Actions Workflow**
   - Workflow file: `.github/workflows/pipeline.yml`
   - Defines four staged jobs mirroring the notebook:
     - `register-dataset` → runs `src/data_register.py`
     - `data-prep` → runs `src/data_prep.py`
     - `model-training` → runs `src/train.py`
     - `deploy-hosting` → runs `src/deploy_to_hf.py`
   - All jobs share dependencies via `requirements.txt` and use GitHub secrets for HF credentials and repo IDs.

### What You Need to Configure

#### 1. Hugging Face Configuration

**Update `src/config.py`** (lines 58-62) with your Hugging Face username:

```python
HF_DATASET_REPO = os.getenv("HF_DATASET_REPO", "your-username/engine-maintenance-dataset")
HF_MODEL_REPO = os.getenv("HF_MODEL_REPO", "your-username/engine-maintenance-model")
HF_SPACE_REPO = os.getenv("HF_SPACE_REPO", "your-username/engine-maintenance-space")
```

Replace `"your-username"` with your actual Hugging Face username (e.g., `"ananttripathi"`).

**Or set environment variables:**
```bash
export HF_TOKEN="hf_your_token_here"
export HF_DATASET_REPO="your-username/engine-maintenance-dataset"
export HF_MODEL_REPO="your-username/engine-maintenance-model"
export HF_SPACE_REPO="your-username/engine-maintenance-space"
```

#### 2. GitHub Repository Configuration

**A. Create GitHub Repository:**
1. Create a new repository on GitHub (e.g., `engine-predictive-maintenance`)
2. Push this `mlops` folder to it:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Predictive maintenance MLOps pipeline"
   git remote add origin https://github.com/your-username/engine-predictive-maintenance.git
   git push -u origin main
   ```

**B. Add GitHub Secrets:**
Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these 4 secrets:
- `HF_TOKEN` – Your Hugging Face access token (from https://huggingface.co/settings/tokens)
- `HF_DATASET_REPO` – e.g., `your-username/engine-maintenance-dataset`
- `HF_MODEL_REPO` – e.g., `your-username/engine-maintenance-model`
- `HF_SPACE_REPO` – e.g., `your-username/engine-maintenance-space`

**C. Update README with GitHub Repo URL:**
Add this section to your README (or in your final notebook):
```markdown
## GitHub Repository
- **Repository URL**: https://github.com/your-username/engine-predictive-maintenance
- **GitHub Actions**: https://github.com/your-username/engine-predictive-maintenance/actions
```

Once these values are set, you can run the scripts locally and/or via GitHub Actions to produce outputs that cover all the rubric sections (data registration, EDA, data prep, modeling, deployment, and automated workflow).

**📖 For detailed setup instructions, see `CONFIGURATION_GUIDE.md`**
