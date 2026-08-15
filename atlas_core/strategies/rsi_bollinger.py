"""
RSI + Bollinger Combo
Double confirmation: must be oversold on BOTH indicators.
"""
from .base import BaseStrategy
from ..indicators import rsi, bollinger as bb

class RSIBollingerCombo(BaseStrategy):
    name = "RSI + Bollinger Combo"

    def __init__(self, rsi_period=14, bb_period=20, rsi_buy=35, rsi_sell=65):
        self.rsi_period = rsi_period
        self.bb_period = bb_period
        self.rsi_buy = rsi_buy
        self.rsi_sell = rsi_sell

    def generate_signals(self, data):
        df = data.copy()
        df['rsi'] = rsi.calculate(df['close'], self.rsi_period)
        df['ma'], df['upper'], df['lower'] = bb.calculate(df['close'], self.bb_period)

        df['signal'] = 0
        position = 0
        for i in range(max(self.rsi_period, self.bb_period), len(df)):
            if not position and df['rsi'].iloc[i] < self.rsi_buy and df['close'].iloc[i] < df['lower'].iloc[i]:
                df.iloc[i, df.columns.get_loc('signal')] = 1
                position = 1
            elif position and (df['rsi'].iloc[i] > self.rsi_sell or df['close'].iloc[i] > df['upper'].iloc[i]):
                df.iloc[i, df.columns.get_loc('signal')] = -1
                position = 0
        return df
