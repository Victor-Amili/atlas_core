"""
Moving Averages
Simple and Exponential.
"""
import pandas as pd

def sma(data, period):
    return data.rolling(window=period).mean()

def ema(data, period):
    return data.ewm(span=period).mean()
