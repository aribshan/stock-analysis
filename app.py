import streamlit as st
from data.fetch_data import fetch_stock_data, read_data, fetch_all_stock_data
from data.process_data import get_holdings, calculate_portfolio_values
from utils.visualizations import plot_stock_prices, plot_portfolio_value

st.set_page_config(
    layout="wide"
)

st.markdown(
    """
    <style>
    /* Add padding to the main content container */
    .block-container {
        padding-left: 300px;
        padding-right: 300px;
    }
    
    /* Optionally add some top/bottom padding */
    .main {
        padding-top: 20px;
        padding-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

option = st.sidebar.selectbox("Choose a feature", ["Home", "Stock Search", "Compare Stocks", "Upload Portfolio", "My Portfolio"])

if 'holdings' not in st.session_state:
    st.session_state.holdings = {}

if option == "Home":
    st.write("## Market Overview")

elif option == "Stock Search":
    ticker = st.text_input("Enter stock ticker:", "AAPL")

    if st.button("## Fetch Data"):
        try:
            data = fetch_stock_data(ticker)
            st.write("Data fetched sucessfully")
            plot = plot_stock_prices(data['Historical Prices'], ticker)
            st.plotly_chart(plot, use_container_width=True)
        except:
            st.write("Error fecthing data")

elif option == "Compare Stocks":
    st.write("## Compare Stocks")

elif option == "Upload Portfolio":
    st.write("## Upload Portfolio")

    uploaded_file = st.file_uploader("Upload your portfolio file (CSV, Excel, or JSON)", type=["csv", "xlsx", "json"])

    if uploaded_file is not None:
        portfolio_data = read_data(uploaded_file)

        if portfolio_data is not None:
            holdings = get_holdings(portfolio_data)
            # stock_data = fetch_all_stock_data(holdings)
            
            st.session_state.holdings = holdings
            # st.session_state.stock_data = stock_data
            st.write("Data Saved")
            # st.write("Updated stock data:", st.session_state.stock_data)

elif option == "My Portfolio":
    st.write("## My Portfolio")

    portfolio_value = calculate_portfolio_values(st.session_state.holdings)
    # st.write(portfolio_value)

    plot = plot_portfolio_value(portfolio_value, "Market Value")
    st.plotly_chart(plot, use_container_width=True)

    stock_data = fetch_all_stock_data(st.session_state.holdings)

    if stock_data:
        st.write("#### My Stock Trends")
        container = st.container()

        num_columns = 2
        columns = container.columns([2, 2])

        for idx, ticker in enumerate(stock_data):
            col_idx = idx % num_columns
            plot = plot_stock_prices(stock_data[ticker]['Historical Prices'], ticker)

            columns[col_idx].plotly_chart(plot, use_container_width=True)
    
    else:
        st.write("No stock data available.")