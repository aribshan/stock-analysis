import yfinance as yf
import pandas as pd
import streamlit as st
import json

INDEX_TICKERS = {
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "Dow Jones": "^DJI",
    "Russell 2000": "^RUT",
    "VIX": "^VIX"
}

def get_market_indices():
    """Fetch latest prices & percentage changes for major indices."""
    index_data = []
    
    for name, ticker in INDEX_TICKERS.items():
        try:
            index = yf.Ticker(ticker)
            hist = index.history(period="5d")
            
            if len(hist) < 2:
                continue

            current_price = hist["Close"].iloc[-1]
            prev_close = hist["Close"].iloc[-2]

            change_percent = ((current_price - prev_close) / prev_close) * 100

            index_data.append({
                "Index": name,
                "Current Price": round(current_price, 2),
                "Change (%)": round(change_percent, 2)
            })
        
        except Exception as e:
            print(f"Error fetching {name}: {e}")
    
    return pd.DataFrame(index_data) if index_data else None


def get_top_gainers_losers():
    """Fetch top gainers & losers from a list of tracked stocks."""
    stock_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "BABA", "AMD"]
    stock_data = []

    for ticker in stock_tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            
            if len(hist) < 2:
                continue

            current_price = hist["Close"].iloc[-1]
            prev_close = hist["Close"].iloc[-2]

            change_percent = ((current_price - prev_close) / prev_close) * 100

            stock_data.append({
                "Ticker": ticker,
                "Current Price": round(current_price, 2),
                "Change (%)": round(change_percent, 2)
            })
        
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

    df = pd.DataFrame(stock_data)

    if df.empty:
        return None, None

    df_sorted = df.sort_values(by="Change (%)", ascending=False)
    top_gainers = df_sorted.head(5)
    top_losers = df_sorted.tail(5)
    top_losers = top_losers.iloc[::-1]

    return top_gainers, top_losers

def fetch_stock_data(ticker, time='1y'):
    stock = yf.Ticker(ticker)
    time_period = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

    hist = stock.history(period=time)
    hist.reset_index(inplace=True)
    financials = stock.financials.T
    balance_sheet = stock.balance_sheet.T
    cashflow = stock.cashflow.T

    data = {
        "Historical Prices": hist,
        "Financials": financials,
        "Balance Sheet": balance_sheet,
        "Cash Flow": cashflow
    }
    
    return data

def fetch_all_stock_data(holdings):
    data = {}

    for stock in holdings['Ticker Symbol']:
        data[stock] = fetch_stock_data(stock)
    
    return data

def read_data(uploaded_file):
    df = None

    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1].lower()  
        
        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
            st.success("CSV file uploaded successfully!")
        elif file_type == "xlsx":
            df = pd.read_excel(uploaded_file)
            st.success("Excel file uploaded successfully!")
        elif file_type == "json":
            data = json.load(uploaded_file)
            df = pd.DataFrame(data)
            st.success("JSON file uploaded successfully!")
        else:
            st.error("Unsupported file format. Please upload a CSV, Excel, or JSON file.")

        # if df is not None:
        #     st.write("### Portfolio Data Preview:")
            # st.dataframe(df)

            # st.download_button("Download Processed Data", df.to_csv(index=False), "portfolio_processed.csv", "text/csv")

    return df