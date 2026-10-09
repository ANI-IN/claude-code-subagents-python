"""Turn customer records into train and test sets for the churn model.

Newly written module for the review exercise.
Deliberate issues for the pipeline-reviewer to find:
  1. Target leakage: the churned label is used as a model feature
  2. Train/test contamination: scaling is fitted on all rows before the split
  3. Unseeded shuffle: the split changes on every run (and duplicates split.py)
  4. Missing values silently replaced with 0.0
"""

import random
from dataclasses import dataclass

from churn_model.config import LABEL_COLUMN, TEST_FRACTION
from churn_model.data.loader import Row
from churn_model.features.scaling import apply_standardizer, fit_standardizer


@dataclass(frozen=True)
class TrainingSets:
    """Feature vectors and labels, ready for a model to fit and evaluate."""

    feature_names: list[str]
    train_features: list[list[float]]
    train_labels: list[int]
    test_features: list[list[float]]
    test_labels: list[int]


def build_training_sets(rows: list[Row]) -> TrainingSets:
    """Clean, scale, and split customer records into train and test sets."""
    # Every column in the data is used as a feature.
    feature_names = list(rows[0])

    # Models cannot handle missing values, so fill the gaps first.
    filled = [_fill_missing(row) for row in rows]

    stats = fit_standardizer(filled, feature_names)
    scaled = apply_standardizer(filled, stats)

    examples = [
        (_to_vector(row, feature_names), _label(original))
        for row, original in zip(scaled, rows, strict=True)
    ]

    random.shuffle(examples)
    cut = int(len(examples) * (1 - TEST_FRACTION))
    train, test = examples[:cut], examples[cut:]

    return TrainingSets(
        feature_names=feature_names,
        train_features=[features for features, _ in train],
        train_labels=[label for _, label in train],
        test_features=[features for features, _ in test],
        test_labels=[label for _, label in test],
    )


def _fill_missing(row: Row) -> Row:
    return {name: 0.0 if value is None else value for name, value in row.items()}


def _to_vector(row: Row, names: list[str]) -> list[float]:
    vector: list[float] = []
    for name in names:
        value = row[name]
        if value is None:
            raise ValueError(f"missing value for {name!r}")
        vector.append(value)
    return vector


def _label(row: Row) -> int:
    value = row[LABEL_COLUMN]
    if value is None:
        raise ValueError(f"row has no {LABEL_COLUMN} label")
    return int(value)
