from pathlib import Path

from churn_model.data.loader import load_customers
from churn_model.training.prepare import build_training_sets


def test_build_training_sets_returns_an_80_20_split(dataset_path: Path) -> None:
    sets = build_training_sets(load_customers(dataset_path))

    assert len(sets.train_features) == len(sets.train_labels) == 32
    assert len(sets.test_features) == len(sets.test_labels) == 8


def test_every_feature_vector_has_one_value_per_feature(dataset_path: Path) -> None:
    sets = build_training_sets(load_customers(dataset_path))

    width = len(sets.feature_names)
    assert all(len(vector) == width for vector in sets.train_features)
    assert all(len(vector) == width for vector in sets.test_features)


def test_labels_are_zero_or_one(dataset_path: Path) -> None:
    sets = build_training_sets(load_customers(dataset_path))

    assert set(sets.train_labels + sets.test_labels) <= {0, 1}
