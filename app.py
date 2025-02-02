import streamlit as st
from data.fetch_data import fetch_stock_data, read_data
from data.process_data import get_holdings
from utils.visualizations import plot_stock_prices

option = st.sidebar.selectbox("Choose a feature", ["Home", "Stock Search", "Compare Stocks", "Portfolio"])

if option == "Home":
    st.write("Market Overview")

elif option == "Stock Search":
    ticker = st.text_input("Enter stock ticker:", "AAPL")

    if st.button("Fetch Data"):
        try:
            data = fetch_stock_data(ticker)
            st.write("Data fetched sucessfully")
            plot = plot_stock_prices(data['Historical Prices'], ticker)
            st.plotly_chart(plot, use_container_width=True)
        except:
            st.write("Error fecthing data")

elif option == "Compare Stocks":
    st.write("Compare Stocks")

elif option == "Portfolio":
    uploaded_file = st.file_uploader("Upload your portfolio file (CSV, Excel, or JSON)", type=["csv", "xlsx", "json"])

    portfolio_data = read_data(uploaded_file)

    holdings = get_holdings(portfolio_data)