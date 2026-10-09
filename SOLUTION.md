# Solution: Three Project Subagents

This branch is the finished result of the exercises. It adds three project-level subagents to `.claude/agents/` (replacing the `.gitkeep` placeholder) and this file. Nothing else changes: the source code, the tests, and the deliberate flaws in `src/churn_model/training/prepare.py` are identical to `main`.

Compare against this branch only after you have built your own subagents.

## What this branch adds

| File | Subagent | Tools | Color |
|---|---|---|---|
| `.claude/agents/codebase-explorer.md` | Answers "where" and "how" questions with file paths and line numbers | Glob, Grep, Read | blue |
| `.claude/agents/pipeline-reviewer.md` | Reviews ML pipeline code for leakage, reproducibility, and correctness | Glob, Grep, Read | purple |
| `.claude/agents/pipeline-doc-writer.md` | Writes developer docs with Overview, Inputs, Usage, and Data caveats | Glob, Grep, Read | green |

All three are read-only. Their behavior comes from the `description` and the system prompt, not from extra tools.

## How to try it

```bash
git checkout solution/subagents
claude
```

Run `/agents` to confirm all three are listed, then run the demo prompts below.

## What to expect

Subagent output varies from run to run. The points below are what a correct run contains. They were checked against real runs on this branch.

### Demo A: exploration

```text
Use the codebase-explorer: where and how is the train/test split made, and how is it kept reproducible?
```

A correct answer:

- Names `split_dataset` in `src/churn_model/data/split.py` (around line 9) as the place the split is made.
- Explains that rows are grouped by label and each group is cut at `test_fraction`, so train and test keep about the same churn rate (around lines 26 to 41).
- Explains reproducibility: one `random.Random(seed)` generator (around line 33) shuffles each group and then both sets, with `seed` defaulting to `RANDOM_SEED = 42` in `src/churn_model/config.py` (line 11).
- Often adds, as a note, that `src/churn_model/training/prepare.py` does not call `split_dataset` and uses an unseeded `random.shuffle` instead.

Your main conversation should contain only the question and this summary, not the files the subagent read.

### Demo B: review

```text
Use the pipeline-reviewer to review src/churn_model/training/prepare.py
```

A correct review follows the six-section format and reports:

| Planted issue | Where | Typical severity |
|---|---|---|
| Target leakage: `churned` is among the features | `feature_names = list(rows[0])` | Critical |
| Scaling fitted on all rows before the split | `fit_standardizer(filled, feature_names)` | Critical |
| Missing values replaced with `0.0` instead of the median imputer | `_fill_missing` | Critical or Major |
| Unseeded, unstratified shuffle that duplicates `split_dataset` | `random.shuffle(examples)` | Major |

It ends with an Approval Status of **"Requires changes"**. Reviews often add minor findings as well, such as `rows[0]` raising `IndexError` on an empty list.

### Demo C: documentation

```text
Use the pipeline-doc-writer to document src/churn_model/training/prepare.py
```

A correct result has the four sections from the system prompt (Overview, Inputs, Usage, and Data caveats), includes a short usage example, and uses Data caveats to state the four problems plainly instead of describing the module as it was intended to work.

## Why the code is not fixed here

The planted flaws are the teaching material for the review exercise, so they stay on both branches. If you want to practice the fix afterwards, the project's own helpers are enough: select only `FEATURE_COLUMNS`, call `split_dataset` first, then fit `fit_median_imputer` and `fit_standardizer` on the training rows and apply them to both sets. Add a test that fails if `churned` appears in `feature_names`, and one that checks two runs give the same split.
