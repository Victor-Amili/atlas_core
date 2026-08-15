"""
Buy & Hold Strategy
The benchmark. Buy once, hold forever.
"""
from .base import BaseStrategy

class BuyAndHold(BaseStrategy):
    name = "Buy & Hold"

    def generate_signals(self, data):
        df = data.copy()
        df['signal'] = 0
        # Buy after warmup period (day 50)
        if len(df) > 50:
            df.iloc[50, df.columns.get_loc('signal')] = 1
        return df
