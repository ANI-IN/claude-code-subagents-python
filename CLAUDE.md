# Project
Customer churn model. A small Python ML codebase that loads customer
records, prepares features, and builds train and test sets. It is used
to practice building and delegating to Claude Code subagents.

# Map
- src/churn_model/config.py        label, feature columns, random seed, test fraction
- src/churn_model/data/loader.py   reads data/customers.csv; missing cells become None
- src/churn_model/data/split.py    seeded, stratified train/test split
- src/churn_model/features/        median imputation and standard scaling (fit, then apply)
- src/churn_model/training/prepare.py  newly written module under review (see below)
- tests/                           pytest suite
- .claude/agents/                  project subagents

# Commands
- Install:    `pip install -e ".[dev]"` (inside a virtual environment)
- Run tests:  `pytest`
- Lint:       `ruff check .` and `ruff format --check .`
- Type check: `mypy`

# Code Style
- PEP 8, 4-space indentation, enforced by Ruff.
- Type hints on every function; mypy runs in strict mode.
- Absolute imports from `churn_model`; no wildcard imports.
- Standard library only at runtime.

# ML Conventions
- Only `FEATURE_COLUMNS` are model inputs. The label is never a feature.
- Split first, then fit imputers and scalers on the training rows only.
- All randomness uses `RANDOM_SEED`; reuse `split_dataset` for splits.
- Missing values stay `None` until a fitted imputer fills them.

# Teaching Exercise
`src/churn_model/training/prepare.py` is the subject of a code-review
exercise. Do not modify it unless the user explicitly asks you to.
