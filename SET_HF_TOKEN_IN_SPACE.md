# How to Set HF_TOKEN in Hugging Face Space

## 🔧 Fix the "Hugging Face token is not set" Error

The app needs `HF_TOKEN` to download the model from Hugging Face Model Hub. Set it as a Space secret.

---

## 📋 Step-by-Step: Add HF_TOKEN Secret

### Step 1: Go to Your Space Settings
1. Visit: **https://huggingface.co/spaces/ananttripathiak/engine-maintenance-space**
2. Click on **"Settings"** tab (top menu)

### Step 2: Add Secret
1. Scroll down to **"Repository secrets"** section
2. Click **"New secret"** button
3. Fill in:
   - **Secret name:** `HF_TOKEN`
   - **Secret value:** Your Hugging Face token (starts with `hf_`)
4. Click **"Add secret"**

### Step 3: Get Your Token (if needed)
If you don't have a token:
1. Go to: **https://huggingface.co/settings/tokens**
2. Click **"New token"**
3. Name it (e.g., "Space Token")
4. Select **"Write"** permission
5. Click **"Generate token"**
6. **Copy the token** (starts with `hf_`)
7. Paste it as the secret value

### Step 4: Restart Space
1. Go back to your Space
2. Click **"Settings"** tab
3. Scroll to **"Space hardware"** section
4. Click **"Restart Space"** button
5. Wait for rebuild (1-2 minutes)

---

## ✅ After Setting the Secret

The app will:
- ✅ Automatically load model from Hugging Face Hub
- ✅ No more "token is not set" errors
- ✅ Work correctly in the Space

---

## 🔍 Verify It's Set

1. Go to Space **Settings** → **Repository secrets**
2. You should see `HF_TOKEN` listed
3. The value will be hidden (shows as `••••••••`)

---

## 🚀 Quick Steps Summary

1. **Space URL:** https://huggingface.co/spaces/ananttripathiak/engine-maintenance-space
2. **Settings** → **Repository secrets** → **New secret**
3. **Name:** `HF_TOKEN`
4. **Value:** Your HF token (from https://huggingface.co/settings/tokens)
5. **Add secret** → **Restart Space**

---

## 📝 Alternative: Update via API

You can also set it programmatically, but the manual method above is easier.

---

**After setting the secret and restarting, the app should work!** ✅
