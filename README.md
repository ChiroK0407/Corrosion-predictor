# 🔩 Corrosion Predictor Dashboard

Welcome to the **Corrosion Intelligence Platform** — a research-driven tool that blends **ISO 9223 standards** with **machine learning models** to estimate corrosion rates.

## 🚀 Features
- 🌍 Fetches weather & pollution data automatically via APIs  
- ⚙️ Combines ISO logic + ML (SVR, Random Forest, XGBoost)  
- 📊 Visualizes predictions with charts & maps  
- 🏛️ Benchmarks against CECRI archival datasets  
- 🔍 Offers explainability via feature importance plots  

## 🧭 Navigation
- **Model 1 (API-driven)** → Predict corrosion rates using live weather & pollution data  
- **Model 2 (CECRI archival)** → Train & benchmark ML models against CECRI datasets  
- **Map Views** → Visualize corrosion intensity across regions  

## 📖 References & Standards
- ISO 9223: Corrosivity of atmospheres  
- ISO 9224: Guiding values for corrosion rates  
- Indian Standard IS 1786:2008  
- CECRI archival datasets  

## 🛠️ Tech Stack
- Streamlit (frontend)  
- FastAPI (backend services)  
- XGBoost, Random Forest, SVR (ML models)  
- Plotly, Matplotlib (visualizations)  

## ▶️ Running Locally
```bash
git clone https://github.com/<your-username>/Corrosion-predictor.git
cd Corrosion-predictor
pip install -r requirements.txt
streamlit run frontend/streamlit_app.py
