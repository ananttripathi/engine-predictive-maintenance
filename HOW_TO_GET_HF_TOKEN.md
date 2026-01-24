# How to Get Your Hugging Face Token

## 🎯 Quick Steps

1. Go to https://huggingface.co/settings/tokens
2. Click **"New token"** or **"Create new token"**
3. Give it a name (e.g., "MLOps Project")
4. Select **"Write"** permission (important!)
5. Click **"Generate token"**
6. **Copy the token immediately** (you won't see it again!)

---

## 📝 Detailed Step-by-Step Guide

### Step 1: Log in to Hugging Face
- Go to https://huggingface.co
- Log in with your account (`ananttripathiak`)

### Step 2: Navigate to Token Settings
- Click on your profile picture (top right)
- Select **"Settings"** from the dropdown menu
- In the left sidebar, click **"Access Tokens"**
- Or go directly to: https://huggingface.co/settings/tokens

### Step 3: Create New Token
- Click the **"New token"** button (or "Create new token")
- **Name**: Enter a descriptive name like:
  - `MLOps Project`
  - `Engine Predictive Maintenance`
  - `Personal Access Token`
- **Type**: Select **"Write"** (this is important!)
  - ✅ **Write** = Can create repos, upload files, deploy apps
  - ❌ **Read** = Only can download/view (not enough for this project)

### Step 4: Generate and Copy Token
- Click **"Generate token"**
- **IMPORTANT**: Copy the token immediately!
  - It will look like: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
  - You won't be able to see it again after closing the page
  - Format: Starts with `hf_` followed by long string

### Step 5: Save Token Securely
- Save it in a secure place (password manager, notes app, etc.)
- You'll need it for:
  - Running scripts locally
  - Setting GitHub Secrets

---

## 🔐 How to Use Your Token

### Option 1: Environment Variable (Local Testing)
```bash
# macOS/Linux
export HF_TOKEN="hf_your_token_here"

# Verify it's set
echo $HF_TOKEN

# Now run your scripts
python src/data_register.py
python src/train.py
python src/deploy_to_hf.py
```

### Option 2: GitHub Secrets (For CI/CD)
1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Name: `HF_TOKEN`
5. Value: Paste your token
6. Click **"Add secret"**

---

## ✅ Verify Your Token Works

Test your token:
```bash
export HF_TOKEN="hf_your_token_here"
python -c "from huggingface_hub import HfApi; api = HfApi(token='$HF_TOKEN'); print('✅ Token is valid!')"
```

Or test by running a simple script:
```bash
export HF_TOKEN="hf_your_token_here"
python src/data_register.py
# If it works without errors, your token is valid!
```

---

## 🚨 Important Notes

### Token Permissions
- **Must be "Write"** - Read-only tokens won't work
- Write tokens can:
  - Create repositories
  - Upload files
  - Deploy apps
  - Delete content (be careful!)

### Token Security
- **Never commit tokens to GitHub!**
- Don't share tokens publicly
- If token is exposed, revoke it immediately and create a new one
- Use GitHub Secrets for CI/CD (never hardcode in code)

### Token Format
- Always starts with `hf_`
- Example: `hf_AbCdEf1234567890XyZ...`
- If you see something different, you might have copied the wrong thing

---

## 🔄 If You Lose Your Token

1. Go to https://huggingface.co/settings/tokens
2. Find your token in the list
3. Click **"Revoke"** (if you think it's compromised)
4. Create a new token following the steps above

---

## 📸 Visual Guide

**Token Settings Page:**
```
Hugging Face → Profile → Settings → Access Tokens
```

**Create Token Form:**
```
Name: [MLOps Project]
Type: [Write ▼]  ← Select "Write"!
[Generate token]
```

**After Generation:**
```
Token: hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
[Copy] ← Click to copy!
```

---

## 🎯 Quick Checklist

- [ ] Logged into Hugging Face (ananttripathiak)
- [ ] Went to https://huggingface.co/settings/tokens
- [ ] Created new token with "Write" permission
- [ ] Copied token (starts with `hf_`)
- [ ] Saved token securely
- [ ] Set as environment variable: `export HF_TOKEN="hf_..."`
- [ ] Verified token works

---

## 💡 Pro Tips

1. **Name your tokens descriptively** - Easier to manage multiple tokens
2. **Use different tokens for different projects** - Better security
3. **Set expiration dates** - For extra security (optional)
4. **Revoke unused tokens** - Keep your account secure
5. **Use GitHub Secrets** - Never hardcode tokens in code

---

## 🆘 Troubleshooting

### "Token is invalid"
- Check you copied the entire token (starts with `hf_`)
- Verify token has "Write" permission
- Make sure no extra spaces when pasting

### "Permission denied"
- Token must have "Write" permission, not "Read"
- Create a new token with Write access

### "Token not found"
- Make sure you're logged into the correct HF account
- Check token wasn't revoked
- Create a new token if needed

---

## 📞 Need Help?

- **HF Token Docs**: https://huggingface.co/docs/hub/security-tokens
- **HF Settings**: https://huggingface.co/settings/tokens
- **HF Support**: Check HF community forums

---

**Your token is your key to uploading to Hugging Face! Keep it secure! 🔐**
