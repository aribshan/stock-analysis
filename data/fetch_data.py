import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    time_period = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

    hist = stock.history(period='1y')
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