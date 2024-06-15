def count_falling_days(highs, days=5):
    """ count how often the daily high was lower than the day before """
    if len(highs) < days + 1:
        raise ValueError(f"need at least {days + 1} candles, got {len(highs)}")
    falling = 0
    for i in range(1, days + 1):
        if highs[-i] - highs[-(i + 1)] < 0:
            falling += 1
    return falling


def should_be_buying(highs, days=5, max_falling_days=2):
    """
    Very simple buy signal.
    Buy if the daily high did not fall on more than max_falling_days of the last days.
    """
    return count_falling_days(highs, days) <= max_falling_days
