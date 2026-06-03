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
</style>
""", unsafe_allow_html=True)

st.title("D464M4664 HPC VALUE SCANNER")
st.markdown("**Best Value for Money in High Performance Computing**")

if st.button("🔄 SCAN HPC STOCKS NOW"):
    with st.spinner("Scanning HPC stocks..."):
        hpc_tickers = ['NVDA','AMD','TSM','AVGO','MU','ASML','SMCI','ANET','VRT','MRVL',
                       'KLAC','ARM','IREN','WULF','HUT','RIOT','CIFR','CORZ','MARA','CLSK']

        data = []
        progress_bar = st.progress(0)
        
        for i, t in enumerate(hpc_tickers):
            try:
                stock = yf.Ticker(t)
                info = stock.info
                price = info.get('currentPrice') or info.get('regularMarketPrice')
                if not price: 
                    progress_bar.progress((i + 1) / len(hpc_tickers))
                    continue
                
                pe = info.get('forwardPE', np.nan)
                pb = info.get('priceToBook', np.nan)
                target = info.get('targetMeanPrice', np.nan)
                upside = (target - price) / price * 100 if not np.isnan(target) and price else 0
                growth = info.get('earningsGrowth', 0) or 0
                
                pe_score = max(0, (50 - min(pe, 50)) / 50) if not np.isnan(pe) else 0.4
                pb_score = max(0, (10 - min(pb, 10)) / 10) if not np.isnan(pb) else 0.4
                upside_score = min(max(upside / 50, 0), 1)
                growth_score = min(growth * 2, 1)
                
                value_score = round((pe_score*0.3 + pb_score*0.2 + upside_score*0.3 + growth_score*0.2) * 100, 1)
                
                # Recommendation Logic
                if value_score >= 68 and pe > 0 and upside > 8:
                    recommendation = "🟢 BUY"
                elif value_score >= 55:
                    recommendation = "🟡 HOLD"
                else:
                    recommendation = "🔴 SELL / AVOID"
                
                data.append({
                    'Ticker': t,
                    'Price': round(price, 2),
                    'Forward P/E': round(pe, 2) if not np.isnan(pe) else 'N/A',
                    'P/B': round(pb, 2) if not np.isnan(pb) else 'N/A',
                    'Target Upside %': round(upside, 1),
                    'Growth %': round(growth*100, 1),
                    'Value Score': value_score,
                    'Recommendation': recommendation
                })
            except:
                pass
            
            progress_bar.progress((i + 1) / len(hpc_tickers))
        
        if data:
            df = pd.DataFrame(data)
            df = df.sort_values('Value Score', ascending=False)
            
            st.success(f"✅ Scan Complete — {len(df)} HPC stocks")

            # Highlighting: Blue for positive P/E, Red for negative
            def highlight_pe(row):
                styles = [''] * len(row)
                pe_val = row['Forward P/E']
                if isinstance(pe_val, (int, float)):
                    if pe_val < 0:
                        styles[2] = 'background-color: #FF3333; color: white; font-weight: bold;'
                    else:
                        styles[2] = 'background-color: #00A19C; color: white; font-weight: bold;'
                return styles

            styled_df = df.style.apply(highlight_pe, axis=1)
            
            st.dataframe(styled_df, use_container_width=True, height=650)

            st.markdown("### 📌 Metric Descriptions")
            st.markdown("""
            - **Forward P/E**: Blue = Positive (better) | Red = Negative (riskier)  
            - **Value Score**: Higher = Better overall value  
            - **Recommendation**: 🟢 BUY = Strong signals | 🟡 HOLD | 🔴 SELL/AVOID
            """)
            
            csv = df.to_csv(index=False)
            st.download_button("⬇️ Download Report", csv, "d464m4664_hpc_picks.csv")
        else:
            st.error("Could not fetch data. Please try again in a few minutes.")

st.caption("**D464M4664 Principle**: Consistent scanning reveals hidden value over time.")



    
     