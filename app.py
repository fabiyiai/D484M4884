import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Mercedes-AMG Intrinsic Velocity", layout="wide", initial_sidebar_state="expanded")

# Deep Black + Petronas Blue Mercedes F1 Theme
st.markdown("""
<style>
    .stApp {background-color: #000000; color: #E5E5E5;}
    .stButton>button {
        background-color: #00A19C; /* Petronas Blue */
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 14px 40px;
        border-radius: 50px;
        width: 100%;
    }
    h1 {color: #00A19C; text-align: center; font-family: 'Arial Black', sans-serif;}
    .stDataFrame {background-color: #111111;}
    .red-alert {color: #FF0000; font-weight: bold; font-size: 18px;}
</style>
""", unsafe_allow_html=True)

st.title("🏎️ MERCEDES-AMG INTRINSIC VELOCITY SCANNER")
st.markdown("**Silver Arrows Precision** — HPC • Crypto • Space • Expert Targets")

# Sidebar
st.sidebar.header("⚙️ Race Controls")
sector = st.sidebar.selectbox("Focus Sector", ["All", "HPC/AI", "Crypto", "Space"])
num_stocks = st.sidebar.slider("Scan Depth", 100, 800, 300)
score_threshold = st.sidebar.slider("Minimum Velocity Score", 0.4, 0.9, 0.60, 0.01)

# Expanded Tickers
hpc_tickers = ['NVDA','AMD','TSM','AVGO','MU','ASML','AMAT','LRCX','ANET','SMCI','VRT','KLAC','ONTO','ARM','MRVL','CRWD','PLTR','DELL','WDC','STX','ORCL']
crypto_tickers = ['COIN','MSTR','RIOT','MARA','HOOD','SQ']
space_tickers = ['RKLB','ASTS','LUNR','PL','KTOS','LDOS','SPCE']

all_tickers = list(set(hpc_tickers + crypto_tickers + space_tickers + ['AAPL','MSFT','AMZN','META','GOOGL']))

@st.cache_data
def load_tickers():
    return all_tickers[:num_stocks]

tickers = load_tickers()

def get_intrinsic_score(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        if not current_price: return None
        
        target_mean = info.get('targetMeanPrice', np.nan)
        debt_eq = info.get('debtToEquity', np.nan)
        eps = info.get('trailingEps', np.nan

    