# Exercise 5: Delegate an Exploration Task

Now put the exploration subagent to work. You will ask a question that would otherwise require reading several files, and watch the subagent return a focused answer while the digging stays out of your main conversation.

## What to do

Ask the exploration subagent how the train/test split works. Use this prompt exactly:

```text
Use the codebase-explorer: where and how is the train/test split made, and how is it kept reproducible?
```

## What to observe

- The explorer spins up in its own context, searches the codebase, and returns a focused answer in the Answer, Key locations, and Notes format you defined.
- It should point you to `split_dataset` in `src/churn_model/data/split.py`, explain that rows are grouped by label so both sets keep the same churn rate, and explain that the shuffle uses `random.Random(seed)`, where the seed defaults to `RANDOM_SEED` in `src/churn_model/config.py`.
- A good explorer may also note, under Notes, that `src/churn_model/training/prepare.py` does its own unseeded split instead of calling `split_dataset`. That is a useful lead, and it is exactly what the reviewer should confirm in the next exercise.
- Look at what your main conversation actually records: the question and the summary. The individual searches and file reads happened inside the subagent's context and were discarded. You got the fact without the clutter.

## What to look for in the code

Open `src/churn_model/data/split.py` and `src/churn_model/config.py` and check the answer against the source. Did the line numbers the subagent cited match the code? A research subagent is only useful if its citations are accurate, so this is the habit to build: trust the summary, but spot-check the locations it gives you.

## The tradeoff

You gained a clean main context, but you gave up visibility into the path the subagent took. That is the deal with delegation: you see the destination, not the journey. It is a good trade when you only need the answer, and a poor one when you need to react to each step along the way.

## Learning outcome

You have delegated a research task and seen how a subagent keeps exploration out of your main context. You can explain the tradeoff between a clean context and lost visibility.
