# What to Upload: GitHub vs Hugging Face

## Quick Summary

| Destination | What to Upload | How |
|------------|----------------|-----|
| **GitHub** | **Everything** (entire project folder) | `git push` |
| **HF Dataset** | Raw data + train/test splits | Scripts auto-upload |
| **HF Model** | Trained model file | Scripts auto-upload |
| **HF Space** | App files (code, Dockerfile, requirements) | Scripts auto-upload |

---

## 📦 GitHub Repository

### Upload: **Everything in the `mlops/` folder**

**What to include:**
```
mlops/
├── data/
│   ├── engine_data.csv          ✅ Upload
│   └── processed/
│       ├── train.csv            ✅ Upload
│       └── test.csv             ✅ Upload
├── src/
│   ├── app.py                   ✅ Upload
│   ├── config.py                ✅ Upload
│   ├── data_prep.py             ✅ Upload
│   ├── data_register.py         ✅ Upload
│   ├── train.py                 ✅ Upload
│   ├── inference.py             ✅ Upload
│   ├── deploy_to_hf.py         ✅ Upload
│   ├── eda.py                  ✅ Upload
│   ├── hf_data_utils.py        ✅ Upload
│   └── hf_model_utils.py       ✅ Upload
├── notebooks/                   ✅ Upload (if you have EDA notebooks)
├── models/
│   └── best_model.joblib        ⚠️ Optional (large file)
├── .github/
│   └── workflows/
│       └── pipeline.yml         ✅ Upload (IMPORTANT!)
├── requirements.txt             ✅ Upload
├── Dockerfile                   ✅ Upload
├── README.md                    ✅ Upload
└── *.md files                   ✅ Upload (documentation)

❌ DON'T upload:
├── .venv/                       ❌ Skip (virtual environment)
├── __pycache__/                 ❌ Skip (Python cache)
├── mlruns/                      ❌ Skip (MLflow tracking - can be large)
└── .git/                        ❌ Skip (git metadata)
```

### How to Upload to GitHub:

```bash
cd /Users/ananttripathi/Desktop/mlops

# Initialize git (if not already done)
git init

# Create .gitignore to exclude large/unnecessary files
cat > .gitignore << EOF
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
mlruns/
*.log
.DS_Store
EOF

# Add all files
git add .

# Commit
git commit -m "Initial commit: Predictive Maintenance MLOps Pipeline"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/ananttripathi/engine-predictive-maintenance.git

# Push
git push -u origin main
```

---

## 🤗 Hugging Face - Dataset Repo

**Repo**: `ananttripathiak/engine-maintenance-dataset`

### Upload: **Data files only**

**Files uploaded automatically by scripts:**
- `data/engine_data.csv` → Uploaded as `data/engine_data.csv`
- `data/processed/train.csv` → Uploaded as `data/train.csv`
- `data/processed/test.csv` → Uploaded as `data/test.csv`

### How to Upload:

**Option 1: Run the scripts (automatic)**
```bash
# Step 1: Register raw data
python src/data_register.py

# Step 2: Prepare and upload train/test
python src/data_prep.py
```

**Option 2: Manual upload via HF Hub**
- Go to https://huggingface.co/datasets/ananttripathiak/engine-maintenance-dataset
- Click "Add file" → Upload `data/engine_data.csv`
- Upload `data/processed/train.csv` and `test.csv`

---

## 🤗 Hugging Face - Model Repo

**Repo**: `ananttripathiak/engine-maintenance-model`

### Upload: **Trained model file only**

**File uploaded automatically:**
- `models/best_model.joblib` → Uploaded as `model.joblib`

### How to Upload:

**Option 1: Run the training script (automatic)**
```bash
python src/train.py
# This will:
# 1. Train the model
# 2. Save to models/best_model.joblib
# 3. Upload to HF Model Repo automatically
```

**Option 2: Manual upload via HF Hub**
- Go to https://huggingface.co/ananttripathiak/engine-maintenance-model
- Click "Add file" → Upload `models/best_model.joblib`
- Rename it to `model.joblib` in the repo

---

## 🤗 Hugging Face - Space (Streamlit App)

**Repo**: `ananttripathiak/engine-maintenance-space`

### Upload: **App deployment files**

