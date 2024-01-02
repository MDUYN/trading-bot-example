from datetime import datetime
import sys

from investing_algorithm_framework import PortfolioConfiguration, \
    pretty_print_backtest, MarketCredential

from app import app


def convert_to_datetime(datetime_str):
    try:
        return datetime.strptime(datetime_str, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid datetime format for '{datetime_str}'. Please use the format 'YYYY-MM-DD HH:MM:SS'")
        sys.exit(1)


app.add_portfolio_configuration(
    PortfolioConfiguration(
        market="BITVAVO",
        trading_symbol="EUR",
        initial_balance=400
    )
)

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(
            "Error: Please provide two datetime "
            "strings as command-line arguments."
        )
        sys.exit(1)

    # Get datetime strings from command-line arguments
    start_date_str = sys.argv[1]
    end_date_str = sys.argv[2]

    # Convert datetime strings to datetime objects
    start_date = convert_to_datetime(start_date_str)
    end_date = convert_to_datetime(end_date_str)
    backtest_report = app.backtest(
        start_date=start_date,
        end_date=end_date,
        pending_order_check_interval="2h"
    )
    pretty_print_backtest(backtest_report)
