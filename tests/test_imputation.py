import pytest

from churn_model.data.loader import Row
from churn_model.features.imputation import apply_imputer, fit_median_imputer


def test_fit_learns_the_median_and_ignores_missing_values() -> None:
    rows: list[Row] = [{"x": 1.0}, {"x": None}, {"x": 3.0}, {"x": 10.0}]

    assert fit_median_imputer(rows, ("x",)) == {"x": 3.0}


def test_apply_fills_only_missing_values() -> None:
    rows: list[Row] = [{"x": None, "y": None}, {"x": 5.0, "y": 1.0}]

    filled = apply_imputer(rows, {"x": 2.0})

    assert filled == [{"x": 2.0, "y": None}, {"x": 5.0, "y": 1.0}]


def test_apply_does_not_modify_the_input() -> None:
    rows: list[Row] = [{"x": None}]

    apply_imputer(rows, {"x": 2.0})

    assert rows == [{"x": None}]


def test_fit_rejects_a_column_with_no_values() -> None:
    with pytest.raises(ValueError, match="no values"):
        fit_median_imputer([{"x": None}], ("x",))
