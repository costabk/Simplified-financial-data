import streamlit as st
import yfinance as yf
import pandas as pd

# Page configuration
st.set_page_config(page_title="Stock Comparison Tool", page_icon="📈", layout="wide")

# --- CACHE LOGIC ---
# This prevents "Too Many Requests" errors by saving data in memory
@st.cache_data(ttl=3600)
def get_stock_data(ticker):
    try:
        data = yf.Ticker(ticker)
        return data.info, data.history(period="1y")['Close']
    except:
        return None, None

st.title("📈 Global Stock Comparison Dashboard")
st.markdown("Enter two stock tickers to compare their performance and fundamentals side-by-side.")

# 1. Inputs in columns
col_input1, col_input2 = st.columns(2)

with col_input1:
    ticker1 = st.text_input("First Ticker (e.g., AAPL)", "AAPL").upper()
with col_input2:
    ticker2 = st.text_input("Second Ticker (e.g., MSFT)", "MSFT").upper()

if ticker1 and ticker2:
    # Fetching data using the cached function
    with st.spinner('Retrieving global market data...'):
        info1, hist1 = get_stock_data(ticker1)
        info2, hist2 = get_stock_data(ticker2)
        
        if info1 and info2 and 'longName' in info1 and 'longName' in info2:
            # --- FUNDAMENTALS COMPARISON ---
            st.subheader("Fundamental Comparison")
            
            comparison_df = pd.DataFrame({
                "Metric": ["Company Name", "Sector", "Total Revenue", "Net Income", "Revenue Growth"],
                f"{ticker1}": [
                    info1.get('longName'), 
                    info1.get('sector'),
                    f"${info1.get('totalRevenue', 0):,.0f}",
                    f"${info1.get('netIncomeToCommon', 0):,.0f}",
                    f"{info1.get('revenueGrowth', 0)*100:.2f}%" if info1.get('revenueGrowth') else "N/A"
                ],
                f"{ticker2}": [
                    info2.get('longName'), 
                    info2.get('sector'),
                    f"${info2.get('totalRevenue', 0):,.0f}",
                    f"${info2.get('netIncomeToCommon', 0):,.0f}",
                    f"{info2.get('revenueGrowth', 0)*100:.2f}%" if info2.get('revenueGrowth') else "N/A"
                ]
            })
            st.table(comparison_df)

            # --- CHART COMPARISON ---
            st.write("---")
            st.subheader("Normalized Performance (Last 12 Months)")
            
            # Normalizing data to 100 for fair comparison
            norm1 = (hist1 / hist1.iloc[0]) * 100
            norm2 = (hist2 / hist2.iloc[0]) * 100
            
            chart_data = pd.DataFrame({ticker1: norm1, ticker2: norm2})
            st.line_chart(chart_data)
        else:
            st.error("Wait a moment or check if the tickers are valid. Yahoo Finance is currently limiting requests.")