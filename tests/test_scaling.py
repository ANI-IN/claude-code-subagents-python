import statistics

import pytest

from churn_model.data.loader import Row
from churn_model.features.scaling import apply_standardizer, fit_standardizer


def test_scaled_column_has_mean_zero_and_unit_spread() -> None:
    rows: list[Row] = [{"x": 2.0}, {"x": 4.0}, {"x": 6.0}, {"x": 8.0}]

    scaled = apply_standardizer(rows, fit_standardizer(rows, ["x"]))

    values = [row["x"] for row in scaled]
    assert all(value is not None for value in values)
    numbers = [value for value in values if value is not None]
    assert statistics.fmean(numbers) == pytest.approx(0.0)
    assert statistics.pstdev(numbers) == pytest.approx(1.0)


def test_missing_values_are_ignored_when_fitting_and_stay_none() -> None:
    rows: list[Row] = [{"x": 1.0}, {"x": None}, {"x": 3.0}]

    stats = fit_standardizer(rows, ["x"])
    scaled = apply_standardizer(rows, stats)

    assert stats["x"].mean == 2.0
    assert scaled[1]["x"] is None


def test_constant_column_scales_to_zero_without_dividing_by_zero() -> None:
    rows: list[Row] = [{"x": 5.0}, {"x": 5.0}]

    scaled = apply_standardizer(rows, fit_standardizer(rows, ["x"]))

    assert [row["x"] for row in scaled] == [0.0, 0.0]


def test_columns_without_stats_are_copied_unchanged() -> None:
    rows: list[Row] = [{"x": 1.0, "label": 1.0}, {"x": 3.0, "label": 0.0}]

    scaled = apply_standardizer(rows, fit_standardizer(rows, ["x"]))

    assert [row["label"] for row in scaled] == [1.0, 0.0]


def test_apply_does_not_modify_the_input() -> None:
    rows: list[Row] = [{"x": 1.0}, {"x": 3.0}]

    apply_standardizer(rows, fit_standardizer(rows, ["x"]))

    assert rows == [{"x": 1.0}, {"x": 3.0}]


def test_fit_rejects_a_column_with_no_values() -> None:
    with pytest.raises(ValueError, match="no values"):
        fit_standardizer([{"x": None}], ["x"])
