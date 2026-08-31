from src.config import SAMPLE_DIR


def test_sample_is_small_enough_to_live_in_git():
    path = SAMPLE_DIR / "hourly_sample.parquet"
    assert path.exists(), "run: uv run python -m src.sample"
    assert path.stat().st_size < 5_000_000, "the sample must stay under 5 MB"


def test_sample_has_the_same_shape_as_the_real_thing():
    import pandas as pd

    frame = pd.read_parquet(SAMPLE_DIR / "hourly_sample.parquet")
    assert list(frame.columns) == ["pickup_hour", "zone_id", "trips"]
    assert frame.pickup_hour.dt.month.nunique() >= 3, "need several months to split on"
