import numpy as np

from src.metrics import mae, mape, wape


def test_mae_is_the_average_absolute_error():
    assert mae(np.array([10, 20]), np.array([12, 18])) == 2.0


def test_wape_divides_total_error_by_total_volume():
    # 4 units of error over 30 units of demand.
    assert wape(np.array([10, 20]), np.array([12, 18])) == 4 / 30


def test_mape_explodes_on_a_quiet_hour():
    # A zone with zero trips this hour. MAPE divides by that zero.
    result = mape(np.array([0, 20]), np.array([3, 20]))
    assert np.isinf(result) or np.isnan(result), (
        "this is the point: 41 of 261 zones see fewer than 100 trips a month, "
        "so zero-trip hours are common and MAPE is unusable here"
    )


def test_wape_survives_the_same_quiet_hour():
    assert wape(np.array([0, 20]), np.array([3, 20])) == 3 / 20
