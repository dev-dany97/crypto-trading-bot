<div align="center">

# Crypto Trading Bot

**A small Python bot that reads prices from Binance and tells you if it is a good moment to buy.**

It reads your wallet and open orders, loads daily candles and checks a simple trend rule. It never places an order on its own.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Binance API](https://img.shields.io/badge/Binance-API-F0B90B?logo=binance&logoColor=black)](https://binance-docs.github.io/apidocs/spot/en/)
[![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Tests](https://github.com/dev-dany97/crypto-trading-bot/actions/workflows/tests.yml/badge.svg)](https://github.com/dev-dany97/crypto-trading-bot/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

> [!WARNING]
> This is a hobby project to learn about trading APIs. It is **not financial advice**. The buy signal is very simple and can be wrong. Use it at your own risk.

## Contents

- [Features](#features)
- [How the signal works](#how-the-signal-works)
- [Setup](#setup)
- [Usage](#usage)
- [Tests](#tests)
- [Project structure](#project-structure)
- [Ideas for later](#ideas-for-later)
- [License](#license)

## Features

| Feature | What it does |
|---|---|
| Live price | Gets the latest price of a coin pair like `ETHEUR` |
| Wallet balance | Shows how much of a coin you hold, for example `AVAX` |
| Open orders | Lists your open orders on Binance |
| Price history | Loads daily candles (open, high, low, close, volume) as a pandas table |
| Buy signal | Looks at the last days and prints `BUY` or `WAIT` |
| Offline mode | Runs the signal on a saved CSV file. No API key needed |
| Live ticker | Optional websocket stream with bid, ask and 24h change |

The bot only **reads** data. It has no code that buys, sells or withdraws coins.

## How the signal works

The bot looks at the **daily high** of the last 5 days. For each day it checks if the high was lower than the day before.

```
day:      1     2     3     4     5     6
high:   100    99   101   100   102   103
          \_↓_/ \_↑_/ \_↓_/ \_↑_/ \_↑_/
falling days: 2 of 5  ->  BUY
```

- **2 or fewer falling days:** the price is stable or going up. The bot says `BUY`.
- **3 or more falling days:** the price is going down. The bot says `WAIT`.

You can change the number of days with `--days`.

## Setup

### Step 1: Get the code

```bash
git clone https://github.com/dev-dany97/crypto-trading-bot.git
cd crypto-trading-bot
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Create a Binance API key

1. Log in to Binance and open [API Management](https://www.binance.com/en/my/settings/api-management).
2. Create a new key. Only tick **Enable Reading**. The bot does not need trading or withdrawal rights.
3. If you can, limit the key to your own IP address.

### Step 3: Add your key

Copy the example file and put your key in it:

```bash
cp config.env.example config.env
```

```ini
BINANCE_API_KEY=your-key
BINANCE_API_SECRET=your-secret
```

`config.env` is in `.gitignore`, so your key never ends up on GitHub.

## Usage

**Try it without an account** (uses the saved ETH/EUR candles in `data/`):

```bash
python -m trader_bot --offline data/etheur_1d.csv
```

```
ETHEUR: high fell on 2 of the last 5 days -> BUY
```

**Run it with your Binance account:**

```bash
python -m trader_bot --symbol ETHEUR --asset AVAX
```

```
ETHEUR price: 2534.12
AVAX balance: {'asset': 'AVAX', 'free': '1.50000000', 'locked': '0.00000000'}
Open orders: None
ETHEUR: high fell on 3 of the last 5 days -> WAIT
```

| Option | Default | Meaning |
|---|---|---|
| `--symbol` | `ETHEUR` | Coin pair to check |
| `--asset` | none | Show the wallet balance of this coin |
| `--days` | `5` | How many days the signal looks back |
| `--offline CSV` | none | Use a saved CSV file instead of the API |

**How to use it:**

```python
from trader_bot.trader import Trader
from trader_bot.strategy import should_be_buying

trader = Trader(api_key="...", api_secret="...")
candles = trader.get_coin_history("BTCEUR", "1d", days=30, csv_file="btc.csv")
print(should_be_buying(list(candles["high"])))
```

## Tests

The tests use a fake Binance client.

```bash
pip install -r requirements-dev.txt
pytest -v
```

## Project structure

```
crypto-trading-bot/
├── trader_bot/
│   ├── __main__.py      # command line tool
│   ├── trader.py        # Binance client: prices, wallet, orders, candles
│   ├── strategy.py      # buy signal
│   └── ticker.py        # live prices via websocket
├── tests/               # pytest tests with a fake client
├── data/
│   └── etheur_1d.csv    # daily ETH/EUR candles (Jan 2020 to Oct 2021)
├── config.env.example   # template for your API key
└── .github/workflows/   # CI
```

## Ideas for later

- [ ] Add more indicators like moving averages or RSI
- [ ] Send the signal as a push message
- [ ] Backtest the rule on the saved candles
- [ ] Paper trading on the Binance testnet

## License

[MIT](LICENSE) © Daniel Mohles
