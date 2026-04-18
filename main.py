import streamlit as st
import yfinance as yf
import pandas as pd

# Page configuration
st.set_page_config(page_title="Stock Comparison Tool", page_icon="📈", layout="wide")

st.title("📈 Global Stock Comparison Dashboard")
st.markdown("Enter two stock tickers to compare their performance and fundamentals side-by-side.")

# 1. Inputs in columns
col_input1, col_input2 = st.columns(2)

with col_input1:
    ticker1 = st.text_input("First Ticker (e.g., AAPL)", "AAPL").upper()
with col_input2:
    ticker2 = st.text_input("Second Ticker (e.g., MSFT)", "MSFT").upper()

if ticker1 and ticker2:
    try:
        # Fetching data for both
        with st.spinner('Comparing data...'):
            data1 = yf.Ticker(ticker1)
            data2 = yf.Ticker(ticker2)
            
            info1 = data1.info
            info2 = data2.info

            # --- FUNDAMENTALS COMPARISON ---
            st.subheader("Fundamental Comparison")
            
            # Creating a comparison table
            comparison_df = pd.DataFrame({
                "Metric": ["Company Name", "Sector", "Total Revenue", "Net Income", "Revenue Growth"],
                f"{ticker1}": [
                    info1.get('longName'), 
                    info1.get('sector'),
                    f"${info1.get('totalRevenue', 0):,.0f}",
                    f"${info1.get('netIncomeToCommon', 0):,.0f}",
                    f"{info1.get('revenueGrowth', 0)*100:.2f}%"
                ],
                f"{ticker2}": [
                    info2.get('longName'), 
                    info2.get('sector'),
                    f"${info2.get('totalRevenue', 0):,.0f}",
                    f"${info2.get('netIncomeToCommon', 0):,.0f}",
                    f"{info2.get('revenueGrowth', 0)*100:.2f}%"
                ]
            })
            st.table(comparison_df)

            # --- CHART COMPARISON ---
            st.write("---")
            st.subheader("Price Performance (Last 12 Months)")
            
            # Fetching historical data
            hist1 = data1.history(period="1y")['Close']
            hist2 = data2.history(period="1y")['Close']
            
            # Normalizing data to compare growth (%) instead of raw price
            # This is important if one stock is $100 and the other is $3000
            norm1 = (hist1 / hist1.iloc[0]) * 100
            norm2 = (hist2 / hist2.iloc[0]) * 100
            
            chart_data = pd.DataFrame({
                ticker1: norm1,
                ticker2: norm2
            })
            
            st.line_chart(chart_data)
            st.caption("Data normalized to 100 (percentage growth) for a fair comparison.")

    except Exception as e:
        st.error(f"Error: Make sure the tickers are correct. Details: {e}")

else:
    st.info("Please enter both tickers to see the comparison.")