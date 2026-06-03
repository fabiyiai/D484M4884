import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Mercedes Intrinsic Velocity", layout="wide", initial_sidebar_state="expanded")

# Mercedes F1 Theme - Black, Silver, Petronas Teal
st.markdown("""
<style>
    .stApp {
        background-color: #0A0A0A;
        color: #E5E5E5;
    }
    .css-1d391kg, .stButton>button {
        background-color: #00A19C; /* Petronas Teal */
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    h1, h2, h3 {
        color: #C8C8C8; /* Silver */
        font-family: 'Arial Black', sans-serif;
    }
    .stDataFrame {background-color: #1A1A1A;}
</style>
""", unsafe_allow_html=True)

st.title("🏎️ Mercedes-AMG Intrinsic Velocity Scanner")
st.markdown("**Silver Arrow Precision**: Scanning for undervalued stocks with true intrinsic speed. Debt resilience • Target upside • Growth catalysts")

# Sidebar
st.sidebar.header("⚙️ Race Controls")
num_stocks = st.sidebar.slider("Scan Depth", 50, 500, 150)
score_threshold = st.sidebar.slider("Minimum Velocity Score", 0.4, 0.9, 0.60, 0.01)

@st.cache_data
def load_tickers():
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
    df =
    