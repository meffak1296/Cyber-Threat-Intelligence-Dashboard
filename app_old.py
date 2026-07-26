import streamlit as st
import pandas as pd

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Cyber Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================================
# Custom CSS
# ==========================================================

st.markdown("""
<style>

.stApp{
    background-color:#0B1120;
}

.title{
    text-align:center;
    font-size:48px;
    font-weight:bold;
    color:#22C55E;
}

.subtitle{
    text-align:center;
    font-size:20px;
    color:white;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# Dashboard Header
# ==========================================================

st.markdown(
    '<div class="title">🛡️ CYBER THREAT INTELLIGENCE DASHBOARD</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Real-Time Network Traffic Monitoring & Threat Detection</div>',
    unsafe_allow_html=True
)

# ==========================================================
# Load Dataset
# ==========================================================

@st.cache_data
def load_data():
    # Dataset ka random sample load hoga
    df = pd.read_csv(
        "cicids2017_cleaned.csv",
        skiprows=lambda x: x > 0 and x % 20 != 0,
        low_memory=True
    )

    return df

df = load_data()

# ==========================================================
# KPI Cards
# ==========================================================

total_records = len(df)
total_features = df.shape[1]
attack_types = df["Attack Type"].nunique()

normal_traffic = 0
if "BENIGN" in df["Attack Type"].values:
    normal_traffic = (df["Attack Type"] == "BENIGN").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("📁 Total Records", f"{total_records:,}")
col2.metric("📊 Total Features", total_features)
col3.metric("🚨 Attack Types", attack_types)
col4.metric("🛡️ Normal Traffic", f"{normal_traffic:,}")

# ==========================================================
# Dataset Preview
# ==========================================================

st.subheader("📋 Dataset Preview")
st.dataframe(df.head())
import plotly.express as px

attack_count = df["Attack Type"].value_counts()

fig = px.bar(
    attack_count,
    x=attack_count.index,
    y=attack_count.values,
    title="Attack Type Distribution"
)

st.plotly_chart(fig, use_container_width=True)