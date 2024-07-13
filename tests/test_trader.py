from unittest.mock import MagicMock

from trader_bot.ticker import parse_ticker_message
from trader_bot.trader import Trader, klines_to_dataframe

KLINES = [
    [1578009600000, "113.8", "120.0", "113.8", "120.0", "50.7", 1578095999999, "6021.0", 56, "35.4", "4205.0", "0"],
    [1578096000000, "120.0", "120.39", "119.29", "120.39", "21.8", 1578182399999, "2611.2", 22, "11.2", "1345.4", "0"],
]


def fake_client():
    client = MagicMock()
    client.get_symbol_ticker.return_value = {"symbol": "ETHEUR", "price": "2500.50"}
    client.get_asset_balance.return_value = {"asset": "AVAX", "free": "1.5", "locked": "0"}
    client.get_open_orders.return_value = []
    client.get_historical_klines.return_value = KLINES
    return client


def test_get_coin_price_returns_float():
    trader = Trader(client=fake_client())
    assert trader.get_coin_price("ETHEUR") == 2500.50


def test_wallet_balance():
    trader = Trader(client=fake_client())
    assert trader.get_wallet_coin_balance("AVAX")["free"] == "1.5"


def test_no_open_orders_returns_none():
    trader = Trader(client=fake_client())
    assert trader.get_open_orders() is None


def test_coin_history(tmp_path):
    client = fake_client()
    trader = Trader(client=client)
    csv_file = tmp_path / "candles.csv"
    coin_df = trader.get_coin_history("ETHEUR", "1d", days=2, csv_file=csv_file)

    client.get_historical_klines.assert_called_once_with("ETHEUR", "1d", "2 days ago UTC")
    assert list(coin_df["high"]) == [120.0, 120.39]
    assert csv_file.exists()


def test_klines_to_dataframe_uses_float_prices():
    df = klines_to_dataframe(KLINES)
    assert df["close"].dtype == float
    assert df.index.name == "dateTime"


def test_parse_ticker_message():
    msg = {"e": "24hrTicker", "c": "2500", "p": "12", "P": "0.5", "b": "2499", "a": "2501"}
    assert parse_ticker_message(msg) == {
        "error": False, "last": "2500", "priceChange": "12",
        "priceChangePercent": "0.5", "bid": "2499", "ask": "2501",
    }


def test_parse_ticker_error():
    assert parse_ticker_message({"e": "error", "m": "boom"}) == {"error": True}
