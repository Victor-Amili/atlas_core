import sys

from atlas_core.analytics.report import Report
sys.path.insert(0, '.')

from datetime import datetime, timedelta
from atlas_core.data.real_fetcher import yahoo
from atlas_core.strategies.buy_hold import BuyAndHold
from atlas_core.strategies.bollinger import BollingerBands
from atlas_core.strategies.rsi_bollinger import RSIBollingerCombo
from atlas_core.strategies.filtered_bollinger import FilteredBollinger
from atlas_core.strategies.stochastic import StochasticStrategy
from atlas_core.tournament.engine import Tournament

# Yahoo limits hourly data to ~730 days (2 years)
start = (datetime.now() - timedelta(days=700)).strftime('%Y-%m-%d')

assets = [
    {'ticker': 'SPY',   'type': 'stock'},
    {'ticker': 'AAPL',  'type': 'stock'},
    {'ticker': 'BTC-USD','type': 'crypto'},
    {'ticker': 'ETH-USD','type': 'crypto'},
]

for asset in assets:
    ticker = asset['ticker']
    asset_type = asset['type']
    
    print(f"\n{'='*75}")
    print(f"🚀 TESTING: {ticker} | HOURLY | {start} → NOW")
    print(f"{'='*75}")
    
    data = yahoo(ticker, start=start, interval='1h')
    if data is None or len(data) < 100:
        print(f"⚠️  Skipping {ticker} — insufficient data")
        continue
    
    # Scale parameters for hourly timeframe
    if asset_type == 'stock':
        # 6.5 trading hours/day
        bb_period = 130       # 20 days × 6.5h
        rsi_period = 91       # 14 days × 6.5h
        stoch_k = 91
        stoch_d = 20          # 3 days × 6.5h ≈ 20
    else:
        # Crypto trades 24/7
        bb_period = 480       # 20 days × 24h
        rsi_period = 336      # 14 days × 24h
        stoch_k = 336
        stoch_d = 72          # 3 days × 24h
    
    strategies = [
        BuyAndHold(),
        BollingerBands(period=bb_period, std_dev=2),
        RSIBollingerCombo(rsi_period=rsi_period, bb_period=bb_period, rsi_buy=35, rsi_sell=65),
        FilteredBollinger(bb_period=bb_period, adx_threshold=25),
        StochasticStrategy(k_period=stoch_k, d_period=stoch_d, oversold=20, overbought=80),
    ]
    
    tournament = Tournament(strategies, data, initial_capital=10000)
    results = tournament.run()
    tournament.leaderboard()
    
    # Generate comparison table
    print("\n📊 Detailed Comparison:")
    table = Report.comparison_table(results)
    print(table.to_string(index=False))

print(f"\n{'='*75}")
print("🏁 ALL ASSETS TESTED")
print(f"{'='*75}")