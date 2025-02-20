import streamlit as st
from data.fetch_data import fetch_stock_data, read_data, fetch_all_stock_data, get_market_indices, get_top_gainers_losers
from data.process_data import get_holdings, calculate_portfolio_values
from utils.visualizations import plot_stock_prices, plot_portfolio_value, create_heatmap

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

    st.subheader("Major Indices")
    index_data = get_market_indices()

    index_data_dict = index_data.set_index('Index').to_dict(orient='index')

    col1, col2, col3 = st.columns(3)

    for i, (name, data) in enumerate(index_data_dict.items()):
        col = [col1, col2, col3][i % 3]

        if data['Change (%)'] > 0:
            change_color = "normal"
        elif data['Change (%)'] < 0:
            change_color = "normal"
        else:
            change_color = "off"

        col.metric(
            label=name, 
            value=f"${data['Current Price']:.2f}", 
            delta=f"{data['Change (%)']:.2f}", 
            delta_color=change_color
        )

    gainers, losers = get_top_gainers_losers()

    if gainers is not None and losers is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 📊 Top Gainers")
            st.dataframe(gainers.set_index("Ticker"))
        
        with col2:
            st.write("### 📉 Top Losers")
            st.dataframe(losers.set_index("Ticker"))
    else:
        st.warning("Could not fetch top gainers and losers.")

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
    container = st.container()

    num_columns = 2
    columns = container.columns([2, 2])

    ticker1 = columns[0].text_input("Enter stock ticker 1:", "AAPL", key="ticker1")
    ticker2 = columns[1].text_input("Enter stock ticker 2:", "MSFT", key="ticker2")

    if st.button("Fetch Data"):
        try:
            st.session_state["data1"] = fetch_stock_data(ticker1)
            st.session_state["plot1"] = plot_stock_prices(st.session_state["data1"]['Historical Prices'], ticker1)
        except:
            st.session_state["data1"] = None
            st.session_state["plot1"] = None
            columns[0].write("Error fetching data")

        try:
            st.session_state["data2"] = fetch_stock_data(ticker2)
            st.session_state["plot2"] = plot_stock_prices(st.session_state["data2"]['Historical Prices'], ticker2)
        except:
            st.session_state["data2"] = None
            st.session_state["plot2"] = None
            columns[1].write("Error fetching data")

    if "plot1" in st.session_state and st.session_state["plot1"]:
        columns[0].write("Data fetched successfully")
        columns[0].plotly_chart(st.session_state["plot1"], use_container_width=True)

    if "plot2" in st.session_state and st.session_state["plot2"]:
        columns[1].write("Data fetched successfully")
        columns[1].plotly_chart(st.session_state["plot2"], use_container_width=True)


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

    if len(st.session_state.holdings):
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
    else:
        st.write("Please upload a portfolio first on the portfolio tab")