---
name: outreach-email
description: >-
  Draft a client outreach or re-engagement email for Spencer's voiceover
  business. Use when Spencer wants to contact a new prospect (cold), reconnect
  with a past client (warm re-engagement), or nudge someone who hasn't replied.
  Produces a ready-to-review draft in Spencer's own voice and logs it — never sends.
---

# Outreach Email

Draft outreach in **Spencer's** voice — casual, direct, warm but plain-spoken,
contractions throughout, first names, warmth before business. Not a generic
cold-email template. **You never send it** — hand Spencer a draft he reviews and
sends himself (hard rule).

## Modes

- **cold** — a new prospect (production company, agency, casting director, brand).
- **warm** — a past client being re-approached. Highest-probability source of the
  next booking; treat it as the priority.
- **follow-up** — a nudge on a cold or warm email that got no reply.

## Step 0b — EMPLOYMENT QC GATE (Spencer, 2026-10-04, HARD RULE: "this is a waste of time")

Ian Wiggins (Hitachi Rail) sat in Drafts for 4 days with a recorded sample and got handed to Spencer as a send candidate after he'd left the company. The "unresolved" flag was buried in FUNNEL-COHORTS.md and nobody told Spencer. Never again:

1. **A contact is send-ready only when their CURRENT employer is confirmed from a live source opened THIS session**: their LinkedIn profile page showing the company as current, or an Apollo people match run today showing the same current employer and title. Two sources that agree is best.
2. **These are NOT proof of current employment:** Apollo `email_status: verified` (only means the mailbox exists, and many companies accept all addresses), a ✅ in ROSTER/batch docs, an earlier session's check, a search-result snippet or summary, a company page or press release that mentions them.
3. **Re-check at every hand-off:** when drafting, when recording/building a sample for them, and whenever Spencer asks what to send or schedule. A check from a week ago doesn't count.
4. **Unresolved = NOT READY, said out loud.** That covers no profile found, several same-name profiles, LinkedIn blocked, or Apollo down. Put a yellow line at the very top of the draft body: `<span style="background-color:#ffff00">[VERIFY EMPLOYMENT: couldn't confirm <Name> is still at <Company>. Check before sending]</span>`. Lead your answer to Spencer with it, before anything else. Never list an unresolved contact as a send candidate. A flag that only lives in a repo doc doesn't count.
5. **FINAL CHECK = LINKEDIN (Spencer, 2026-10-04; widened 2026-10-05).** Two ways count: (a) the cloud LinkedIn API check, where the CURRENT company on the public profile (Bright Data / ZenRows via `cloud_check.py`) matches AND Apollo confirmed the title the same day (Spencer, 2026-10-05: "it can clear a draft"); or (b) the live profile page in the desktop browser. HIDDEN or MISMATCH from the API = not cleared, the desktop check decides. Original rule, still the standard for (b): Apollo, company pages and search results only find and shortlist people. Nobody is send-ready until someone has opened their live `linkedin.com/in/...` profile page and seen <Company> as the CURRENT position, with the right title. Log it in the contacts doc as `LinkedIn final check: <date>, <URL>, "<headline/current role as shown>"`.
   - **Who does it:** Bingo, never Spencer (Spencer, 2026-10-05: "this is your job"). It runs as the `linkedin-final-check` skill in the Claude Desktop app's built-in browser: a daily desktop scheduled task, or on demand ("LinkedIn-check the drafts"). Results are logged in `reference/client-acquisition/LINKEDIN-CHECKS.md`. Cloud sessions and routines can't load LinkedIn: WebFetch/curl get HTTP 999, and the sandbox blocks scripted LinkedIn browsing. So every cloud-built draft starts with the NOT READY line below, and it stays until the browser check is done.
   - **The line, first in the body:** `<span style="background-color:#ffff00">[NOT READY: final LinkedIn check pending for <Name>, <Title>, <Company>. Delete this line once done]</span>`. Spencer schedules nothing that still carries it. Any answer about what to send or schedule lists every NOT READY draft first.
   - **Check fails** (left, different title, no matching profile): handle it per item 6 the same turn.
6. **Contact left → enact it in Gmail the same turn.** Clear the To field so the draft can't go to them, then update ROSTER.md and FUNNEL-COHORTS.md. Swap in the backup only after the backup passes check 1 (same lesson as Kyle Osher, 09-23).

## Step 0c — HOUSE TEMPLATE + FULL CHECK ON EVERY EDIT (Spencer, 2026-10-05)

