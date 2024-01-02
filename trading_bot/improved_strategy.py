import pandas as pd
import tulipy as tp
from investing_algorithm_framework import TimeUnit, \
    TradingStrategy, Algorithm, OrderSide, Task


def is_crossover(fast_series, slow_series):
    """
    Expect df to have columns: Date, ma_<period_one>, ma_<period_two>.
    With the given date time it will check if the ma_<period_one> is a
    crossover with the ma_<period_two>
    """

    return fast_series[-2] <= slow_series[-2] \
           and fast_series[-1] > slow_series[-1]


def is_crossunder(fast_series, slow_series):
    """
    Expect df to have columns: Date, ma_<period_one>, ma_<period_two>.
    With the given date time it will check if the ma_<period_one> is a
    crossover with the ma_<period_two>
    """

    return fast_series[-2] >= slow_series[-2] \
        and fast_series[-1] < slow_series[-1]


def is_above_trend(fast_series, slow_series):
    return fast_series[-1] > slow_series[-1]


def is_within_rsi_bounds(rsi_series, lower_bound, upper_bound):
    return lower_bound <= rsi_series[-1] <= upper_bound


class ImprovedGoldenCrossDeathCrossTradingStrategy(TradingStrategy):
    time_unit = TimeUnit.HOUR
    interval = 2
    market_data_sources = [
        "BTC/EUR-ohlcv",
        "BTC/EUR-ticker",
    ]
    symbols = ["BTC/EUR"]

    def apply_strategy(self, algorithm: Algorithm, market_data: dict):

        for symbol in self.symbols:
            target_symbol = symbol.split('/')[0]

            # Don't open a new order when we already have an open order
            if algorithm.has_open_orders(target_symbol):
                continue

            ohlcv_data = market_data[f"{symbol}-ohlcv"]
            df = pd.DataFrame(
                ohlcv_data,
                columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
            )
            fast = tp.sma(df["Close"].to_numpy(), period=9)
            slow = tp.ema(df["Close"].to_numpy(), period=50)
            trend = tp.sma(df["Close"].to_numpy(), period=100)
            price = market_data[f"{symbol}-ticker"]["bid"]

            # Sell when crossunder with trend
            if algorithm.has_position(target_symbol) \
                    and is_crossunder(fast, trend):
                algorithm.close_position(target_symbol)

            # Only buy when above trend and crossover
            elif not algorithm.has_position(target_symbol) \
                    and is_crossover(fast, slow):
                algorithm.create_limit_order(
                    target_symbol=target_symbol,
                    order_side=OrderSide.BUY,
                    price=price,
                    percentage_of_portfolio=25,
                    precision=4
                )

            # Checking manual stopp losses with a 6% stop loss
            open_trades = algorithm.get_open_trades(target_symbol)

            for open_trade in open_trades:
                filtered_df = df[open_trade.opened_at <= df['Datetime']]
                close_prices = filtered_df['Close'].tolist()
                current_price = market_data[f"{symbol}-ticker"]

                if open_trade.is_manual_stop_loss_trigger(
                    prices=close_prices,
                    current_price=current_price["bid"],
                    stop_loss_percentage=6
                ):
                    algorithm.close_trade(open_trade)
