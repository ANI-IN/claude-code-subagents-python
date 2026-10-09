"""Shared fixtures: a small customer table with a few missing cells."""

from pathlib import Path

import pytest

SAMPLE_CSV = """\
tenure_months,monthly_charges,support_tickets,churned
2,99.50,5,1
40,30.00,0,0
,55.25,1,0
12,,3,1
60,20.00,0,0
8,85.00,,1
33,45.10,1,0
50,25.75,0,0
5,105.00,4,1
24,60.00,2,0
"""

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    path = tmp_path / "customers.csv"
    path.write_text(SAMPLE_CSV, encoding="utf-8")
    return path


@pytest.fixture
def dataset_path() -> Path:
    """The 40-row sample dataset shipped in data/."""
    return PROJECT_ROOT / "data" / "customers.csv"
