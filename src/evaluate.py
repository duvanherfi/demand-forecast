"""The harness. Built before any model exists, and reused unchanged after.

Anything with fit/predict/name can be scored, which is what keeps later laps
honest: a gradient boosting model is compared against the baselines by exactly
the same code, on exactly the same rows.
"""

from pathlib import Path

import pandas as pd

from src.config import REPORTS_DIR
from src.metrics import mae, wape


def score(predictors, train: pd.DataFrame, val: pd.DataFrame) -> pd.DataFrame:
    truth = val.trips.to_numpy()
    rows = []
    for predictor in predictors:
        fitted = predictor.fit(train)
        prediction = fitted.predict(val)
        rows.append(
            {
                "predictor": predictor.name,
                "mae": round(mae(truth, prediction), 3),
                "wape": round(wape(truth, prediction), 4),
            }
        )
    return pd.DataFrame(rows).sort_values("mae").reset_index(drop=True)


def write_scoreboard(table: pd.DataFrame) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    target = REPORTS_DIR / "scoreboard.md"
    best = table.iloc[0]
    target.write_text(
        "# Marcador\n\n"
        "Error sobre el mes de validación (2025-11). El mes de prueba (2025-12) "
        "sigue sin tocarse.\n\n"
        f"{table.to_markdown(index=False)}\n\n"
        f"Mejor hasta ahora: **{best.predictor}**, MAE {best.mae} viajes por "
        "zona y hora.\n"
    )
    return target


def main() -> None:
    from src.baselines import ALL
    from src.ingest import load_all
    from src.split import split

    train, val = split(load_all())
    table = score([cls() for cls in ALL], train, val)
    print(table.to_string(index=False))
    print(f"\nwritten to {write_scoreboard(table)}")


if __name__ == "__main__":
    main()
