"""Standardize feature columns to mean 0 and standard deviation 1."""

import statistics
from collections.abc import Sequence
from dataclasses import dataclass

from churn_model.data.loader import Row


@dataclass(frozen=True)
class ColumnStats:
    """The mean and standard deviation learned for one column."""

    mean: float
    std: float


def fit_standardizer(rows: list[Row], columns: Sequence[str]) -> dict[str, ColumnStats]:
    """Learn the mean and standard deviation of each column.

    Missing values are ignored. Fit on training rows only, then apply the
    same statistics to the test rows.
    """
    stats: dict[str, ColumnStats] = {}
    for column in columns:
        values = [value for row in rows if (value := row[column]) is not None]
        if not values:
            raise ValueError(f"column {column!r} has no values to fit")
        mean = statistics.fmean(values)
        std = statistics.pstdev(values, mu=mean)
        # A constant column has no spread; keep it at 0 instead of dividing by 0.
        stats[column] = ColumnStats(mean=mean, std=std or 1.0)
    return stats


def apply_standardizer(rows: list[Row], stats: dict[str, ColumnStats]) -> list[Row]:
    """Return new rows with each fitted column scaled to z-scores.

    Missing values stay None, and columns without stats are copied unchanged.
    """
    scaled: list[Row] = []
    for row in rows:
        new_row = dict(row)
        for column, column_stats in stats.items():
            value = new_row[column]
            if value is not None:
                new_row[column] = (value - column_stats.mean) / column_stats.std
        scaled.append(new_row)
    return scaled