**Files uploaded automatically by script:**
```
✅ src/app.py                    (Main Streamlit app)
✅ src/inference.py             (Inference utilities)
✅ src/config.py                (Configuration)
✅ Dockerfile                   (Container definition)
✅ requirements.txt             (Dependencies)
✅ README.md                    (Documentation)
✅ Other src/*.py files         (If needed by app)

❌ NOT uploaded (ignored):
├── data/                       ❌ Too large
├── mlruns/                     ❌ MLflow tracking
├── models/                     ❌ Model is in Model Repo
├── .github/                    ❌ GitHub-specific
└── .venv/                      ❌ Virtual environment
```

### How to Upload:

**Option 1: Run the deployment script (automatic)**
```bash
python src/deploy_to_hf.py
# This will:
# 1. Create/update the HF Space
# 2. Upload all deployment files
# 3. Configure it as a Streamlit app
```

**Option 2: Manual upload via HF Hub**
- Go to https://huggingface.co/spaces/ananttripathiak/engine-maintenance-space
- Upload files one by one or use HF CLI

---

## 📋 Complete Upload Checklist

### ✅ Step 1: GitHub (Manual - Do First)
- [ ] Create GitHub repository
- [ ] Add `.gitignore` file
- [ ] Push entire `mlops/` folder to GitHub
- [ ] Add GitHub Secrets (HF_TOKEN, HF_DATASET_REPO, HF_MODEL_REPO, HF_SPACE_REPO)

### ✅ Step 2: Hugging Face Dataset (Automatic)
- [ ] Set `HF_TOKEN` environment variable
- [ ] Run `python src/data_register.py` (uploads raw data)
- [ ] Run `python src/data_prep.py` (uploads train/test)

### ✅ Step 3: Hugging Face Model (Automatic)
- [ ] Run `python src/train.py` (trains model and uploads to HF)

### ✅ Step 4: Hugging Face Space (Automatic)
- [ ] Run `python src/deploy_to_hf.py` (deploys app to HF Space)

### ✅ Step 5: Verify
- [ ] Check GitHub repo: https://github.com/ananttripathi/engine-predictive-maintenance
- [ ] Check HF Dataset: https://huggingface.co/datasets/ananttripathiak/engine-maintenance-dataset
- [ ] Check HF Model: https://huggingface.co/ananttripathiak/engine-maintenance-model
- [ ] Check HF Space: https://huggingface.co/spaces/ananttripathiak/engine-maintenance-space

---

## 🎯 Key Differences

| Aspect | GitHub | Hugging Face |
|--------|--------|--------------|
| **Purpose** | Code repository & version control | Data/Model/App hosting |
| **What** | Entire project (code, data, docs) | Specific artifacts (data/model/app) |
| **How** | Manual `git push` | Automatic via scripts |
| **Size** | Can be large (includes everything) | Optimized (only what's needed) |
| **Access** | Public/Private repo | Public datasets/models/spaces |
| **CI/CD** | GitHub Actions workflow | HF Spaces auto-deploy |

---

## 💡 Pro Tips

1. **GitHub First**: Always push to GitHub first, then run HF scripts
2. **Use .gitignore**: Exclude large files like `mlruns/` and `.venv/` from GitHub
3. **HF Scripts are Smart**: They automatically create repos if they don't exist
4. **Check File Sizes**: HF has file size limits, so scripts exclude large files
5. **GitHub Secrets**: Store HF credentials in GitHub Secrets for CI/CD

---

## 🚨 Common Mistakes to Avoid

❌ **Don't upload to GitHub:**
- Virtual environment (`.venv/`)
- Large MLflow runs (`mlruns/`)
- Python cache files (`__pycache__/`)

❌ **Don't upload to HF Space:**
- Raw data files (too large)
- Model files (use Model Repo instead)
- MLflow tracking data

✅ **Do upload to GitHub:**
- All source code
- Configuration files
- Documentation
- GitHub Actions workflow

✅ **Do upload to HF:**
- Only what each repo type needs (data → Dataset, model → Model, app → Space)

---

## 📞 Need Help?

- **GitHub Issues**: Check your repo settings and secrets
- **HF Upload Errors**: Verify `HF_TOKEN` is set correctly
- **File Size Issues**: Check HF file size limits (usually 10GB for datasets)
