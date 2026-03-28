EcoVision: NOAA Microplastic Intelligence System

Problem Statement: Microplastic Detection & Risk Assessment
Team Name:Heisenbugs

🔍 Project Overview

EcoVision is an AI-powered ecological monitoring platform designed to close the Identification Gap in marine conservation. By integrating YOLOv8 Object Detection with historical NOAA Global Data, the system transforms raw microscopy images into a quantified Environmental Risk Index (ERI).

Our solution provides researchers with real-time, explainable insights into:

Microplastic density
Morphology (Fibers, Fragments, Films)
Regional threat levels
🏗️ System Architecture

The platform is built on a modular data-to-insight pipeline:

User Interface: Streamlit-based batch image uploader and geospatial configuration.
AI Inference: YOLOv8 engine for morphological classification.
XAI Layer: Custom heatmap generation for model interpretability.
NOAA Data Engine: Geospatial filtering and temporal baseline analysis.
ERI Scoring: Multi-factor index combining density, proximity, and variance.
📊 Datasets and Preprocessing
1. NOAA Global Microplastic Database

We utilize the National Centers for Environmental Information (NCEI) / NOAA dataset as our ground-truth baseline to compare current samples against decades of global records.

Preprocessing Steps:

Column Standardization: Cleaning headers for uniform mapping of Latitude/Longitude and Measurement units.
Date Parsing: Converting strings to datetime objects for temporal filtering (1970–2026).
Missing Value Handling: Systematic removal of records lacking valid geospatial coordinates.
Temporal Filtering: Dynamic windowing based on user-defined "Temporal Baseline" inputs.
2. Microplastic Microscopy Dataset
Source: Custom-curated dataset of microscopic imagery labeled via Roboflow.
Classes: Fiber, Fragment, Film
🧠 Model & Performance Metrics
YOLOv8 Morphological Engine

We utilized YOLOv8 (Small) for its optimal balance between inference speed and detection accuracy for small-scale micro-particles.

Classes:
Fiber (High aspect ratio)
Fragment (Jagged edges)
Film (Planar)
Inference Speed: ~15ms per image
mAP@50: [Insert Your Value, e.g., 0.88]
Explainable AI (XAI)

To ensure scientific validity, we implemented a custom MicroplasticXAI class.

Generates Gaussian-blurred heatmaps based on YOLO detection confidence.
Confirms the model focuses on polymeric textures rather than slide artifacts.
🚀 Environmental Risk Index (ERI) Formula

Our unique contribution is the Ecological Synergy Protocol (ESP), which calculates risk beyond simple counting:

𝑅
𝑖
𝑠
𝑘
=
𝛼
(
𝐷
𝑏
𝑎
𝑡
𝑐
ℎ
⋅
𝜇
𝑠
𝑒
𝑡
𝑡
𝑖
𝑛
𝑔
)
+
𝛽
(
1
𝑑
𝑖
𝑠
𝑡
ℎ
𝑜
𝑡
𝑠
𝑝
𝑜
𝑡
)
+
𝛾
(
𝐷
𝑏
𝑎
𝑡
𝑐
ℎ
𝑥
ˉ
𝑁
𝑂
𝐴
𝐴
)
Risk=α(D
batch
	​

⋅μ
setting
	​

)+β(
dist
hotspot
	​

1
	​

)+γ(
x
ˉ
NOAA
	​

D
batch
	​

	​

)

Components:

Factor	Description	Contribution
Density	Weighted count based on sample medium (Water, Beach, or Sediment)	45%
Proximity	Distance to historically recorded "High-Density" hotspots	35%
Statistical Variance	Deviation from the regional historical mean	20%
✨ Key Features
Batch Microscopy Processing: Upload multiple images for a statistically stable average.
Contextual Intelligence: Adjusts risk based on environment (e.g., Water samples weighted 20% higher than sediment).
Global Hotspot Mapping: Real-time Plotly-based visualization of your station relative to global threats.
Explainable Visuals: Sunburst charts for morphology distribution and XAI overlays for verification.
💻 Tech Stack
Layer	Technology
Language	Python 3.9+
Frontend	Streamlit
AI/CV	Ultralytics YOLOv8, OpenCV
Analytics	Pandas, Scipy, NumPy
Visualization	Plotly Express, Plotly Graph Objects
