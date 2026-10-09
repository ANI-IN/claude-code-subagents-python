# Claude Code Subagents: A Python ML Project

A small, hands-on project that teaches how to build and use custom Claude Code **subagents**. You create two complementary subagents for a Python machine learning codebase that predicts customer churn: one that **explores** the code to answer a question, and one that **reviews** a newly written training-data module with fresh eyes. You then see how each runs in its own isolated context and returns only a summary. An optional third subagent writes developer documentation in a set voice.

It is written for early-career software and AI/ML engineers. The code is deliberately small, but it is organized like a real Python project: a `src/` package layout, type hints checked by mypy, linting with Ruff, and a pytest suite.

## 1. Project Overview

A subagent is a specialized assistant that Claude Code can delegate a task to. Each subagent runs in its own context window. It receives a system prompt and a task description, does the work privately by reading and searching, and returns only a summary. The intermediate steps are discarded, so your main conversation stays clean.

The sample code is the data side of a churn model. It loads customer records from `data/customers.csv` (tenure, monthly charges, support tickets, and whether the customer churned), keeps missing cells as `None`, and prepares train and test sets. Two parts matter for the demo:

- **`src/churn_model/data/split.py`** is an existing, well-behaved module. It makes a seeded, stratified train/test split. The exploration subagent locates it when you ask how the split works and how it stays reproducible.
- **`src/churn_model/training/prepare.py`** is a newly written module that turns customer records into train and test sets. It contains classic ML mistakes that a fresh-eyes review should catch.

The demo ships with:

- The churn-model package under `src/`, a 40-row sample dataset under `data/`, and a pytest suite under `tests/`.
- The full lesson in [`docs/subagents.docx`](docs/subagents.docx), covering the concepts and the walkthrough.
- Step-by-step exercises under [`exercises/`](exercises/) that turn the lesson into a lab.

The subagents themselves are what you build while working through the exercises. On `main`, the `.claude/agents/` folder starts empty on purpose.

## 2. Intentional Flaws

**Some code in this project is flawed on purpose. Do not fix it, and do not ask a subagent to fix it.** The flaws give the review subagent something real to find.

The module documents its own planted issues in the docstring at the top of `src/churn_model/training/prepare.py`:

```text
Deliberate issues for the pipeline-reviewer to find:
  1. Target leakage: the churned label is used as a model feature
  2. Train/test contamination: scaling is fitted on all rows before the split
  3. Unseeded shuffle: the split changes on every run (and duplicates split.py)
  4. Missing values silently replaced with 0.0
```

Each is a mistake that makes a model look better in evaluation than it will be in production, or makes results impossible to reproduce. When an exercise leads you to one of these issues, your task is to notice it and understand why it matters, not to repair it.

The test suite passes on `main` even with these flaws in place. `tests/test_prepare.py` only checks the shape of the output: the split sizes, the vector widths, and the label values. That is part of the lesson. Green tests do not prove that a training pipeline is free of leakage, which is why a fresh-eyes review is worth having.

## 3. Branches

