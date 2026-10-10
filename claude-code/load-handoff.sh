#!/bin/bash
# The Alignment Desk kit: offer recent handoffs to a new Claude Code session.
# Runs as a SessionStart hook. Whatever it prints is added to Claude's context.
# It lists up to 5 recent handoffs (title, age, next step) so Claude can ask which one,
# instead of loading the newest one, which may belong to a different task.
# It only reads files; it never sends anything anywhere.
MAX_AGE_DAYS="${HANDOFF_MAX_AGE_DAYS:-7}"
MAX_COUNT="${HANDOFF_LIST_COUNT:-5}"
ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
DIR="$ROOT/handoffs"
[ -d "$DIR" ] || exit 0
NOW=$(date +%s); N=0; LIST=""
while IFS= read -r F; do
  [ -n "$F" ] || continue
  M=$(stat -f %m "$F" 2>/dev/null || stat -c %Y "$F")
  AGE=$(( (NOW - M) / 3600 ))
  [ "$AGE" -lt $(( MAX_AGE_DAYS * 24 )) ] || continue
  N=$((N + 1))
  TITLE=$(grep -m1 '^# ' "$F" | sed -e 's/^# *//' -e 's/^Handoff: *//')
  NEXT=$(awk '/^## Next step/{f=1;next} /^## /{f=0} f && NF{print; exit}' "$F" | cut -c1-160)
  if [ "$AGE" -lt 24 ]; then WHEN="${AGE}h ago"; else WHEN="$((AGE / 24))d ago"; fi
  LIST="$LIST
$N. ${F#$ROOT/}  ($WHEN)
   ${TITLE:-untitled}
   Next step: ${NEXT:-not stated}"
  [ "$N" -lt "$MAX_COUNT" ] || break
done <<< "$(ls -t "$DIR"/HANDOFF-*.md 2>/dev/null)"
[ "$N" -gt 0 ] || exit 0
cat <<MSG
Recent handoffs exist in this project (the user may run several sessions on different tasks, so do NOT assume the newest one is theirs):
$LIST

How to use this:
- If the user's first message clearly matches one of these, read that file and continue from it; say in one line which handoff you loaded.
- If it's unclear, ask once: show this numbered list (title, age) plus "none, new task", and wait. Then read the chosen file.
- If the user is clearly starting something unrelated, ignore this list and don't mention it.
MSG
