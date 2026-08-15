"""
MACD Momentum Strategy
Buy on bullish crossover, sell on bearish crossover.
"""
from .base import BaseStrategy
from ..indicators import macd

class MACDMomentum(BaseStrategy):
    name = "MACD Momentum"

    def __init__(self, fast=12, slow=26, signal=9):
        self.fast = fast
        self.slow = slow
        self.signal = signal

    def generate_signals(self, data):
        df = data.copy()
        df['macd_line'], df['macd_signal'], _ = macd.calculate(df['close'], self.fast, self.slow, self.signal)

        df['signal'] = 0
        for i in range(self.slow, len(df)):
            if (df['macd_line'].iloc[i] > df['macd_signal'].iloc[i] and 
                df['macd_line'].iloc[i-1] <= df['macd_signal'].iloc[i-1]):
                df.iloc[i, df.columns.get_loc('signal')] = 1
            elif (df['macd_line'].iloc[i] < df['macd_signal'].iloc[i] and 
                  df['macd_line'].iloc[i-1] >= df['macd_signal'].iloc[i-1]):
                df.iloc[i, df.columns.get_loc('signal')] = -1
        return df
