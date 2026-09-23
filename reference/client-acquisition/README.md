# Client Acquisition — synced from the claude.ai Project

**Synced:** 23 September 2026 · **Source of truth:** the "Client Aquisition" Project on claude.ai
**Synced by:** the Cowork cloud session that runs the daily 8am VO lead batch

---

## Where this actually lives

These files are a **copy**. The originals are project docs inside a claude.ai Project called **Client Aquisition** — cloud-hosted by Anthropic, visible under Projects in the Claude web and desktop apps. They are not files on any disk by default, which is why Bingo could not see them.

There are three separate places this pipeline's material sits, and they are not the same thing:

| Where | What | Who can read it |
|---|---|---|
| claude.ai Project "Client Aquisition" | the 13 research docs, source of truth | Claude web/desktop, the Cowork session |
| **this folder** | a synced copy as real `.md` files | Bingo, and anything else on this machine |
| Google Sheets "VO Outreach Pipeline Tracker" | the 100-row contact tracker, updated on send | Claude via the FGAC connector |

The Cowork session that generates these docs runs in an **ephemeral cloud container**. Nothing it writes survives the session unless it is pushed either to the Project or here. That is the whole reason this folder exists.

## Sync direction

One-way, cloud → local, on request. Nothing here is read back into the Project automatically. If Bingo edits a file in this folder, say so in the Cowork session and it can be merged upward — otherwise the next sync will overwrite it.

`C:\Users\spenc\Bingo` is a git repo, so these files can be committed like anything else in it. They were not previously tracked because they had never been written to disk.

---

## What is in here

### Current-state docs
- `funnel-c-top-10.md` — the ranked Funnel C shortlist, the live working doc for building that pipeline
- `funnels-c-d-e.md` — the original C/D/E sweep, 3 Sep; contains the D and E contacts and the method note

### Batch docs, newest first
Each is one day's run of the `vo-lead-batch` skill: 8–10 companies, a primary and backup contact each, Apollo-verified emails, a dated hook per company, and a send order.

- `batch-11-held-companies-resolved.md`
- `batch-10-cybersecurity-leftovers-and-ixdf.md`
- `batch-09-backlog-consolidation.md`
- `batch-08-cybersecurity-fintech-branch-out.md`
- `batch-07-saas-inhouse-video-held-items-closed.md`
- `batch-06-consumer-brands-and-branch-out.md`
- `batch-05-funnel-a-and-branch-out.md`
- `batch-04-saas-and-elearning-marketing.md`
- `batch-03-studios-and-corporate-inhouse.md`
- `batch-02-saas-inhouse-video.md`
- `monday-com.md` — the first contact card, and the template the rest follow

---

## The five funnels

- **A** — SaaS, design-led (Figma, Notion, Linear, Vercel, Framer, Webflow, Miro). Launch films and feature explainers. Low volume, high rate.
- **B** — SaaS with an in-house video team (HubSpot, Atlassian, Canva, Asana, Zoom, ClickUp, Zapier…). Weekly output. **Best retainer funnel.**
- **C** — E-learning platforms (MasterClass, Skillshare, LinkedIn Learning, Coursera, Udemy…). Target their *marketing* output, not their course catalogue. One deliberate exception: IxDF, where course narration is the product.
- **D** — Corporate L&D software (Articulate, Docebo, 360Learning, Go1, Absorb…). Product demos and thought-leadership.
- **E** — Streaming and promo. **Parked** until a dedicated promo demo exists — promo VO is a separate performance discipline with its own casting route through agents.

---

## The one blocking fact

**35 outreach drafts sit unsent in `spencer@spencerzvoice.com`.** The lead batch has a hard gate at step 0: if unsent drafts exist, the run researches and banks contacts but writes no new drafts. That gate has now held for nine consecutive runs.

Roughly 110 fully-vetted, zero-touch contacts are banked across these docs. **Research is not the constraint on this pipeline. Sending is.**

Two traps worth carrying into any work Bingo does here:

1. **Two Gmail accounts exist.** `spencerzpearman@gmail.com` is personal; `spencer@spencerzvoice.com` is the VO business account and the only one that matters. A run on 11 September checked the wrong one, found it empty, and drafted nine emails into the personal account. They were deleted; nothing was sent. Always target the business account explicitly.
2. **A verified email is not proof of a current job.** Enrichment has repeatedly caught people who had already moved on. A first-party team page beats a verified mailbox.
