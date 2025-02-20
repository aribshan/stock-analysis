import pandas as pd
import yfinance as yf

def get_holdings(data):
    holdings_columns = {"Ticker Symbol", "Total Holdings", "Average Buy Price"}
    if holdings_columns.issubset(data.columns):
        return data

    required_columns = {"Ticker Symbol", "Transaction Type", "Quantity", "Price per Unit"}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"Missing required columns: {required_columns - set(data.columns)}")

    data["Quantity"] = data.apply(
        lambda row: row["Quantity"] if row["Transaction Type"].lower() == "buy" else -row["Quantity"], axis=1
    )

    holdings = data.groupby("Ticker Symbol").agg(
        Total_Holdings=pd.NamedAgg(column="Quantity", aggfunc="sum"),
        Total_Cost=pd.NamedAgg(column="Price per Unit", aggfunc=lambda x: (x * data.loc[x.index, "Quantity"]).sum())
    ).reset_index()

    holdings = holdings[holdings["Total_Holdings"] > 0]

    holdings["Average Buy Price"] = holdings["Total_Cost"] / holdings["Total_Holdings"]

    holdings = holdings.drop(columns=["Total_Cost"])

    return holdings

def calculate_portfolio_values(holdings):
    portfolio_values = holdings.copy()

    portfolio_values["Total Invested"] = portfolio_values["Total Holdings"] * portfolio_values["Average Buy Price"]
    
    def get_current_price(ticker):
        try:
            stock = yf.Ticker(ticker)
            return stock.history(period="1d")["Close"].iloc[-1]
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

    portfolio_values["Current Price"] = portfolio_values["Ticker Symbol"].apply(get_current_price)

    portfolio_values["Current Value"] = portfolio_values["Total Holdings"] * portfolio_values["Current Price"]

    return portfolio_values