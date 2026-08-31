"""Download the monthly TLC parquet files, skipping what is already local."""

import urllib.request
from pathlib import Path

from src.config import MONTHS, RAW_DIR, URL_TEMPLATE


def download_month(month: str) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    target = RAW_DIR / f"yellow_tripdata_{month}.parquet"
    if target.exists():
        print(f"{month}: already downloaded ({target.stat().st_size / 1e6:.1f} MB)")
        return target

    url = URL_TEMPLATE.format(month=month)
    print(f"{month}: downloading from {url}")
    # Download to a temporary name first, so an interrupted run never leaves a
    # truncated file that the next run would happily treat as complete.
    tmp = target.with_suffix(".parquet.part")
    urllib.request.urlretrieve(url, tmp)
    tmp.rename(target)
    print(f"{month}: done ({target.stat().st_size / 1e6:.1f} MB)")
    return target


def main() -> None:
    for month in MONTHS:
        download_month(month)


if __name__ == "__main__":
    main()
