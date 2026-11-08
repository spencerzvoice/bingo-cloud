---
name: committee
description: "Cold-eyes review of a finished piece of work before it goes out — a fresh-context reviewer that never saw the reasoning behind the work, only the output. TRIGGERS: 'committee this', 'run the committee', 'cold review', 'cold eyes on this', 'review before I send', 'check this before it goes out', 'devil's advocate this', 'fact-check this', 'reader reaction', 'poke holes in this'. Use AFTER something is drafted (a plan, report, recommendation, code change, outreach copy, anything with numbers/names/claims going external). Do NOT use for an undecided question with no work product yet — that's the llm-council skill. Skip for small, low-stakes, easily reversible work."
---

# The Committee — Cold-Eyes Review Before Delivery

**What it is:** a fresh-context AI reviewer that checks your work before it goes out, instead of after someone else catches the mistake.

## The problem it solves

When you write something and then reread it yourself, you're checking it with the same brain that made the mistake in the first place. If you missed a bad assumption while writing, you'll miss it again while reviewing — you already believe it's fine. That's not a discipline problem, it's structural: you can't see your own blind spot from inside it.

The fix is a second, independent set of eyes that never saw the reasoning behind the work — only the finished output. It reviews it the way a stranger would: no context on why you made the choices you made, no assumption that any of it was done for a good reason.

## The Committee vs. the LLM Council — not the same tool

| | **The Committee** | **The LLM Council** |
|---|---|---|
| **Question it answers** | "Is this piece of work good?" | "Which option should I choose?" |
| **When you run it** | AFTER something is drafted | BEFORE you've decided |
| **Input** | The finished work, pasted in cold | The open decision + context, no work product yet |
| **Structure** | One reviewer (or a stacked sequence of specialists), each seeing only the work | Five advisors argue independently, peer-review anonymously, chairman gives a verdict |
| **Output** | What's wrong, what's missing, what's weak — a fix list | A recommendation on what to do, with the disagreement shown |

**Rule of thumb:** if the thing already exists and you want it checked, that's the Committee. If the thing doesn't exist yet and you're stuck choosing, that's the Council. A real workflow often uses both: Council to decide the direction, then Committee to check the plan that came out of it before it ships.

## The one rule that makes it work: never let it become an echo chamber

The reviewer must never see:
- The reasoning or conversation that produced the work
- Your own explanation of why you made each choice
- Any self-assessment ("I think this part is weak, can you check?")

Paste **only the finished work**. Nothing else. Spawn a genuinely separate sub-agent with a clean context (or, in a plain chat, open a brand-new conversation).

## Timing rule

Run it **before** the work reaches whoever it's for — never after they've already caught a problem.

## When to run it

- Strategy, plans, recommendations, decisions you're about to act on
- Reports or write-ups someone else will read and act on
- Any outward-facing writing — copy, scripts, posts — before it publishes
- Code changes, especially anything touching money, user data, or access control
- Any numbers, dates, names, or claims in something going external

Skip it for small, low-stakes, easily reversible stuff.

## The five review modes

Pick the one that matches what you're worried about. Run more than one on the same piece if it's high-stakes.

### 1. Cold Review (the everyday default)
> Review the work above with completely fresh eyes. Do not assume anything was done for a good reason. Tell me three things: what is actually wrong, what is missing, and what is weak or unclear. Then give me one prioritized list of fixes, ranked by how much each improves the result. Be blunt and specific, not polite. If something is genuinely strong, say so in one line and move on.

### 2. Devil's Advocate (before committing to a plan or pitch)
> Argue against the work above. Take the opposite side and build the strongest possible case that this idea, plan, or argument is wrong. Attack the weakest assumptions, the holes in the logic, and the risks being glossed over. Be the smartest critic in the room, not a cheerleader. End with the single objection that most needs a good answer before moving forward.

### 3. Fact-Checker (anything with numbers, names, dates, or claims)
> Fact-check the work above with a skeptical eye. Hunt for claims that are wrong, exaggerated, unverified, or made up — including numbers, names, dates, quotes, and any "everyone knows" statement. For each one, flag it, say why it's questionable, and give either the accurate version or exactly what needs to be checked to confirm it. Assume at least one thing is wrong and go find it.

### 4. Reader's Reaction (anything outward-facing)
> Role-play the exact audience this is for and react to the work above the way that real person would. Here is who it's for: [one line]. Read it cold and say: where it loses their attention, what confuses them, what they quietly doubt or disagree with, and the one thing that would make them actually take the action this is asking for. React like a real, slightly impatient human, not a helpful assistant trying to be nice.

### 5. Expert Panel (high-stakes only — a major call, not routine work)
> Spawn three reviewers, each in their own separate context so they cannot see each other's notes. First, pick the three most useful expert lenses for this specific piece of work (for example: a sharp editor, a real subject-matter expert, a skeptical buyer, a numbers person) and say who was picked and why. Have each give their top three changes ranked by impact. Then summarize where they agree, where they disagree, and exactly what to fix first.

## How to actually run this

**In a tool with sub-agents (Claude Code):** spawn a real sub-agent for the review — genuinely separate context, no chance it inherits the reasoning that produced the work.

**In a plain chat:** open a brand-new conversation. Paste in only the finished work and the review prompt.

## Building this into a team of AI agents

Every agent that produces anything weighty runs it through a Committee review before handing it up the chain or out to a human. Pick the review mode by role — a writer runs Reader's Reaction on copy, a planner runs Cold Review + Devil's Advocate on strategy, anything with numbers gets Fact-Checker regardless of role. Bake it in as a default rule, not something to remember to ask for.
