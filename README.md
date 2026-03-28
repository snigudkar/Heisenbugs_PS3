# Heisenbugs_PS3

# EcoVision: NOAA Microplastic Intelligence System

**AI-Powered Environmental Risk Analytics Platform for Microplastics Detection and Assessment**

---

## 🔍 Overview

EcoVision is a research-grade platform that combines **computer vision, geospatial analytics, and historical NOAA data** to detect microplastics in environmental samples and compute a **comprehensive Environmental Risk Index (ERI)**. The system features **Explainable AI (XAI)** to visualize model predictions and make results interpretable.

Key features:

- Automated microplastic detection in microscopy images using **YOLOv8**.
- Explainable AI heatmaps for confidence visualization.
- Integration with NOAA microplastic datasets (or synthetic fallback data).
- Environmental Risk Index (ERI) calculation combining:
  - Particle density
  - Geospatial proximity to hotspots
  - Regional statistical variance
- Interactive dashboard and global hotspot visualization using **Streamlit** and **Plotly**.

---

## 📊 System Architecture

```text
User Interface (Streamlit App)
│
├── Image Processing & AI Inference (YOLO)
│     └── Bounding boxes and confidence
│
├── NOAA Data Engine
│     └── Load, clean, and filter geospatial and temporal data
│
├── Explainable AI (XAI)
│     └── Heatmap generation and overlay
│
├── Geospatial Analysis
│     └── Hotspot detection, distance metrics
│
└── Risk Scoring Engine (ERI)
      └── Combines density, proximity, variance
          ↓
      Visualization Layer (Streamlit)
          └── Risk score cards, sunburst charts, global maps
