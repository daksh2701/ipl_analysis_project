import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------------
# Page config
# ------------------------------------------------
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

# ------------------------------------------------
# Load data
# ------------------------------------------------
@st.cache_data
def load_data():
    matches = pd.read_csv("matches (2).csv")
    deliveries = pd.read_csv("deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

if "date" in matches.columns:
    matches["date"] = pd.to_datetime(matches["date"])

st.title("🏏 IPL Analytics Dashboard")

st.markdown(
    """
Simple IPL dashboard using match and ball-by-ball data.  
Use this as a base and extend it with more charts later.
"""
)

tab1, tab2 = st.tabs(["Overview", "Sample Analysis"])

# -------- Overview tab --------
with tab1:
    st.subheader("Dataset Snapshot")

    col1, col2, col3 = st.columns(3)
    col1.metric("Matches rows", len(matches))
    col2.metric("Deliveries rows", len(deliveries))
    col3.metric("Seasons", matches["season"].nunique() if "season" in matches.columns else 0)

    st.write("Matches head:")
    st.dataframe(matches.head())

    st.write("Deliveries head:")
    st.dataframe(deliveries.head())

# -------- Sample Analysis tab --------
with tab2:
    st.subheader("Matches per Season")

    if "season" in matches.columns:
        matches_per_season = matches.groupby("season")["id"].count().reset_index()
        matches_per_season.columns = ["season", "matches"]

        fig = px.bar(
            matches_per_season,
            x="season",
            y="matches",
            title="Number of matches per season",
            text="matches"
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Column 'season' not found in matches dataset.")
