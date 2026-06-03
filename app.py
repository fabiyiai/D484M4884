import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="🌌 Intrinsic Mycelium Scanner", layout="wide")
st.title("🌌 Intrinsic Value Stock Scanner")
st.markdown("**Mycelium beneath market soil**: Debt health, forward targets, catalysts & intrinsic estimates.")

# Sidebar
st.sidebar.header("Filters")
num_stocks = st.sidebar.slider("Scan Top Stocks", 50, 500, 100)
score_threshold = st.sidebar.slider("Intrinsic Score Threshold", 0.5, 0.9, 0.65)

@st.cache_data
def load_tickers():
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
    df = pd.read_csv(url)
    return df['Symbol'].tolist()[:num_stocks]

tickers = load_tickers()

def get_intrinsic_score(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        if not current_price: return None
        
        target_mean = info.get('targetMeanPrice', np.nan)
        debt_eq = info.get('debtToEquity', np.nan)
        pb = info.get('priceToBook', np.nan)
        eps = info.get('trailingEps', np.nan)
        growth = info.get('earningsGrowth', 0) or 0
        
        debt_score = max(0, 100 - (debt_eq or 100)) / 100
        target_upside = max(0, (target_mean - current_price) / current_price) if not np.isnan(target_mean) else 0
        
        intrinsic_est = eps * (8.5 + 2 * growth * 100) if eps else current_price
        graham_margin = max(0, (intrinsic_est - current_price) / current_price)
        
        news_score = 0.6
        score = (0.35 * debt_score + 0.3 * target_upside + 0.25 * graham_margin + 0.1 * news_score)
        
        return {
            'Ticker': ticker,
            'Price': round(current_price, 2),
            'Target Upside %': round(target_upside * 100, 1),
            'Debt/Eq': round(debt_eq, 1) if debt_eq else 'N/A',
            'P/B': round(pb, 2),
            'Intrinsic Score': round(score, 3),
        }
    except:
        return None

if st.button("Scan Market Now"):
    with st.spinner("Scanning..."):
        results = []
        for t in tickers:
            data = get_intrinsic_score(t)
            if data and data['Intrinsic Score'] > score_threshold:
                results.append(data)
        df = pd.DataFrame(results)
        df = df.sort_values('Intrinsic Score', ascending=False)
        
        st.dataframe(df.head(20))
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "undervalued_stocks.csv")

st.caption("Your Intrinsic Value Dashboard - Powered by true metrics")