# 🚊 Smart City Mobility Dashboard
### Urban Traffic Analysis · Augsburg & Munich

A data analytics and machine learning project exploring urban mobility patterns in two Bavarian cities. Built as a portfolio project for **Geo Data Analyst / Smart City** roles — particularly relevant to organizations like **Augsburger Verkehrs- und Tarifverbund (AVV)** and **Münchner Verkehrsgesellschaft (MVG)**.

---

## 🎯 Problem Statement

Urban mobility planners need to understand:
- **When** congestion peaks occur and why
- **How** smaller and larger cities differ in demand patterns
- **Where** infrastructure investments would have the highest impact

This project analyzes hourly traffic volume across key transit stations in Augsburg and Munich, compares weekday vs weekend demand, and delivers a predictive model for traffic forecasting.

---

## 📊 Key Insights

| Finding | Detail |
|---|---|
| **Synchronized morning peak** | Both cities peak at **08:00** on weekdays — shared commuter pressure along the A8/rail corridor |
| **Munich scale** | Munich generates **~2× more traffic** at peak than Augsburg |
| **Weekend resilience** | Augsburg drops only ~20% on weekends vs Munich's ~40% — more local/leisure mobility in smaller cities |
| **Off-peak capacity** | 10:00–15:00 has 40–55% spare capacity in both cities — strong case for demand-shifting incentives |
| **PM bias in Munich** | Munich's PM peak (17:00) exceeds its AM peak — asymmetric commute patterns driven by larger catchment area |

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Data processing | `pandas`, `numpy` |
| Visualization | `matplotlib`, `seaborn` |
| Geospatial | `folium`, `streamlit-folium` |
| Machine learning | `scikit-learn` (LinearRegression) |
| Dashboard | `streamlit` |
| Notebook | `jupyterlab` |

---

## 🗂️ Project Structure

```
smart-city-mobility/
│
├── app.py                    # Streamlit dashboard (4 views)
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── config.toml           # Theme + server config
│
├── data/
│   └── mobility.csv          # Hourly traffic data · Augsburg & Munich
│
├── notebooks/
│   └── eda.ipynb             # Exploratory Data Analysis
│
├── src/
│   ├── __init__.py
│   ├── model.py              # TrafficPredictor class (sklearn)
│   └── utils.py              # Helpers, constants, congestion labels
│
└── images/
    └── ...                   # Charts exported from EDA
```

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/smart-city-mobility.git
cd smart-city-mobility

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch dashboard
streamlit run app.py

# 5. (Optional) Open EDA notebook
jupyter lab notebooks/eda.ipynb
```

---

## 📱 Dashboard Views

| Tab | Description |
|---|---|
| **Overview** | Hourly traffic profile per city + day type, with peak metrics |
| **City Comparison** | Side-by-side Augsburg vs Munich — volume, congestion index, key ratios |
| **Traffic Prediction** | Linear regression model — predict volume by hour + day of week |
| **Geo Map** | Interactive folium map — station load, circle-size encoding, A8 corridor |

---

## 🤖 Prediction Model

Simple **Linear Regression** on two features:
- `hour` — hour of day (0–23)
- `day_of_week` — 0 (Monday) … 6 (Sunday)

Intentionally transparent for portfolio purposes. Documented extension paths in `src/model.py`:
- `RandomForestRegressor` for non-linear patterns
- Weather features (temperature, precipitation)
- Public holiday flag
- LSTM for sequence-aware forecasting

---

## 🗺️ Geo Coverage

| City | Stations | Corridor |
|---|---|---|
| Augsburg | Hbf, Mitte, Uni, West, Lechhausen | AVV network |
| Munich | Hbf, Marienplatz, Ostbahnhof, Sendlinger Tor, Pasing | MVV / MVG network |
| Inter-city | A8 motorway + S-Bahn rail | ~75 km Augsburg–Munich |

---

## 📈 Potential Extensions

- Integrate **open GTFS data** from AVV / MVV for real stop-level analysis
- Add **bike sharing** and **Park & Ride** datasets
- Build **geo clustering** to identify mobility hotspots
- Deploy on **Streamlit Cloud** for live public access
- Add **OpenStreetMap** routing layer with `osmnx`

---

## 👤 About

Built by **[Your Name]** · Junior Geo Data Analyst  
Focus: Smart Cities · Urban Mobility · Geospatial Analytics  
Stack: Python · SQL · GIS (QGIS, GeoPandas) · Streamlit

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/YOUR_PROFILE)
[![GitHub](https://img.shields.io/badge/GitHub-Portfolio-black?logo=github)](https://github.com/YOUR_USERNAME)

---

*Data is simulated from realistic urban mobility patterns for the Augsburg–Munich corridor. For production use, integrate GTFS feeds from AVV / MVV open data portals.*
