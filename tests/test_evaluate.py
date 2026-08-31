import numpy as np
import pandas as pd

from src.evaluate import score


class Constant:
    def __init__(self, value, name):
        self.value, self.name = value, name

    def fit(self, train):
        return self

    def predict(self, frame):
        return np.full(len(frame), self.value)


def test_scoreboard_ranks_the_better_predictor_first():
    hours = pd.date_range("2025-01-01", periods=48, freq="h")
    train = pd.DataFrame({"pickup_hour": hours, "zone_id": 1, "trips": 10})
    val = pd.DataFrame({"pickup_hour": hours, "zone_id": 1, "trips": 10})

    table = score([Constant(10, "exact"), Constant(0, "hopeless")], train, val)

    assert list(table.predictor) == ["exact", "hopeless"]
    assert table.iloc[0].mae == 0.0
    assert table.iloc[1].mae == 10.0
