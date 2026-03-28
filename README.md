# EcoVision: NOAA Microplastic Intelligence System

**Problem Statement:** Microplastic Detection & Risk Assessment  
**Team Name:** Heisenbugs

---

## 🔍 Project Overview

**EcoVision** is an AI-powered ecological monitoring platform designed to close the *Identification Gap* in marine conservation. By integrating **YOLOv8 Object Detection** with historical **NOAA Global Data**, the system transforms raw microscopy images into a quantified **Environmental Risk Index (ERI)**.

Our solution provides researchers with **real-time, explainable insights** into:

- Microplastic **density**
- **Morphology** (Fibers, Fragments, Films)
- **Regional threat levels**

---

## 🏗️ System Architecture

The platform is built on a modular **data-to-insight pipeline**:

1. **User Interface**: Streamlit-based batch image uploader and geospatial configuration  
2. **AI Inference**: YOLOv8 engine for morphological classification  
3. **XAI Layer**: Custom heatmap generation for model interpretability  
4. **NOAA Data Engine**: Geospatial filtering and temporal baseline analysis  
5. **ERI Scoring**: Multi-factor index combining **density**, **proximity**, and **variance**

---

## 📊 Datasets and Preprocessing

### 1. NOAA Global Microplastic Database

We utilize the **National Centers for Environmental Information (NCEI) / NOAA dataset** as our ground-truth baseline to compare current samples against decades of global records.

**Preprocessing Steps:**

- **Column Standardization**: Clean headers for uniform mapping of Latitude/Longitude and measurement units  
- **Date Parsing**: Convert strings to datetime objects for temporal filtering (1970–2026)  
- **Missing Value Handling**: Remove records lacking valid geospatial coordinates  
- **Temporal Filtering**: Dynamic windowing based on user-defined *Temporal Baseline*

### 2. Microplastic Microscopy Dataset

- **Source**: Custom-curated dataset of microscopic imagery labeled via Roboflow  
- **Classes**: Fiber, Fragment, Film

---

## 🧠 Model & Performance Metrics

### YOLOv8 Morphological Engine

We utilized **YOLOv8 (Small)** for its optimal balance between **inference speed** and **detection accuracy** for small-scale micro-particles.

- **Classes**:  
  - Fiber (High aspect ratio)  
  - Fragment (Jagged edges)  
  - Film (Planar)  
- **Inference Speed**: ~15ms per image  
- **mAP@50**: [Insert Your Value, e.g., 0.88]  

### Explainable AI (XAI)

To ensure scientific validity, we implemented a custom **MicroplasticXAI** class:

- Generates **Gaussian-blurred heatmaps** based on YOLO detection confidence  
- Confirms the model focuses on **polymeric textures** rather than slide artifacts  

---

## 🚀 Environmental Risk Index (ERI) Formula

Our unique contribution is the **Ecological Synergy Protocol (ESP)**, which calculates risk beyond simple counting:

\[
\text{Risk} = \alpha (D_{\text{batch}} \cdot \mu_{\text{setting}}) + \beta \left(\frac{1}{dist_{\text{hotspot}}}\right) + \gamma \left(\frac{D_{\text{batch}}}{\bar{x}_{\text{NOAA}}}\right)
\]

### Components

| Factor                  | Description                                        | Contribution |
|-------------------------|---------------------------------------------------|-------------|
| **Density**             | Weighted count based on sample medium (Water, Beach, or Sediment) | 45%         |
| **Proximity**           | Distance to historically recorded "High-Density" hotspots          | 35%         |
| **Statistical Variance**| Deviation from the regional historical mean                     | 20%         |

### Formulas

1. **Proximity Score**  
\[
\text{Proximity Score} = \max(0, 35 - 1.5 \times \text{distance})
\]

2. **Density Score**  
\[
\text{Density Score} = \min\Big(45, \frac{N_{\text{detected}}}{N_{\text{ref}}} \times 10 \times \mu_{\text{setting}}\Big)
\]

3. **Variance Score**  
\[
\text{Variance Score} = \min\Big(20, \frac{N_{\text{detected}}}{\bar{N}_{\text{NOAA}} + 1} \times 5\Big)
\]

4. **Total Risk Score**  
\[
\text{Total Risk} = \text{Proximity Score} + \text{Density Score} + \text{Variance Score}
\]

5. **Risk Category**

| Score Range | Category  |
|-------------|-----------|
| 0–25        | LOW       |
| 26–50       | MODERATE  |
| 51–75       | ELEVATED  |
| 76–100      | CRITICAL  |

---

## 🔢 Example Flow: Single Image

Suppose YOLO detects **3 particles**:

| Particle | Morphology | Size (µm) |
|----------|------------|------------|
| 1        | Fiber      | 120        |
| 2        | Fragment   | 90         |
| 3        | Film       | 50         |

**Step 1: Proximity Score**  
Station is 10° from nearest hotspot:  
\[
\text{Proximity Score} = \max(0, 35 - 1.5 \times 10) = 20
\]

**Step 2: Density Score**  
3 particles in **ocean** (multiplier = 1.2):  
\[
\text{Density Score} = \min\Big(45, \frac{3}{15} \times 10 \times 1.2\Big) = 2
\]

**Step 3: Variance Score**  
Historical average = 2 particles:  
\[
\text{Variance Score} = \min\Big(20, \frac{3}{2+1} \times 5\Big) = 5
\]

**Step 4: Total Risk Score**  
\[
\text{Total Risk} = 20 + 2 + 5 = 27
\]

**Step 5: Risk Category**  
27 → **MODERATE risk**

---

## 📊 Dashboard Summary

- **Pie Chart**: Fiber = 1, Fragment = 1, Film = 1  
- **Heatmap**: Shows YOLO attention regions  
- **Risk Score**: 27 → MODERATE → actionable insights  

---

## ⚡ Key Takeaways

1. Original problem: classify shape & size → hazard identification  
2. Extension: add **location**, **particle count**, and **variance** → holistic risk index  
3. Formula design:
   - **Normalization** → scale counts to reference  
   - **Scaling** → human-readable points  
   - **Capping** → balanced contribution to total risk  
4. Outcome: automated **0–100 risk score** + visual dashboard for researchers  

---

## 💻 Tech Stack

| Layer         | Technology                                |
|---------------|------------------------------------------|
| Language      | Python 3.9+                               |
| Frontend      | Streamlit                                 |
| AI/CV         | Ultralytics YOLOv8, OpenCV               |
| Analytics     | Pandas, Scipy, NumPy                      |
| Visualization | Plotly Express, Plotly Graph Objects      |
