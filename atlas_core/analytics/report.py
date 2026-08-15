"""
Analytics & Reporting
Produces metrics, charts, and comparison reports.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class Report:
    """Generate reports from backtest results."""

    @staticmethod
    def comparison_table(results):
        """
        Create comparison table of multiple strategies.

        Args:
            results: List of BacktestResult objects

        Returns:
            DataFrame
        """
        data = []
        for r in results:
            data.append({
                'Strategy': r.strategy_name,
                'Final ($)': f"{r.final_capital:,.0f}",
                'Return (%)': f"{r.total_return:+.1f}",
                'Trades': r.total_trades,
                'Win Rate': f"{r.win_rate:.0f}%",
                'Profit Factor': f"{r.profit_factor:.2f}",
                'Max DD (%)': f"{r.max_drawdown:.1f}",
                'Expectancy ($)': f"{r.expectancy:+.0f}"
            })
        return pd.DataFrame(data)

    @staticmethod
    def plot_equity_curves(results, save_path=None):
        """Plot equity curves for all strategies."""
        fig, ax = plt.subplots(figsize=(14, 7))
        colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728', '#9467bd', '#8c564b', '#e377c2']

        for i, r in enumerate(results):
            ax.plot(r.df.index, r.df['portfolio'], label=r.strategy_name, 
                   color=colors[i % len(colors)], linewidth=1.8, alpha=0.85)

        ax.axhline(y=results[0].df['portfolio'].iloc[0], color='black', 
                  linestyle='--', alpha=0.4, label='Start Capital')
        ax.set_title('Equity Curves Comparison', fontsize=14, fontweight='bold')
        ax.set_ylabel('Portfolio Value ($)', fontsize=12)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.2)

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
        return fig

    @staticmethod
    def plot_returns_bar(results, save_path=None):
        """Bar chart of returns."""
        fig, ax = plt.subplots(figsize=(12, 6))
        names = [r.strategy_name for r in results]
        returns = [r.total_return for r in results]
        colors = ['#2ca02c' if r > 0 else '#d62728' for r in returns]

        bars = ax.bar(range(len(names)), returns, color=colors, edgecolor='black', alpha=0.9)
        ax.axhline(y=0, color='black', linewidth=0.8)
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels([n.replace(' ', '\n') for n in names], fontsize=9)
        ax.set_ylabel('Return (%)', fontsize=12)
        ax.set_title('Strategy Returns Comparison', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.2, axis='y')

        for bar, val in zip(bars, returns):
            ax.annotate(f'{val:+.1f}%', 
                       xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 3 if val > 0 else -12), textcoords='offset points',
                       ha='center', fontsize=10, fontweight='bold')

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
        return fig

    @staticmethod
    def composite_score(result, weights=None):
        """
        Calculate composite score for ranking strategies.

        Default weights:
        40% risk-adjusted return (return / max_dd)
        25% max drawdown (inverted)
        15% profit factor
        10% win rate
        10% expectancy
        """
        if weights is None:
            weights = {'ret_dd': 0.40, 'dd': 0.25, 'pf': 0.15, 'wr': 0.10, 'exp': 0.10}

        # Normalize each metric to 0-100 scale
        ret_dd_score = min(max(result.total_return / max(result.max_drawdown, 0.1) * 5, 0), 100)
        dd_score = max(0, 100 - result.max_drawdown * 2)
        pf_score = min(result.profit_factor * 10, 100)
        wr_score = result.win_rate
        exp_score = min(max(result.expectancy / 10 * 50 + 50, 0), 100)

        composite = (weights['ret_dd'] * ret_dd_score +
                    weights['dd'] * dd_score +
                    weights['pf'] * pf_score +
                    weights['wr'] * wr_score +
                    weights['exp'] * exp_score)

        return composite
