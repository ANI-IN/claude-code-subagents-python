from pathlib import Path

import pytest

from churn_model.config import FEATURE_COLUMNS, LABEL_COLUMN
from churn_model.data.loader import load_customers, parse_value


def test_parse_value_reads_numbers() -> None:
    assert parse_value(" 12.5 ") == 12.5


@pytest.mark.parametrize("cell", ["", "  ", "NA", "nan", "null"])
def test_parse_value_keeps_missing_cells_as_none(cell: str) -> None:
    assert parse_value(cell) is None


def test_load_customers_parses_every_row(sample_csv: Path) -> None:
    rows = load_customers(sample_csv)

    assert len(rows) == 10
    assert rows[0] == {
        "tenure_months": 2.0,
        "monthly_charges": 99.5,
        "support_tickets": 5.0,
        "churned": 1.0,
    }


def test_load_customers_keeps_missing_values_as_none(sample_csv: Path) -> None:
    rows = load_customers(sample_csv)

    assert rows[2]["tenure_months"] is None
    assert rows[3]["monthly_charges"] is None
    assert rows[5]["support_tickets"] is None


def test_load_customers_rejects_missing_columns(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    path.write_text("tenure_months,churned\n3,1\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing columns"):
        load_customers(path)


def test_load_customers_rejects_rows_without_a_label(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    path.write_text(
        "tenure_months,monthly_charges,support_tickets,churned\n3,50,1,\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="line 2: no churned label"):
        load_customers(path)


def test_load_customers_reports_the_line_of_a_bad_number(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    path.write_text(
        "tenure_months,monthly_charges,support_tickets,churned\n3,50,1,0\n4,lots,1,0\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="line 3"):
        load_customers(path)


def test_shipped_dataset_loads(dataset_path: Path) -> None:
    rows = load_customers(dataset_path)

    assert len(rows) == 40
    assert set(rows[0]) == {*FEATURE_COLUMNS, LABEL_COLUMN}
    assert sum(row[LABEL_COLUMN] == 1.0 for row in rows) == 10
