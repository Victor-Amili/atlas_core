"""
Bollinger Bands
Volatility bands placed above/below a moving average.
"""
import pandas as pd

def calculate(data, period=20, std_dev=2):
    """Calculate Bollinger Bands. Returns (middle, upper, lower)."""
    middle = data.rolling(window=period).mean()
    std = data.rolling(window=period).std()
    upper = middle + (std * std_dev)
    lower = middle - (std * std_dev)
    return middle, upper, lower

def position(data, period=20, std_dev=2):
    """Returns position within bands (0=lower, 0.5=middle, 1=upper)."""
    middle, upper, lower = calculate(data, period, std_dev)
    return (data - lower) / (upper - lower)
