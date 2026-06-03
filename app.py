import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Mercedes Intrinsic Velocity", layout="wide", initial_sidebar_state="expanded")

# Mercedes F1 Theme - Black, Silver, Petronas Teal
st.markdown("""
<style>
    .stApp {
        background-color: #0A0A0A;
        color: #E5E5E5;
    }
    .css-1d391kg, .stButton>button {
        background-color: #00A19C; /* Petronas Teal */
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    h1, h2, h3 {
        color: #C8C8C8; /* Silver */
        font-family: 'Arial Black', sans-serif;
    }
    .stDataFrame {background-color: #1A1A1A;}
</style>
""", unsafe_allow_html=True)

st.title("🏎️ Mercedes-AMG Intrinsic Velocity Scanner")
st.markdown("**Silver Arrow Precision**: Scanning for undervalued stocks with true intrinsic speed. Debt resilience • Target upside • Growth catalysts")

# Sidebar
st.sidebar.header("⚙️ Race Controls")
num_stocks = st.sidebar.slider("Scan Depth", 50, 500, 150)
score_threshold = st.sidebar.slider("Minimum Velocity Score", 0.4, 0.9, 0.60, 0.01)

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
        
        score = (0.35 * debt_score + 0.3 * target_upside + 0.25 * graham_margin + 0.1 * 0.6)
        
        return {
            'Ticker': ticker,
            'Price': round(current_price, 2),
            'Target Upside %': round(target_upside * 100, 1),
            'Debt/Eq': round(debt_eq, 1) if debt_eq else 'N/A',
            'P/B': round(pb, 2),
            'Intrinsic Score': round(score, 3),
            'Growth %': round(growth * 100, 1)
        }
    except:
        return None

if st.button("🏁 SCAN THE TRACK — Find Undervalued Opportunities"):
    with st.spinner("Pushing to qualifying..."):
        results = []
        progress = st.progress(0)
        
        for i, t in enumerate(tickers):
            data = get_intrinsic_score(t)
            if data and data['Intrinsic Score'] > score_threshold:
                results.append(data)
            progress.progress((i + 1) / len(tickers))
        
        if results:
            df = pd.DataFrame(results)
            df = df.sort_values('Intrinsic Score', ascending=False)
            
            st.success(f"🏆 {len(df)} High-Velocity Picks Aligned")
            
            # Main visuals
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Growth Potential Bar Chart
                fig = px.bar(df.head(12), x='Ticker', y='Target Upside %', 
                            color='Intrinsic Score', color_continuous_scale=['#C8C8C8', '#00A19C'],
                            title="Growth Potential (Target Upside)")
                fig.update_layout(template="plotly_dark", plot_bgcolor="#1A1A1A")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Score Gauge for Top Pick
                top = df.iloc[0]
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=top['Intrinsic Score'] * 100,
                    title={'text': f"Top Pick: {top['Ticker']} Velocity"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "#00A19C"},
                           'steps': [{'range': [0, 60], 'color': "#333333"}, {'range': [60, 100], 'color': "#1A3C3A"}]}))
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            st.dataframe(df.head(20), use_container_width=True, height=500)
            
            csv = df.to_csv(index=False)
            st.download_button("⬇️ Download Pit Strategy CSV", csv, "mercedes_undervalued.csv", "text/csv")
        else:
            st.warning("No cars reached qualifying speed. Lower the threshold and try again.")

st.caption("**Mercedes Philosophy**: Precision over noise. Intrinsic value compounds like championship points. Correlation ≠ causation — always verify before full throttle.")
    