"""
Average Directional Index (ADX)
Measures trend strength regardless of direction.
"""
import pandas as pd
import numpy as np

def calculate(data_high, data_low, data_close, period=14):
    """Calculate ADX, +DI, -DI."""
    tr1 = data_high - data_low
    tr2 = abs(data_high - data_close.shift(1))
    tr3 = abs(data_low - data_close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    plus_dm = np.where((data_high - data_high.shift(1)) > (data_low.shift(1) - data_low),
                       np.maximum(data_high - data_high.shift(1), 0), 0)
    minus_dm = np.where((data_low.shift(1) - data_low) > (data_high - data_high.shift(1)),
                        np.maximum(data_low.shift(1) - data_low, 0), 0)

    atr = pd.Series(tr, index=data_high.index).ewm(alpha=1/period, min_periods=period).mean()
    plus_di = 100 * (pd.Series(plus_dm, index=data_high.index).ewm(alpha=1/period, min_periods=period).mean() / atr)
    minus_di = 100 * (pd.Series(minus_dm, index=data_high.index).ewm(alpha=1/period, min_periods=period).mean() / atr)

    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.ewm(alpha=1/period, min_periods=period).mean()

    return adx, plus_di, minus_di
