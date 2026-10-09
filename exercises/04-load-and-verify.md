# Exercise 4: Load and Verify Your Subagents

Claude Code registers subagents when it starts. If you created a subagent through `/agents`, it is available right away. If you wrote or edited the file by hand, restart Claude Code so it picks up the new configuration.

## What to do

Exit Claude Code, then start it again from the project root:

```bash
claude
```

Then confirm the subagents are available:

```text
/agents
```

Both `codebase-explorer` and `pipeline-reviewer` should appear in the list, scoped to the project.

## What to look for in the code

If a subagent does not show up, open its file under `.claude/agents/` and check the frontmatter:

- The file must live in `.claude/agents/` and end in `.md`.
- The YAML block must open and close with `---` lines.
- A `description` that spans several lines needs every continuation line indented, as in the examples from Exercises 2 and 3.

Compare your file with the examples in Exercises 2 and 3 line by line. A missing `---` or an unindented continuation line is enough to stop a subagent from loading.

## What to observe

- Subagents are project-level, so anyone who clones this project sees the same subagents. That is why they belong in `.claude/agents/` rather than in your personal `~/.claude/agents/` folder.
- The list shows the color you set for each one. Color helps you tell which subagent is active when several are running.

## Troubleshooting

| Symptom | Resolution |
| --- | --- |
| A subagent is not listed | The file must be in `.claude/agents/` with valid YAML frontmatter. Restart after any change. |
| The wrong subagent runs later | Two descriptions overlap. Make them distinct so each one clearly owns its task. |

## Learning outcome

You know how to load subagents and confirm they are registered, and you can diagnose the most common reason a subagent fails to appear.
