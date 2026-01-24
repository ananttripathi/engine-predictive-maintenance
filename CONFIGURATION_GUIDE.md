# Configuration Guide: Hugging Face & GitHub Setup

This guide shows you exactly where to configure your Hugging Face Space details and GitHub repository information.

---

## 1. Hugging Face Configuration

### Option A: Update `src/config.py` (Recommended for Local Testing)

Edit `/Users/ananttripathi/Desktop/mlops/src/config.py` and replace the placeholder values:

```python
# Lines 58-62 in src/config.py
HF_DATASET_REPO = os.getenv(
    "HF_DATASET_REPO", "your-username/engine-maintenance-dataset"  # <-- Replace "your-username"
)
HF_MODEL_REPO = os.getenv("HF_MODEL_REPO", "your-username/engine-maintenance-model")  # <-- Replace
HF_SPACE_REPO = os.getenv("HF_SPACE_REPO", "your-username/engine-maintenance-space")  # <-- Replace
```

**Example** (HF username: `ananttripathiak`, GitHub username: `ananttripathi`):
```python
HF_DATASET_REPO = os.getenv(
    "HF_DATASET_REPO", "ananttripathiak/engine-maintenance-dataset"
)
HF_MODEL_REPO = os.getenv("HF_MODEL_REPO", "ananttripathiak/engine-maintenance-model")
HF_SPACE_REPO = os.getenv("HF_SPACE_REPO", "ananttripathiak/engine-maintenance-space")
```

### Option B: Set Environment Variables (For Local Testing)

Instead of editing `config.py`, you can export these in your terminal:

```bash
export HF_TOKEN="hf_your_token_here"
export HF_DATASET_REPO="your-username/engine-maintenance-dataset"
export HF_MODEL_REPO="your-username/engine-maintenance-model"
export HF_SPACE_REPO="your-username/engine-maintenance-space"
```

---

## 2. GitHub Repository Configuration

### A. GitHub Secrets (Required for GitHub Actions)

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these 4 secrets:

1. **`HF_TOKEN`**
   - Value: Your Hugging Face access token (get it from https://huggingface.co/settings/tokens)
   - Example: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

2. **`HF_DATASET_REPO`**
   - Value: Your Hugging Face dataset repo ID
   - Example: `ananttripathiak/engine-maintenance-dataset`

3. **`HF_MODEL_REPO`**
   - Value: Your Hugging Face model repo ID
   - Example: `ananttripathiak/engine-maintenance-model`

4. **`HF_SPACE_REPO`**
   - Value: Your Hugging Face Space repo ID
   - Example: `ananttripathiak/engine-maintenance-space`

**Note:** The GitHub Actions workflow (`.github/workflows/pipeline.yml`) automatically reads these secrets. No code changes needed!

### B. Update README.md with Your GitHub Repo URL

Edit `/Users/ananttripathi/Desktop/mlops/README.md` and add your GitHub repository link:

```markdown
## GitHub Repository

- **Repository URL**: https://github.com/your-username/engine-predictive-maintenance
- **GitHub Actions**: https://github.com/your-username/engine-predictive-maintenance/actions
```

---

## 3. Quick Setup Checklist

- [ ] **Hugging Face Account**: Create account at https://huggingface.co
- [ ] **HF Access Token**: Generate at https://huggingface.co/settings/tokens (needs `write` permission)
- [ ] **Update `src/config.py`**: Replace `"username"` with your actual HF username
- [ ] **Create HF Repos** (optional - scripts will create them automatically):
  - Dataset repo: `your-username/engine-maintenance-dataset`
  - Model repo: `your-username/engine-maintenance-model`
  - Space repo: `your-username/engine-maintenance-space`
- [ ] **GitHub Repository**: Create a new repo and push this `mlops` folder
- [ ] **GitHub Secrets**: Add the 4 secrets listed above in your GitHub repo settings
- [ ] **Test Locally**: Run `python src/data_register.py` to verify HF connection

---

## 4. Testing Your Configuration

### Test Local Configuration

```bash
cd /Users/ananttripathi/Desktop/mlops
source .venv/bin/activate

# Set your HF token (if not in config.py)
export HF_TOKEN="hf_your_token_here"

# Test data registration
python src/data_register.py

# Test data preparation
python src/data_prep.py

# Test model training
python src/train.py

# Test deployment
python src/deploy_to_hf.py
```

### Test GitHub Actions

1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit: Predictive maintenance MLOps pipeline"
   git push origin main
   ```

2. Go to your GitHub repo → **Actions** tab
3. You should see the "Predictive Maintenance Pipeline" workflow running
4. All 4 jobs should complete successfully (green checkmarks)

---

## 5. Where Each Configuration is Used

| Configuration | Used In | Purpose |
|--------------|---------|---------|
| `HF_DATASET_REPO` | `src/data_register.py`, `src/data_prep.py`, `src/train.py` | Dataset storage and retrieval |
| `HF_MODEL_REPO` | `src/train.py`, `src/inference.py`, `src/app.py` | Model storage and loading |
| `HF_SPACE_REPO` | `src/deploy_to_hf.py` | Streamlit app deployment |
| `HF_TOKEN` | All HF-related scripts | Authentication |
| GitHub Secrets | `.github/workflows/pipeline.yml` | CI/CD automation |

---

## Need Help?

- **Hugging Face Docs**: https://huggingface.co/docs/hub
- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **GitHub Secrets**: https://docs.github.com/en/actions/security-guides/encrypted-secrets
