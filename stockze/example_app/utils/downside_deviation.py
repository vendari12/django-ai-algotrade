import math

from datetime import date

import pandas as pd

from environ import Env

from stockze.example_app.utils.yfinance_history import yfinance_history

env = Env()

def downside_deviation(ticker):
    today = date.today().strftime("%Y-%m-%d")
    try:
        hist = yfinance_history(ticker=ticker, timeframe="1y", category=False, new=False)
        hist['Date'] = pd.to_datetime(hist['Date'])
        most_recent_date = hist['Date'].max()
        most_recent_date = most_recent_date.strftime("%Y-%m-%d")
        assert most_recent_date == today
    except:
        hist = yfinance_history(ticker=ticker, timeframe="1y")
        # TODO: replace w func to update data
    rows = len(hist.index)
    prices = []
    for price in hist['Close']:
        prices.append(price)
    return_series = []
    for i in range(1, len(prices)):
        return_series.append((prices[i] / prices[i-1]) - 1)
    adjusted_benchmark_rate = (1 ** (1/rows)) - 1
    downside_series = []
    for return_ in return_series:
        downside_series.append(adjusted_benchmark_rate - return_)
    downside_squares = []
    for downside in downside_series:
        if downside > 0:
            downside_squares.append(downside ** 2)
    downside_sum_of_squares = sum(downside_squares)
    downside_dev = math.sqrt(downside_sum_of_squares / int(rows - 1))
    downside_dev *= math.sqrt(rows)
    return downside_dev
