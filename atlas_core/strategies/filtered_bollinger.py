"""
Filtered Bollinger (ADX Filter)
Only trade Bollinger signals when ADX confirms ranging market.
"""
from .base import BaseStrategy
from ..indicators import bollinger as bb, adx

class FilteredBollinger(BaseStrategy):
    name = "Filtered Bollinger (ADX<25)"

    def __init__(self, bb_period=20, bb_std=2, adx_threshold=25):
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.adx_threshold = adx_threshold

    def generate_signals(self, data):
        df = data.copy()
        df['ma'], df['upper'], df['lower'] = bb.calculate(df['close'], self.bb_period, self.bb_std)
        df['adx'], _, _ = adx.calculate(df['high'], df['low'], df['close'])

        df['signal'] = 0
        position = 0
        for i in range(self.bb_period, len(df)):
            if df['adx'].iloc[i] < self.adx_threshold:
                if not position and df['close'].iloc[i] < df['lower'].iloc[i]:
                    df.iloc[i, df.columns.get_loc('signal')] = 1
                    position = 1
                elif position and df['close'].iloc[i] > df['upper'].iloc[i]:
                    df.iloc[i, df.columns.get_loc('signal')] = -1
                    position = 0
        return df
