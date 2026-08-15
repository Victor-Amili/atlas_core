"""
Risk Management Engine
Handles position sizing, stop losses, and portfolio protection.
"""
import pandas as pd
import numpy as np

class RiskEngine:
    """
    Manages risk for every trade.

    Rules:
    - Risk only X% of capital per trade
    - Stop loss at Y% below entry
    - Max daily/weekly loss limits
    """

    def __init__(self, risk_per_trade=0.02, stop_loss_pct=0.05, 
                 max_daily_loss=None, max_drawdown=None):
        self.risk_per_trade = risk_per_trade
        self.stop_loss_pct = stop_loss_pct
        self.max_daily_loss = max_daily_loss
        self.max_drawdown = max_drawdown
        self.daily_pnl = 0
        self.current_date = None

    def calculate_position_size(self, capital, entry_price):
        """Calculate shares to buy based on risk rules."""
        risk_amount = capital * self.risk_per_trade
        loss_per_share = entry_price * self.stop_loss_pct
        shares = int(risk_amount / loss_per_share)

        # Can't exceed available capital
        max_shares = int(capital / entry_price)
        shares = min(shares, max_shares)

        return max(shares, 0)

    def check_stop_loss(self, entry_price, current_price):
        """Check if stop loss is hit."""
        return current_price <= entry_price * (1 - self.stop_loss_pct)

    def check_drawdown(self, portfolio_value, peak_value):
        """Check if max drawdown exceeded."""
        if self.max_drawdown is None or peak_value == 0:
            return False
        dd = (peak_value - portfolio_value) / peak_value
        return dd > self.max_drawdown
