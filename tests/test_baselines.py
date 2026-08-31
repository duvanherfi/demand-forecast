import numpy as np
import pandas as pd
import pytest

from src.baselines import GlobalMean, LastWeekSameHour, ZoneHourWeekdayMean, ZoneMean


@pytest.fixture
def train():
    hours = pd.date_range("2025-01-01", "2025-01-28 23:00", freq="h")
    rows = []
    for hour in hours:
        rows.append({"pickup_hour": hour, "zone_id": 1, "trips": 10})
        rows.append({"pickup_hour": hour, "zone_id": 2, "trips": 20})
    return pd.DataFrame(rows)


def test_global_mean_predicts_one_number_everywhere(train):
    pred = GlobalMean().fit(train).predict(train)
    assert np.allclose(pred, 15.0)


def test_zone_mean_predicts_per_zone(train):
    pred = ZoneMean().fit(train).predict(train)
    assert np.allclose(pred[train.zone_id == 1], 10.0)
    assert np.allclose(pred[train.zone_id == 2], 20.0)


def test_zone_hour_weekday_mean_falls_back_when_a_zone_is_unseen(train):
    unseen = pd.DataFrame(
        {"pickup_hour": [pd.Timestamp("2025-02-01 03:00")], "zone_id": [999], "trips": [0]}
    )
    pred = ZoneHourWeekdayMean().fit(train).predict(unseen)
    # A zone absent from training must still get a number, not a NaN. Falling
    # back to the global mean is the honest default.
    assert not np.isnan(pred).any()


def test_last_week_same_hour_looks_exactly_seven_days_back(train):
    model = LastWeekSameHour().fit(train)
    target = pd.DataFrame(
        {"pickup_hour": [pd.Timestamp("2025-01-29 05:00")], "zone_id": [2], "trips": [0]}
    )
    # 2025-01-22 05:00 in zone 2 had 20 trips.
    assert np.allclose(model.predict(target), 20.0)
