# Client acquisition — shared pipeline folder

**Last sync:** 23 September 2026
**Written by:** the Cowork cloud session that runs the daily VO lead batch
**Read by:** Bingo, and anything else with this repo checked out

---

## Start here

| File | What it is |
|---|---|
| **`FUNNELS.md`** | The A–M taxonomy. What each funnel is, what they buy, how to pitch them, which door to knock on. |
| **`ROSTER.md`** | All 132 companies grouped by funnel, with contact, email status and pipeline status. The master index. |
| `funnel-c-top-10.md` | The ranked e-learning shortlist — a worked example of a funnel taken to depth. |
| `funnels-c-d-e.md` | The original 3 Sep C/D/E sweep. Superseded by ROSTER.md but keeps the raw findings. |
| `monday-com.md` | The first contact card, and the template the rest follow. |
| `batch-02` … `batch-11` | Historical daily runs, in order. Raw material — ROSTER.md is the current view. |

The batch files are kept as a record of how each contact was found. **They are no longer the working view.** Work from `ROSTER.md`.

---

## How this gets here

Three places hold this material and they are not the same thing:

| Where | What | Who reads it |
|---|---|---|
| claude.ai Project "Client Aquisition" | the research docs, source of truth | Claude web/desktop, the Cowork session |
| **this folder, in the `bingo-cloud` repo** | a mirror as real `.md` files | Bingo, and any checkout |
| Google Sheets "VO Outreach Pipeline Tracker" | the contact tracker, updated on send | Claude via the FGAC connector |

The daily batch runs in an ephemeral cloud container. Nothing it writes survives unless it is pushed to the Project **and** committed here. It now does both, automatically, every weekday morning — no computer required at either end.

**Sync direction is one-way: cloud → repo.** If Bingo edits a file in this folder, the next sync overwrites it. Anything Bingo wants to persist upstream should go somewhere else in the repo, or be said in the Cowork session so it can be merged into the Project.

---

## The one blocking fact

**28 outreach drafts sit unsent in `spencer@spencerzvoice.com`** — and the count is rising, not falling.

The lead batch has a hard gate at step 0: while unsent drafts exist, the run researches and banks contacts but writes no new drafts. That gate has held for nine consecutive runs — but six drafts appeared on 23 Sep anyway, from a source not yet identified, so treat the gate as unproven until that is understood.

The oldest ten drafts (Shell, Experian, Shelter, Purdue, Snowflake, Sarofsky, Tendril, Goalhanger, iAM Learning, Skillsoft) are dated **4 September** and have never been sent. One send session has happened: 22 September, 15 messages to Asana, monday.com, Zoom, HubSpot, Grammarly, ClickUp, Canva and Atlassian.

Roughly 95 fully-vetted, zero-touch contacts are banked across these files. **Research is not the constraint on this pipeline. Sending is.** The single highest-value action available is clearing that queue.

---

## Two traps

1. **Two Gmail accounts exist.** `spencerzpearman@gmail.com` is personal; `spencer@spencerzvoice.com` is the VO business account and the only one that matters. A run on 11 September checked the wrong one, found it empty, and drafted nine emails into the personal account. They were deleted; nothing was sent. Always target the business account explicitly.

2. **A verified email is not proof of a current job.** Enrichment has repeatedly caught people who had already moved on. A first-party team page beats a verified mailbox — most of all in Funnel J, where studio staff churn fastest.

---

## Do not touch

The sync only ever writes inside `reference/client-acquisition/`. Everything else in this repo — `reference/outreach-pipeline.md`, `memory/`, `CLAUDE.md`, `AGENTS.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`, `voice.md` — is Bingo's and is never written by the batch.
