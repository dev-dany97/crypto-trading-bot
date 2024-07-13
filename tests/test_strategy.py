from pathlib import Path

import pandas as pd
import pytest

from trader_bot.strategy import count_falling_days, should_be_buying

DATA = Path(__file__).resolve().parent.parent / "data" / "etheur_1d.csv"


def test_rising_prices_give_buy_signal():
    highs = [100, 101, 102, 103, 104, 105]
    assert count_falling_days(highs) == 0
    assert should_be_buying(highs) is True


def test_falling_prices_give_no_buy_signal():
    highs = [105, 104, 103, 102, 101, 100]
    assert count_falling_days(highs) == 5
    assert should_be_buying(highs) is False


def test_two_falling_days_still_buy():
    highs = [100, 99, 101, 100, 102, 103]
    assert count_falling_days(highs) == 2
    assert should_be_buying(highs) is True


def test_three_falling_days_wait():
    highs = [100, 99, 101, 100, 99, 103]
    assert count_falling_days(highs) == 3
    assert should_be_buying(highs) is False


def test_only_last_days_count():
    highs = [200, 100, 101, 102, 103, 104, 105]
    assert count_falling_days(highs, days=5) == 0


def test_too_few_candles_raise_error():
    with pytest.raises(ValueError):
        count_falling_days([1, 2, 3], days=5)


def test_signal_on_saved_candles():
    coin_df = pd.read_csv(DATA, index_col=0)
    assert len(coin_df) > 600
    assert isinstance(should_be_buying(list(coin_df["high"])), bool)
