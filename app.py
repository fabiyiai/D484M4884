import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Mercedes Intrinsic Velocity", layout="wide", initial_sidebar_state="expanded")

# Mercedes F1 Dark Theme
st.markdown("""
<style>
    .stApp {background-color: #0A0A0A; color: #E5E5E5;}
    .stButton>button {background-color: #00A19C; color: white; font-weight: bold;}
    h1, h2 {color: #C8C8C8; font-family: 'Arial Black', sans-serif;}
</style>
""", unsafe_allow_html=True)

st.title("🏎️ Mercedes-AMG Intrinsic Velocity Scanner")
st.markdown("**Silver Arrow Precision**: HPC • Crypto • Space • True Intrinsic Value with Expert Targets")

# Sidebar
st.sidebar.header("⚙️ Race Controls")
sector = st.sidebar.selectbox("Focus Sector", ["All", "HPC/AI", "Crypto", "Space", "Broad Market"])
num_stocks = st.sidebar.slider("Scan Depth", 100, 600, 250)
score_threshold = st.sidebar.slider("Minimum Velocity Score", 0.4, 0.9, 0.60, 0.01)

# Expanded Ticker Universe
base_tickers = ['AAPL','MSFT','GOOGL','AMZN','META','NVDA','AMD','TSM','AVGO','MU','ASML','AMAT','LRCX']  # HPC
crypto_tickers = ['COIN','MSTR','RIOT','MARA','HOOD','SQ']
space_tickers = ['RKLB','ASTS','LUNR','PL','KTOS','LDOS']

all_tickers = list(set(base_tickers + crypto_tickers + space_tickers + 
                      ['JPM','XOM','JNJ','DIS','NFLX']))  # Broader mix

@st.cache_data
def load_tickers():
    return all_tickers
    