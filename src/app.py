"""
Enhanced Streamlit application for engine predictive maintenance.

Intended to be run locally or deployed as a Hugging Face Space.
Features an interactive, modern UI with real-time predictions,
visualizations, and detailed insights.
"""

from __future__ import annotations

import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

import config
from inference import predict_engine_condition


def _is_running_in_hf_space() -> bool:
    """Check if app is running in Hugging Face Space."""
    # HF Spaces set SPACE_ID or SYSTEM environment variable
    return os.getenv("SPACE_ID") is not None or os.getenv("SYSTEM") == "spaces"


def _get_default_source() -> str:
    """Decide whether to load the model from HF or local based on env vars."""
    # In HF Space, always use HF model
    if _is_running_in_hf_space():
        return "hf"
    if config.HF_TOKEN and config.HF_MODEL_REPO:
        return "hf"
    return "local"


def create_gauge_chart(value: float, title: str, color: str) -> go.Figure:
    """Create a gauge chart for sensor readings."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 16}},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
    return fig


def create_sensor_comparison_chart(sensor_data: dict) -> go.Figure:
    """Create a radar chart comparing sensor values."""
    categories = list(sensor_data.keys())
    values = list(sensor_data.values())
    
    # Normalize values for better visualization (0-100 scale)
    max_values = {
        "Engine_RPM": 4000,
        "Lub_Oil_Pressure": 10,
        "Fuel_Pressure": 30,
        "Coolant_Pressure": 10,
        "Lub_Oil_Temperature": 150,
        "Coolant_Temperature": 150,
    }
    
    normalized_values = [
        (v / max_values.get(k, 100)) * 100 for k, v in zip(categories, values)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_values + [normalized_values[0]],  # Close the loop
        theta=[k.replace("_", " ") for k in categories] + [categories[0].replace("_", " ")],
        fill='toself',
        name='Current Readings',
        line_color='#1f77b4'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        height=400,
        title="Sensor Readings Overview"
    )
    
    return fig


def main() -> None:
    # MUST be first Streamlit command
    st.set_page_config(
        page_title="Engine Predictive Maintenance",
        page_icon="🛠️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
        }
        .prediction-box {
            padding: 2rem;
            border-radius: 15px;
            margin: 1.5rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .success-box {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
        }
        .warning-box {
            background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);
            color: white;
        }
        .stSlider > div > div > div {
            background-color: #1f77b4;
        }
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: bold;
            font-size: 1.2rem;
            padding: 0.75rem;
            border-radius: 10px;
            border: none;
            transition: all 0.3s;
        }
        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)

    # Compact Header
    st.markdown('<h1 style="font-size: 2rem; text-align: center; color: #1f77b4; margin-bottom: 0.5rem;">🛠️ Engine Predictive Maintenance</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; margin-bottom: 1rem; font-size: 0.9rem;">AI-Powered Engine Health Monitoring & Failure Prediction</p>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        # In HF Space, always use HF model and hide selection
        is_in_space = _is_running_in_hf_space()
        default_source = _get_default_source()
        
        if is_in_space:
            # In Space: completely hide model source selection, always use HF
            source = "hf"
            # Don't show any configuration UI in Space
        else:
            # Local development: show configuration section
            st.header("⚙️ Configuration")
            source = st.radio(
                "📦 Model Source:",
                options=["local", "hf"],
                index=0 if default_source == "hf" else 1,
                format_func=lambda x: "🤖 Hugging Face Hub" if x == "hf" else "💾 Local File",
                help="Select where to load the trained model from"
            )
        
        st.markdown("---")
        
        st.header("📊 Quick Stats")
        if is_in_space:
            # In Space: always show HF model status
            if config.HF_TOKEN and config.HF_MODEL_REPO:
                st.success("✅ Model Ready")
                st.caption(f"Loading from: {config.HF_MODEL_REPO}")
            else:
                st.error("❌ Configuration Missing")
                st.caption("Set HF_TOKEN as Space secret in Settings")
                st.markdown("""
                **To fix:**
                1. Go to Space Settings
                2. Add secret: `HF_TOKEN`
                3. Restart Space
                """)
        else:
            # Local development: check local model
            if os.path.exists(config.BEST_MODEL_LOCAL_PATH):
                st.success("✅ Model Available")
                st.caption("Trained model found locally")
            else:
                st.warning("⚠️ Model Not Found")
                st.caption("Run training script first")
        
        st.markdown("---")
        
        st.header("ℹ️ About")
        st.markdown("""
        This application uses machine learning to predict engine failures based on:
        - Engine RPM
        - Oil & Fuel Pressures
        - Coolant Pressure
        - Temperature Readings
        
        **Status**: 0 = Normal | 1 = Requires Maintenance
        """)
        
        st.markdown("---")
        st.caption("Built with ❤️ using Streamlit & Scikit-learn")

    # Balanced layout - inputs on left, larger visualization on right
    col_input, col_viz = st.columns([1, 1.2])
    
    with col_input:
        # Input form
        with st.form(key="engine_form", clear_on_submit=False):
            st.markdown("### 🔧 Sensor Inputs")
            
            # 2 columns for inputs
            col_a, col_b = st.columns(2)
            
            with col_a:
                engine_rpm = st.number_input(
                    "⚙️ Engine RPM",
                    min_value=0.0,
                    max_value=4000.0,
                    value=800.0,
                    step=10.0,
                    help="Revolutions per minute"
                )
                lub_oil_pressure = st.number_input(
                    "🛢️ Lub Oil Pressure",
                    min_value=0.0,
                    max_value=10.0,
                    value=3.0,
                    step=0.1,
                    help="bar/kPa"
                )
                fuel_pressure = st.number_input(
                    "⛽ Fuel Pressure",
                    min_value=0.0,
                    max_value=30.0,
                    value=10.0,
                    step=0.1,
                    help="bar/kPa"
                )
            
            with col_b:
                coolant_pressure = st.number_input(
                    "💧 Coolant Pressure",
                    min_value=0.0,
                    max_value=10.0,
                    value=2.0,
                    step=0.1,
                    help="bar/kPa"
                )
                lub_oil_temp = st.number_input(
                    "🌡️ Lub Oil Temp",
                    min_value=0.0,
                    max_value=150.0,
                    value=80.0,
                    step=0.5,
                    help="°C"
                )
                coolant_temp = st.number_input(
                    "🌡️ Coolant Temp",
                    min_value=0.0,
                    max_value=150.0,
                    value=80.0,
                    step=0.5,
                    help="°C"
                )
            
            submitted = st.form_submit_button("🚀 Predict Engine Condition", use_container_width=True)
    
    with col_viz:
        st.markdown("### 📊 Sensor Visualization")
        
        # Real-time sensor visualization
        sensor_data = {
            "Engine_RPM": engine_rpm,
            "Lub_Oil_Pressure": lub_oil_pressure,
            "Fuel_Pressure": fuel_pressure,
            "Coolant_Pressure": coolant_pressure,
            "Lub_Oil_Temperature": lub_oil_temp,
            "Coolant_Temperature": coolant_temp,
        }
        
        # Larger, more readable radar chart
        radar_fig = create_sensor_comparison_chart(sensor_data)
        radar_fig.update_layout(height=450, margin=dict(l=40, r=40, t=50, b=40))  # Larger and more readable
        st.plotly_chart(radar_fig, use_container_width=True, config={'displayModeBar': False})

    # Prediction results
    if submitted:
        inputs = {
            "Engine_RPM": engine_rpm,
            "Lub_Oil_Pressure": lub_oil_pressure,
            "Fuel_Pressure": fuel_pressure,
            "Coolant_Pressure": coolant_pressure,
            "Lub_Oil_Temperature": lub_oil_temp,
            "Coolant_Temperature": coolant_temp,
        }

        # Check if HF_TOKEN is set when using HF model
        if source == "hf" and not config.HF_TOKEN:
            st.error("❌ **HF_TOKEN not configured**")
            st.markdown("""
            **To fix this:**
            1. Go to Space Settings → Repository secrets
            2. Add secret: `HF_TOKEN` with your Hugging Face token
            3. Restart the Space
            
            Get token from: https://huggingface.co/settings/tokens
            """)
            st.stop()
        
        with st.spinner("🤖 Loading model and analyzing sensor data..."):
            try:
                result = predict_engine_condition(inputs=inputs, source=source)
            except Exception as e:
                st.error(
                    f"❌ **Prediction Failed**\n\n"
                    f"Error: {str(e)}\n\n"
                    f"**Troubleshooting:**\n"
                    f"- Ensure the model is trained: `python src/train.py`\n"
                    f"- Check model file exists: `models/best_model.joblib`\n"
                    f"- Verify HF credentials if using Hugging Face Hub"
                )
                return

        pred_label = result["prediction"]
        prob_faulty = result["probability_faulty"]
        prob_normal = 1 - prob_faulty

        # Compact results section
        st.markdown("---")
        
        result_col1, result_col2 = st.columns([1.5, 1])
        
        with result_col1:
            if pred_label == 1:
                st.markdown(
                    f'<div class="prediction-box warning-box" style="padding: 1rem;">'
                    f'<h2 style="color: white; margin: 0; font-size: 1.5rem;">🚨 MAINTENANCE REQUIRED</h2>'
                    f'<p style="font-size: 1.1rem; margin: 0.5rem 0;">Engine is <b>LIKELY FAULTY</b> - Fault Probability: <b>{prob_faulty:.1%}</b></p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                with st.expander("🔧 Recommended Actions", expanded=False):
                    st.markdown("""
                    - Schedule immediate engine inspection
                    - Verify sensor readings are accurate
                    - Review maintenance history
                    - Consult maintenance specialist
                    """)
            else:
                st.markdown(
                    f'<div class="prediction-box success-box" style="padding: 1rem;">'
                    f'<h2 style="color: white; margin: 0; font-size: 1.5rem;">✅ ENGINE HEALTHY</h2>'
                    f'<p style="font-size: 1.1rem; margin: 0.5rem 0;">Engine is <b>OPERATING NORMALLY</b> - Fault Probability: <b>{prob_faulty:.1%}</b></p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                st.success("✅ All sensors within normal ranges. Continue regular monitoring.")
        
        with result_col2:
            # Compact probability gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob_faulty * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Fault Risk %", 'font': {'size': 16}},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkred" if pred_label == 1 else "darkgreen"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgreen"},
                        {'range': [30, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "lightcoral"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 70
                    }
                }
            ))
            fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # Compact metrics
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Normal", f"{prob_normal:.0%}")
            with col_m2:
                st.metric("Fault", f"{prob_faulty:.0%}")

    # Compact Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 0.5rem; font-size: 0.85rem;'>
        <p>🛠️ <b>Predictive Maintenance System</b> | Built with Streamlit, Scikit-learn & Plotly | Developed by <b>Anant Tripathi</b></p>
        <p style='font-size: 0.75rem; color: #888; margin-top: 0.25rem;'>⚠️ Use as decision-support tool, not replacement for expert diagnostics</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
