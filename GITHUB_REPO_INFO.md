# GitHub Repository Information

## Repository Details

- **GitHub Username**: `ananttripathi`
- **Repository Name**: `engine-predictive-maintenance` (or your chosen name)
- **Full Repository URL**: `https://github.com/ananttripathi/engine-predictive-maintenance`

## Where to Add This Information

### 1. In Your Final Notebook/Report

Add a section like this:

```markdown
## GitHub Repository

- **Repository URL**: https://github.com/ananttripathi/engine-predictive-maintenance
- **GitHub Actions Workflow**: https://github.com/ananttripathi/engine-predictive-maintenance/actions
- **Repository Structure**: [Screenshot of folder structure]
- **Workflow Execution**: [Screenshot of successful pipeline runs]
```

### 2. In README.md

The README already includes a placeholder. After you create the repo, update it with your actual repo name.

### 3. GitHub Actions Workflow

**No changes needed!** The `.github/workflows/pipeline.yml` file automatically runs in the context of whatever repository it's pushed to. It doesn't need the repo URL hardcoded.

## Steps to Set Up GitHub Repository

1. **Create the repository on GitHub:**
   - Go to https://github.com/new
   - Repository name: `engine-predictive-maintenance` (or your choice)
   - Description: "Predictive Maintenance MLOps Pipeline for Engine Failure Classification"
   - Choose Public or Private
   - **Don't** initialize with README, .gitignore, or license (we already have files)

2. **Push your code:**
   ```bash
   cd /Users/ananttripathi/Desktop/mlops
   git init
   git add .
   git commit -m "Initial commit: Predictive maintenance MLOps pipeline"
   git branch -M main
   git remote add origin https://github.com/ananttripathi/engine-predictive-maintenance.git
   git push -u origin main
   ```

3. **Add GitHub Secrets:**
   - Go to: https://github.com/ananttripathi/engine-predictive-maintenance/settings/secrets/actions
   - Click "New repository secret"
   - Add these 4 secrets:
     - `HF_TOKEN` → Your Hugging Face token
     - `HF_DATASET_REPO` → `ananttripathiak/engine-maintenance-dataset`
     - `HF_MODEL_REPO` → `ananttripathiak/engine-maintenance-model`
     - `HF_SPACE_REPO` → `ananttripathiak/engine-maintenance-space`

4. **Verify GitHub Actions:**
   - After pushing, go to: https://github.com/ananttripathi/engine-predictive-maintenance/actions
   - You should see the "Predictive Maintenance Pipeline" workflow running
   - All 4 jobs should complete successfully

## Important Notes

- **GitHub username** (`ananttripathi`) is used for the repository URL
- **Hugging Face username** might be different - check your HF account and update `src/config.py` if needed
- The GitHub Actions workflow reads secrets automatically - no code changes needed
- Repository name can be anything you want (e.g., `engine-predictive-maintenance`, `mlops-project`, etc.)
