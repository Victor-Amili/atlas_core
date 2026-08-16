import sys
sys.path.insert(0, '.')

from atlas_core.analytics.report import Report
from atlas_core.data.real_fetcher import yahoo
from atlas_core.strategies.buy_hold import BuyAndHold
from atlas_core.strategies.bollinger import BollingerBands
from atlas_core.strategies.rsi_bollinger import RSIBollingerCombo
from atlas_core.strategies.filtered_bollinger import FilteredBollinger
from atlas_core.strategies.stochastic import StochasticStrategy
from atlas_core.tournament.engine import Tournament

# CHANGE THIS to test different assets
ticker = 'SPY'        # SPY = S&P 500 (safest)
ticker = 'BTC-USD'  # Bitcoin (volatile)
ticker = 'AAPL'     # Apple (single stock)
# ticker = 'ETH-USD'  # Ethereum

start = '2020-01-01'

print(f"Fetching {ticker} daily data...")
data = yahoo(ticker, start=start)

if data is None:
    print("Failed. Run: pip install yfinance")
    sys.exit(1)

print(f"Loaded {len(data)} daily candles")

strategies = [
    BuyAndHold(),
    BollingerBands(period=20, std_dev=2),
    RSIBollingerCombo(rsi_buy=35, rsi_sell=65),
    FilteredBollinger(adx_threshold=25),
    StochasticStrategy(oversold=20, overbought=80),
]

tournament = Tournament(strategies, data, initial_capital=10000)
results = tournament.run()
tournament.leaderboard()

# Generate comparison table
print("\n📊 Detailed Comparison:")
table = Report.comparison_table(results)
print(table.to_string(index=False))