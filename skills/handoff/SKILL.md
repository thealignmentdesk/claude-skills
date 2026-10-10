---
name: handoff
description: Packs the current conversation into a short, self-contained handoff so the work can continue in a fresh chat or session without re-explaining anything. Use when the user says "handoff", "hand off", "save where we are", "continue in a new chat", "this chat is getting long", "before I take a break", or is about to switch device, app, person or AI.
---

# Handoff

A fresh chat knows nothing about this one. Your job is to write the note that lets it carry on at full speed: what we're doing, what's decided, where we are, and the exact next step. Nothing else.

## 1. Write the handoff

Use this template. Leave out any section that would be empty. Aim for under 400 words; go longer only for real detail (numbers, names, file paths) the next chat can't work without.

```
# Handoff: <short title> (<date and time>)

## Goal
<What we're trying to achieve, for whom, and what "done" looks like. 1-3 lines.>

## Decisions made (don't reopen)
- <Decision>: <why, in a few words>

## Where we are
- Done: <finished items>
- In progress: <half-done items and exactly how far they got>

## Tried and didn't work
- <What, and why it failed>

## Key facts
- <Exact numbers, names, dates, settings, file paths or links the work depends on>

## Open questions
- <Anything still undecided, and who decides it>

## Next step
<The single next action, specific enough to start immediately.>

## Start the new chat with
"<One sentence the user can send first, e.g. 'Read the handoff above and do the next step.'>"
```

Rules:
- **Self-contained.** Write for a reader who saw none of this conversation. No "as discussed", no "the file from earlier": name it.
- **Exact, not vague.** Copy real figures, names and paths. Don't round or paraphrase them.
- **Decisions with reasons.** The reason stops the next chat from undoing a decision.
- **Mark guesses.** If something wasn't checked, say "(not verified)".
- **No secrets.** Never include passwords, API keys, tokens, card numbers or other credentials, even if they appeared in the chat. Write "(stored separately)" instead.
- **The user's words win.** If the user says what to keep or drop, follow that.
- Don't ask questions first. Write the best handoff you can from the conversation; the user can correct it.

## 2. Deliver it where the user can use it

Check what you can do here, then use the first option that works:

1. **You can write files** (Claude Code, Cowork with a folder): save it as `handoffs/HANDOFF-<YYYY-MM-DD-HHMM>-<topic>.md`, where `<topic>` is 2-4 lowercase words joined by hyphens (e.g. `HANDOFF-2026-10-10-0215-sister-party-invites.md`), so the user can tell several sessions' handoffs apart. Use the real current time (run `date +%Y-%m-%d-%H%M` if you can; if you can't get the time, use the date and a counter) in the project or chosen folder (create `handoffs/` if needed). Never overwrite or delete an earlier handoff. Then tell the user:
   - Claude Code: "Saved. Type /clear or start a new session. If you installed the kit's start-up hook, the new session will offer your recent handoffs; otherwise say 'continue from the handoff'."
   - Cowork: "Saved in your folder. Open a new chat on the same folder and say 'continue from the handoff'."
2. **You can't write files** (claude.ai, desktop or phone chat): show the whole handoff in **one** code block so it has a single copy button, then say: "Copy this, open a new chat, paste it and send."

Keep your own message around the handoff to two lines.

## 3. When asked to continue from a handoff

If the user pastes a handoff, use it. If they ask to continue from a saved one ("continue from the handoff", "load a handoff"):
- If they named the task, or only one recent handoff exists, read that file.
- Otherwise list the 5 newest files in `handoffs/` (title line and age) as a numbered list plus "none, new task", and ask which one. The user may run several sessions at once, so never assume the newest is theirs.

Then say in one line what you understood the next step to be, and do it. Treat "Decisions made" as settled unless the user reopens them.
