import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Mercedes-AMG Value Scanner", layout="wide")

# Mercedes F1 Black + Blue Theme
st.markdown("""
<style>
    .stApp {background-color: #000000; color: #E5E5E5;}
    .stButton>button {
        background-color: #00A19C;
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 14px;
        border-radius: 50px;
        width: 100%;
    }
    h1 {color: #00A19C; text-align: center;}
    .high-value {color: #00FF9F; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.title("🏎️ MERCEDES-AMG VALUE SCANNER")
st.markdown("**Best Value for Money Investments** — HPC • Crypto • Space")

# Sidebar
st.sidebar.header("Race Controls")
category = st.sidebar.selectbox("Select Category", ["All", "HPC/AI", "Crypto", "Space"])
refresh = st.sidebar.button("Refresh Market Data")

# Full Stock Universe
hpc_tickers = ['NVDA','AMD','TSM','AVGO','MU','ASML','AMAT','LRCX','ANET','SMCI','VRT','KLAC','ONTO','ARM','MRVL','CRWD','PLTR','DELL','WDC','STX','ORCL','INTC','ALAB','CRDO']
crypto_tickers = ['COIN','MSTR','RIOT','MARA','HOOD','SQ']
space_tickers = ['RKLB','ASTS','LUNR','PL','KTOS','LDOS','SPCE']
broad = ['AAPL','MSFT','AMZN','META','GOOGL']

all_tickers = list(set(hpc_tickers + crypto_tickers + space_tickers + broad))

def get_value_score(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice') or info.get('regularMarketPrice')
        if not price: return None
        
        pe = info.get('forwardPE', np.nan)
        pb = info.get('priceToBook', np.nan)
        target = info.get('targetMeanPrice', np.nan)
        upside = (target - price) / price * 100 if not np.isnan(target) else 0
        growth = info.get('earningsGrowth', 0) or 0
        debt = info.get('debtToEquity', np.nan)
        
        # Value for Money Score (higher = better value)
        pe_score = max(0, (50 - min(pe, 50)) / 50) if not np.isnan(pe) else 0.4
        pb_score = max(0, (10 - min(pb, 10)) / 10) if not np.isnan(pb) else 0.4
        upside_score = min(max(upside / 50, 0), 1)
        growth_score = min(growth * 2, 1)
        debt_score = max(0, (100 - min(debt or 100, 100))) / 100
        
        value_score = round((pe_score*0.25 + pb_score*0.2 + upside_score*0.25 + growth_score*0.2 + debt_score*0.1) * 100, 1)
        
        return {
            'Ticker': ticker,
            'Price': round(price, 2),
            'Forward P/E': round(pe, 2) if not np.isnan(pe) else 'N/A',
            'P/B': round(pb, 2) if not np.isnan(pb) else 'N/A',
            'Target Upside %': round(upside, 1),
            'Growth %': round(growth*100, 1),
            'Value Score': value_score,
            'Category': 'HPC/AI' if ticker in hpc_tickers else 'Crypto' if ticker in crypto_tickers else 'Space' if ticker in space_tickers else 'Broad'
        }
    except:
        return None

if refresh or st.button("🏁 REFRESH & RANK ALL STOCKS"):
    with st.spinner("Loading real-time value rankings..."):
        data = []
        for t in all_tickers:
            result = get_value_score(t)
            if result:
                data.append(result)
        
        df = pd.DataFrame(data)
        df = df.sort_values('Value Score', ascending=False)
        
        # Filter by category
        if category != "All":
            df = df[df['Category'] == category]
        
        st.success(f"Top Value-for-Money Stocks — Sorted by Score")

        # Top Value Highlights
        st.markdown("### 🏆 Top 10 Best Value for Money")
        st.dataframe(df.head(10)[['Ticker','Price','Forward P/E','Target Upside %','Growth %','Value Score']], 
                    use_container_width=True, height=400)

        # Full Category View
        st.markdown(f"### 📊 All {category if category != 'All' else 'Stocks'} Ranked")
        st.dataframe(df[['Ticker','Category','Price','Forward P/E','Target Upside %','Growth %','Value Score']], 
                    use_container_width=True, height=700)

        csv = df.to_csv(index=False)
        st.download_button("⬇️ Download Full Value Report", csv, "mercedes_value_picks.csv")

st.caption("**Mercedes-AMG Philosophy**: Best value for money compounds like championship points. Higher Value Score = stronger combination of price vs potential. Always verify before investing.")
    
     