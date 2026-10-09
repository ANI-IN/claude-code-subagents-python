"""Fill missing feature values with medians learned from training data."""

import statistics
from collections.abc import Sequence

from churn_model.data.loader import Row


def fit_median_imputer(rows: list[Row], columns: Sequence[str]) -> dict[str, float]:
    """Learn the median of each column, ignoring missing values.

    Fit on training rows only, then apply the same medians to the test rows.
    """
    medians: dict[str, float] = {}
    for column in columns:
        values = [value for row in rows if (value := row[column]) is not None]
        if not values:
            raise ValueError(f"column {column!r} has no values to fit")
        medians[column] = statistics.median(values)
    return medians


def apply_imputer(rows: list[Row], medians: dict[str, float]) -> list[Row]:
    """Return new rows with missing values replaced by the fitted medians.

    Columns without a fitted median are copied unchanged.
    """
    filled: list[Row] = []
    for row in rows:
        new_row = dict(row)
        for column, median in medians.items():
            if new_row[column] is None:
                new_row[column] = median
        filled.append(new_row)
    return filled
