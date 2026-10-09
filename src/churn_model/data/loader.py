"""Load customer records from a CSV file."""

import csv
import math
from pathlib import Path

from churn_model.config import FEATURE_COLUMNS, LABEL_COLUMN

# One customer record: column name -> value, with None for a missing cell.
Row = dict[str, float | None]

MISSING_MARKERS = {"", "na", "nan", "null"}


def parse_value(cell: str) -> float | None:
    """Parse one CSV cell into a float, or None if the cell is missing."""
    text = cell.strip()
    if text.lower() in MISSING_MARKERS:
        return None
    value = float(text)
    if not math.isfinite(value):
        raise ValueError(f"not a finite number: {text!r}")
    return value


def load_customers(path: str | Path) -> list[Row]:
    """Read customer records, keeping missing feature values as None.

    Raises ValueError if a required column is absent, a row has the wrong
    number of fields, a cell is not a finite number, or a label is missing
    or not 0 or 1.
    """
    required = {*FEATURE_COLUMNS, LABEL_COLUMN}
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        absent = required - set(columns)
        if absent:
            raise ValueError(f"missing columns: {', '.join(sorted(absent))}")

        rows: list[Row] = []
        for line_number, record in enumerate(reader, start=2):
            # DictReader fills short rows with None and puts extras under None.
            if None in record or None in record.values():
                raise ValueError(f"line {line_number}: expected {len(columns)} fields")
            try:
                row = {name: parse_value(record[name]) for name in columns}
            except ValueError as error:
                raise ValueError(f"line {line_number}: {error}") from error
            label = row[LABEL_COLUMN]
            if label is None:
                raise ValueError(f"line {line_number}: no {LABEL_COLUMN} label")
            if label not in (0.0, 1.0):
                raise ValueError(f"line {line_number}: {LABEL_COLUMN} must be 0 or 1")
            rows.append(row)
    return rows
