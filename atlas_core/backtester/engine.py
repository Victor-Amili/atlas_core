"""
Backtester Engine
Runs strategies through historical data with risk management.
"""
import pandas as pd
import numpy as np
from ..risk.engine import RiskEngine

class Backtester:
    """
    Universal backtester for single-asset strategies.
    """

    def __init__(self, strategy, initial_capital=10000, 
                 risk_per_trade=0.02, stop_loss_pct=0.05):
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.risk_engine = RiskEngine(risk_per_trade, stop_loss_pct)
        self.results = None

    def run(self, data):
        """
        Run backtest on historical data.

        Args:
            data: DataFrame with OHLCV columns

        Returns:
            BacktestResult object
        """
        df = self.strategy.generate_signals(data)

        # For Buy & Hold, handle separately
        if 'Buy & Hold' in self.strategy.name:
            return self._run_buy_hold(df)

        capital = self.initial_capital
        trades = []
        in_trade = False
        entry_price = 0
        entry_date = None
        shares = 0
        portfolio_value = []
        peak_value = self.initial_capital

        for i in range(len(df)):
            current_price = df['close'].iloc[i]
            current_date = df.index[i]

            if not in_trade:
                if df['signal'].iloc[i] == 1 and capital > 0:
                    entry_price = current_price
                    entry_date = current_date
                    shares = self.risk_engine.calculate_position_size(capital, entry_price)
                    if shares > 0:
                        capital -= shares * entry_price
                        in_trade = True
            else:
                exit_trade = False
                exit_reason = ""

                if self.risk_engine.check_stop_loss(entry_price, current_price):
                    exit_trade = True
                    exit_reason = "Stop Loss"
                elif df['signal'].iloc[i] == -1:
                    exit_trade = True
                    exit_reason = "Signal"

                if exit_trade:
                    exit_price = current_price
                    capital += shares * exit_price
                    pnl = (exit_price - entry_price) * shares
                    pnl_pct = (exit_price / entry_price - 1) * 100

                    trades.append({
                        'entry_date': entry_date,
                        'exit_date': current_date,
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'shares': shares,
                        'pnl': pnl,
                        'pnl_pct': pnl_pct,
                        'reason': exit_reason
                    })

                    in_trade = False
                    shares = 0

            current_value = capital + (shares * current_price if in_trade else 0)
            portfolio_value.append(current_value)
            peak_value = max(peak_value, current_value)

        df['portfolio'] = portfolio_value
        trades_df = pd.DataFrame(trades)

        # Calculate metrics
        total_return = ((capital / self.initial_capital) - 1) * 100
        max_dd = ((pd.Series(portfolio_value).cummax() - pd.Series(portfolio_value)) / 
                  pd.Series(portfolio_value).cummax()).max() * 100

        if len(trades_df) > 0:
            wins = (trades_df['pnl'] > 0).sum()
            losses = (trades_df['pnl'] <= 0).sum()
            win_rate = (wins / len(trades_df)) * 100
            avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if wins > 0 else 0
            avg_loss = trades_df[trades_df['pnl'] <= 0]['pnl'].mean() if losses > 0 else 0
            pf_denom = trades_df[trades_df['pnl'] <= 0]['pnl'].sum()
            profit_factor = abs(trades_df[trades_df['pnl'] > 0]['pnl'].sum() / pf_denom) if pf_denom != 0 else float('inf')
            expectancy = (win_rate/100 * avg_win) + ((1-win_rate/100) * avg_loss) if len(trades_df) > 0 else 0
        else:
            wins = losses = win_rate = avg_win = avg_loss = profit_factor = expectancy = 0

        return BacktestResult(
            strategy_name=self.strategy.name,
            final_capital=capital,
            total_return=total_return,
            total_trades=len(trades_df),
            wins=wins,
            losses=losses,
            win_rate=win_rate,
            avg_win=avg_win,
            avg_loss=avg_loss,
            profit_factor=profit_factor,
            max_drawdown=max_dd,
            expectancy=expectancy,
            df=df,
            trades=trades_df
        )

    def _run_buy_hold(self, df):
        """Special handling for Buy & Hold."""
        buyhold_shares = self.initial_capital / df['close'].iloc[50]
        df['portfolio'] = buyhold_shares * df['close']
        capital = df['portfolio'].iloc[-1]
        total_return = ((capital / self.initial_capital) - 1) * 100
        max_dd = ((df['portfolio'].cummax() - df['portfolio']) / df['portfolio'].cummax()).max() * 100

        return BacktestResult(
            strategy_name=self.strategy.name,
            final_capital=capital,
            total_return=total_return,
            total_trades=0,
            wins=0, losses=0, win_rate=0,
            avg_win=0, avg_loss=0, profit_factor=0,
            max_drawdown=max_dd, expectancy=0,
            df=df, trades=pd.DataFrame()
        )


class BacktestResult:
    """Container for backtest results."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def summary(self):
        """Print summary of results."""
        print(f"\n{'='*60}")
        print(f"BACKTEST RESULTS: {self.strategy_name}")
        print(f"{'='*60}")
        print(f"Final Capital:    ${self.final_capital:,.2f}")
        print(f"Total Return:     {self.total_return:+.2f}%")
        print(f"Total Trades:     {self.total_trades}")
        print(f"Win Rate:         {self.win_rate:.1f}%")
        print(f"Profit Factor:    {self.profit_factor:.2f}")
        print(f"Max Drawdown:     {self.max_drawdown:.2f}%")
        print(f"Expectancy:       ${self.expectancy:+.2f}")
        print(f"{'='*60}")
