# Agent team prompt (Claude Code)

Fill in the [brackets], delete the roles you don't need, then paste it into Claude Code.

> [What the job is, in one sentence.] Start with [the file that describes the job, e.g. BRIEF.md].
> Use an agent team. You are the coordinator. Spawn [number] teammates with these names and jobs:
> - **[Specialist 1 name]:** [one-line job, e.g. "Compare the options in suppliers/ and recommend the ones that meet the brief."]
> - **[Specialist 2 name]:** [one-line job]
> - **[Gatekeeper name]:** Check every proposal against [the brief / the budget / the rules] and send back anything that doesn't meet them.
> - **[Finisher name]:** Write [the deliverables] in [output folder] from the agreed plan.
>
> Have them message each other and challenge each other's findings.
> Each teammate writes only its own files.
> Nothing is final until [Gatekeeper name] signs it off.
> Wait for your teammates to finish before you write the final answer.
> Put the deliverables in [output folder].
