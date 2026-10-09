# Exercise 2: Build the Exploration Subagent

Your first subagent is a research assistant. Its job is to answer "where" and "how" questions about the codebase and return precise file paths and line numbers, without flooding your main conversation with every file it reads.

A subagent is a Markdown file with two parts: YAML frontmatter that configures it, followed by a system prompt that instructs it. These subagents are project-level, which means they live in `.claude/agents/` and travel with the project.

## What to do

The project already has an empty `.claude/agents/` folder. If you ever need to create it from scratch, use:

```bash
mkdir -p .claude/agents
```

You have two ways to author the subagent.

### Option A: let Claude generate it (recommended)

Run the slash command:

```text
/agents
```

Choose **Create new agent**, pick **Project** as the scope, and let Claude generate the configuration from a description. Give it a brief along these lines:

- Purpose: navigate the churn-model codebase and explain where a piece of logic lives and how it works, then return a concise answer.
- Behavior: search and read only. It must never modify code.
- Tools: Glob, Grep, Read.
- Model: sonnet. Color: blue.
- Output format: a short answer, a list of key locations with file path and line number, and a notes section for assumptions or gaps. It should cite locations rather than paste large blocks of code.

### Option B: write the file yourself

Create `.claude/agents/codebase-explorer.md`:

```markdown
---
name: codebase-explorer
description: Explores the churn-model codebase to answer "where" and
  "how" questions about how something works - data loading, train/test
  splitting, feature scaling, configuration. Use when the user needs
  to locate logic or understand a flow without reading every file
  themselves. Return precise file paths and line numbers.
tools: Glob, Grep, Read
model: sonnet
color: blue
---
You are a codebase navigator for a Python machine learning project that
predicts customer churn. Your job is to locate relevant code and explain
how a piece of the system works, then return a concise answer. You only
read and search; you do not modify code.

When given a question:
1. Search the codebase for the relevant files and functions.
2. Trace the flow only as far as needed to answer the question.
3. Return a short answer in this format:
   - Answer - one or two sentences stating where the logic lives and how
     it works.
   - Key locations - file path and line number for each important point.
   - Notes - anything the caller should know (assumptions, gaps).

Do not paste large blocks of code. Cite locations instead.
```

## What to look for in the code

- The `tools` line lists only `Glob, Grep, Read`. That makes the subagent read-only. It can never alter the code it explores. This is least privilege in practice: give a subagent only what its job requires.
- The `description` is specific. It names the kinds of questions the subagent handles, and it ends with a clear instruction to return file paths and line numbers. That instruction does two jobs. It helps Claude decide when to reach for this subagent, and it shapes the task prompt Claude writes when it delegates.
- The system prompt does not say "You are a Python expert". Claude already knows Python. An expert persona adds nothing. What the prompt adds is a job, a boundary (read only), and an output format.

## What to observe

You have not run anything yet. What you have produced is a configuration file. Notice how small it is, and how much of its behavior comes from two things: the tool list and the description.

## Learning outcome

You can create a read-only research subagent, and you understand why its tool list and its description matter more than its length. Next you will build a second subagent with a very different job.
