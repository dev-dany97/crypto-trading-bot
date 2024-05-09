from time import sleep

from binance import ThreadedWebsocketManager

btc_price = {'error': False}
last_btc_price = {'error': False}


def btc_trade_history(msg):
    """ define how to process incoming WebSocket messages """
    if msg['e'] != 'error':
        btc_price['last'] = msg['c']
        btc_price['priceChange'] = msg['p']
        btc_price['priceChangePercent'] = msg['P']
        btc_price['bid'] = msg['b']
        btc_price['last'] = msg['a']
        btc_price['error'] = False
    else:
        btc_price['error'] = True


class Socket:
    def __init__(self):
        self.__bsm = ThreadedWebsocketManager()
        self.__bsm.start()

    def add_subscriber(self, coin):
        # get latest price from Binance API
        self.__bsm.start_symbol_ticker_socket(callback=btc_trade_history, symbol=coin)
        pass

    def __del__(self):
        # body of destructor
        # stop websocket
        self.__bsm.stop()
