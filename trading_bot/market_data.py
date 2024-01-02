from datetime import datetime, timedelta

from investing_algorithm_framework import CCXTOHLCVMarketDataSource, \
    CCXTTickerMarketDataSource

bitvavo_btc_eur_ohlcv_1d = CCXTOHLCVMarketDataSource(
    identifier="BTC/EUR-ohlcv",
    market="bitvavo",
    symbol="BTC/EUR",
    timeframe="2h",
    # We want to retrieve data from the last 3 days (3 days * 24 hours * 4(15m) = 288 candlesticks)
    start_date_func=lambda: datetime.utcnow() - timedelta(days=17)
)
# Ticker data to track orders, trades and positions we make with symbol BTC/EUR
bitvavo_btc_eur_ticker = CCXTTickerMarketDataSource(
    identifier="BTC/EUR-ticker",
    market="bitvavo",
    symbol="BTC/EUR",
    backtest_timeframe="2h" # Because we will run out trading bot every 2 hours
)
