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
        background-color: #00A19C;
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
num_stocks = st.sidebar.slider("Scan Depth", 100, 800, 350)
score_threshold = st.sidebar.slider("Minimum Velocity Score", 0.4, 0.9, 0.60, 0.01)

# Full HPC Universe + Other Categories
hpc_tickers = ['NVDA','AMD','TSM','AVGO','MU','ASML','AMAT','LRCX','ANET','SMCI','VRT',
               'KLAC','ONTO','ARM','MRVL','CRWD','PLTR','DELL','WDC','STX','ORCL','INTC',
               'ALAB','CRDO']

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
        eps = info.get('trailingEps', np.nan)
        growth = info.get('earningsGrowth', 0) or 0
        
        debt_score = max(0, 100 - (debt_eq or 100)) / 100
        target_upside = max(0, (target_mean - current_price) / current_price) if not np.isnan(target_mean) else 0
        intrinsic_est = eps * (8.5 + 2 * growth * 100) if eps else current_price
        graham_margin = max(0, (intrinsic_est - current_price) / current_price)
        
        score = (0.35 * debt_score + 0.35 * target_upside + 0.2 * graham_margin + 0.1 * 0.6)
        
        is_deep_undervalued = (score > 0.75 and target_upside > 0.25)
        
        return {
            'Ticker': ticker,
            'Price': round(current_price, 2),
            'Expert Target': round(target_mean, 2) if not np.isnan(target_mean) else 'N/A',
            'Target Upside %': round(target_upside * 100, 1),
            'Debt/Eq': round(debt_eq, 1) if debt_eq else 'N/A',
            'Intrinsic Score': round(score, 3),
            'Growth %': round(growth * 100, 1),
            'Deep Value Alert': '🔴 STRONG BUY - Significantly Undervalued' if is_deep_undervalued else ''
        }
    except:
        return None

# Prominent Scan Button
if st.button("🏁 SCAN THE TRACK NOW"):
    with st.spinner("Pushing for Pole Position..."):
        results = []
        progress = st.progress(0)
        
        for i, t in enumerate(tickers):
            data = get_intrinsic_score(t)
            if data and data['Intrinsic Score'] > score_threshold:
                if sector == "All" or \
                   (sector == "HPC/AI" and t in hpc_tickers) or \
                   (sector == "Crypto" and t in crypto_tickers) or \
                   (sector == "Space" and t in space_tickers):
                    results.append(data)
            progress.progress((i + 1) / len(tickers))
        
        if results:
            df = pd.DataFrame(results)
            df = df.sort_values('Intrinsic Score', ascending=False)
            
            st.success(f"🏆 {len(df)} High-Velocity Opportunities Found")
            
            # Red Alerts Section
            alerts = df[df['Deep Value Alert'] != '']
            if not alerts.empty:
                st.markdown("### 🔴 RED ALERT — Deep Value Signals")
                st.dataframe(alerts[['Ticker','Price','Expert Target','Target Upside %','Intrinsic Score','Deep Value Alert']], 
                           use_container_width=True)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                fig = px.bar(df.head(15), x='Ticker', y='Target Upside %', 
                            color='Intrinsic Score', color_continuous_scale=['#C8C8C8', '#00A19C'],
                            title="🚀 Expert Growth Potential")
                fig.update_layout(template="plotly_dark", plot_bgcolor="#111111")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                top = df.iloc[0]
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=top['Intrinsic Score'] * 100,
                    title={'text': f"Top Pick: {top['Ticker']}"},
                    gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#00A19C"}}))
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            st.dataframe(df.head(30), use_container_width=True, height=700)
            
            csv = df.to_csv(index=False)
            st.download_button("⬇️ Download Full Pit Report", csv, "mercedes_intrinsic_picks.csv")
        else:
            st.warning("No cars qualified this session. Lower threshold.")

st.caption("**Mercedes-AMG Wisdom**: The mycelium of HPC powers the future. Red alerts reveal hidden intrinsic value. Scan consistently, invest with discipline. Correlation ≠ causation.")

    