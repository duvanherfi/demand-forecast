from src import config


def test_splits_do_not_overlap_and_cover_every_month():
    assert set(config.TRAIN_MONTHS).isdisjoint({config.VAL_MONTH})
    assert set(config.TRAIN_MONTHS).isdisjoint({config.TEST_MONTH})
    assert config.VAL_MONTH != config.TEST_MONTH
    assert config.TRAIN_MONTHS + [config.VAL_MONTH, config.TEST_MONTH] == config.MONTHS


def test_validation_comes_after_training_and_test_after_validation():
    assert max(config.TRAIN_MONTHS) < config.VAL_MONTH
    assert config.VAL_MONTH < config.TEST_MONTH
