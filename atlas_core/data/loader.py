"""
Data Loader
Fetch historical market data from various sources.
"""
import pandas as pd
import numpy as np

def from_yahoo(ticker, start='2020-01-01', end=None, interval='1d'):
    """
    Load data from Yahoo Finance using yfinance.

    Args:
        ticker: Stock/crypto symbol (e.g., 'AAPL', 'BTC-USD')
        start: Start date
        end: End date
        interval: '1d', '1h', etc.

    Returns:
        DataFrame with OHLCV columns
    """
    try:
        import yfinance as yf
        df = yf.download(ticker, start=start, end=end, interval=interval, progress=False)

        # Flatten multi-index columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Rename columns to standard names
        column_map = {
            'Open': 'open', 'High': 'high', 'Low': 'low', 
            'Close': 'close', 'Adj Close': 'close', 'Volume': 'volume'
        }
        df = df.rename(columns=column_map)

        # Ensure all required columns exist
        required = ['open', 'high', 'low', 'close']
        for col in required:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Drop rows with NaN in required columns
        df = df.dropna(subset=required)

        return df

    except ImportError:
        print("❌ yfinance not installed. Install with: pip install yfinance")
        return None
    except Exception as e:
        print(f"❌ Error loading {ticker}: {e}")
        return None

def from_csv(filepath):
    """Load data from local CSV file."""
    df = pd.read_csv(filepath, parse_dates=True, index_col=0)
    df.columns = df.columns.str.lower()
    return df

def generate_synthetic(days=500, seed=42):
    """Generate synthetic market data for testing."""
    np.random.seed(seed)
    returns = np.random.normal(0.0003, 0.015, days)
    price = 100 * np.exp(np.cumsum(returns))
    dates = pd.date_range(start='2023-01-01', periods=days, freq='D')

    df = pd.DataFrame({
        'open': price * (1 + np.random.normal(0, 0.001, days)),
        'high': price * (1 + abs(np.random.normal(0, 0.008, days))),
        'low': price * (1 - abs(np.random.normal(0, 0.008, days))),
        'close': price,
        'volume': np.random.randint(1000000, 10000000, days)
    }, index=dates)
    return df
