"""
Shared utilities for the Smart City Mobility project.
"""

CITY_COLORS = {
    "Augsburg": "#185FA5",
    "Munich": "#993556",
}

CITY_MAX_VOLUMES = {
    "Augsburg": 280,
    "Munich": 580,
}

DAY_NAMES = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday",
]


def get_peak_hour(hourly_df) -> int:
    """Return the hour with maximum traffic volume."""
    return int(hourly_df.loc[hourly_df["traffic_volume"].idxmax(), "hour"])


def get_peak_ratio(hourly_df) -> float:
    """Return the ratio of peak to minimum traffic volume."""
    max_vol = hourly_df["traffic_volume"].max()
    min_vol = hourly_df["traffic_volume"].min()
    if min_vol == 0:
        return 0.0
    return round(max_vol / min_vol, 1)


def get_congestion_label(volume: float, city: str) -> str:
    """Convert raw volume to a human-readable congestion label."""
    max_vol = CITY_MAX_VOLUMES.get(city, 500)
    pct = volume / max_vol
    if pct >= 0.80:
        return "🔴 Severe"
    elif pct >= 0.60:
        return "🟠 High"
    elif pct >= 0.40:
        return "🟡 Moderate"
    elif pct >= 0.20:
        return "🟢 Low"
    else:
        return "⚪ Free flow"


def congestion_pct(volume: float, city: str) -> int:
    """Return congestion as a percentage of max capacity."""
    max_vol = CITY_MAX_VOLUMES.get(city, 500)
    return round((volume / max_vol) * 100)
