import streamlit as st
import cv2
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ultralytics import YOLO
from PIL import Image
from scipy.spatial import distance
from datetime import datetime, timedelta

# --- 1. CONFIGURATION AND PROFESSIONAL STYLING ---
st.set_page_config(
    page_title="EcoVision: NOAA Microplastic Intelligence", 
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 4px; 
        border-left: 5px solid #2c3e50;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .insight-box { 
        padding: 25px; 
        background-color: #ffffff;
        color: #2c3e50;
        border-radius: 4px;
        border: 1px solid #dee2e6;
        margin: 15px 0;
    }
    .risk-score-card {
        padding: 30px;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .score-value { font-size: 4rem; font-weight: 800; line-height: 1; }
    .score-label { font-size: 1.2rem; font-weight: 600; letter-spacing: 2px; margin-top: 10px; }
    
    .bg-critical { background: linear-gradient(135deg, #cb2d3e, #ef473a); }
    .bg-elevated { background: linear-gradient(135deg, #f2994a, #f2c94c); }
    .bg-moderate { background: linear-gradient(135deg, #2193b0, #6dd5ed); }
    .bg-low { background: linear-gradient(135deg, #11998e, #38ef7d); }

    h1, h2, h3 { color: #2c3e50 !important; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. EXPLAINABLE AI (XAI) ENGINE ---
class MicroplasticXAI:
    def __init__(self, model):
        self.model = model

    def generate_explanation(self, img_np):
        results = self.model(img_np)[0]
        heatmap = np.zeros(img_np.shape[:2], dtype=np.float32)
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            heatmap[y1:y2, x1:x2] += conf
        heatmap = cv2.GaussianBlur(heatmap, (51, 51), 0)
        if heatmap.max() > 0:
            heatmap = (heatmap / heatmap.max() * 255).astype(np.uint8)
        color_heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        overlay = cv2.addWeighted(cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR), 0.7, color_heatmap, 0.3, 0)
        return cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB), results

# --- 3. DATA ARCHITECTURE ---
@st.cache_resource
def load_yolo_model():
    try: return YOLO('best.pt')
    except Exception: return None

@st.cache_data
def load_noaa_data():
    try:
        df = pd.read_csv('microplastics_dataset.csv')
        df.columns = [c.strip() for c in df.columns]
        df['Sample Date'] = pd.to_datetime(df['Sample Date'], errors='coerce')
        if 'Marine Setting' not in df.columns:
            df['Marine Setting'] = "Ocean water"
        return df.dropna(subset=['Latitude (degree)', 'Longitude (degree)'])
    except Exception:
        np.random.seed(42)
        n_samples = 1200
        settings = ["Ocean water", "Beach", "Ocean sediment"]
        df = pd.DataFrame({
            'Latitude (degree)': np.random.uniform(-70, 80, n_samples),
            'Longitude (degree)': np.random.uniform(-180, 180, n_samples),
            'Microplastics Measurement': np.random.uniform(0, 60, n_samples),
            'Concentration Class': np.random.choice(["Very High", "High", "Medium", "Low", "Very Low"], n_samples),
            'Marine Setting': np.random.choice(settings, n_samples),
            'Sample Date': [datetime.now() - timedelta(days=x) for x in range(n_samples)]
        })
        return df

model = load_yolo_model()
xai_engine = MicroplasticXAI(model) if model else None
noaa_df = load_noaa_data()

# --- 4. UPDATED ANALYTICS & RISK SCORING ENGINE ---
def calculate_risk_index(df_results, u_lat, u_lon, noaa_data, u_setting):
    env_baseline = noaa_data[noaa_data['Marine Setting'] == u_setting]
    if env_baseline.empty: env_baseline = noaa_data 
        
    hotspots = env_baseline[env_baseline['Concentration Class'].isin(['Very High', 'High'])][['Latitude (degree)', 'Longitude (degree)']].values
    dist = distance.cdist([(u_lat, u_lon)], hotspots).min() if len(hotspots) > 0 else 100
    prox_score = max(0, 35 - (dist * 1.5))

    setting_multipliers = {"Ocean water": 1.2, "Beach": 1.0, "Ocean sediment": 0.8}
    mult = setting_multipliers.get(u_setting, 1.0)
    
    particle_count = len(df_results) if df_results is not None else 0
    density_score = min(45, (particle_count / 15) * 10 * mult)

    local_mean = env_baseline['Microplastics Measurement'].mean()
    variance = min(20, (particle_count / (local_mean + 1)) * 5)

    total_score = int(prox_score + density_score + variance)
    
    if total_score > 75: label, color = "CRITICAL", "critical"
    elif total_score > 50: label, color = "ELEVATED", "elevated"
    elif total_score > 25: label, color = "MODERATE", "moderate"
    else: label, color = "LOW", "low"

    return total_score, label, color, round(dist, 2)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("EcoVision")
    st.markdown("---")
    st.subheader("Station Configuration")
    u_lat = st.number_input("Station Latitude", value=19.0760, format="%.4f")
    u_lon = st.number_input("Station Longitude", value=72.8777, format="%.4f")
    u_setting = st.selectbox("Sample Medium", ["Ocean water", "Beach", "Ocean sediment"])
    year_range = st.slider("Temporal Baseline", 1970, 2026, (2018, 2026))

# --- 6. MAIN INTERFACE ---
st.title("EcoVision: NOAA Microplastic Intelligence System")
tab1, tab2 = st.tabs(["Laboratory Analysis", "Global Monitoring Network"])

with tab1:
    files = st.file_uploader("Upload Batch Microscopy Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    if files:
        all_detections = []
        for file in files:
            img = Image.open(file).convert("RGB")
            img_np = np.array(img)
            if model and xai_engine:
                with st.spinner(f"Analyzing {file.name}..."):
                    xai_img, results = xai_engine.generate_explanation(img_np)
                with st.expander(f"Data Sheet: {file.name}"):
                    c1, c2, c3 = st.columns(3)
                    c1.image(img, caption="Input", use_container_width=True)
                    c2.image(results.plot(), caption="Detections", use_container_width=True)
                    c3.image(xai_img, caption="XAI Activation", use_container_width=True)
                for box in results.boxes:
                    all_detections.append({"Sample ID": file.name, "Type": model.names[int(box.cls[0])], "Confidence": float(box.conf[0])})

        if all_detections:
            df_res = pd.DataFrame(all_detections)
            score, label, color, dist = calculate_risk_index(df_res, u_lat, u_lon, noaa_df, u_setting)
            
            st.divider()
            col_l, col_r = st.columns([1, 1])
            with col_l:
                st.markdown(f"<div class='risk-score-card bg-{color}'><div style='text-transform: uppercase; font-size: 0.8rem; opacity: 0.9;'>{u_setting} Risk Index</div><div class='score-value'>{score}</div><div class='score-label'>{label}</div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='insight-box'><strong>Contextual Intelligence</strong><br>• Setting: <b>{u_setting}</b><br>• Proximity to {u_setting} Hotspot: <b>{dist}°</b><br>• Particle Count: <b>{len(df_res)}</b></div>", unsafe_allow_html=True)
            with col_r:
                fig_pie = px.sunburst(df_res, path=['Type', 'Sample ID'], values='Confidence', color_discrete_sequence=px.colors.qualitative.Bold)
                st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.subheader(f"Global Hotspot Mapping: {u_setting} Baseline")
    map_df = noaa_df[(noaa_df['Sample Date'].dt.year.between(year_range[0], year_range[1])) & (noaa_df['Marine Setting'] == u_setting)].copy()
    
    if map_df.empty:
        st.info(f"Showing global data: No specific records for {u_setting} in this date range.")
        map_df = noaa_df[noaa_df['Sample Date'].dt.year.between(year_range[0], year_range[1])].copy()

    fig = go.Figure()
    c_map = {"Very High": "#b2182b", "High": "#ef8a62", "Medium": "#fddbc7", "Low": "#67a9cf", "Very Low": "#2166ac"}
    for cls, clr in c_map.items():
        subset = map_df[map_df['Concentration Class'] == cls]
        if not subset.empty:
            fig.add_trace(go.Scattergeo(lat=subset['Latitude (degree)'], lon=subset['Longitude (degree)'], mode='markers', marker=dict(size=6, color=clr, opacity=0.7, line=dict(width=0.5, color='white')), name=cls))
    
    fig.add_trace(go.Scattergeo(lat=[u_lat], lon=[u_lon], mode='markers', marker=dict(size=16, color='#ffffff', symbol='diamond', line=dict(width=2, color='#2c3e50')), name='Station'))
    fig.update_layout(geo=dict(projection_type="natural earth", showland=True, landcolor="#f1f3f5", showocean=True, oceancolor="#ffffff"), height=700, margin={"r":0,"t":30,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("EcoVision Intelligence Platform | Integrated NOAA Data Services | © 2026")