import yfinance as yf
import pandas as pd

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="1d", interval="1m")  # Real-time data at 1-minute intervals
    return df

# Example Usage
# df = get_stock_data("AAPL")