**The template is Spencer's own Hitachi Rail email** (sent 10-05, "copy across all other drafts now and moving forward"). The full text is in `reference/client-acquisition/PITCH-TEMPLATE.md`. Read it before writing or touching any pitch draft. Fill only the slots (greeting name, optional hook paragraph, company, credits, video title, link) and leave the wording alone. It replaces the old "Let me introduce myself" / "Would love to be a voice you can call on regularly" format.

Every edit to a pitch draft, even a recipient swap or a one-word fix, means rebuilding it to the template, then reading it back. Spencer's own hook text and takes are kept word for word. `.claude/hooks/pitch_draft_qc.py` blocks any FGAC draft write that doesn't match. If it blocks you, rebuild the draft; never route around the hook.
**If Spencer has the draft open in Gmail** (the message id changes between your GET and PUT), stop PUTting. His compose window overwrites yours.

## Step 0 — Never guess a fact about Spencer

Accent, location, studio gear, availability, credits, rates — if it's not in the
files, it's a `[bracket]` in the draft, not a plausible fill-in. His voice is
**native American English, neutral** and a **warm bass/baritone** (identity block
in Step 4). Do NOT infer "British" or any other accent from the market, the
currency, or anything else. Guessing his accent nearly ended the engagement
(2026-09-02). See AGENTS.md RULE 0.

## Step 1 — Pull what's already known

Before asking Spencer anything, read:
- `MEMORY.md` and `reference/vo-client-directory.md` — his positioning, credits,
  the end client behind a past job, prior rates, relationship history.
