import streamlit as st
import yfinance as yf
import pandas as pd

# Page configuration
st.set_page_config(page_title="Global Financial Dashboard", page_icon="📊")

st.title("📊 Simplified Financial Dashboard")
st.markdown("Enter the stock ticker of a major company to retrieve its financial data.")

# Sidebar for user input
ticker_symbol = st.text_input("Enter Ticker Symbol (e.g., AAPL, MSFT, TSLA, GOOGL)", "AAPL").upper()

if ticker_symbol:
    try:
        # Fetch data from Yahoo Finance
        company = yf.Ticker(ticker_symbol)
        info = company.info
        
        # Display Company Name and Sector
        st.header(f"{info.get('longName', 'Company Information')}")
        st.subheader(f"Sector: {info.get('sector', 'N/A')} | Industry: {info.get('industry', 'N/A')}")

        # Creating columns for key metrics
        col1, col2, col3 = st.columns(3)

        # 1. Total Revenue
        revenue = info.get('totalRevenue')
        if revenue:
            col1.metric("Total Revenue", f"${revenue:,.0f}")
        else:
            col1.metric("Total Revenue", "N/A")

        # 2. Net Income (Profit)
        net_income = info.get('netIncomeToCommon')
        if net_income:
            col2.metric("Net Income", f"${net_income:,.0f}")
        else:
            col2.metric("Net Income", "N/A")

        # 3. Revenue Growth
        growth = info.get('revenueGrowth')
        if growth:
            col3.metric("Revenue Growth (YoY)", f"{growth * 100:.2f}%")
        else:
            col3.metric("Revenue Growth", "N/A")

        # Visualizing Stock History (Bonus for a better Dashboard)
        st.write("---")
        st.subheader("Stock Price History (Last 12 Months)")
        history = company.history(period="1y")
        st.line_chart(history['Close'])

        # Financial Summary Table
        st.subheader("Financial Summary")
        summary_data = {
            "Metric": ["Profit Margin", "Operating Margins", "EBITDA", "Total Cash"],
            "Value": [
                f"{info.get('profitMargins', 0)*100:.2f}%",
                f"{info.get('operatingMargins', 0)*100:.2f}%",
                f"${info.get('ebitda', 0):,.0f}",
                f"${info.get('totalCash', 0):,.0f}"
            ]
        }
        st.table(pd.DataFrame(summary_data))

    except Exception as e:
        st.error(f"Error: Could not find data for '{ticker_symbol}'. Please check the ticker and try again.")
        