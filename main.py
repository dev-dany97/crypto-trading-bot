import os
from TraderSocket import Socket, btc_price
from binance.client import Client
import pandas as pd


class Trader:

    def __init__(self, api_key, api_secret):
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__client = Client(api_key, api_secret)

    def get_coin_price(self, coin):
        # get latest price from Binance API
        return self.__client.get_symbol_ticker(symbol=coin)["price"]

    def get_wallet_coin_balance(self, coin):
        # get balance for a specific asset
        return self.__client.get_asset_balance(asset=coin)

    def get_account_information(self):
        # get balances for all assets & some account information
        return self.__client.get_account()

    def get_open_orders(self):
        """
        Get all open orders for the account
        :return: None if no open orders
        """
        return self.__client.get_open_orders() or None

    def get_coin_history(self, coin, candle_interval):
        """

        :param coin: coin name (for more see: https://data.binance.vision/?prefix=data/spot/daily/klines/)
        :param candle_interval: candle interval for coin history; valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        :return:
        """
        timestamp = self.__client._get_earliest_valid_timestamp(coin, candle_interval)
        # request historical candle (or klines) data
        # see: https://data.binance.vision/?prefix=data/spot/daily/klines/BTCUSDT/1d/
        bars = self.__client.get_historical_klines(coin, candle_interval, timestamp, limit=100)
        btc_df = pd.DataFrame(bars, columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime',
                                             'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol',
                                             'takerBuyQuoteVol', 'ignore'])
        btc_df.set_index('dateTime', inplace=True)
        # print(btc_df.head())

        # export DataFrame to csv
        btc_df.to_csv('btc_bars3.csv')

        # load DataFrame
        btc_df = pd.read_csv('btc_bars3.csv', index_col=0)

        return btc_df


class AIBot:
    def __init__(self):
        buying = self.should_be_buying()
        print(buying)

    def should_be_buying(self):
        buyingIdx = 0  # buying index
        # Kurs niedrig bzw. Kurssteigerung erkennbar?

        # War der Kurs die letzten Tage fallend?
        coin_df = trader.get_coin_history('ETHEUR', '1d')

        chart_history_high = []
        chart_history_low = []
        for index, row in coin_df.iterrows():
            chart_history_high.append(row["high"])
            chart_history_low.append(row["low"])
            # print(row["high"], row["low"])

        # check if difference is positive in the last 5 days for more then 3 days
        i = 1
        while i <= 5:
            difference = chart_history_high[-i] - chart_history_high[-(i + 1)]
            if difference < 0:
                buyingIdx += 1
            i += 1

        if buyingIdx < 3:
            return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # socket = Socket()
    # socket.add_subscriber('BTCUSDT')
    # socket.add_subscriber('ETHEUR')

    trader = Trader(api_key="YOUR_API_KEY",
                    api_secret="YOUR_API_SECRET")
    coin_price = trader.get_coin_price("ETHEUR")
    print(coin_price)
    coins_from_wallet = trader.get_wallet_coin_balance("AVAX")
    print(coins_from_wallet)
    print(trader.get_open_orders())
    # while True:
    #    if btc_price["error"] is False:
    #        print(btc_price.get("priceChangePercent", "None"))

    aibot = AIBot()

    # trader.get_coin_history('ETHEUR', '1m')
