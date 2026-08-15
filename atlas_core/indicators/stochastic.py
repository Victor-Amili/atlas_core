"""
Stochastic Oscillator
Compares closing price to price range over a period.
"""
import pandas as pd

def calculate(data_high, data_low, data_close, k_period=14, d_period=3):
    """Calculate Stochastic %K and %D."""
    lowest_low = data_low.rolling(window=k_period).min()
    highest_high = data_high.rolling(window=k_period).max()
    k = 100 * (data_close - lowest_low) / (highest_high - lowest_low)
    d = k.rolling(window=d_period).mean()
    return k, d
