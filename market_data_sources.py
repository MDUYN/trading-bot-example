from datetime import datetime, timedelta

from investing_algorithm_framework import CCXTOHLCVMarketDataSource, \
    CCXTTickerMarketDataSource

bitvavo_btc_eur_ohlcv_1d = CCXTOHLCVMarketDataSource(
    identifier="BTC/EUR-ohlcv",
    market="coinbase",
    symbol="BTC/EUR",
    timeframe="1d",
    # We want to retrieve data from the last 3 days (3 days * 24 hours * 4(15m) = 288 candlesticks)
    start_date_func=lambda: datetime.utcnow() - timedelta(days=200)
)
# Ticker data to track orders, trades and positions we make with symbol BTC/EUR
bitvavo_btc_eur_ticker = CCXTTickerMarketDataSource(
    identifier="BTC/EUR-ticker",
    market="coinbase",
    symbol="BTC/EUR",
    backtest_timeframe="1d"
)
