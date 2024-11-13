import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from data_fetch import get_stock_data
from models import train_arima_model, predict_future
import pandas as pd
import datetime

app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Real-Time Stock Market Dashboard"),
    dcc.Input(id='ticker', type='text', value='AAPL', placeholder='Enter Stock Ticker'),
    dcc.Interval(id='interval', interval=60000, n_intervals=0),  # 1-minute interval
    dcc.Graph(id='live-graph'),
    dcc.Graph(id='forecast-graph')
])

# Callback for updating the live data graph
@app.callback(Output('live-graph', 'figure'), [Input('ticker', 'value'), Input('interval', 'n_intervals')])
def update_live_graph(ticker, n):
    df = get_stock_data(ticker)
    fig = go.Figure(data=[go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price')])
    fig.update_layout(title=f'Real-Time Stock Price of {ticker}', xaxis_title='Time', yaxis_title='Price')
    return fig

# Callback for updating the forecast graph
@app.callback(Output('forecast-graph', 'figure'), [Input('ticker', 'value')])
def update_forecast_graph(ticker):
    df = get_stock_data(ticker)
    model = train_arima_model(df)
    forecast = predict_future(model)
    forecast_index = pd.date_range(df.index[-1], periods=len(forecast) + 1, freq='1T')[1:]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Actual Price'))
    fig.add_trace(go.Scatter(x=forecast_index, y=forecast, mode='lines', name='Predicted Price'))
    fig.update_layout(title=f'Price Prediction for {ticker}', xaxis_title='Time', yaxis_title='Price')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
