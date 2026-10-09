# Exercise 1: Explore the Sample Codebase

Before you build any subagents, get familiar with the code they will act on. The project already contains a small churn-model codebase, so you do not have to create it. This exercise is about reading it with intent.

## What to do

Open these files and read them closely:

- `src/churn_model/config.py` holds the project settings: the label column, the feature columns, the random seed, and the test fraction.
- `src/churn_model/data/split.py` is an existing, well-behaved module. Your exploration subagent will locate it later.
- `src/churn_model/training/prepare.py` is a newly written module that turns customer records into train and test sets. Your review subagent will examine it later. It contains several deliberate problems.

Then run the new module twice on the sample data and compare the results. With your virtual environment active, run this from the project root in a bash, zsh, or PowerShell terminal (Windows `cmd.exe` does not accept a multi-line command):

```bash
python -c "
from churn_model.data.loader import load_customers
from churn_model.training.prepare import build_training_sets

rows = load_customers('data/customers.csv')
for run in (1, 2):
    sets = build_training_sets(rows)
    first = [round(value, 2) for value in sets.test_features[0]]
    print(f'run {run}: features={sets.feature_names}')
    print(f'  first test row={first} churners in test set={sum(sets.test_labels)}')
"
```

## What to look for in the code

In `src/churn_model/data/split.py`:

- The `split_dataset` function groups rows by their `churned` label, so the churn rate is the same in the train and test sets. This is called a stratified split.
- It shuffles with `random.Random(seed)`, where `seed` defaults to `RANDOM_SEED` from `config.py`. The same seed always produces the same split.

In `src/churn_model/training/prepare.py`, look for four planted issues. The file does not point them out, so trace each one in the code:

1. **Target leakage.** `feature_names = list(rows[0])` takes every column as a feature, including `churned`, which is the label the model is supposed to predict. A model trained this way scores close to perfectly in evaluation and is useless in production, where the label is not known in advance.
2. **Train/test contamination.** `fit_standardizer` learns the mean and spread from all rows before the split. The test rows influence the scaling, so the evaluation is no longer a fair test on unseen data. Compare this with the docstring of `fit_standardizer`, which says to fit on training rows only.
3. **Unseeded shuffle.** `random.shuffle(examples)` uses Python's global random generator, so every run produces a different split and different results. The module also reimplements a split that `split_dataset` already does correctly.
4. **Missing values filled with zero.** `_fill_missing` replaces every `None` with `0.0`. A missing tenure becomes "a brand-new customer" and a missing monthly charge becomes "free". The project already has `fit_median_imputer` for this.

Trace each item to the exact line that causes it.

## Important: do not fix anything

These issues are deliberate. They exist so that your review subagent has something real to find in a later exercise. Leave the code exactly as it is. Your task here is to notice the flaws and understand why each one is a problem, not to repair them.

## What to observe

- The output of the two runs shows two of the flaws directly. `churned` appears in the feature list, and the first test row differs between the runs, because the split is not seeded. The number of churners in the test set can change too; run the snippet a few times to see it move.
- Run `pytest`. Every test passes, including `tests/test_prepare.py`. Those tests check only the shape of the output: the split sizes, the vector widths, and the label values. None of them can see leakage. That is why a review with fresh eyes is still worth doing.
- The correct building blocks (`split_dataset`, `fit_median_imputer`, `fit_standardizer`) live in separate files under `src/churn_model/`. That separation is what makes the exploration subagent useful later. It can point you to the right file without you reading everything.

## Learning outcome

You understand the material your subagents will work against, and you can name the four deliberate weaknesses in `prepare.py` and explain why each one leads to misleading or unrepeatable results. You also understand that these weaknesses are teaching material and must stay in place.
