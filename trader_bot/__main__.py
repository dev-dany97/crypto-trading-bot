import os

from dotenv import load_dotenv

from trader_bot.strategy import should_be_buying
from trader_bot.trader import Trader


def main():
    load_dotenv('config.env')
    trader = Trader(api_key=os.environ["BINANCE_API_KEY"],
                    api_secret=os.environ["BINANCE_API_SECRET"])

    print("ETHEUR price:", trader.get_coin_price("ETHEUR"))
    print("AVAX balance:", trader.get_wallet_coin_balance("AVAX"))
    print("Open orders:", trader.get_open_orders())

    coin_df = trader.get_coin_history("ETHEUR", "1d")
    print("Buy signal:", should_be_buying(list(coin_df["high"])))


if __name__ == '__main__':
    main()