- `reference/outreach-pipeline.md` and `memory/outreach-log.md` — has this person
  been contacted before? When? What was pitched? Any reply or bounce? (Create the
  log from the template at the bottom if it doesn't exist.)

## Step 2 — Gather the gaps

Ask Spencer only for what's missing:
- Who: company/person, the specific contact, their role, email, and — because it
  changes the opener — a rough read on gender and age.
- Why now: the hook. **For warm:** the exact past project and roughly when.
- What Spencer wants: a call, a custom audition, roster addition, representation.
- Which reel/sample fits their work best.
- Whether this goes as a **brand-new email or a reply in an existing thread** —
  and tell Spencer which in the handoff (a "Re:" subject with no real prior
  thread is a stylistic convention here, not a literal reply; flag that).

**HOOK = EVENT REFERENCE ONLY. SPENCER WRITES THE TAKE (Spencer, 2026-10-03, HARD RULE; supersedes the "write 3 options" rule below).** Bingo's reactions kept reading as nerdy or generic ("Hablo español, so that was a fun surprise" was the last straw). So the hook paragraph is now: one plain, factual sentence naming the event (e.g. "Saw HOOD Summit '26 just wrapped in Houston.", "Saw the Toast Fuel launch."), followed by a yellow-highlighted `[YOUR TAKE]` placeholder **that carries a clickable link to the hook's source**, so Spencer can watch/read it before writing his take (Spencer, 2026-10-03: "I have no way of knowing what the piece of news is"): `<span style="background-color:#ffff00">[YOUR TAKE] Source: <a href="URL">Publication, Mon D, YYYY</a></span>`. The link is the page the event line is based on and that Bingo opened this session: the video itself when the hook says watched/spot/film (YouTube/Vimeo/iSpot), otherwise the press release or article. Two links max (article + video, separated by " · "). No URL = no hook: if you can't link the source, use the `[HOOK: nothing current found…]` line instead. The event line must say only what the linked source shows (ABB 10-03: "Just watched the Ferrari Hypersail film" was backed by a press release with no film; corrected to the partnership). Spencer deletes the whole placeholder, link included, when he writes his take. No jokes, no opinion, no tie-in to Spencer. Spencer researches the event and writes the reaction himself. Then "Let me introduce myself, my name is Spencer Pearman…". If nothing current turns up, the paragraph is `[HOOK: nothing current found. Add one or delete this line]`, highlighted the same way. Log the event, its date and the source in the contacts doc so he has the research trail. Every take Spencer writes goes into `voice.md` as a gold example. Once there are about 10, Bingo may offer ONE suggested take in brackets for him to keep or cut, but only if he asks.

**HOOK TOPIC = VO-RELATED OR PLAIN BUSINESS NEWS. NEVER OBSCURE (Spencer, 2026-10-05, HARD RULE).** The event has to be something it's natural for a voiceover artist to bring up, in one of two lanes:
1. **VO / video / creative:** a new campaign, spot, film, series, brand video, launch video, rebrand, podcast or show, or anything with a voice in it (e.g. Nat Geo premiering a narrated series, the Smithsonian launching a video series).
2. **General business milestone, in plain words:** an award, a "named a leader / best place to work / top 10" recognition, an anniversary, a big launch, a new HQ or expansion, a funding round or acquisition (e.g. "Saw F5 was named a Leader in the 2026 IDC MarketScape").

**Never** technical, regulatory, engineering or industry-insider news that needs a glossary. Rejected examples: TVA "received the NRC construction permit for the first BWRX-300 small modular reactor" ("What? What are we talking about?"), and anything like a permit, a filing, a spec, a protocol, a factory process, or a supply deal between two companies. The test: would a friend outside the industry understand the sentence and see why a VO artist noticed it? If not, pick another event, or use the `[HOOK: nothing current found…]` line. No hook beats an obscure one.

**HOOK STYLE (for Spencer's takes, and for reading his examples) = playful, down to earth, grounded (Spencer, 2026-10-03).** Gold example and the rejected styles are in `voice.md`.

**WATCH EVERY VIDEO A HOOK REFERENCES (Spencer, 2026-10-03, HARD RULE).** If a hook mentions a video, spot or campaign film, watch it first: download it (yt-dlp), pull a timestamped transcript (captions or Whisper) and a frame sheet (`ffmpeg -vf "fps=20/<dur>,scale=320:-2,tile=5x4"`), then Read the sheet. The hook must react to something actually in the video (a scene, a line, the premise) and match its tone. DraftKings "Take Your Game Anywhere" went out with "had me cracking up" on a spot that isn't comedic (it's a coast-to-coast road trip). A press article about a video is not watching it. If you can't watch it, don't react to its content: use a different hook or none. Log what you saw (scenes + key lines) next to the hook in the contacts doc.

**Hook quality bar (Spencer, 2026-09-29: he deleted most Funnel C2/E/F hooks).** A bare "Saw your post / saw the new X video go up." followed straight by "My name is Spencer" is dead weight, so don't write it. The hook has to *go somewhere*. Name something specific in the post or video (a line they said, a choice they made, what stood out and why), react to it like a human would, and let it lead naturally into who Spencer is. If you can't say anything real about the content, drop the hook instead of padding it.

**Timing check — every cold pitch (Spencer, 2026-10-05).** Look up the company's row in `reference/client-acquisition/BUDGET-CALENDAR.md` (add one if missing) and say in the hand-over whether today falls in its best pitch window. Outside the window = still draft it, but name the better send window. Never let it block a draft.

**Current-event hook — REQUIRED step for every cold email (Spencer, 2026-09-24).**
Before drafting, find one genuine, *current* hook, ideally from the last ~30 days.
Run it in this order and stop at the first real hit:
1. **The contact's own LinkedIn activity.** In Spencer's logged-in Chrome (Claude in
   Chrome, not the in-app browser), open `linkedin.com/in/<slug>/recent-activity/all/`,
   scroll once, and read the top ~6 posts *with their age* ("17h", "3w"). Best hits:
   something they're presenting or attending, a launch they posted, a festival or
   award, a new role, a press feature they shared.
2. **The company's LinkedIn posts** (`linkedin.com/company/<slug>/posts/?feedView=all`):
   a new series or campaign, a line from a brand post worth quoting (keep the quote
   under 15 words), an event.
3. **The contact's recent-post pattern ties to Spencer.** If a hook links to a
   verified credit, use it: e.g. The Rest Is Football ↔ the FIFA World Cup 2026
   preview series.

Rules:
- **The post itself is the source.** Cite it in the verification footer as
  "<person/company> LinkedIn post, <age>, read <date>". A search snippet is not a
  source (AGENTS.md).
- **Say only what the post shows.** If they *shared* an article, the hook is "saw
  your Campaign UK feature", not "I read…", unless the article was opened. Don't
  credit them with producing something the post doesn't say they made.
- **One or two plain, fan-note sentences**, placed right after the greeting and
  before the "I put together a re-voice of…" line. No analysis of their business
  (Step 4 voice rule).
- **Stale hooks:** reposts older than ~3 months, or a 1-year-old job post, don't
  count. Event-dated hooks ("this week", "this Thursday") go stale fast: write them
  so they still read right a week or two later ("Saw your post about presenting…"),
  and flag those drafts in the handoff as send-soon.
- **If nothing current turns up, do NOT invent one.** Skip the hook line and let
  the re-voice sample be the opener, then say so in the handoff ("no current hook:
  latest activity 8mo"). (Spencer nearly sent a fabricated Cisco connection once
  because of a name collision, so verify every credit/connection claim.)
- Re-check the hook when a draft has sat unsent for more than 2 weeks, since it
  may have gone stale.

## Step 3 — Rate guardrail

If Spencer's framing implies underselling — leading with price, a discount,
"whatever works for your budget," or a rate below his target — **say so before
drafting.** That's the pattern he asked Bingo to break. For any actual numbers,
use the `vo-pricing` skill.

## Step 4 — Draft (Spencer's rules, verbatim)

**Whose voice this is (Spencer, 2026-08-30 — he flagged this TWICE, do not drift):**
a 36-year-old artist building his VO business — produces great work, wants to get
better, *not corporate*. 

THE RULE: **write only what any ordinary viewer could genuinely notice. No insider
analysis, no industry-authority framing, no posturing.** Killed phrases, learn the
pattern: "you're publishing at a pace most in-house teams…", "does quiet work for
the brand", "a real editorial quality — written and paced by someone who cares about
story", "rare in this space", "lives or dies on how clear the narration is". All of
these = pretending to survey/diagnose their operation. He doesn't do that.

The opener is a plain fan note, his own words: *"I went through your video catalog
recently and really liked it — the style, the current/edgy vibe, the design — and I
wanted to reach out."* That's the whole move. Then who he is, the samples, the
credits, the close. Allowed observations are concrete and surface-level ("some of
the VO sounds in-house, some more polished", "a lot of the product videos have no
voice at all"). Sell what's true — he can do the work — without dressing him up as
something he isn't. Plain words, contractions, short paragraphs.

**From Spencer's own edits to the first sent batch (2026-08-31) — match this:**
- Name where he watched: "…going through your videos on LinkedIn and YouTube and really enjoyed them."
- Let genuine enthusiasm show: "really enjoyed them", "attractive to my eye", "(that I truly liked)", "I even like [specific other video]". Warmer than a neutral draft.
- "Hey [First]" is fine even for senior people — don't over-formalise.
- Use specifics and timeframes: "back in July", "went out a week ago", exact product names ("AWS Sagemaker", "Artlist.io").
- Showing he did his homework beats caution — if a spot was made with an outside studio, name it as shared credit ("the spot you all made with [studio]"), don't tiptoe.
- Be honest about where he's not established yet ("wanting to expand more into animation", not "I do character voices").
- Credit line ends "…among others."

- **Opener by recipient:** women and older men get a formal opener —
  "Hello [Name], I hope this message finds you well." Younger men get casual —
  "Hey [Name], hope you're doing well."
- **Never** open with "Firstly," or any formal pivot opener. Flow straight from
  the greeting into the content. Lead with a friendly check-in / warmth before
  any business.
- **Full-name intro (required, for cold or anyone who won't remember him):**
  "My name is Spencer Pearman and I'm a professional Voiceover Artist and audio
  engineer based in Lisbon, Portugal." ("Voiceover Artist" capitalized, Spencer 10-05.)
- **Voice descriptor: NONE in cold pitches (Spencer, 2026-10-05 night).** "I have a warm bass/baritone
  voice, and I record and produce everything myself" is cut: the attached samples show the voice and
  self-producing is irrelevant. Never "American voice" or "low-register" anywhere.
- **Reference a specific, verified piece of their work** by name and say what
  stood out — only if confirmed. Never assume or fabricate a credit.
- **Cold email order = `reference/client-acquisition/PITCH-TEMPLATE.md`, word for word (Spencer, 2026-10-05; replaces the 09-24 order/close).** Greeting → optional hook → "My name is..." intro → "I'm reaching out because I'd love to be your go-to Voiceover Artist..." → "My recent work includes..." → "Also, I put together a re-voice of your ..." → "Feel free to reach out or schedule a call if this is something you need. Hope to hear from you soon!" → sign-off. `pitch_draft_qc.py` blocks anything else.

  Never lead with the sample. Introduce first, then show the work.
- **The re-voice line is NEVER omitted from a cold pitch (Spencer, 2026-10-02 — all 19 Funnel G drafts went out of the batch without it).** If the video isn't picked yet, write the line with the literal marker: `Also, I put together a re-voice of your <a href="https://drive.google.com/REPLACE-WITH-SAMPLE-LINK">"VIDEO TITLE PENDING"</a> spot so you can hear how my voice meshes well with your content. I'd appreciate it if you gave it a listen!` — never a "custom read" offer or any other substitute. The **Video Title Sync** routine (`trig_01MEKNw1RisQBJax4WELao1z`, 06:50 UTC weekdays) swaps the marker for the winner title from the funnel's `_candidates` doc and flags anything still pending.
- **Sample link = the video's title, hyperlinked (Spencer, 2026-09-24).** Never write "your video", "[LINK]" or a bare URL. Write e.g. `I put together a re-voice of your <a href="DRIVE_URL">"Better your score. Better your story."</a> spot. Give it a listen!` — the recipient recognises their own title, which reads as real work, not spam. Until the take exists, href = `https://drive.google.com/REPLACE-WITH-SAMPLE-LINK` (two videos: `...-2` for the second) and the plain-text part says `(LINK)`; swap in the Drive link when the take lands.
- **Website as a full sentence:** "You can hear my work at spencerzvoice.com." —
  never a bare URL fragment.
- **Close** warm and low-pressure: "please keep me in mind" or "Hope to hear from
  you soon!" — not "I'd love to be considered."
- **Sign-off, exactly:**
  ```
  Best,
  Spencer
  spencerzvoice.com
  ```
- Keep it to something readable on a phone in one screen. Proofread this specific
  draft — never batch-reuse a skeleton across emails.
- Draft it via the **Gmail compose module** so a "Send with Gmail" button renders
  — not plain text for manual copy-paste, unless Spencer says otherwise.

**Warm re-engagement adds:**
- Name the exact past project and roughly when; one specific warm memory of it.
- For 6+ months of silence: acknowledge the gap directly — a soft, slightly more
  explanatory reconnect, not a breezy "hey, checking in."
- On rates: the mission is to move them up — usually "my rates have shifted a
  little since then; happy to send a current quote for anything you have coming,"
  not "same as last time."

**Follow-up adds:**
- Short. Bring a new angle or new proof, not "just bumping this."

## Step 5 — Follow-up cadence (for scheduling the nudge)

- **Cold agency contacts:** 7–10 days. 0–6 days is too soon; 10+ with no reply =
  overdue, send the follow-up. Touch 3 = final in the sequence, then a **quarterly
  long-tail touch** every ~90 days (new email, must bring something new): full
  rules in the `followup-drafts` skill (Spencer, 2026-10-05).
- **Warm / recurring clients:** slower — fast follow-up reads as needy.
  2–3 weeks if mid-conversation on a live project or recent quote; 4–8 weeks for
  a pure check-in with no open thread; 6+ months = treat as a soft reconnect.

### Send-date check (do this before handing over OR scheduling — [[outreach-send-timing]])

Never send to US agencies/brands on a **US federal holiday**, the business day
**before or after** one, or **Friday afternoon ET**. Best window: Tue–Thu
mid-morning recipient-local. Non-US recipients (e.g. Untold Studios = London)
follow their own calendar. If the natural send date is bad, say so and give the
next good date. US holidays: New Year's · MLK (3rd Mon Jan) · Presidents' (3rd Mon
Feb) · Memorial (last Mon May) · Juneteenth · July 4 · Labor Day (1st Mon Sep) ·
Columbus/Indigenous Peoples' (2nd Mon Oct) · Veterans (Nov 11) · Thanksgiving
(4th Thu Nov) + Fri after · Christmas. Slow zone: last 2 weeks of December.
(Missed Labor Day 2026-09-07 — a 12-email batch went out into holiday inboxes.)

## Step 6 — Hand it over

0. **Verification footer (RULE 0 — required).** Before the draft, list every factual
   claim in it and where each came from:
   ```
   — Verified: <fact — source file/page> · …
   — Bracketed (you fill): <item> · …
   — Unknown: <item> · …
   ```
   Write "none" for an empty section. Any claim about the client's work, a credit,
   or a connection that isn't from a primary source I opened this session → bracket
   it or cut it, never assert it.
1. Subject-line options (2–3). Specific, a reason to open — never "Voiceover
   artist available."
2. The draft, ready to paste / the compose link.
3. One line: why this angle, whether it's a new email or a thread reply, and what
   a good reply looks like.
4. The reminder: **Spencer reviews and sends it himself.**
5. Offer to draft the follow-up now and note the cadence date — run the Step 5
   send-date check on that date before naming it.
6. **Send-date sanity line:** state whether *today* (or the intended send day) is a
   clean day to send per the Step 5 check. If it isn't, say so plainly before
   Spencer sends.

## Step 7 — Log it

Append to `memory/outreach-log.md`, drop `🧠 remembered: drafted <mode> outreach
to <client>`, and update `reference/outreach-pipeline.md` / `MEMORY.md` if it's a
new tracked relationship.

---

## Template: `memory/outreach-log.md`

```markdown
# Outreach Log — Bingo

One entry per email. Update "Result" when a reply lands.

## <YYYY-MM-DD> — <Client / Company> — <cold | warm | follow-up N>
- Contact: <name, role, email>
- Hook / angle: <one line>
- Ask: <the CTA>
- Reel linked: <which one>
- New email or thread reply: <which>
- Status: draft in Bingo / Spencer sent <date>
- Follow up on: <date> if no reply
- Result: <blank until known>
```
