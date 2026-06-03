import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="D484M4884 HPC Scanner", layout="wide")

# Deep Black + Blue Theme
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

st.title("D484M4884 HPC VALUE SCANNER")
st.markdown("**Best Value for Money in High Performance Computing** (AI + Compute Infrastructure + Miners)")

# Sidebar
st.sidebar.header("Controls")
num_stocks = st.sidebar.slider("Scan Size", 20, 120, 60)

if st.button("🔄 SCAN HPC STOCKS NOW"):
    with st.spinner("Fetching HPC & Compute data..."):
        # Combined HPC + Miners from your image
        hpc_tickers = [
            'NVDA','AMD','TSM','AVGO','MU','ASML','SMCI','ANET','VRT','MRVL','KLAC','ARM',
            'IREN','WULF','HUT','RIOT','CIFR','CORZ','MARA','CLSK','BTDR','HIVE','BTBT'
        ]

        data = []
        progress_bar = st.progress(0)
        
        for i, t in enumerate(hpc_tickers[:num_stocks]):
            try:
                stock = yf.Ticker(t)
                info = stock.info
                price = info.get('currentPrice') or info.get('regularMarketPrice')
                if not price:
                    continue
                
                pe = info.get('forwardPE', np.nan)
                pb = info.get('priceToBook', np.nan)
                target = info.get('targetMeanPrice', np.nan)
                upside = (target - price) / price * 100 if not np.isnan(target) and price else 0
                growth = info.get('earningsGrowth', 0) or 0
                debt = info.get('debtToEquity', np.nan)
                
                pe_score = max(0, (50 - min(pe, 50)) / 50) if not np.isnan(pe) else 0.4
                pb_score = max(0, (10 - min(pb, 10)) / 10) if not np.isnan(pb) else 0.4
                upside_score = min(max(upside / 50, 0), 1)
                growth_score = min(growth * 2, 1)
                debt_score = max(0, (100 - min(debt or 100, 100))) / 100
                
                value_score = round((pe_score*0.25 + pb_score*0.2 + upside_score*0.25 + growth_score*0.2 + debt_score*0.1) * 100, 1)
                
                data.append({
                    'Ticker': t,
                    'Price': round(price, 2),
                    'Forward P/E': round(pe, 2) if not np.isnan(pe) else 'N/A',
                    'P/B': round(pb, 2) if not np.isnan(pb) else 'N/A',
                    'Target Upside %': round(upside, 1),
                    'Growth %': round(growth*100, 1),
                    'Value Score': value_score
                })
            except:
                pass
            
            progress_bar.progress((i + 1) / len(hpc_tickers))
        
        if data:
            df = pd.DataFrame(data)
            df = df.sort_values('Value Score', ascending=False)
            
            st.success(f"✅ HPC Scan Complete — {len(df)} stocks")
            
            st.markdown("### 🏆 Top Value HPC Stocks")
            st.dataframe(df.head(15), use_container_width=True)
            
            st.markdown("### 📊 Full HPC List")
            st.dataframe(df, use_container_width=True, height=600)
            
            csv = df.to_csv(index=False)
            st.download_button("⬇️ Download HPC Report", csv, "d484m4884_hpc_picks.csv")
        else:
            st.warning("No data received. Try again in a few minutes.")

st.caption("**D484M4884 Focus**: High Performance Computing & Compute Infrastructure. Higher Value Score = better value for money.")




    
     