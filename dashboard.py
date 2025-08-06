import streamlit as st
import pandas as pd
import ast
import re
from datetime import datetime

LOG_FILE = "api_requests.log"

st.title("Threat Detection Dashboard")
st.markdown("Real-time Monitoring of Predictions from FastAPI Service")

def parse_log_line(line):
    try:
        timestamp_match = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})", line)
        ip_match = re.search(r"IP:\s([\d\.]+)", line)
        input_match = re.search(r"Input:\s(\[.*?\])", line)
        prediction_match = re.search(r"Prediction:\s(\w+)", line)

        if timestamp_match and ip_match and input_match and prediction_match:
            timestamp = datetime.strptime(timestamp_match.group(1), "%Y-%m-%d %H:%M:%S,%f")
            ip = ip_match.group(1)
            features = ast.literal_eval(input_match.group(1))
            prediction = prediction_match.group(1)
            return {
                "timestamp": timestamp,
                "ip": ip,
                "prediction": prediction,
                "features": features
            }
    except Exception as e:
        st.error(f"Parsing error: {e}")
    return None

@st.cache_data(ttl=5)
def load_logs():
    data = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            parsed = parse_log_line(line.strip())
            if parsed:
                data.append(parsed)
    return pd.DataFrame(data)

df = load_logs()

if not df.empty:
    # Show prediction summary
    st.subheader("Prediction Summary")
    st.dataframe(df["prediction"].value_counts().rename_axis("Prediction").reset_index(name="Count"))

    # Show recent logs
    st.subheader("Recent Predictions")
    st.dataframe(df.sort_values("timestamp", ascending=False).head(10))

    # Line chart of prediction counts over time
    df['minute'] = df['timestamp'].dt.floor("min")
    summary = df.groupby(['minute', 'prediction']).size().unstack().fillna(0)
    st.subheader("Predictions Over Time")
    st.line_chart(summary)
else:
    st.warning("No data found in log file yet.")

st.caption("Dashboard updates every 5 seconds. Press 'R' to refresh.")
