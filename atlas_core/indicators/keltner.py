"""
Keltner Channels
Volatility bands using ATR instead of standard deviation.
"""
import pandas as pd
import numpy as np

def calculate(data_high, data_low, data_close, period=20, atr_multiplier=2):
    """Calculate Keltner Channels."""
    ema = data_close.ewm(span=period).mean()
    tr1 = data_high - data_low
    tr2 = abs(data_high - data_close.shift(1))
    tr3 = abs(data_low - data_close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    upper = ema + (atr * atr_multiplier)
    lower = ema - (atr * atr_multiplier)
    return ema, upper, lower
