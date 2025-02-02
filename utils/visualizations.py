import plotly.graph_objects as go
import pandas as pd

def plot_stock_prices(data, ticker):
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                    open=data['Open'], high=data['High'],
                    low=data['Low'], close=data['Close'])
                    ])

    fig.update_layout(
        title=dict(text=f"{ticker} stock prices"),
        font=dict(size=12, color='#9999dd'),
        yaxis=dict(
            title=dict(
                text=f"{ticker} stock price (USD)"
            )
        ),
        xaxis=dict(
            title=dict(
                text="Date"
            )
        ),
        template='plotly_dark'
    )

    return fig