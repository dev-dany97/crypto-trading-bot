import argparse
import os

import pandas as pd
from dotenv import load_dotenv

from trader_bot.strategy import count_falling_days, should_be_buying
from trader_bot.trader import Trader


def parse_args(argv=None):
    parser = argparse.ArgumentParser(prog="trader_bot",
                                     description="Read Binance prices and show a simple buy signal.")
    parser.add_argument("--symbol", default="ETHEUR", help="coin pair, default: ETHEUR")
    parser.add_argument("--asset", default=None, help="show the wallet balance of this asset, e.g. AVAX")
    parser.add_argument("--days", type=int, default=5, help="days to look back for the signal, default: 5")
    parser.add_argument("--offline", metavar="CSV", default=None,
                        help="use saved daily candles from a csv file instead of the API")
    return parser.parse_args(argv)


def print_signal(symbol, highs, days):
    falling = count_falling_days(highs, days)
    signal = "BUY" if should_be_buying(highs, days) else "WAIT"
    print(f"{symbol}: high fell on {falling} of the last {days} days -> {signal}")
    return signal


def main(argv=None):
    args = parse_args(argv)

    if args.offline:
        coin_df = pd.read_csv(args.offline, index_col=0)
        return print_signal(args.symbol, list(coin_df["high"]), args.days)

    load_dotenv('config.env')
    trader = Trader(api_key=os.environ["BINANCE_API_KEY"],
                    api_secret=os.environ["BINANCE_API_SECRET"])

    print(f"{args.symbol} price:", trader.get_coin_price(args.symbol))
    if args.asset:
        print(f"{args.asset} balance:", trader.get_wallet_coin_balance(args.asset))
    print("Open orders:", trader.get_open_orders())

    coin_df = trader.get_coin_history(args.symbol, "1d", days=args.days + 5)
    return print_signal(args.symbol, list(coin_df["high"]), args.days)


if __name__ == '__main__':
    main()
