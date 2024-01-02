import pathlib

from investing_algorithm_framework import create_app, RESOURCE_DIRECTORY

from trading_bot import bitvavo_btc_eur_ohlcv_1d, bitvavo_btc_eur_ticker, \
    ImprovedGoldenCrossDeathCrossTradingStrategy

# Set the resource directory to the directory of this file. The framework
# will store all resources in this directory such databases and backtest data.
app = create_app({RESOURCE_DIRECTORY: pathlib.Path(__file__).parent.resolve()})
app.add_market_data_source(bitvavo_btc_eur_ohlcv_1d)
app.add_market_data_source(bitvavo_btc_eur_ticker)
app.add_strategy(ImprovedGoldenCrossDeathCrossTradingStrategy)
