import pandas as pd
import pytest

from src.split import load_test, split


@pytest.fixture
def frame():
    hours = pd.date_range("2025-01-01", "2025-12-31 23:00", freq="h")
    return pd.DataFrame({"pickup_hour": hours, "zone_id": 1, "trips": range(len(hours))})


def test_no_validation_row_precedes_the_last_training_row(frame):
    train, val = split(frame)
    assert train.pickup_hour.max() < val.pickup_hour.min()


def test_split_loses_no_rows_and_duplicates_none(frame):
    train, val = split(frame)
    test = load_test(frame)
    total = len(train) + len(val) + len(test)
    assert total == len(frame)
    assert set(train.pickup_hour) & set(val.pickup_hour) == set()
    assert set(val.pickup_hour) & set(test.pickup_hour) == set()


def test_split_never_hands_back_the_test_month(frame):
    train, val = split(frame)
    december = pd.Timestamp("2025-12-01")
    assert (train.pickup_hour >= december).sum() == 0
    assert (val.pickup_hour >= december).sum() == 0
