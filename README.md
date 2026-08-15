# Atlas Core

A quantitative research framework for backtesting and comparing trading strategies.

## Philosophy

Instead of searching for one "holy grail" strategy, Atlas Core tests many strategies
across market conditions and ranks them by composite score — not just win rate.

## Architecture

```
Data → Indicators → Strategy → Risk → Backtest → Analytics
```

Every module is independent. Swap indicators without touching strategies.
Swap strategies without touching the backtester.

## Quick Start

```python
from atlas_core.data.loader import from_yahoo
from atlas_core.strategies.bollinger import BollingerBands
from atlas_core.backtester.engine import Backtester

# Load data
data = from_yahoo('AAPL', start='2020-01-01')

# Create strategy
strategy = BollingerBands(period=20, std_dev=2)

# Backtest
bt = Backtester(strategy, initial_capital=10000)
result = bt.run(data)
result.summary()
```

## Strategy Tournament

```python
from atlas_core.tournament.engine import Tournament
from atlas_core.strategies import *

strategies = [
    BollingerBands(),
    RSIBollingerCombo(),
    StochasticStrategy(),
    FilteredBollinger(),
]

tournament = Tournament(strategies, data)
results = tournament.run()
tournament.leaderboard()
```

## Included Strategies

- Buy & Hold (benchmark)
- Bollinger Bands
- RSI + Bollinger Combo
- Filtered Bollinger (ADX filter)
- Stochastic Oscillator
- MA + RSI Filter
- MACD Momentum
- Keltner Channels

## Risk Management

Every strategy uses:
- 2% risk per trade
- 5% stop loss
- Position sizing based on volatility

## License

MIT
