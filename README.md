# EcoVision: NOAA Microplastic Intelligence System

**Problem Statement:** Microplastic Detection & Risk Assessment 
**Team Name:** [Heisenbugs]

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

1. **User Interface**: Streamlit-based batch image uploader and geospatial configuration.  
2. **AI Inference**: YOLOv8 engine for morphological classification.  
3. **XAI Layer**: Custom heatmap generation for model interpretability.  
4. **NOAA Data Engine**: Geospatial filtering and temporal baseline analysis.  
5. **ERI Scoring**: Multi-factor index combining **density**, **proximity**, and **variance**.  

---

## 📊 Datasets and Preprocessing

### 1. NOAA Global Microplastic Database

We utilize the **National Centers for Environmental Information (NCEI) / NOAA dataset** as our ground-truth baseline to compare current samples against decades of global records.

**Preprocessing Steps:**

- **Column Standardization**: Clean headers for uniform mapping of Latitude/Longitude and measurement units.  
- **Date Parsing**: Convert strings to datetime objects for temporal filtering (1970–2026).  
- **Missing Value Handling**: Remove records lacking valid geospatial coordinates.  
- **Temporal Filtering**: Dynamic windowing based on user-defined *Temporal Baseline*.  

### 2. Microplastic Microscopy Dataset

- **Source**: Custom-curated dataset of microscopic imagery labeled via Roboflow.  
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

- Generates **Gaussian-blurred heatmaps** based on YOLO detection confidence.  
- Confirms the model focuses on **polymeric textures** rather than slide artifacts.  

---

## 🚀 Environmental Risk Index (ERI) Formula

Our unique contribution is the **Ecological Synergy Protocol (ESP)**, which calculates risk beyond simple counting:

\[
Risk = \alpha(D_{batch} \cdot \mu_{setting}) + \beta \left(\frac{1}{dist_{hotspot}}\right) + \gamma \left(\frac{D_{batch}}{\bar{x}_{NOAA}}\right)
\]

### Components

| Factor               | Description                                        | Contribution |
|----------------------|---------------------------------------------------|-------------|
| **Density**          | Weighted count based on sample medium (Water, Beach, or Sediment) | 45%         |
| **Proximity**        | Distance to historically recorded "High-Density" hotspots          | 35%         |
| **Statistical Variance** | Deviation from the regional historical mean                     | 20%         |

---
