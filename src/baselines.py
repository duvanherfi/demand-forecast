"""The four predictors every model has to beat.

They are not strawmen. ZoneHourWeekdayMean encodes the fact that Tuesday 8am in
midtown looks like last Tuesday 8am in midtown, which is most of what there is
to know. A gradient boosting model that cannot beat it has learnt nothing.
"""

import numpy as np
import pandas as pd


class GlobalMean:
    name = "global mean"

    def fit(self, train: pd.DataFrame) -> "GlobalMean":
        self.value = train.trips.mean()
        return self

    def predict(self, frame: pd.DataFrame) -> np.ndarray:
        return np.full(len(frame), self.value)


class ZoneMean:
    name = "zone mean"

    def fit(self, train: pd.DataFrame) -> "ZoneMean":
        self.fallback = train.trips.mean()
        self.by_zone = train.groupby("zone_id").trips.mean()
        return self

    def predict(self, frame: pd.DataFrame) -> np.ndarray:
        return frame.zone_id.map(self.by_zone).fillna(self.fallback).to_numpy()


class ZoneHourWeekdayMean:
    """The one to beat: average trips for this zone, this hour, this weekday."""

    name = "zone x hour x weekday mean"

    def fit(self, train: pd.DataFrame) -> "ZoneHourWeekdayMean":
        self.fallback = train.trips.mean()
        keyed = train.assign(
            hour=train.pickup_hour.dt.hour,
            weekday=train.pickup_hour.dt.weekday,
        )
        self.table = keyed.groupby(["zone_id", "hour", "weekday"]).trips.mean()
        return self

    def predict(self, frame: pd.DataFrame) -> np.ndarray:
        keys = pd.MultiIndex.from_arrays(
            [frame.zone_id, frame.pickup_hour.dt.hour, frame.pickup_hour.dt.weekday]
        )
        # An unseen combination gets the global mean rather than a NaN: a
        # predictor that declines to answer cannot be scored.
        return pd.Series(self.table.reindex(keys).to_numpy()).fillna(self.fallback).to_numpy()


class LastWeekSameHour:
    """Whatever happened seven days ago at this hour in this zone."""

    name = "same hour last week"

    def fit(self, train: pd.DataFrame) -> "LastWeekSameHour":
        self.fallback = train.trips.mean()
        self.history = train.set_index(["pickup_hour", "zone_id"]).trips
        return self

    def predict(self, frame: pd.DataFrame) -> np.ndarray:
        keys = pd.MultiIndex.from_arrays(
            [frame.pickup_hour - pd.Timedelta(days=7), frame.zone_id]
        )
        return pd.Series(self.history.reindex(keys).to_numpy()).fillna(self.fallback).to_numpy()


ALL = [GlobalMean, ZoneMean, ZoneHourWeekdayMean, LastWeekSameHour]
