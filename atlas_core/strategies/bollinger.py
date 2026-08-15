"""
Bollinger Bands Strategy
Mean reversion: buy at lower band, sell at upper band.
"""
from .base import BaseStrategy
from ..indicators import bollinger as bb

class BollingerBands(BaseStrategy):
    name = "Bollinger Bands"

    def __init__(self, period=20, std_dev=2):
        self.period = period
        self.std_dev = std_dev

    def generate_signals(self, data):
        df = data.copy()
        df['ma'], df['upper'], df['lower'] = bb.calculate(df['close'], self.period, self.std_dev)

        df['signal'] = 0
        position = 0
        for i in range(self.period, len(df)):
            if df['close'].iloc[i] < df['lower'].iloc[i] and position == 0:
                df.iloc[i, df.columns.get_loc('signal')] = 1
                position = 1
            elif df['close'].iloc[i] > df['upper'].iloc[i] and position == 1:
                df.iloc[i, df.columns.get_loc('signal')] = -1
                position = 0
        return df
