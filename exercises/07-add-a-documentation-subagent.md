# Exercise 7: Add a Documentation Subagent (Optional)

This final exercise shows where a custom system prompt makes a subagent genuinely better. The default Claude Code voice is concise and code-focused, which is great for coding and wrong for documentation. A documentation subagent sets a different audience, tone, and structure.

## What to do

You will create `.claude/agents/pipeline-doc-writer.md`.

### Option A: let Claude generate it (recommended)

Run:

```text
/agents
```

Choose **Create new agent**, pick **Project** scope, and describe the subagent:

- Purpose: write clear, developer-facing documentation for modules in a Python machine learning codebase. The audience is engineers who will call the module or build on it.
- Tone: precise and practical, not marketing copy.
- Tools: Glob, Grep, Read.
- Model: sonnet. Color: green.
- Output sections: an Overview of what the module does, an Inputs section for the data it expects, a Usage section for the main functions with a short example, and a Data caveats section for leakage, reproducibility, and other limits.
- A firm rule: read the code to ground every statement, and do not invent behavior that is not in the source.

`/agents` asks for some of these settings in its own steps rather than reading them from your brief. Before you move on, make sure the saved file matches the brief:

- **Name.** Claude proposes a name. If it is not `pipeline-doc-writer`, change the `name:` line and the file name to `pipeline-doc-writer`. The prompts in later exercises use that exact name.
- **Tools.** In the tool step, select only Glob, Grep, and Read. The read-only category can include extra tools such as WebFetch, so open the file afterwards and make sure the `tools:` line reads `Glob, Grep, Read`.
- **Model and color.** Pick Sonnet and Green in their steps.

Compare the generated file with Option B below. The wording of the system prompt will differ, and that is fine. The name, the tools, and the output format should match.

### Option B: write the file yourself

Create `.claude/agents/pipeline-doc-writer.md`:

```markdown
---
name: pipeline-doc-writer
description: Writes developer documentation for data and training
  pipeline modules in the team's standard format. Use when a new
  pipeline module is ready and needs developer-facing docs.
tools: Glob, Grep, Read
model: sonnet
color: green
---
You write clear, developer-facing documentation for a Python machine
learning codebase. Your audience is engineers who will call a module or
build on it. Use a precise, practical tone - not marketing copy.

For the module you are given, produce:
- Overview - what the module does, in two or three sentences.
- Inputs - the data it expects: columns, types, and missing values.
- Usage - the main functions, their parameters, and a short example.
- Data caveats - leakage, reproducibility, and other limits a caller
  must know before trusting the results.

Read the code to ground every statement. Do not invent behavior that is
not in the source.
```

## Run it

If you wrote the file by hand, restart Claude Code. Then use this prompt exactly:

```text
Use the pipeline-doc-writer to document src/churn_model/training/prepare.py
```

## What to observe

The result reads like documentation, not a code dump, because the system prompt set the audience, the tone, and the structure. Compare it with what the default voice produces if you ask the main thread to "document this file". The difference is the custom system prompt.

## What to look for in the code

The tool list is identical to the other two subagents: Glob, Grep, Read. The documentation subagent has no extra tools. What changes its output is the system prompt alone.

## A note on the sample module

Because `src/churn_model/training/prepare.py` contains deliberate flaws, honest Data caveats for this module describe problems: the label is among the features, scaling is fitted before the split, the split is not seeded, and missing values become zero. That is expected. A grounded documentation subagent reports what the code actually does rather than what the `build_training_sets` docstring ("Clean, scale, and split...") suggests it does. This is the same discipline you would want in a model card.

## Learning outcome

You can create a subagent whose value comes from a custom system prompt rather than from special tools, and you can explain why tone, audience, and structure belong in the system prompt.

## Where to go next

- Add concrete example conversations to each `description` to sharpen when Claude delegates.
- Commit `.claude/agents/` so everyone who clones the project inherits the same subagents.
- Keep the anti-patterns in mind. Do not chain subagents into pipelines where each step depends on the last, do not create expert persona subagents that add no capability your main thread lacks, and do not use a subagent to run tests when you need the full output to debug.
