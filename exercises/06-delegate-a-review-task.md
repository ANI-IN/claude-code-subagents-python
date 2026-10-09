# Exercise 6: Delegate a Review Task

Hand the new training-data module to the review subagent. Because the reviewer sees the file fresh, in its own context, it catches issues that a thread which just wrote the code might overlook.

## What to do

Ask the review subagent to review the module. Use this prompt exactly:

```text
Use the pipeline-reviewer to review src/churn_model/training/prepare.py
```

## What to observe

The reviewer examines the file in a clean context and returns a structured report that follows your output format. Against `src/churn_model/training/prepare.py` it should report:

- **Target leakage** as a Critical Issue: `feature_names = list(rows[0])` includes the `churned` label, so the model is shown the answer.
- **Train/test contamination** as a Critical Issue: `fit_standardizer` runs on all rows before the split, so test rows shape the scaling.
- **The unseeded `random.shuffle`**, which makes every run different, and the fact that it duplicates `split_dataset`, which is seeded and stratified.
- **Missing values replaced with `0.0`** instead of using the project's median imputer.
- An Approval Status of **"Requires changes"**.

The reviewer may rank the last two items as Critical or as Major, and it may add smaller findings, such as `rows[0]` failing on an empty list. Any of those is a reasonable review. What matters is that the four planted issues are found and explained.

## What to look for in the code

Open `src/churn_model/training/prepare.py` and match each reported issue to its line. Then compare the report with the list of planted issues in Exercise 1 or in section 2 of the project README. The file itself does not mention them, so everything the reviewer found came from reading the code against its checklist and the conventions in `CLAUDE.md`.

Ask yourself which of these you would have caught on your own. Target leakage and contamination are easy to miss when you are the one who wrote the pipeline, because the code runs, the tests pass, and the evaluation score looks great. A reviewer with these failure modes written into its checklist looks for them every time. That is the value of encoding your team's review standards in one place.

## Important: these flaws are deliberate

The issues the reviewer finds are planted on purpose. They are the reason this file exists. Do not fix them, and do not ask the subagent to fix them. The reviewer is read-only by design, so it reports issues rather than changing code.

## Why fresh eyes matter

If you had written this module over many turns and then asked the same conversation to review it, the feedback would likely be weak, because that thread helped create the code and already believes it is correct. A reviewer subagent starts clean, with no memory of writing the code, and applies its criteria without that history.

## Why the reviewer does not run the tests

You might be tempted to give the reviewer Bash and ask it to run `pytest`. Here that would not help. The tests pass, so a "tests passed" summary tells you nothing about leakage. And when tests do fail, you want the full output in your main thread to debug, not a one-line summary from a subagent. Run `pytest` yourself; let the subagent read and reason.

## Learning outcome

You have delegated a review to a subagent, confirmed it found the planted ML mistakes, and seen why a fresh, isolated context with a specific checklist produces a stronger review than asking the author to check its own work.
