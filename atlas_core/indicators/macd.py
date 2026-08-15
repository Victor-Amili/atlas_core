"""
MACD (Moving Average Convergence Divergence)
Trend-following momentum indicator.
"""
import pandas as pd

def calculate(data, fast=12, slow=26, signal=9):
    """Calculate MACD line, signal line, and histogram."""
    ema_fast = data.ewm(span=fast).mean()
    ema_slow = data.ewm(span=slow).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram
