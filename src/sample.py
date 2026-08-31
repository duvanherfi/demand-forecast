"""Build the committed sample: the twenty busiest zones, every month.

A reader who clones the repo can run everything in two minutes without
downloading 700 MB. Zones are kept whole rather than sampled at random, so the
sample behaves like the real data instead of like noise.
"""

from pathlib import Path

from src.config import SAMPLE_DIR
from src.ingest import load_all


def build_sample() -> Path:
    frame = load_all()
    busiest = frame.groupby("zone_id").trips.sum().nlargest(20).index
    sample = frame[frame.zone_id.isin(busiest)].reset_index(drop=True)

    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    target = SAMPLE_DIR / "hourly_sample.parquet"
    sample.to_parquet(target, index=False, compression="zstd")
    print(f"{len(sample):,} rows, {target.stat().st_size / 1e6:.2f} MB")
    return target


if __name__ == "__main__":
    build_sample()
