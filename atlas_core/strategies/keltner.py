"""
Keltner Channels Strategy
Mean reversion using ATR-based bands.
"""
from .base import BaseStrategy
from ..indicators import keltner as kelt

class KeltnerChannels(BaseStrategy):
    name = "Keltner Channels"

    def __init__(self, period=20, atr_mult=2):
        self.period = period
        self.atr_mult = atr_mult

    def generate_signals(self, data):
        df = data.copy()
        df['ema'], df['upper'], df['lower'] = kelt.calculate(df['high'], df['low'], df['close'], 
                                                               self.period, self.atr_mult)

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
