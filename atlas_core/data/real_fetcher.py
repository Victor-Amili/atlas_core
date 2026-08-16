"""
Real Data Fetcher
Fetches daily data from Yahoo Finance.
"""
import pandas as pd
import numpy as np

def yahoo(ticker, start='2020-01-01', end=None):
    """
    Fetch DAILY data from Yahoo Finance.
    
    Tickers:
    - Stocks: 'AAPL', 'TSLA', 'NVDA', 'MSFT'
    - ETFs: 'SPY', 'QQQ', 'VTI'
    - Crypto: 'BTC-USD', 'ETH-USD', 'SOL-USD'
    - Forex: 'EURUSD=X', 'GBPUSD=X'
    - Commodities: 'GC=F' (Gold), 'CL=F' (Oil)
    """
    try:
        import yfinance as yf
        print(f"Downloading {ticker} daily data from Yahoo Finance...")
        df = yf.download(ticker, start=start, end=end, interval='1d', progress=False)
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        col_map = {
            'Open': 'open', 'High': 'high', 'Low': 'low',
            'Close': 'close', 'Adj Close': 'close', 'Volume': 'volume'
        }
        df = df.rename(columns=col_map)
        df = df.dropna(subset=['open', 'high', 'low', 'close'])
        
        print(f"   Loaded {len(df)} days | {df.index[0].date()} -> {df.index[-1].date()}")
        print(f"   Price: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
        return df
        
    except ImportError:
        print("Install yfinance: pip install yfinance")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None