import yfinance as yf
import pandas as pd
import streamlit as st
import json

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