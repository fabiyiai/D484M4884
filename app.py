import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="D484M4884 Value Scanner", layout="wide")

# Deep Black + Petronas Blue Theme
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
    .stSidebar {background-color: #111111;}
</style>
""", unsafe_allow_html=True)

st.title("D484M4884 VALUE SCANNER")
st.markdown("**Best Value for Money** — Categorized by Industry")

# Sidebar (Black)
st.sidebar.header("Controls")
category = st.sidebar.selectbox("Select Industry/Category", 
    ["All", "HPC/AI", "Crypto", "Space", "Technology", "Healthcare", "Finance", "Energy", "Consumer"])
refresh = st.sidebar.button("Refresh Market Data")

# Load S&P 500 + Focused Tickers
@st.cache_data
def load_all_tickers():
    # S&P 500
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
    df = pd.read_csv(url)
    sp500 = df['Symbol'].tolist()
    
    # Add focused high-interest
    extra = ['RKLB','ASTS','LUNR','COIN','MSTR','RIOT','MARA']
    return list(set(sp500 + extra))

all_tickers = load_all_tickers()

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
        sector = info.get('sector', 'Other')
        
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
            'Industry': sector
        }
    except:
        return None

if refresh or st.button("🔄 REFRESH & RANK ALL STOCKS"):
    with st.spinner("Scanning market mycelium..."):
        data = []
        for t in all_tickers[:400]:   # Limit for speed
            result = get_value_score(t)
            if result:
                data.append(result)
        
        df = pd.DataFrame(data)
        df = df.sort_values('Value Score', ascending=False)
        
        if category != "All":
            df = df[df['Industry'].str.contains(category, case=False, na=False)]
        
        st.success(f"**D484M4884 Value Rankings** — {category if category != 'All' else 'All Industries'}")

        st.markdown("### 🏆 Top 10 Best Value for Money")
        st.dataframe(df.head(10), use_container_width=True, height=400)

        st.markdown("### 📊 Full Ranked List")
        st.dataframe(df, use_container_width=True, height=700)

        st.markdown("### 📌 Metric Descriptions")
        st.markdown("""
        - **Value Score**: Higher = better value for money (valuation + growth + upside).
        - **Forward P/E**: Lower usually = better value.
        - **Target Upside %**: Analyst expected growth.
        """)

        csv = df.to_csv(index=False)
        st.download_button("⬇️ Download Full Report", csv, "d484m4884_value_picks.csv")

st.caption("**D484M4884 Principle**: True value grows beneath the surface. Scan regularly with a growth mindset.")

    
     