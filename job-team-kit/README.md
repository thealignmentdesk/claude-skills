# Job search agent team kit

A free kit for running a job search with a team of five Claude agents in **Cowork** (claude.ai › Projects), with no code. From The Alignment Desk: "AI Agent Team: 5 Agents and the 1 That Says No".

The team finds jobs, writes a CV and cover letter for each one, checks every line against your real CV, and leaves each finished package in Gmail as a **draft**. It never sends, submits or applies. You read the draft and apply yourself.

## The team
| Role card | Job |
|---|---|
| `roles/coordinator.md` | Runs the board: hands out tasks, passes messages on. Never does the work itself. |
| `roles/job-searcher.md` | Finds jobs from the last 7 days, opens each one, picks the best 3, lists the skipped ones with reasons. |
| `roles/writer.md` | Writes a CV and cover letter per job, using only facts from `candidate/master-cv.md`. |
| `roles/reviewer.md` | Checks every line. Sends anything not in the CV back, quoting the exact line. The only one who can sign a job off. |
| `roles/applier.md` | Builds the package (job link, pay, form answers, letter, CV) for signed-off jobs. Never submits. |

`BOARD.md` is the shared task board every agent reads and writes. `drafts/`, `jobs/` and `ready/` start empty; the agents fill them.

## You need
- A paid Claude plan with Cowork.
- The Gmail connector, with sending blocked: Customize › Connectors › Gmail › tool permissions. Create draft email: Always allow. Send email message, Reply to email, Forward email: Blocked.

## Make it yours (do all of this before you make the project; scheduled runs use the project's own copy)
1. `roles/job-searcher.md`: change the job titles and the city.
2. `candidate/master-cv.md`: delete Jordan's details (Jordan Reyes is made up) and paste in your whole CV. The writer can only use what's there, and the reviewer checks against it.
3. `roles/reviewer.md`: make it as strict as you like, for example "check that every date matches the CV".

## Run it once
1. In Claude, open Projects › New project, add this folder, create it.
2. Paste `coordinator-prompt.md` (change "I'm Jordan" to your name). Allow the folder when Claude asks.
3. Watch `BOARD.md` fill up. When the packages are ready, the team stops and asks which ones may go to Gmail.

## Put it on a schedule
Paste `scheduled/routine-prompt.md` into the project chat. Claude makes a routine (weekdays at about 7 AM). On a schedule nobody is there to answer, so the checkpoint moves: every signed-off package goes straight to a Gmail draft, and the draft is your checkpoint. The reviewer's sign-off still comes first. Every run leaves a draft, even with no new jobs ("Job search ran: no new jobs" + the date), so a quiet day doesn't look like a failure.

Already have a routine? `scheduled/change-prompt.md` adds the "it ran" draft to it.

`scheduled/coordinator.md`, `applier.md` and `job-searcher.md` are versions of those cards written for unattended runs (never stop to ask, skip jobs that already have a draft, always finish with the applier). If your scheduled runs stop to ask questions or skip the "it ran" draft, copy them over the matching cards in `roles/`.

## Before you rely on it
- Read every draft before you apply. Job sites such as LinkedIn and Indeed ban bots that apply, and a sent application can't be unsent.
- Teams use much more than one chat (Anthropic measured multi-agent systems at about 15× the tokens of a chat). For a short, clear job, one agent is enough.
