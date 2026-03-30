import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

# Configure page settings
st.set_page_config(page_title="Distributed Log Dashboard", layout="wide")

# Custom CSS for white UI and visible headings
st.markdown("""
<style>
.stApp {
    background-color: white;
}

/* Force Streamlit headings to be visible */
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    color: #003366 !important;
    opacity: 1 !important;
    font-weight: bold !important;
}

/* Metric card style */
.metric-card {
    background: linear-gradient(135deg, #42a5f5, #26c6da);
    color: white;
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

# Dashboard title
st.title("Distributed Log Aggregation Dashboard")
st.subheader("Real-Time Monitoring of Encrypted Logs")

logs = []

# Read logs from JSON file
try:
    with open("logs.json", "r") as f:
        for line in f:
            try:
                logs.append(json.loads(line))
            except:
                continue
except:
    st.warning("No logs found yet")

if logs:
    # Convert logs to dataframe
    df = pd.DataFrame(logs)

    # Convert UNIX timestamp to readable datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    # Dashboard summary
    st.header("Dashboard Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"<div class='metric-card'>Total Logs<br>{len(df)}</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"<div class='metric-card'>Log Levels<br>{df['level'].nunique()}</div>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"<div class='metric-card'>Machines<br>{df['machine_ip'].nunique()}</div>",
            unsafe_allow_html=True
        )

    # Display all logs
    st.header("Complete Log Stream")
    st.dataframe(df, use_container_width=True, height=300)

    # Log level distribution
    st.header("Log Level Distribution")
    st.bar_chart(df["level"].value_counts())

    # Logs over time
    st.header("Logs Generated Over Time")
    time_series = df.groupby(df["timestamp"].dt.second).size()
    st.line_chart(time_series)

    # Filter logs section
    st.header("Filter Logs by Severity")
    selected_level = st.selectbox("Choose Log Level", df["level"].unique())
    filtered_logs = df[df["level"] == selected_level]
    st.dataframe(filtered_logs, use_container_width=True)

    # Error vs normal trend
    st.header("Error vs Normal Trend")

    error_levels = ["ERROR", "CRITICAL", "ALERT", "EMERGENCY"]

    # Create log type column
    df["type"] = df["level"].apply(
        lambda x: "Error" if x in error_levels else "Normal"
    )

    # Round timestamps to nearest second
    df["time_sec"] = df["timestamp"].dt.floor("s")

    # Group logs by time and type
    grouped = df.groupby(["time_sec", "type"]).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(10, 4))

    # Plot error logs
    if "Error" in grouped.columns:
        ax.plot(grouped.index, grouped["Error"], linewidth=2)

    # Plot normal logs
    if "Normal" in grouped.columns:
        ax.plot(grouped.index, grouped["Normal"], linewidth=2)

    ax.set_title("Error vs Normal Logs")
    ax.set_xlabel("Time")
    ax.set_ylabel("Log Count")
    ax.grid(True)

    st.pyplot(fig)

else:
    st.warning("No logs to display yet")