| Branch | Contents |
|---|---|
| `main` | The starting point. `.claude/agents/` is empty. Do the exercises here. |
| `solution/subagents` | The finished result: all three subagents in `.claude/agents/`, plus [`SOLUTION.md`](https://github.com/ANI-IN/claude-code-subagents-python/blob/solution/subagents/SOLUTION.md) with the expected output of each demo. Compare against it only after you finish. |

## 4. Prerequisites

- Python 3.10 or newer. Check with `python3 --version`. On some systems, including macOS, `python3` can be older than 3.10. If so, install a newer Python and create the virtual environment with it by name, for example `python3.12 -m venv .venv`.
- Git.
- [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) installed, so that `claude` is available in your terminal.

## 5. Setup

```bash
git clone https://github.com/ANI-IN/claude-code-subagents-python.git
cd claude-code-subagents-python

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
```

`pip install -e ".[dev]"` installs the package in editable mode along with the development tools: pytest, Ruff, and mypy. The package itself uses only the Python standard library.

## 6. Commands

| Task | Command |
|---|---|
| Run the tests | `pytest` |
| Lint | `ruff check .` |
| Check formatting | `ruff format --check .` |
| Type check | `mypy` |

All four should pass on both branches. `pytest` reports `36 passed`.

## 7. Project Structure

```text
claude-code-subagents-python/
├── CLAUDE.md                     Project conventions Claude reads every session
├── README.md                     This file
├── pyproject.toml                Package metadata, dev dependencies, and tool settings
├── .gitignore
├── .claude/
│   └── agents/                   Project subagents. Empty on main; you add files here
├── data/
│   └── customers.csv             40 customers, 10 churned, a few missing cells
├── docs/
│   └── subagents.docx            The full lesson: concepts and walkthrough
├── src/
│   └── churn_model/
│       ├── config.py             Label, feature columns, random seed, test fraction
│       ├── data/
│       │   ├── loader.py         Reads the CSV; missing cells become None
│       │   └── split.py          Seeded, stratified split. The explorer locates this
│       ├── features/
│       │   ├── imputation.py     Median imputation (fit on train, apply to both)
│       │   └── scaling.py        Standard scaling (fit on train, apply to both)
│       └── training/
│           └── prepare.py        New module with deliberate flaws. The reviewer examines this
├── tests/
│   ├── conftest.py               Shared fixtures
│   ├── test_loader.py
│   ├── test_split.py
│   ├── test_imputation.py
│   ├── test_scaling.py
│   └── test_prepare.py           Shape checks only. They pass despite the flaws
└── exercises/
    ├── README.md                 Index, how to use the exercises, key takeaways
    ├── 01-explore-the-sample-codebase.md
    ├── 02-build-the-exploration-subagent.md
    ├── 03-build-the-review-subagent.md
    ├── 04-load-and-verify.md
    ├── 05-delegate-an-exploration-task.md
    ├── 06-delegate-a-review-task.md
    └── 07-add-a-documentation-subagent.md
```

## 8. Running the Demos

The demos run inside Claude Code. Start it from the project root:

```bash
claude
```

Each step below maps to an exercise in `exercises/`, where you will find the full detail.

### Step 1: build the two subagents

Follow [exercise 2](exercises/02-build-the-exploration-subagent.md) to create the `codebase-explorer` subagent, then [exercise 3](exercises/03-build-the-review-subagent.md) to create the `pipeline-reviewer` subagent. The quickest path is the `/agents` slash command, which lets Claude generate each configuration from a description.

### Step 2: load and verify

Restart Claude Code so it registers the new subagents, then list them:

```text
/agents
```

Both `codebase-explorer` and `pipeline-reviewer` should appear, scoped to the project. See [exercise 4](exercises/04-load-and-verify.md).

### Demo A: delegate an exploration task

```text
Use the codebase-explorer: where and how is the train/test split made, and how is it kept reproducible?
```

It should point you to `split_dataset` in `src/churn_model/data/split.py` and to `RANDOM_SEED` in `src/churn_model/config.py`. Notice that your main conversation records only the question and the summary. See [exercise 5](exercises/05-delegate-an-exploration-task.md).

### Demo B: delegate a review task

```text
Use the pipeline-reviewer to review src/churn_model/training/prepare.py
```

It should return a structured review that flags the planted flaws and ends with an Approval Status of "Requires changes". See [exercise 6](exercises/06-delegate-a-review-task.md).

### Demo C: add a documentation subagent (optional)

Build the `pipeline-doc-writer` subagent, then document the module:

```text
Use the pipeline-doc-writer to document src/churn_model/training/prepare.py
```

See [exercise 7](exercises/07-add-a-documentation-subagent.md).

## 9. Exercises

Start with [exercises/README.md](exercises/README.md), which explains how to use the guides and lists the key takeaways. Then work through the numbered files in order:

1. Explore the sample codebase.
2. Build the exploration subagent.
3. Build the review subagent.
4. Load and verify your subagents.
5. Delegate an exploration task.
6. Delegate a review task.
7. Add a documentation subagent (optional).

Each guide states what to do, what to observe, what to look for in the code, and the learning outcome. Every example prompt is quoted exactly so you can copy it without changes.

## 10. Additional Notes

- **Different jobs deserve different subagents.** An explorer for research, a reviewer for code review, and a writer for docs. Each one gets its own tools and its own system prompt.
- **Tool access is least privilege.** All three subagents here are read-only, with just Glob, Grep, and Read. Reserve edit or write access for subagents whose job is to change code.
- **A defined output format matters.** It gives a subagent clear stopping points and returns a result the main thread can use. The reviewer's Obstacles Encountered section surfaces workarounds and quirks so they are not rediscovered later.
- **Know when not to use a subagent.** Subagents hurt as expert personas that add no real capability, as sequential pipelines where each step depends on the last, and as test runners when you need the full output to debug. Run `pytest` in your main thread. The lesson in `docs/subagents.docx` covers these anti-patterns in detail.
- **Skills versus subagents.** A skill runs inline in your main conversation and is best for injecting a standard or checklist into the current task. A subagent runs in a separate context and is best for delegating self-contained work and getting a summary back.
- **Scope.** This is a teaching project, not production software. There is no model training code. The data preparation is the part where leakage happens, so that is where the review focuses.
