"""
MA Crossover with RSI Filter
Trend following, but skip overbought entries.
"""
from .base import BaseStrategy
from ..indicators import ma, rsi

class MAWithRSIFilter(BaseStrategy):
    name = "MA + RSI Filter"

    def __init__(self, fast=10, slow=50, rsi_period=14):
        self.fast = fast
        self.slow = slow
        self.rsi_period = rsi_period

    def generate_signals(self, data):
        df = data.copy()
        df['fast_ma'] = ma.sma(df['close'], self.fast)
        df['slow_ma'] = ma.sma(df['close'], self.slow)
        df['rsi'] = rsi.calculate(df['close'], self.rsi_period)

        df['signal'] = 0
        for i in range(self.slow, len(df)):
            if (df['fast_ma'].iloc[i] > df['slow_ma'].iloc[i] and 
                df['fast_ma'].iloc[i-1] <= df['slow_ma'].iloc[i-1] and 
                df['rsi'].iloc[i] < 70):
                df.iloc[i, df.columns.get_loc('signal')] = 1
            elif (df['fast_ma'].iloc[i] < df['slow_ma'].iloc[i] and 
                  df['fast_ma'].iloc[i-1] >= df['slow_ma'].iloc[i-1] and 
                  df['rsi'].iloc[i] > 30):
                df.iloc[i, df.columns.get_loc('signal')] = -1
        return df
