"""
Relative Strength Index (RSI)
Momentum oscillator measuring speed of price changes.
"""
import pandas as pd
import numpy as np

def calculate(data, period=14):
    """Calculate RSI for a price series."""
    delta = data.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
