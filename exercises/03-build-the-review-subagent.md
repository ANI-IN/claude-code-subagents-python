# Exercise 3: Build the Review Subagent

Your second subagent reviews code with fresh eyes. Claude reviews code more effectively when it sees the work as someone else's, in a clean context, rather than as something it just helped write. A review subagent gives you that fresh perspective, and it lets you encode your team's review standards in one place.

For an ML codebase, the most expensive mistakes are not crashes. They are pipelines that run cleanly and produce results you cannot trust: a label that leaks into the features, a test set that influenced training, a split that changes every run. This reviewer is built to look for exactly those.

## What to do

You will create `.claude/agents/pipeline-reviewer.md`.

### Option A: let Claude generate it (recommended)

Run:

```text
/agents
```

Choose **Create new agent**, pick **Project** scope, and describe the subagent:

- Purpose: a correctness reviewer for a Python machine learning codebase that predicts customer churn. It examines pipeline code with fresh eyes and reports issues.
- Behavior: read and analyze only. It must not modify code.
- Tools: Glob, Grep, Read.
- Model: sonnet. Color: purple.
- Focus areas: target leakage (the label used as a feature), train/test contamination (statistics fitted on data that includes the test set), reproducibility (randomness without a fixed seed), missing values silently dropped or replaced with made-up numbers, and logic that duplicates an existing helper.
- Output format: a numbered report with Summary, Critical Issues, Major Issues, Minor Issues, an Approval Status of either "Safe to merge" or "Requires changes", and an Obstacles Encountered section.

`/agents` asks for some of these settings in its own steps rather than reading them from your brief. Before you move on, make sure the saved file matches the brief:

- **Name.** Claude proposes a name. If it is not `pipeline-reviewer`, change the `name:` line and the file name to `pipeline-reviewer`. The prompts in later exercises use that exact name.
- **Tools.** In the tool step, select only Glob, Grep, and Read. The read-only category can include extra tools such as WebFetch, so open the file afterwards and make sure the `tools:` line reads `Glob, Grep, Read`.
- **Model and color.** Pick Sonnet and Purple in their steps.

Compare the generated file with Option B below. The wording of the system prompt will differ, and that is fine. The name, the tools, and the output format should match.

One phrase in the description is worth adding on purpose: **you must tell the agent precisely which files to review**. With that instruction present, Claude writes a sharper task prompt that names the actual files, instead of leaving the subagent to guess which files matter.

### Option B: write the file yourself

Create `.claude/agents/pipeline-reviewer.md`:

```markdown
---
name: pipeline-reviewer
description: Reviews Python ML pipeline code - data loading, feature
  preparation, and train/test splitting - for data leakage,
  reproducibility, and correctness. Use after writing or modifying
  pipeline, feature, or training code. You must tell the agent
  precisely which files to review.
tools: Glob, Grep, Read
model: sonnet
color: purple
---
You are a correctness reviewer for a Python machine learning codebase
that predicts customer churn. You examine pipeline code with fresh eyes
and report issues. You read and analyze; you do not modify code.

Focus on:
- Target leakage - the label, or anything derived from it, used as a
  model feature.
- Train/test contamination - statistics such as means, medians, or
  vocabularies fitted on data that includes the test set.
- Reproducibility - randomness without a fixed seed, or results that
  change from run to run.
- Missing values silently dropped or replaced with made-up numbers.
- Logic that duplicates an existing helper instead of reusing it.

Provide your review in this format:
1. Summary - what you reviewed and an overall assessment.
2. Critical Issues - leakage or logic errors that make results wrong.
3. Major Issues - reproducibility, quality, or architecture concerns.
4. Minor Issues - style, documentation, or edge-case notes.
5. Approval Status - "Safe to merge" or "Requires changes".
6. Obstacles Encountered - any setup issues or quirks discovered during
   the review.
```

## What to look for in the code

Two design choices carry this subagent:

- **The tools are read-only.** The reviewer reads and searches the files you point it at, but it has no edit or write access. It reviews; it does not change. The lesson notes that a reviewer can also be given Bash so it can run `git diff`. This one does not need it, because you tell it exactly which file to review.
- **The output format is explicit.** Numbered sections give the subagent clear stopping points and return a result the main thread can use. The Obstacles Encountered section surfaces anything unexpected, such as a setup quirk or a workaround, so it is not rediscovered later.

## What to observe

Compare this configuration with the explorer from Exercise 2. The tool lists are the same, yet the two subagents do very different jobs. The difference lives entirely in the description and the system prompt. Behavior comes from instructions, not from tools alone.

## Learning outcome

You can create a read-only review subagent with a structured output format, you understand how a specific description steers both when it runs and what it is told to do, and you can name the ML-specific failure modes it checks for.
