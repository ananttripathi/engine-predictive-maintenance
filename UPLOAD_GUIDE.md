# File Upload Guide: Where Each File Goes

This guide shows exactly which files are uploaded to which location (Hugging Face or GitHub) and when.

---

## Overview: Three Upload Destinations

1. **Hugging Face Dataset Repo** (`ananttripathiak/engine-maintenance-dataset`)
2. **Hugging Face Model Repo** (`ananttripathiak/engine-maintenance-model`)
3. **Hugging Face Space** (`ananttripathiak/engine-maintenance-space`)
4. **GitHub Repository** (`ananttripathi/engine-predictive-maintenance`)

---

## 1. Hugging Face Dataset Repo

**Repo ID**: `ananttripathiak/engine-maintenance-dataset`  
**Created by**: `src/data_register.py` and `src/data_prep.py`

### Files Uploaded:

#### A. Raw Data (via `src/data_register.py`)
- **File**: `data/engine_data.csv`
- **Uploaded to**: `data/engine_data.csv` in the dataset repo
- **When**: Run `python src/data_register.py`

#### B. Processed Data (via `src/data_prep.py`)
- **File**: `data/processed/train.csv`
- **Uploaded to**: `data/train.csv` in the dataset repo
- **When**: Run `python src/data_prep.py`

- **File**: `data/processed/test.csv`
- **Uploaded to**: `data/test.csv` in the dataset repo
- **When**: Run `python src/data_prep.py`

**Scripts that upload here:**
- `src/data_register.py` → uploads raw data
- `src/data_prep.py` → uploads train/test splits

---

## 2. Hugging Face Model Repo

**Repo ID**: `ananttripathiak/engine-maintenance-model`  
**Created by**: `src/train.py`

### Files Uploaded:

- **File**: `models/best_model.joblib`
- **Uploaded to**: `model.joblib` in the model repo
- **When**: Run `python src/train.py` (after training completes)

**Scripts that upload here:**
- `src/train.py` → uploads the trained model

---

## 3. Hugging Face Space (Streamlit App)

**Repo ID**: `ananttripathiak/engine-maintenance-space`  
**Created by**: `src/deploy_to_hf.py`

### Files Uploaded:

The `src/deploy_to_hf.py` script uploads the entire project folder **except**:
- `data/` (ignored - too large)
- `mlruns/` (ignored - MLflow tracking data)
- `models/` (ignored - model is in model repo)
- `.github/` (ignored - GitHub-specific)

**Files that ARE uploaded to Space:**
- `src/app.py` ← **Main Streamlit app**
- `src/inference.py` ← Inference utilities
- `src/config.py` ← Configuration
- `Dockerfile` ← Container definition
- `requirements.txt` ← Python dependencies
- `README.md` ← Documentation
- Other `src/*.py` files (if needed by app)

**Scripts that upload here:**
- `src/deploy_to_hf.py` → uploads deployment files

---

## 4. GitHub Repository

**Repo URL**: `https://github.com/ananttripathi/engine-predictive-maintenance`  
**Created by**: You (manually via `git push`)

### Files Uploaded:

**Everything in the `mlops/` folder**, including:
- ✅ `data/` (including `engine_data.csv`, `processed/train.csv`, `processed/test.csv`)
- ✅ `src/` (all Python scripts)
- ✅ `notebooks/` (EDA notebooks, etc.)
- ✅ `.github/workflows/pipeline.yml` ← **GitHub Actions workflow**
- ✅ `requirements.txt`
- ✅ `Dockerfile`
- ✅ `README.md`
- ✅ `models/` (if you want to track model versions in git)
- ✅ `mlruns/` (MLflow tracking data - optional)
- ✅ All other project files

**How to upload:**
```bash
cd /Users/ananttripathi/Desktop/mlops
git init
git add .
git commit -m "Initial commit: Predictive maintenance MLOps pipeline"
git remote add origin https://github.com/ananttripathi/engine-predictive-maintenance.git
git push -u origin main
```

---

## Upload Workflow Summary

### Step-by-Step Upload Process:

1. **Data Registration** → Hugging Face Dataset Repo
   ```bash
   python src/data_register.py
   ```
   - Uploads: `data/engine_data.csv` → HF Dataset Repo

2. **Data Preparation** → Hugging Face Dataset Repo
   ```bash
   python src/data_prep.py
   ```
   - Uploads: `data/processed/train.csv` and `test.csv` → HF Dataset Repo

3. **Model Training** → Hugging Face Model Repo
   ```bash
   python src/train.py
   ```
   - Uploads: `models/best_model.joblib` → HF Model Repo

4. **Deploy App** → Hugging Face Space
   ```bash
   python src/deploy_to_hf.py
   ```
   - Uploads: `src/app.py`, `Dockerfile`, `requirements.txt`, etc. → HF Space

5. **Push to GitHub** → GitHub Repository
   ```bash
   git add .
   git commit -m "Complete MLOps pipeline"
   git push origin main
   ```
   - Uploads: Everything → GitHub Repo

---

## What Gets Uploaded Automatically vs Manually

### Automatic (via Scripts):
- ✅ Hugging Face Dataset Repo → `src/data_register.py` and `src/data_prep.py`
- ✅ Hugging Face Model Repo → `src/train.py`
- ✅ Hugging Face Space → `src/deploy_to_hf.py`
- ✅ GitHub Actions → Runs automatically when you push to GitHub

### Manual:
- ⚠️ **GitHub Repository** → You need to run `git push` yourself

---

## File Size Considerations

### Large Files (may be ignored):
- `data/engine_data.csv` → Uploaded to HF Dataset, but you might want to add to `.gitignore` for GitHub
- `mlruns/` → MLflow tracking data (can be large) - ignored by HF Space deploy
- `models/best_model.joblib` → Uploaded to HF Model Repo, but you might want to add to `.gitignore` for GitHub

### Recommended `.gitignore`:
```
# Large data files
data/*.csv
data/processed/*.csv

# MLflow tracking
mlruns/

# Model files (already in HF Model Repo)
models/*.joblib

# Python cache
__pycache__/
*.pyc
.venv/
```

---

## Quick Reference Table

| File/Folder | HF Dataset | HF Model | HF Space | GitHub |
|------------|------------|----------|----------|--------|
| `data/engine_data.csv` | ✅ | ❌ | ❌ | ⚠️ Optional |
| `data/processed/train.csv` | ✅ | ❌ | ❌ | ⚠️ Optional |
| `data/processed/test.csv` | ✅ | ❌ | ❌ | ⚠️ Optional |
| `models/best_model.joblib` | ❌ | ✅ | ❌ | ⚠️ Optional |
| `src/app.py` | ❌ | ❌ | ✅ | ✅ |
| `src/train.py` | ❌ | ❌ | ❌ | ✅ |
| `src/data_prep.py` | ❌ | ❌ | ❌ | ✅ |
| `Dockerfile` | ❌ | ❌ | ✅ | ✅ |
| `requirements.txt` | ❌ | ❌ | ✅ | ✅ |
| `.github/workflows/pipeline.yml` | ❌ | ❌ | ❌ | ✅ |
| `README.md` | ❌ | ❌ | ✅ | ✅ |

**Legend:**
- ✅ = Uploaded automatically or should be uploaded
- ❌ = Not uploaded to this location
- ⚠️ Optional = Can be uploaded but might want to exclude from GitHub due to size

---

## Need Help?

- **Hugging Face Dataset**: Check `src/hf_data_utils.py`
- **Hugging Face Model**: Check `src/hf_model_utils.py`
- **Hugging Face Space**: Check `src/deploy_to_hf.py`
- **GitHub**: Standard git commands
