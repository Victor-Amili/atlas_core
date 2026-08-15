"""
Atlas Core Demo
Run all strategies on synthetic data and generate comparison report.
"""
import sys
sys.path.insert(0, '.')

import matplotlib.pyplot as plt
from atlas_core.data.loader import generate_synthetic
from atlas_core.strategies.buy_hold import BuyAndHold
from atlas_core.strategies.bollinger import BollingerBands
from atlas_core.strategies.rsi_bollinger import RSIBollingerCombo
from atlas_core.strategies.filtered_bollinger import FilteredBollinger
from atlas_core.strategies.stochastic import StochasticStrategy
from atlas_core.strategies.ma_rsi_filter import MAWithRSIFilter
from atlas_core.strategies.macd_momentum import MACDMomentum
from atlas_core.strategies.keltner import KeltnerChannels
from atlas_core.tournament.engine import Tournament
from atlas_core.analytics.report import Report

# Generate test data
print("📊 Generating synthetic market data...")
data = generate_synthetic(days=800, seed=42)
print(f"   {len(data)} days | Price range: ${data['close'].min():.1f} - ${data['close'].max():.1f}")

# Create all strategies
strategies = [
    BuyAndHold(),
    BollingerBands(period=20, std_dev=2),
    RSIBollingerCombo(rsi_buy=35, rsi_sell=65),
    FilteredBollinger(adx_threshold=25),
    StochasticStrategy(oversold=20, overbought=80),
    MAWithRSIFilter(fast=10, slow=50),
    MACDMomentum(),
    KeltnerChannels(),
]

# Run tournament
print("\n🏆 Running Strategy Tournament...")
tournament = Tournament(strategies, data, initial_capital=10000)
results = tournament.run()

# Show leaderboard
tournament.leaderboard()

# Generate comparison table
print("\n📊 Detailed Comparison:")
table = Report.comparison_table(results)
print(table.to_string(index=False))

# Generate plots
print("\n📈 Generating charts...")
Report.plot_equity_curves(results, save_path='results/equity_curves.png')
Report.plot_returns_bar(results, save_path='results/returns_comparison.png')

# Export results
import os
os.makedirs('results', exist_ok=True)
tournament.export_csv('results/tournament_results.csv')

print("\n✅ Demo complete! Check the 'results/' folder for outputs.")
