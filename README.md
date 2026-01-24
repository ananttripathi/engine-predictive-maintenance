## Predictive Maintenance – Engine Failure Classification (MLOps Project)

> 🎉 **Status: Complete** - All pipeline steps successfully deployed!

This project builds an end‑to‑end **predictive maintenance system** for small and large engines using sensor data (RPM, pressures, temperatures) to classify whether an engine is **healthy** or **requires maintenance**.

The work is organized to satisfy the provided **interim and final report rubrics**, including:

- ✅ **Data registration on Hugging Face**
- ✅ **Exploratory Data Analysis (EDA)**
- ✅ **Data preparation and dataset versioning**
- ✅ **Model building with experimentation tracking**
- ✅ **Model deployment with Docker + Streamlit on Hugging Face Spaces**
- ✅ **Automated GitHub Actions workflow**

---

## 🔗 Live Resources

### 🌐 Live Application
**[🚀 Try the Live App](https://huggingface.co/spaces/ananttripathiak/engine-maintenance-space)**

Interactive Streamlit application for real-time engine condition predictions with sensor visualizations.

### 🤖 Trained Model
**[📦 View Model on Hugging Face](https://huggingface.co/ananttripathiak/engine-maintenance-model)**

Trained Random Forest model with hyperparameter tuning, versioned on Hugging Face Model Hub.

### 📊 Dataset Repository
**[📁 Access Dataset Repository](https://huggingface.co/datasets/ananttripathiak/engine-maintenance-dataset)**

Version-controlled datasets including raw data and train/test splits.

### 💻 GitHub Repository
**[🔧 View Source Code](https://github.com/ananttripathi/engine-predictive-maintenance)**

Complete source code, documentation, and CI/CD pipeline.

### ⚙️ GitHub Actions
**[🔄 View Workflow Runs](https://github.com/ananttripathi/engine-predictive-maintenance/actions)**

Automated CI/CD pipeline with 4 sequential jobs for data registration, preparation, training, and deployment.

---

## 📁 Repository Structure

```
mlops/
├── data/                          # Raw and processed data
│   ├── engine_data.csv           # Original engine sensor dataset
│   └── processed/                # Train/test splits
│       ├── train.csv
│       └── test.csv
├── notebooks/                     # EDA and experimentation notebooks
├── src/                          # Main source code
│   ├── config.py                 # Central configuration
│   ├── data_register.py          # Register raw data to HF Dataset
│   ├── data_prep.py              # Data cleaning and splitting
│   ├── hf_data_utils.py          # HF Dataset Hub utilities
│   ├── train.py                  # Model training with MLflow
│   ├── hf_model_utils.py         # HF Model Hub utilities
│   ├── inference.py              # Prediction utilities
│   ├── app.py                    # Streamlit web application
│   └── deploy_to_hf.py          # Deploy to HF Space
├── .github/
│   └── workflows/
│       └── pipeline.yml           # CI/CD pipeline
├── Dockerfile                    # Container definition for deployment
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

### Key Files

- **`src/config.py`** – Central configuration (paths, Hugging Face repo names, MLflow config)
- **`src/data_register.py`** – Registers raw dataset to Hugging Face Dataset Hub
- **`src/data_prep.py`** – Loads data, cleans it, and creates train/test splits
- **`src/train.py`** – Model training, hyperparameter tuning, MLflow logging
- **`src/app.py`** – Streamlit web application for interactive predictions
- **`src/deploy_to_hf.py`** – Deploys app to Hugging Face Space
- **`.github/workflows/pipeline.yml`** – Automated CI/CD pipeline

## 🔄 Pipeline Overview

The MLOps pipeline consists of 6 stages, automated via GitHub Actions:

### 1. **Data Registration** ✅
- **Script:** `src/data_register.py`
- **Action:** Creates/uses Hugging Face dataset repo and uploads raw data
- **Output:** [`ananttripathiak/engine-maintenance-dataset`](https://huggingface.co/datasets/ananttripathiak/engine-maintenance-dataset) with `data/engine_data.csv`

### 2. **Exploratory Data Analysis (EDA)**
- **Script:** `src/eda.py` (or use notebooks)
- **Action:** Performs data overview, univariate/bivariate/multivariate analysis
- **Output:** Visualizations and insights about engine health patterns

### 3. **Data Preparation** ✅
- **Script:** `src/data_prep.py`
- **Action:** Cleans data, creates train/test splits, uploads to dataset repo
- **Output:** `data/train.csv` and `data/test.csv` in dataset repo

### 4. **Model Building + Experiment Tracking** ✅
- **Script:** `src/train.py`
- **Action:** Trains Random Forest with hyperparameter tuning, logs to MLflow, uploads best model
- **Output:** [`ananttripathiak/engine-maintenance-model`](https://huggingface.co/ananttripathiak/engine-maintenance-model) with trained model

### 5. **Deployment & Hosting** ✅
- **App:** `src/app.py` - Streamlit web application
- **Container:** `Dockerfile` - Container definition
- **Script:** `src/deploy_to_hf.py` - Deploys to Hugging Face Space
- **Output:** Live app at [`ananttripathiak/engine-maintenance-space`](https://huggingface.co/spaces/ananttripathiak/engine-maintenance-space)

### 6. **GitHub Actions Workflow** ✅
- **File:** `.github/workflows/pipeline.yml`
- **Jobs:**
  1. `register-dataset` → runs `src/data_register.py`
  2. `data-prep` → runs `src/data_prep.py`
  3. `model-training` → runs `src/train.py`
  4. `deploy-hosting` → runs `src/deploy_to_hf.py`
- **View Runs:** [GitHub Actions](https://github.com/ananttripathi/engine-predictive-maintenance/actions)

---

## 🚀 Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ananttripathi/engine-predictive-maintenance.git
   cd engine-predictive-maintenance
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run pipeline steps:**
   ```bash
   # Register data
   python src/data_register.py
   
   # Prepare data
   python src/data_prep.py
   
   # Train model
   python src/train.py
   
   # Run app locally
   streamlit run src/app.py
   ```

### Automated Pipeline

The pipeline runs automatically on every push to `main` branch via GitHub Actions. View workflow runs at:
**[🔄 GitHub Actions](https://github.com/ananttripathi/engine-predictive-maintenance/actions)**

---

## 📊 Technologies Used

- **Python 3.10** - Programming language
- **scikit-learn** - Machine learning (Random Forest)
- **MLflow** - Experiment tracking and model registry
- **Hugging Face Hub** - Dataset, model, and space hosting
- **Streamlit** - Web application framework
- **Docker** - Containerization
- **GitHub Actions** - CI/CD automation
- **Plotly** - Interactive visualizations

## ⚙️ Configuration

### Current Configuration

This project is configured with:

- **Hugging Face Username:** `ananttripathiak`
- **GitHub Username:** `ananttripathi`
- **Dataset Repo:** [`ananttripathiak/engine-maintenance-dataset`](https://huggingface.co/datasets/ananttripathiak/engine-maintenance-dataset)
- **Model Repo:** [`ananttripathiak/engine-maintenance-model`](https://huggingface.co/ananttripathiak/engine-maintenance-model)
- **Space Repo:** [`ananttripathiak/engine-maintenance-space`](https://huggingface.co/spaces/ananttripathiak/engine-maintenance-space)
- **GitHub Repo:** [`ananttripathi/engine-predictive-maintenance`](https://github.com/ananttripathi/engine-predictive-maintenance)

### For New Users: Setup Instructions

#### 1. Hugging Face Configuration

**Update `src/config.py`** with your Hugging Face username:

```python
HF_DATASET_REPO = os.getenv("HF_DATASET_REPO", "ananttripathiak/engine-maintenance-dataset")
HF_MODEL_REPO = os.getenv("HF_MODEL_REPO", "ananttripathiak/engine-maintenance-model")
HF_SPACE_REPO = os.getenv("HF_SPACE_REPO", "ananttripathiak/engine-maintenance-space")
```

**Or set environment variables:**
```bash
export HF_TOKEN="hf_your_token_here"
export HF_DATASET_REPO="ananttripathiak/engine-maintenance-dataset"
export HF_MODEL_REPO="ananttripathiak/engine-maintenance-model"
export HF_SPACE_REPO="ananttripathiak/engine-maintenance-space"
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
- `HF_TOKEN` – Your Hugging Face access token (from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens))
- `HF_DATASET_REPO` – e.g., `ananttripathiak/engine-maintenance-dataset`
- `HF_MODEL_REPO` – e.g., `ananttripathiak/engine-maintenance-model`
- `HF_SPACE_REPO` – e.g., `ananttripathiak/engine-maintenance-space`

**📖 For detailed setup instructions, see [`CONFIGURATION_GUIDE.md`](CONFIGURATION_GUIDE.md)**
