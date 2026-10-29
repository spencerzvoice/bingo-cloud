# Model routing + handoffs (Spencer, 2026-10-29)

Spencer: "if I'm asking you a question that is better suited for a model that isn't what the chat is set to, you write a handoff document (an MD file) and send it to a new chat, and choose the model that is most efficient." He should never have to pick the model himself.

## Which model
| Model | Use for |
|---|---|
| Haiku | single lookups, reading back one value or file line |
| Sonnet | marketplace quotes, logging, tracker updates, follow-up queue checks, draft sweeps, file moves, routine checklists |
| Opus | pitches, hooks, buyer-gate calls, script coaching, research, anything client-facing, daily judgment |
| Fable | big money or strategy decisions (€10k plan, lane choice, DDO plan, a large contract/buyout), one-time system redesigns |

API prices per MTok in/out (claude-api skill, 2026-10-29): Fable $10/$50 · Opus $4/$20 · Sonnet $2/$10 · Haiku $0.10/$0.50.

## When to hand off (desktop only)
- **Stay here** when it's a quick answer or a handful of tool calls. A new chat reloads the whole instruction stack (~21k tokens) and has to rediscover context, so a small task costs more handed off than answered on the "wrong" model.
- **Stay here** when the task leans on this conversation (what we just found or decided). Re-explaining it in a brief loses detail.
- **Hand off** when the task is substantial and its best model differs from this chat's: a mechanical batch (down to Sonnet/Haiku) or a big decision (up to Fable, or Opus from a Sonnet chat).
- Say it in one line first: "Handing this to a Sonnet chat: <task>." No asking for permission; Spencer set this rule.
- Cloud/phone sessions can't start chats: just do the work there.

## How
1. Write `handoffs/YYYY-MM-DD-<slug>.md` (gitignored, desktop only) from the template below.
2. **Going down (cheaper model):** `start_session` initiation `user_asked`, context `fresh`, `use_worktree: false`, `model` = the cheaper id, prompt = "Read `handoffs/<file>.md` and do the task in it." The app accepts a same-or-cheaper model without asking.
3. **Going up (Fable, or Opus from a Sonnet chat):** `start_session` can't pick a pricier model (it's ignored). So: start it with prompt "Reply only 'Ready' and stop. The task comes in the next message.", then `set_session_model` on it to the higher model (the app shows Spencer one approval), then `send_message` "Read `handoffs/<file>.md` and do the task in it."
4. Model ids: use the ids the app's picker offers; if one is refused, the result lists the valid ones. Record the working ids here once seen.
5. Link the new chat to Spencer, then stop working the task here.

## Handoff template
```markdown
# Handoff: <task>  (<date>, from <model> chat → <model>)
**Why this model:** <one line>
**Task:** <what Spencer asked, in his words where possible>
**Done looks like:** <deliverable + where it goes>
**Context already established:** <facts, decisions, numbers, with source + ✅/🟡/❓ tags>
**Files to read:** <paths>
**Rules that apply:** <e.g. outreach-email skill, buyer gate, send window, pitch cap>
**Don't redo:** <checks already run this session and their results>
**Report back:** wrap up with the result; Spencer reads that chat directly.
```
