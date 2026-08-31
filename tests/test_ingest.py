import pandas as pd
import pytest

from src.ingest import aggregate_trips


@pytest.fixture
def raw():
    # Two trips in zone 1 during the 10:00 hour, one in zone 2 at 11:00, and one
    # row whose timestamp belongs to the previous month — the TLC ships those.
    return pd.DataFrame(
        {
            "tpep_pickup_datetime": pd.to_datetime(
                [
                    "2025-01-15 10:05:00",
                    "2025-01-15 10:59:59",
                    "2025-01-15 11:00:00",
                    "2024-12-31 23:00:00",
                ]
            ),
            "PULocationID": [1, 1, 2, 1],
        }
    )


def test_counts_trips_per_zone_and_hour(raw):
    out = aggregate_trips(raw, month="2025-01", zone_ids=[1, 2])
    at_10 = out[(out.zone_id == 1) & (out.pickup_hour == pd.Timestamp("2025-01-15 10:00"))]
    assert at_10.trips.item() == 2


def test_drops_rows_outside_the_month(raw):
    out = aggregate_trips(raw, month="2025-01", zone_ids=[1, 2])
    # The December row must not appear at all, at any count.
    assert (out.pickup_hour < pd.Timestamp("2025-01-01")).sum() == 0
    assert out.trips.sum() == 3


def test_grid_is_complete_and_missing_hours_are_zero(raw):
    out = aggregate_trips(raw, month="2025-01", zone_ids=[1, 2])
    hours_in_january = 31 * 24
    assert len(out) == hours_in_january * 2
    # Zone 2 at 10:00 saw no trips. It must exist as a zero, not be missing:
    # a missing row silently becomes "no data" instead of "no demand".
    quiet = out[(out.zone_id == 2) & (out.pickup_hour == pd.Timestamp("2025-01-15 10:00"))]
    assert quiet.trips.item() == 0
