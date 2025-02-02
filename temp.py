import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from utils.visualizations import plot_stock_prices

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    time_period = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

    hist = stock.history(period='1mo')
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


ticker = input("Enter stock ticker (e.g., AAPL): ")
stock_data = fetch_stock_data(ticker)

# for key, df in stock_data.items():
#     print(f"\n{key}:\n")
#     print(df.head())

data = stock_data['Historical Prices']

plot = plot_stock_prices(data, ticker)
plot.show()
# print(data)
# print(data.index)
# fig = go.Figure(data=[go.Candlestick(x=data.index,
#                     open=data['Open'], high=data['High'],
#                     low=data['Low'], close=data['Close'])
#                     ])

# fig.update_layout(
#     title=dict(text=f"{ticker} stock prices"),
#     font=dict(size=12, color='#9999dd'),
#     yaxis=dict(
#         title=dict(
#             text=f"{ticker} stock price"
#         )
#     ),
#     xaxis=dict(
#         title=dict(
#             text="Date"
#         )
#     ),
#     template='plotly_dark'
# )

# fig.show()