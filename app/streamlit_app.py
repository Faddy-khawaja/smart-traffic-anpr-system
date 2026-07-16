import sqlite3
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
DB_PATH = "database/traffic.db"

st.set_page_config(page_title="Smart City Traffic ANPR Dashboard", layout="wide")


@st.cache_data(ttl=5)
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM vehicle_logs ORDER BY id DESC", conn)
    conn.close()
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


st.title("🚦 Smart City Traffic Monitoring Dashboard")
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

df = load_data()

if df.empty:
    st.warning("No records yet. Run `src/anpr_pipeline.py` on a video first to generate data.")
    st.stop()

# ---------------------------------------------------------
# Live class-wise counts
# ---------------------------------------------------------
st.subheader("Live Vehicle Counts (Class-wise)")

counts = df["vehicle_type"].value_counts()
all_classes = ["car", "motorcycle", "bus", "truck"]
cols = st.columns(len(all_classes))
for col, cls in zip(cols, all_classes):
    col.metric(cls.capitalize(), int(counts.get(cls, 0)))

# ---------------------------------------------------------
# Analytics graphs
# ---------------------------------------------------------
st.subheader("Traffic Analytics")

col1, col2 = st.columns(2)

with col1:
    class_counts_df = df["vehicle_type"].value_counts().reset_index()
    class_counts_df.columns = ["vehicle_type", "count"]
    fig_pie = px.pie(
        class_counts_df, names="vehicle_type", values="count",
        title="Vehicle Type Distribution",
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    df_time = df.copy()
    df_time["minute"] = df_time["timestamp"].dt.floor("min")
    timeline = df_time.groupby(["minute", "vehicle_type"]).size().reset_index(name="count")
    fig_line = px.line(
        timeline, x="minute", y="count", color="vehicle_type",
        title="Vehicles Crossed Over Time", markers=True,
    )
    st.plotly_chart(fig_line, use_container_width=True)

# ---------------------------------------------------------
# Plate recognition success rate
# ---------------------------------------------------------
st.subheader("License Plate Recognition Rate")
recognized = df["plate_number"].notna().sum()
total = len(df)
rate = (recognized / total * 100) if total else 0
st.progress(rate / 100, text=f"{recognized}/{total} plates recognized ({rate:.1f}%)")

# ---------------------------------------------------------
# License plate logs / historical reports
# ---------------------------------------------------------
st.subheader("License Plate Logs")

vehicle_filter = st.multiselect(
    "Filter by vehicle type", options=all_classes, default=all_classes
)
filtered_df = df[df["vehicle_type"].isin(vehicle_filter)]

st.dataframe(
    filtered_df[["id", "vehicle_type", "plate_number", "timestamp"]],
    use_container_width=True,
    hide_index=True,
)

st.download_button(
    "Download logs as CSV",
    data=filtered_df.to_csv(index=False),
    file_name="traffic_logs_export.csv",
    mime="text/csv",
)

if st.button("Refresh data"):
    st.cache_data.clear()
    st.rerun()