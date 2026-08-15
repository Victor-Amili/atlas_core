"""
Base Strategy Class
All strategies inherit from this.
"""
import pandas as pd
import numpy as np

class BaseStrategy:
    """Base class for all trading strategies."""

    name = "Base Strategy"

    def generate_signals(self, data):
        """
        Generate trading signals.

        Args:
            data: DataFrame with OHLCV data

        Returns:
            DataFrame with 'signal' column (1=buy, -1=sell, 0=hold)
        """
        raise NotImplementedError("Subclasses must implement generate_signals()")

    def prepare_indicators(self, data):
        """Add required indicators to data. Override in subclass."""
        return data
