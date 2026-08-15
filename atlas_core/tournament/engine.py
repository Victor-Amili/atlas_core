"""
Strategy Tournament
Compare multiple strategies across assets and timeframes.
"""
import pandas as pd
from ..backtester.engine import Backtester
from ..analytics.report import Report

class Tournament:
    """
    Run multiple strategies and rank them.
    """

    def __init__(self, strategies, data, initial_capital=10000,
                 risk_per_trade=0.02, stop_loss_pct=0.05):
        self.strategies = strategies
        self.data = data
        self.initial_capital = initial_capital
        self.risk_per_trade = risk_per_trade
        self.stop_loss_pct = stop_loss_pct
        self.results = []

    def run(self):
        """Run all strategies and collect results."""
        print(f"\n🏆 STRATEGY TOURNAMENT")
        print(f"   Asset: {len(self.data)} days of data")
        print(f"   Strategies: {len(self.strategies)}")
        print(f"   Capital: ${self.initial_capital:,}")
        print("-" * 60)

        for strategy in self.strategies:
            bt = Backtester(strategy, self.initial_capital, 
                           self.risk_per_trade, self.stop_loss_pct)
            result = bt.run(self.data)
            result.composite = Report.composite_score(result)
            self.results.append(result)
            print(f"✅ {result.strategy_name:30s} | {result.total_return:+6.1f}% | "
                  f"{result.total_trades:2d} trades | WR {result.win_rate:4.0f}% | "
                  f"Score {result.composite:5.1f}")

        # Sort by composite score
        self.results.sort(key=lambda x: x.composite, reverse=True)
        return self.results

    def leaderboard(self):
        """Print formatted leaderboard."""
        print(f"\n{'='*80}")
        print(f"🏆 LEADERBOARD (Ranked by Composite Score)")
        print(f"{'='*80}")
        print(f"{'Rank':<6} {'Strategy':<30} {'Return':>10} {'Trades':>8} {'WR':>6} {'PF':>6} {'DD':>6} {'Score':>8}")
        print("-"*80)

        for i, r in enumerate(self.results, 1):
            print(f"{i:<6} {r.strategy_name:<30} {r.total_return:>+9.1f}% {r.total_trades:>8d} "
                  f"{r.win_rate:>5.0f}% {r.profit_factor:>6.2f} {r.max_drawdown:>5.1f}% {r.composite:>8.1f}")

        print(f"{'='*80}")

    def best_strategy(self):
        """Return the top-performing strategy result."""
        if not self.results:
            return None
        return self.results[0]

    def export_csv(self, filepath):
        """Export results to CSV."""
        data = []
        for r in self.results:
            data.append({
                'strategy': r.strategy_name,
                'final_capital': r.final_capital,
                'total_return': r.total_return,
                'total_trades': r.total_trades,
                'win_rate': r.win_rate,
                'profit_factor': r.profit_factor,
                'max_drawdown': r.max_drawdown,
                'expectancy': r.expectancy,
                'composite_score': r.composite
            })
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        print(f"\n✅ Results exported to {filepath}")
