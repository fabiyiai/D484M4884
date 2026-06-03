import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Mercedes-AMG Intrinsic Velocity", layout="wide", initial_sidebar_state="expanded")

# Strong Mercedes F1 Black + Petronas Blue Theme
st.markdown("""
<style>
    .stApp {
        background-color: #000000;
        color: #E5E5E5;
    }
    .stButton>button {
        background-color: #00A19C; /* Petronas Blue */
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 12px 30px;
        border-radius: 50px;
        width: 100%;
    }
    h1 {
        color: #00A19C;
        font-family: 'Arial Black', sans-serif;
        text-align: center;
    }
    .stDataFrame {background-color: #111111;}
</style>
""", unsafe_allow_html=True)

st.title("🏎️ MERCEDES-AMG INTRINSIC VELOCITY SCANNER")
st.markdown("**Silver Arrows in the Market** — HPC • Crypto • Space • Expert Price Targets")

# Sidebar
st.sidebar.header("⚙️ Race Controls")
sector = st.sidebar.selectbox("Focus Sector", ["All", "HPC/AI", "Crypto", "Space"])
num_stocks = st.sidebar.slider("Scan Depth", 100, 600, 250)
score_threshold = st.sidebar.slider("Minimum Velocity Score", 0.4, 0.9,

    