# Claude agent team kit

A free starter kit for running a small team of Claude agents on one job: in **Claude Code** (built-in agent teams) or in **Cowork** (a shared task board and a coordinator). From The Alignment Desk, video 15.

## What's inside
| File | Use it for |
|---|---|
| `roles/` | Five role cards: coordinator, specialist, checker, gatekeeper, finisher. Copy, rename and fill in the blanks. |
| `claude-code/settings-snippet.json` | The one setting that switches agent teams on. |
| `claude-code/team-prompt.md` | A fill-in-the-blanks prompt that starts a team and makes the teammates talk to each other. |
| `cowork/BOARD.md` | The shared task board every agent reads and writes. |
| `cowork/coordinator-prompt.md` | The prompt that runs the board in Cowork. |

## Four rules that make a team actually work together
1. **One job per agent.** Write it as a one-line role card. If two agents could do the same task, merge them.
2. **Someone can say no.** Include a checker or gatekeeper whose job is to send work back.
3. **Tell them to talk.** Put "message each other and challenge each other's findings" in the prompt. Without it, agents tend to work side by side and report only to the coordinator.
4. **Define "done".** For example: "Nothing is final until the gatekeeper signs it off."

## Before you start
- **Is a team worth it?** A team uses many times the usage of a single Claude (Anthropic's docs say about 7× in some setups; our small test used more). For a small job that fits in one conversation, one Claude is faster and cheaper. Teams pay off when the work splits into independent parts, needs a second opinion, or is too big for one context.
- Start with **3–5 agents**.
- Give each agent **its own files to write** so they don't overwrite each other.
- Agent teams in Claude Code are **experimental** and off by default.

## Claude Code: quick start
1. Add the contents of `claude-code/settings-snippet.json` to your `~/.claude/settings.json` (or project `.claude/settings.json`), or run `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` before `claude`.
2. Open the folder with your job's files, start `claude`, and paste your filled-in `team-prompt.md`.
3. Watch and steer: press **Down** to move into the panel under the prompt, **Down** again to pick a teammate, **Enter** to open it and message it, **x** to stop it. To go back, press **Down**, choose **main** and press **Enter** (pressing Up from main brings back your last message instead).
4. If the coordinator starts doing the work itself, tell it: "Wait for your teammates to complete their tasks before proceeding."

## Cowork: quick start
1. Put `cowork/BOARD.md` and the `roles/` folder (your filled-in cards) into the folder with your job's files.
2. Give Cowork that folder and paste your filled-in `cowork/coordinator-prompt.md`.
3. Watch `BOARD.md` fill up: tasks, owners, results, and messages between roles.
4. If it stops early, say: "Read BOARD.md and carry on until every task is done and signed off."

## Example
In the video, the job was planning a company day out for 42 people on a fixed budget. The team was a coordinator, a venue scout and a catering lead (specialists), a budget and rules keeper (gatekeeper) and a writer (finisher). The rules keeper sent work back (wrong transport, then fixes to the writer's draft) before signing it off.
