"""Error metrics, and one that is here only to show why it does not fit.

MAE is the headline: it is in trips, so "we are off by 4 trips an hour" is a
sentence anyone in the business understands.

WAPE is the scale-free companion — total error over total volume — which lets a
quiet zone and Penn Station be compared without the quiet zone dominating.

MAPE is the one everybody reaches for and it cannot be used here. It divides by
the actual value, and 41 of the 261 zones see fewer than 100 trips in a whole
month, so zero-trip hours are ordinary. Dividing by them gives infinity.
"""

import numpy as np


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean(np.abs(y_true - y_pred)))


def wape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sum(np.abs(y_true - y_pred)) / np.sum(y_true))


def mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Kept to demonstrate the failure. Never put this in the scoreboard."""
    with np.errstate(divide="ignore", invalid="ignore"):
        return float(np.mean(np.abs((y_true - y_pred) / y_true)))
