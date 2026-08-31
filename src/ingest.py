"""Turn raw TLC parquet into a complete (zone, hour) -> trips grid."""

import pandas as pd

from src.config import INTERIM_DIR, MONTHS, RAW_DIR

COLUMNS = ["tpep_pickup_datetime", "PULocationID"]


def aggregate_trips(raw: pd.DataFrame, month: str, zone_ids: list[int]) -> pd.DataFrame:
    start = pd.Timestamp(f"{month}-01")
    end = start + pd.offsets.MonthBegin(1)

    # The TLC ships rows whose pickup timestamp falls outside the file's own
    # month — 22 of them in 2025-01. Left in, they create phantom hours at the
    # edges that no model can predict and every metric pays for.
    ts = raw["tpep_pickup_datetime"]
    inside = raw[(ts >= start) & (ts < end)]

    counts = (
        inside.assign(pickup_hour=inside["tpep_pickup_datetime"].dt.floor("h"))
        .groupby(["pickup_hour", "PULocationID"])
        .size()
        .rename("trips")
        .reset_index()
        .rename(columns={"PULocationID": "zone_id"})
    )

    # Reindex onto the full zone x hour grid. An hour with no trips is real
    # information — demand was zero — and must be a 0, not an absent row.
    grid = pd.MultiIndex.from_product(
        [pd.date_range(start, end, freq="h", inclusive="left"), zone_ids],
        names=["pickup_hour", "zone_id"],
    )
    return (
        counts.set_index(["pickup_hour", "zone_id"])
        .reindex(grid, fill_value=0)
        .reset_index()
        .astype({"zone_id": "int32", "trips": "int64"})
    )


def zone_ids_from(months: list[str]) -> list[int]:
    """The zone set must be identical across months, or the grid changes shape."""
    seen: set[int] = set()
    for month in months:
        path = RAW_DIR / f"yellow_tripdata_{month}.parquet"
        seen |= set(pd.read_parquet(path, columns=["PULocationID"])["PULocationID"].unique())
    return sorted(int(z) for z in seen)


def load_month(month: str, zone_ids: list[int]) -> pd.DataFrame:
    path = RAW_DIR / f"yellow_tripdata_{month}.parquet"
    return aggregate_trips(pd.read_parquet(path, columns=COLUMNS), month, zone_ids)


def load_all() -> pd.DataFrame:
    cached = INTERIM_DIR / "hourly.parquet"
    if cached.exists():
        return pd.read_parquet(cached)

    zone_ids = zone_ids_from(MONTHS)
    print(f"{len(zone_ids)} zones across {len(MONTHS)} months")
    frames = []
    for month in MONTHS:
        frame = load_month(month, zone_ids)
        print(f"{month}: {len(frame):,} rows, {frame.trips.sum():,} trips")
        frames.append(frame)

    out = pd.concat(frames, ignore_index=True).sort_values(["pickup_hour", "zone_id"])
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    out.to_parquet(cached, index=False)
    return out


def main() -> None:
    frame = load_all()
    print(f"\ntotal: {len(frame):,} rows")
    print(f"range: {frame.pickup_hour.min()} -> {frame.pickup_hour.max()}")


if __name__ == "__main__":
    main()
