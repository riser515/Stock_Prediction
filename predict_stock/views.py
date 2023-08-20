from django.http import JsonResponse
from rest_framework.decorators import api_view
import yfinance as yf
from django.shortcuts import render
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd

def index(request):
    return render(request, "predict_stock/index.html")

def fetch_data_from_yahoo(ticker_symbol):
    data = yf.download(ticker_symbol, start="2020-01-01", end="2023-01-01")
    return data['Close'].values, data['Close'].index

def transform_time_series(data, window_size=5):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i+window_size])
        y.append(data[i+window_size])
    return np.array(X), np.array(y)

def train_model_for_stock(ticker_symbol):
    data, dates = fetch_data_from_yahoo(ticker_symbol)
    X, y = transform_time_series(data)

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)

    return model, data, dates

MODELS = {ticker: train_model_for_stock(ticker) for ticker in ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA', 'NFLX', 'NVDA', 'JPM', 'V', 'DIS', 'BABA']}

@api_view(http_method_names=["GET"])
def stock_predict(request, ticker_symbol):
    if ticker_symbol not in MODELS:
        return JsonResponse({'error': 'Invalid stock ticker.'}, status=400)
    model, past_data, dates = MODELS[ticker_symbol]

    predictions = []
    for _ in range(365):
        next_point = model.predict([past_data[-5:]])[0]
        predictions.append(next_point)
        past_data = np.append(past_data, next_point)

    forecast_dates = pd.date_range(start=dates[-1], periods=366)[1:]
    
    response_data = {
        'dates': [date.strftime('%Y-%m-%d') for date in forecast_dates],
        'predictions': predictions
    }

    return JsonResponse(response_data, safe=False)

def show_predictions(request, ticker_symbol):
    if ticker_symbol not in MODELS:
        return JsonResponse({'error': 'Invalid stock ticker.'}, status=400)

    model, past_data, dates = MODELS[ticker_symbol]

    predictions = []
    for _ in range(365):
        next_point = model.predict([past_data[-5:]])[0]
        predictions.append(next_point)
        past_data = np.append(past_data, next_point)

    forecast_dates = pd.date_range(start=dates[-1], periods=366)[1:]

    response_data = {
        'dates': [date.strftime('%Y-%m-%d') for date in forecast_dates],
        'predictions': predictions
    }


    return render(request, 'predict_stock/predictions.html', {
        'data': response_data,
        'ticker_symbol': ticker_symbol
    })