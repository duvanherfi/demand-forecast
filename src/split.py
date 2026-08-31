"""Split by time, never at random.

A random split lets the model see February while being scored on January, which
is not a mistake a deployed model can make. It inflates every metric and the
inflation is invisible: nothing errors, the numbers just come out good.
"""

import pandas as pd

from src.config import TEST_MONTH, TRAIN_MONTHS, VAL_MONTH


def _month_of(frame: pd.DataFrame) -> pd.Series:
    return frame.pickup_hour.dt.strftime("%Y-%m")


def split(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    month = _month_of(frame)
    train = frame[month.isin(TRAIN_MONTHS)].reset_index(drop=True)
    val = frame[month == VAL_MONTH].reset_index(drop=True)
    return train, val


def load_test(frame: pd.DataFrame) -> pd.DataFrame:
    """Held out until the project is finished. Calling this is a decision."""
    return frame[_month_of(frame) == TEST_MONTH].reset_index(drop=True)
