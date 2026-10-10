# Installing the handoff skill

## Claude Code
Easiest:
```
npx skills add thealignmentdesk/claude-skills --skill handoff
```
Or by hand: download the repo, then
```
mkdir -p ~/.claude/skills && cp -R skills/handoff ~/.claude/skills/
```
Then in any session type **`/handoff`** (or just say "handoff"). It saves `handoffs/HANDOFF-<date-time>.md` in your project.

**Optional: have new sessions offer your recent handoffs.** A small start-up hook runs when you start a session or type `/clear`. It shows Claude your 5 newest handoffs from the last 7 days (title, age, next step). If your first message matches one, Claude loads it; if not, it asks which one (or none). Running several sessions on different tasks is fine: it never assumes the newest is yours. It only reads files. Read `claude-code/load-handoff.sh` first, then:
```
mkdir -p ~/.claude/hooks && cp claude-code/load-handoff.sh ~/.claude/hooks/ && chmod +x ~/.claude/hooks/load-handoff.sh
```
and add the `hooks` block from `claude-code/settings-snippet.json` to `~/.claude/settings.json` (merge it if you already have hooks). Change the limits with `HANDOFF_MAX_AGE_DAYS` (default 7) and `HANDOFF_LIST_COUNT` (default 5).

Tip: add `handoffs/` to `.gitignore` if you don't want handoffs in your repo.

## claude.ai, Claude desktop and Cowork
1. Download **handoff.zip** from this repo's [Releases](../../releases/latest) page (right-hand side of the repo page).
2. In Claude: Customize (or Settings) › Skills › upload the zip, and switch it on. Skills need code execution / file creation turned on in Settings.
3. Say "handoff" in any chat, or pick it from **+ › Skills › handoff** under the message box. In a normal chat you get one block with a copy button: copy it, open a new chat, paste, send. In Cowork with a folder, it saves the file there; in a new chat on the same folder say "continue from the handoff" (if there are several, it asks which).

On the phone app, skills you've switched on in your account work too.
