"""Split customer records into reproducible train and test sets."""

import random

from churn_model.config import LABEL_COLUMN, RANDOM_SEED, TEST_FRACTION
from churn_model.data.loader import Row


def split_dataset(
    rows: list[Row],
    *,
    test_fraction: float = TEST_FRACTION,
    seed: int = RANDOM_SEED,
    label_column: str = LABEL_COLUMN,
) -> tuple[list[Row], list[Row]]:
    """Return (train, test) with the same label balance in both sets.

    Rows are grouped by label and each group is shuffled by one generator
    seeded with `seed`, so the same seed always produces the same split.
    """
    if not 0 < test_fraction < 1:
        raise ValueError("test_fraction must be between 0 and 1")

    groups: dict[float, list[Row]] = {}
    for row in rows:
        label = row[label_column]
        if label is None:
            raise ValueError(f"row has no {label_column} label")
        groups.setdefault(label, []).append(row)

    rng = random.Random(seed)
    train: list[Row] = []
    test: list[Row] = []
    for label in sorted(groups):
        group = groups[label][:]
        rng.shuffle(group)
        test_size = round(len(group) * test_fraction)
        test.extend(group[:test_size])
        train.extend(group[test_size:])
    return train, test
