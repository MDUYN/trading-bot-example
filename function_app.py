import azure.functions as func
from investing_algorithm_framework import StatelessAction, \
    PortfolioConfiguration, MarketCredential

from app import app as trading_bot_app

trading_bot_app.add_portfolio_configuration(
    PortfolioConfiguration(
        market="BITVAVO",
        trading_symbol="EUR"
    )
)
trading_bot_app.add_market_credential(
    MarketCredential(
        market="BITVAVO",
        api_key="<YOUR_BITVAVO_API_KEY>",
        secret_key="<YOUR_BITVAVO_SECRET_KEY>"
    )
)
app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 */2 * * * *",
    arg_name="myTimer",
    run_on_startup=True,
    use_monitor=False
)
def trading_bot_azure_function(myTimer: func.TimerRequest) -> None:
    trading_bot_app.run(payload={"ACTION": StatelessAction.RUN_STRATEGY.value})
