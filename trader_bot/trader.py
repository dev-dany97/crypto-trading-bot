import pandas as pd

KLINE_COLUMNS = ['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime',
                 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol',
                 'takerBuyQuoteVol', 'ignore']
PRICE_COLUMNS = ['open', 'high', 'low', 'close', 'volume']


def klines_to_dataframe(bars):
    """ turn raw Binance klines into a DataFrame with float prices """
    df = pd.DataFrame(bars, columns=KLINE_COLUMNS)
    df.set_index('dateTime', inplace=True)
    df[PRICE_COLUMNS] = df[PRICE_COLUMNS].astype(float)
    return df


class Trader:
    """ read only wrapper around the Binance client """

    def __init__(self, api_key=None, api_secret=None, client=None):
        if client is None:
            from binance.client import Client
            client = Client(api_key, api_secret)
        self.__client = client

    def get_coin_price(self, coin):
        # get latest price from Binance API
        return float(self.__client.get_symbol_ticker(symbol=coin)["price"])

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

    def get_coin_history(self, coin, candle_interval='1d', days=30, csv_file=None):
        """
        :param coin: coin pair, e.g. ETHEUR (for more see: https://data.binance.vision/?prefix=data/spot/daily/klines/)
        :param candle_interval: valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        :param days: how many days to load
        :param csv_file: optional path to save the candles as csv
        :return: DataFrame with one row per candle
        """
        bars = self.__client.get_historical_klines(coin, candle_interval, f"{days} days ago UTC")
        coin_df = klines_to_dataframe(bars)
        if csv_file:
            coin_df.to_csv(csv_file)
        return coin_df
