def parse_ticker_message(msg):
    """ turn a Binance 24h ticker message into a small dict """
    if msg.get('e') == 'error':
        return {'error': True}
    return {
        'error': False,
        'last': msg['c'],
        'priceChange': msg['p'],
        'priceChangePercent': msg['P'],
        'bid': msg['b'],
        'ask': msg['a'],
    }


class TickerSocket:
    """ live prices via the Binance websocket """

    def __init__(self):
        from binance import ThreadedWebsocketManager
        self.prices = {}
        self.__bsm = ThreadedWebsocketManager()
        self.__bsm.start()

    def add_subscriber(self, coin):
        def on_message(msg):
            self.prices[coin] = parse_ticker_message(msg)
        self.__bsm.start_symbol_ticker_socket(callback=on_message, symbol=coin)

    def stop(self):
        self.__bsm.stop()
