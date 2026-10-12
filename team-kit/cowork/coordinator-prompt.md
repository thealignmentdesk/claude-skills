# Coordinator prompt (Cowork)

Put `BOARD.md` and your `roles/` folder into the job folder first. Fill in the [brackets], then paste this into Cowork with that folder selected.

> [What the job is, in one sentence.] Start with [the file that describes the job].
> You are the coordinator described in roles/coordinator.md. Run the work through BOARD.md: break the job into tasks, and for each task start a separate sub-agent with the matching role card from roles/ and only the files it needs.
> Every sub-agent must update BOARD.md when it finishes: status, findings, and any messages to other roles (@name).
> After each update, read the board, pass on any messages, and assign the next task.
> Nothing is final until [Gatekeeper name] signs it off on the board.
> Put the deliverables in [output folder].
