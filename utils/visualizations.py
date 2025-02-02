import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

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

def plot_portfolio_value(data, values):
    fig = px.pie(data, values=values, names='Ticker Symbol', color_discrete_sequence=["#00296d", "#2e89c1", "#66fffa"])

    fig.update_layout(
        font=dict(size=12, color='#9999dd'),
        template='plotly_dark',
    )

    fig.layout.showlegend = True

    return fig

def create_heatmap():
    sectors = ["Tech", "Healthcare", "Energy", "Finance"]
    performance = [2.5, -1.2, 0.5, -0.8]

    fig = go.Figure(data=go.Heatmap(
        z=performance,
        x=sectors,
        y=["Performance"],
        colorscale="RdYlGn",
        showscale=True
    ))
    
    fig.update_layout(title="Stock Market Sector Performance", height=300)
    return fig