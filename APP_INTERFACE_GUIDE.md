# Streamlit App Interface Guide

## 🚀 Accessing the App

The Streamlit app should now be running. Open your web browser and navigate to:

**http://localhost:8501**

If port 8501 is busy, Streamlit will automatically use the next available port (8502, 8503, etc.). Check the terminal output for the exact URL.

---

## 📱 Interface Overview

### **Main Page Layout**

```
┌─────────────────────────────────────────────────────────┐
│  🛠️ Engine Predictive Maintenance – Failure Prediction  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  This app predicts whether an engine is operating        │
│  normally (0) or requires maintenance / at risk of      │
│  failure (1) based on real-time sensor readings.        │
│                                                           │
│  Adjust the sensor values below and click Predict to    │
│  see the model's classification and the probability of   │
│  a potential fault.                                       │
│                                                           │
├─────────────────────────────────────────────────────────┤
│  Input Sensor Readings                                   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────┐  ┌─────────────────────┐     │
│  │ Engine RPM           │  │ Coolant Pressure    │     │
│  │ [800.0]              │  │ [2.0]               │     │
│  │                      │  │                     │     │
│  │ Lub Oil Pressure     │  │ Lub Oil Temperature │     │
│  │ [3.0]                │  │ [80.0]              │     │
│  │                      │  │                     │     │
│  │ Fuel Pressure        │  │ Coolant Temperature │     │
│  │ [10.0]               │  │ [80.0]              │     │
│  └─────────────────────┘  └─────────────────────┘     │
│                                                           │
│              [Predict Button]                            │
│                                                           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Sidebar: Model Source                                   │
├─────────────────────────────────────────────────────────┤
│  Load model from:                                        │
│  ○ Hugging Face Hub                                      │
│  ● Local file                                            │
│                                                           │
│  Note: On Hugging Face Spaces, the model is typically   │
│  loaded from the model hub. Locally, you can choose     │
│  either source as long as you have run the training      │
│  pipeline or configured your HF token.                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 How to Use the Interface

### **Step 1: Select Model Source (Sidebar)**
- Choose **"Local file"** if you've run `python src/train.py` locally
- Choose **"Hugging Face Hub"** if you've uploaded the model to HF and set `HF_TOKEN`

### **Step 2: Enter Sensor Values**

Adjust the 6 sensor inputs:

1. **Engine RPM** (0-4000)
   - Default: 800.0
   - Typical range: 500-2000 RPM

2. **Lub Oil Pressure** (0-10 bar/kPa)
   - Default: 3.0
   - Typical range: 2-5 bar

3. **Fuel Pressure** (0-30 bar/kPa)
   - Default: 10.0
   - Typical range: 5-20 bar

4. **Coolant Pressure** (0-10 bar/kPa)
   - Default: 2.0
   - Typical range: 1-4 bar

5. **Lub Oil Temperature** (0-150°C)
   - Default: 80.0
   - Typical range: 70-90°C

6. **Coolant Temperature** (0-150°C)
   - Default: 80.0
   - Typical range: 70-90°C

### **Step 3: Click "Predict"**

After clicking the **Predict** button, you'll see one of two results:

#### ✅ **Normal Operation**
```
✅ The engine is LIKELY OPERATING NORMALLY (probability of fault X.XX%).
```

#### 🚨 **Faulty / Requires Maintenance**
```
🚨 The engine is LIKELY FAULTY / REQUIRES MAINTENANCE (probability XX.XX%).
```

---

## 📊 Example Predictions

### **Example 1: Normal Engine**
- Engine RPM: 1200
- Lub Oil Pressure: 3.5
- Fuel Pressure: 12.0
- Coolant Pressure: 2.5
- Lub Oil Temperature: 82.0
- Coolant Temperature: 85.0
- **Result**: ✅ Normal operation (low fault probability)

### **Example 2: Faulty Engine**
- Engine RPM: 400
- Lub Oil Pressure: 1.5
- Fuel Pressure: 5.0
- Coolant Pressure: 1.0
- Lub Oil Temperature: 95.0
- Coolant Temperature: 100.0
- **Result**: 🚨 Requires maintenance (high fault probability)

---

## 🔧 Troubleshooting

### **App Not Loading?**
1. Check terminal for errors
2. Verify port 8501 is available: `lsof -ti:8501`
3. Try a different port: `streamlit run src/app.py --server.port 8502`

### **Model Not Found Error?**
1. **For Local**: Run `python src/train.py` first to create `models/best_model.joblib`
2. **For HF**: Set `HF_TOKEN` and `HF_MODEL_REPO` environment variables

### **Import Errors?**
1. Activate virtual environment: `source .venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`

---

## 🎨 Interface Features

- **Clean, centered layout** for easy input
- **Two-column form** for organized sensor inputs
- **Real-time prediction** with probability scores
- **Color-coded results**: Green for normal, Red for faulty
- **Sidebar model selection** for flexibility
- **Responsive design** that works on different screen sizes

---

## 📸 Screenshots for Your Report

When documenting this in your final report, you can:
1. Take a screenshot of the input form
2. Take a screenshot showing a "Normal" prediction
3. Take a screenshot showing a "Faulty" prediction
4. Include the URL: `http://localhost:8501` (or your deployed HF Space URL)

---

## 🚀 Next Steps

1. **Test the app locally** with different sensor values
2. **Deploy to Hugging Face Space** using `python src/deploy_to_hf.py`
3. **Include screenshots** in your final report/notebook
4. **Document the interface** in your submission

The app is ready to use! 🎉
