import pytest

from churn_model.data.loader import Row
from churn_model.data.split import split_dataset


def make_rows(count: int, churn_every: int = 4) -> list[Row]:
    """Build simple rows where every churn_every-th customer churned."""
    return [
        {
            "tenure_months": float(index),
            "monthly_charges": 20.0 + index,
            "support_tickets": float(index % 3),
            "churned": 1.0 if index % churn_every == 0 else 0.0,
        }
        for index in range(count)
    ]


def test_split_holds_out_the_test_fraction() -> None:
    train, test = split_dataset(make_rows(40), test_fraction=0.25)

    assert len(train) == 30
    assert len(test) == 10


def test_split_keeps_every_row_exactly_once() -> None:
    rows = make_rows(40)

    train, test = split_dataset(rows)

    assert sorted(train + test, key=repr) == sorted(rows, key=repr)


def test_same_seed_gives_the_same_split() -> None:
    rows = make_rows(40)

    assert split_dataset(rows, seed=7) == split_dataset(rows, seed=7)


def test_different_seeds_give_different_splits() -> None:
    rows = make_rows(40)

    assert split_dataset(rows, seed=1) != split_dataset(rows, seed=2)


def test_split_preserves_the_churn_rate() -> None:
    rows = make_rows(40, churn_every=4)  # 25% churned

    train, test = split_dataset(rows, test_fraction=0.2)

    assert sum(row["churned"] == 1.0 for row in train) == 8
    assert sum(row["churned"] == 1.0 for row in test) == 2


def test_split_does_not_modify_the_input() -> None:
    rows = make_rows(20)
    snapshot = [dict(row) for row in rows]

    split_dataset(rows)

    assert rows == snapshot


@pytest.mark.parametrize("fraction", [0.0, 1.0, -0.1, 1.5])
def test_split_rejects_an_invalid_fraction(fraction: float) -> None:
    with pytest.raises(ValueError, match="test_fraction"):
        split_dataset(make_rows(10), test_fraction=fraction)


def test_split_rejects_rows_without_a_label() -> None:
    rows = make_rows(5)
    rows[2]["churned"] = None

    with pytest.raises(ValueError, match="label"):
        split_dataset(rows)
