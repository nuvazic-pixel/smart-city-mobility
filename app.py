"""
Smart City Mobility Dashboard
Augsburg vs Munich — Urban Traffic Analysis
Self-contained version (no src/ imports needed)
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="Smart City Mobility · Augsburg & Munich",
    page_icon="🚊",
    layout="wide",
)

CITY_COLORS = {"Augsburg": "#185FA5", "Munich": "#993556"}
CITY_MAX_VOLUMES = {"Augsburg": 280, "Munich": 580}
DAY_NAMES = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def get_congestion_label(volume, city):
    pct = volume / CITY_MAX_VOLUMES.get(city, 500)
    if pct >= 0.80: return "🔴 Severe"
    elif pct >= 0.60: return "🟠 High"
    elif pct >= 0.40: return "🟡 Moderate"
    elif pct >= 0.20: return "🟢 Low"
    else: return "⚪ Free flow"

def get_peak_hour(hourly_df):
    return int(hourly_df.loc[hourly_df["traffic_volume"].idxmax(), "hour"])

def get_peak_ratio(hourly_df):
    mx = hourly_df["traffic_volume"].max()
    mn = hourly_df["traffic_volume"].min()
    return round(mx / mn, 1) if mn > 0 else 0.0

@st.cache_data
def load_data():
    return pd.read_csv("data/mobility.csv")

df = load_data()

st.sidebar.title("🚊 Mobility Dashboard")
st.sidebar.markdown("Urban traffic analysis for **Augsburg** and **Munich**.")
st.sidebar.divider()
tab = st.sidebar.radio(
    "View",
    ["Overview", "City Comparison", "Traffic Prediction", "Geo Map"],
    label_visibility="collapsed",
)
st.sidebar.divider()
st.sidebar.caption("Data: simulated from realistic urban mobility patterns · AVV/MVV corridor")

if tab == "Overview":
    st.title("📊 Traffic Overview")
    col1, col2 = st.columns(2)
    city = col1.selectbox("City", ["Augsburg", "Munich"])
    day_type = col2.selectbox("Day type", ["weekday", "weekend"])

    filtered = df[(df["city"] == city) & (df["day_type"] == day_type)]
    hourly = filtered.groupby("hour")["traffic_volume"].mean().reset_index()

    peak_hour = get_peak_hour(hourly)
    peak_vol = int(hourly["traffic_volume"].max())
    avg_vol = int(hourly["traffic_volume"].mean())
    ratio = get_peak_ratio(hourly)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Peak hour", f"{peak_hour:02d}:00")
    m2.metric("Peak volume", f"{peak_vol} veh/h")
    m3.metric("Daily average", f"{avg_vol} veh/h")
    m4.metric("Peak/off ratio", f"{ratio:.1f}×")

    st.markdown("#### Hourly traffic volume")
    colors = ["#EF9F27" if v >= 0.75 * peak_vol else CITY_COLORS[city] for v in hourly["traffic_volume"]]
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.bar(hourly["hour"], hourly["traffic_volume"], color=colors, width=0.7, edgecolor="none")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Vehicles / hour")
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(0, 24, 2)], rotation=45)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_facecolor("none")
    fig.patch.set_alpha(0)
    st.pyplot(fig, use_container_width=True)

    am_peak = hourly[hourly["hour"].between(7, 9)]["traffic_volume"].mean()
    pm_peak = hourly[hourly["hour"].between(16, 18)]["traffic_volume"].mean()
    pm_diff = int(((pm_peak - am_peak) / am_peak) * 100)
    st.info(
        f"**Insight · {city} {day_type}s** — Peak at **{peak_hour:02d}:00** ({peak_vol} veh/h). "
        f"PM peak is **{abs(pm_diff)}% {'higher' if pm_diff > 0 else 'lower'}** than AM peak. "
        f"Peak/off ratio of {ratio:.1f}× indicates "
        f"{'strong commuter dependency.' if ratio > 3.5 else 'relatively balanced daily demand.'}"
    )

elif tab == "City Comparison":
    st.title("🏙️ City Comparison")
    day_type = st.radio("Day type", ["weekday", "weekend"], horizontal=True)

    aug_hourly = df[(df["city"] == "Augsburg") & (df["day_type"] == day_type)].groupby("hour")["traffic_volume"].mean()
    muc_hourly = df[(df["city"] == "Munich") & (df["day_type"] == day_type)].groupby("hour")["traffic_volume"].mean()
    comparison = pd.DataFrame({"Augsburg": aug_hourly, "Munich": muc_hourly})

    st.markdown("#### Hourly traffic — Augsburg vs Munich")
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.plot(comparison.index, comparison["Augsburg"], color=CITY_COLORS["Augsburg"], linewidth=2.5, label="Augsburg", marker="o", markersize=3)
    ax.plot(comparison.index, comparison["Munich"], color=CITY_COLORS["Munich"], linewidth=2.5, label="Munich", marker="o", markersize=3)
    ax.fill_between(comparison.index, comparison["Augsburg"], alpha=0.12, color=CITY_COLORS["Augsburg"])
    ax.fill_between(comparison.index, comparison["Munich"], alpha=0.12, color=CITY_COLORS["Munich"])
    ax.set_xlabel("Hour")
    ax.set_ylabel("Vehicles / hour")
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(0, 24, 2)], rotation=45)
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_facecolor("none")
    fig.patch.set_alpha(0)
    st.pyplot(fig, use_container_width=True)

    aug_peak = int(aug_hourly.max())
    muc_peak = int(muc_hourly.max())
    ratio = round(muc_peak / aug_peak, 1)
    c1, c2, c3 = st.columns(3)
    c1.metric("Munich / Augsburg peak ratio", f"{ratio}×")
    c2.metric("Augsburg peak hour", f"{aug_hourly.idxmax():02d}:00", f"{aug_peak} veh/h")
    c3.metric("Munich peak hour", f"{muc_hourly.idxmax():02d}:00", f"{muc_peak} veh/h")
    st.info(
        f"**Key finding** — Munich generates **{ratio}× more traffic** at peak on {day_type}s. "
        + ("Weekend demand softer — Augsburg drops ~20% vs Munich ~40%." if day_type == "weekend"
           else "Munich's PM peak (17:00) exceeds AM peak, driven by larger commuter catchment area.")
    )

elif tab == "Traffic Prediction":
    st.title("🤖 Traffic Prediction")
    st.caption("Linear regression model trained on hourly + day-of-week patterns.")

    @st.cache_resource
    def train_models(data):
        models = {}
        for city, group in data.groupby("city"):
            X = group[["hour", "day_of_week"]].values
            y = group["traffic_volume"].values
            m = LinearRegression()
            m.fit(X, y)
            models[city] = m
        return models

    models = train_models(df)

    col1, col2 = st.columns(2)
    hour = col1.slider("Hour of day", 0, 23, 8)
    day = col2.slider("Day of week  (0=Mon … 6=Sun)", 0, 6, 1)

    aug_pred = max(0, int(round(models["Augsburg"].predict([[hour, day]])[0])))
    muc_pred = max(0, int(round(models["Munich"].predict([[hour, day]])[0])))

    st.markdown(f"##### Prediction for **{DAY_NAMES[day]}** at **{hour:02d}:00**")
    c1, c2 = st.columns(2)
    c1.metric("Augsburg", f"{aug_pred} veh/h", get_congestion_label(aug_pred, "Augsburg"))
    c2.metric("Munich", f"{muc_pred} veh/h", get_congestion_label(muc_pred, "Munich"))

    hours = list(range(24))
    aug_all = [max(0, int(round(models["Augsburg"].predict([[h, day]])[0]))) for h in hours]
    muc_all = [max(0, int(round(models["Munich"].predict([[h, day]])[0]))) for h in hours]

    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.plot(hours, aug_all, color=CITY_COLORS["Augsburg"], linewidth=2, label="Augsburg")
    ax.plot(hours, muc_all, color=CITY_COLORS["Munich"], linewidth=2, label="Munich")
    ax.axvline(x=hour, color="#EF9F27", linewidth=1.5, linestyle="--", label="Selected hour")
    ax.fill_between(hours, aug_all, alpha=0.1, color=CITY_COLORS["Augsburg"])
    ax.fill_between(hours, muc_all, alpha=0.1, color=CITY_COLORS["Munich"])
    ax.set_xlabel("Hour")
    ax.set_ylabel("Predicted vehicles / hour")
    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(0, 24, 2)], rotation=45)
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_facecolor("none")
    fig.patch.set_alpha(0)
    st.pyplot(fig, use_container_width=True)

    st.info(
        f"**{DAY_NAMES[day]} {hour:02d}:00** — "
        f"{'Weekend: smoother demand. ' if day >= 5 else 'Workday pattern. '}"
        f"Gap between cities: **{abs(aug_pred - muc_pred)} veh/h**."
    )

elif tab == "Geo Map":
    st.title("🗺️ Geo Map — Station Traffic Load")

    col1, col2 = st.columns(2)
    city_filter = col1.selectbox("Show", ["Both cities", "Augsburg", "Munich"])
    map_hour = col2.selectbox("Time", [7, 8, 12, 17, 19, 22], index=1, format_func=lambda h: f"{h:02d}:00")
    day_type = st.radio("Day type", ["weekday", "weekend"], horizontal=True)

    filtered = df[(df["hour"] == map_hour) & (df["day_type"] == day_type)]
    if city_filter != "Both cities":
        filtered = filtered[filtered["city"] == city_filter]

    m = folium.Map(location=[48.25, 11.22], zoom_start=9, tiles="CartoDB positron")

    for _, row in filtered.iterrows():
        load = row["traffic_volume"] / CITY_MAX_VOLUMES[row["city"]]
        color = "#E24B4A" if load > 0.75 else "#EF9F27" if load > 0.5 else CITY_COLORS[row["city"]]
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=5 + load * 12,
            color=color, fill=True, fill_color=color, fill_opacity=0.75,
            popup=folium.Popup(
                f"<b>{row['station']}</b><br>City: {row['city']}<br>"
                f"Traffic: {row['traffic_volume']} veh/h<br>Load: {int(load*100)}%<br>"
                f"Status: {get_congestion_label(row['traffic_volume'], row['city'])}",
                max_width=200,
            ),
            tooltip=f"{row['station']} · {row['traffic_volume']} veh/h",
        ).add_to(m)

    folium.PolyLine(
        locations=[[48.3656, 10.8854], [48.1402, 11.5597]],
        color="#888", weight=2, dash_array="8 6", opacity=0.5,
        tooltip="A8/Rail corridor Augsburg–Munich (~75 km)",
    ).add_to(m)

    st_folium(m, height=480, use_container_width=True)
    st.info(
        f"**{map_hour:02d}:00 · {day_type}** — Circle size encodes traffic load. "
        "Red = >75% capacity. The A8/rail corridor (dashed) is the primary regional mobility axis."
    )