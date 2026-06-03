import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="D464M4664 HPC Scanner", layout="wide")

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

st.title("D464M4664 HPC VALUE SCANNER")
st.markdown("**Best Value for Money in High Performance Computing** — Blue = Strong Buy Signal")

if st.button("🔄 SCAN HPC STOCKS NOW"):
    with st.spinner("Fetching HPC data..."):
        hpc_tickers = [
            'NVDA','AMD','TSM','AVGO','MU','ASML','SMCI','ANET','VRT','MRVL','KLAC','ARM',
            'IREN','WULF','HUT','RIOT','CIFR','CORZ','MARA','CLSK','BTDR','HIVE','BTBT'
        ]

        data = []
        progress_bar = st.progress(0)
        
        for i, t in enumerate(hpc_tickers):
            try:
                stock = yf.Ticker(t)
                info = stock.info
                price = info.get('currentPrice') or info.get('regularMarketPrice')
                if not price: continue
                
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

            # Fixed Mercedes Blue Highlight for Value Score >= 75
            def highlight_blue(row):
                if row['Value Score'] >= 75:
                    return ['background-color: #00A19C; color: white; font-weight: bold'] * len(row)
                return [''] * len(row)

            styled_df = df.style.apply(highlight_blue, axis=1)
            
            st.dataframe(styled_df, use_container_width=True, height=700)

            # Metric Descriptions
            st.markdown("### 📌 Metric Descriptions")
            st.markdown("""
            - **Price**: Current market price per share  
            - **Forward P/E**: Expected price-to-earnings ratio. Lower = better value  
            - **P/B**: Price-to-Book ratio. Lower = better value  
            - **Target Upside %**: Analyst expected price increase  
            - **Growth %**: Expected earnings growth rate  
            - **Value Score**: Overall score (0-100). **Blue highlight = Strong Buy Signal** (≥75)
            """)
            
            csv = df.to_csv(index=False)
            st.download_button("⬇️ Download HPC Report", csv, "d464m4664_hpc_picks.csv")
        else:
            st.warning("No data received. Try again in a few minutes.")

st.caption("**D464M4664 Principle**: Blue highlights show timely value in the HPC universe.")




    
     