from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

def train_arima_model(data):
    model = ARIMA(data['Close'], order=(5, 1, 0))  # Parameters can be tuned
    model_fit = model.fit()
    return model_fit

def predict_future(model, steps=10):
    forecast = model.forecast(steps=steps)
    return forecast
