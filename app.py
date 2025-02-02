import streamlit as st
from data.fetch_data import fetch_stock_data
from utils.visualizations import plot_stock_prices

option = st.sidebar.selectbox("Choose a feature", ["Home", "Stock Search", "Portfolio"])

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

elif option == "Portfolio":
    st.write("Portfolio Analysis")