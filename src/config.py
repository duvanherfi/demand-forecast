from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
INTERIM_DIR = ROOT / "data" / "interim"
SAMPLE_DIR = ROOT / "data" / "sample"
REPORTS_DIR = ROOT / "reports"

MONTHS = [f"2025-{m:02d}" for m in range(1, 13)]

# The split is by time, never at random. The last month is held out and is not
# looked at until the whole project is finished.
TRAIN_MONTHS = MONTHS[:10]   # 2025-01 .. 2025-10
VAL_MONTH = MONTHS[10]       # 2025-11
TEST_MONTH = MONTHS[11]      # 2025-12

URL_TEMPLATE = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month}.parquet"
)
