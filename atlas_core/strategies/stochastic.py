"""
Stochastic Oscillator Strategy
Buy oversold, sell overbought.
"""
from .base import BaseStrategy
from ..indicators import stochastic as stoch

class StochasticStrategy(BaseStrategy):
    name = "Stochastic Oscillator"

    def __init__(self, k_period=14, d_period=3, oversold=20, overbought=80):
        self.k_period = k_period
        self.d_period = d_period
        self.oversold = oversold
        self.overbought = overbought

    def generate_signals(self, data):
        df = data.copy()
        df['k'], df['d'] = stoch.calculate(df['high'], df['low'], df['close'], 
                                            self.k_period, self.d_period)

        df['signal'] = 0
        position = 0
        for i in range(self.k_period, len(df)):
            if df['k'].iloc[i] < self.oversold and position == 0:
                df.iloc[i, df.columns.get_loc('signal')] = 1
                position = 1
            elif df['k'].iloc[i] > self.overbought and position == 1:
                df.iloc[i, df.columns.get_loc('signal')] = -1
                position = 0
        return df
