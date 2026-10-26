# Buyer-gate audit, 2026-10-26

Spencer asked for this after Maersk ("build the buyer gate into the pipeline and audit the current weak-fit contacts").
Gate: `scripts/buyer_gate.py` + `.claude/hooks/buyer_gate_guard.py`, rule in CLAUDE.md override 3b. Verdicts for all 85
live contacts are in `BUYER-GATE.json`. Titles for sent contacts come from the tracker/contacts docs (inherited, not
re-opened today) unless the row says otherwise.

Scope: 11 unsent pitch drafts + every pitch sent since 10-06 that is still in cold cadence (74).
Result: 43 PASS, 30 REVIEW, 10 FAIL (+2 new PASS replacements).

## Unsent drafts: fixed today
| Company | Was | Now | Evidence |
|---|---|---|---|
| Zscaler | Warren Yu, Senior Video Producer (REVIEW) | **LeighAnna Cina, Senior Head of Production / EP**, lcina@zscaler.com | ✅ live LinkedIn /details/experience (Sep 2026-Present, "vendor partnerships"); ZB valid |
| ServiceNow | Daniel Koga, Producer (REVIEW) | **Vince Genovese, Director Global Brand Video**, vince.genovese@servicenow.com | ✅ live LinkedIn /details/experience (Nov 2024-Present, ex EP Global Brand); ZB valid |
| Freshworks | Pete Anderson, "Global Video Lead" (REVIEW) | kept: Apollo match today = **Executive Producer** since 2022 | Apollo match 10-26 (LinkedIn not reopened) |
Drafts r3267529201144020045 (Zscaler, Label_12) and r-6820553657357055252 (ServiceNow, Label_11) re-addressed: To + greeting
only, body word for word, labels re-applied, format sweep all PASS. The other 8 drafts already PASS.
Backup at ServiceNow: Ron Fugelseth, CD Video & Storytelling (email ZB unknown, not usable yet).

## Sent pitches that FAIL (crew/adjacent, not the buyer)
Buyer candidates are from Apollo people search (title field only, 🟡 not verified on LinkedIn, no email pulled yet).
| Company | Pitched | Why it fails | Buyer candidate (🟡) |
|---|---|---|---|
| Maersk | Cameron Robertson, Sr Producer & Videographer | crew + in-house video uses interviewee voices | **done**: Sam Poulter emailed 10-26 (referral) |
| New Relic | Moe Hung, Lead Brand Designer (sent 10-26) | designer | Evan Ch***g, Senior Director, Brand Experience |
| JetBrains | Alex Gauermann, Broadcast Engineer / Video Producer (sent 10-26) | engineer | Nikolay Ko***v, Head of Content; Melanie Sh***w, Head of Marketing & Brand (AI & Cloud) |
| Docusign | Matthew Moresco, Video Producer/Editor (sent 10-23) | editor | Ryan Cl***k, Senior Creative Director, Digital Experience |
| Okta | Reed Jones, Keynote Producer (sent 10-23) | keynote/event | Devin Co***l, Creative Director (Devin Cornwall's email was ZB invalid 10-13); Katie Mitchell, Sr Creative Producer / EP (no email 10-13) |
| HashiCorp | Raven Kenemer, Sr PMM Content Strategy @ IBM (sent 10-23) | product marketing | none: HashiCorp has no one left in Apollo (absorbed into IBM). Recommend let the cadence finish, then drop |
| Justworks | Jonathan Lopez, Video Producer & Editor (sent 10-23) | editor (may be the only video person) | Alexander Ri***k, Creative Director; Kim Ry***a, Sr Director Brand Marketing |
| Schneider Electric | Deepika Upadhyay, Web Content Producer (touch 2 sent 10-26) | web content | Roxanne Hu***s, Head of Brand Storytelling; Ray Ch***n, Global Creative Director |
| Lonely Planet | Max Dickson, Video Producer & Editor (touch 2 10-20) | editor | Deepa La***n, Head of Social Media & Video; Annie Gr***g, VP Creative Brand Marketing / ECD (no email) |
| Smithsonian NASM | Jonathan Ray, Producer (Webcast) (touch 2 10-15) | webcast | none found in Apollo |

## Sent pitches at REVIEW (IC producers / marketing managers): no action now
Acceptable doors in many in-house teams, but not proven buyers. If any is silent after touch 3, the next move is the
buyer above them, not a new crew contact. LaunchDarkly (Jamal Farley), Twilio (Riley West), MongoDB (Pablo Zubieta),
Applied Intuition (Jorge Salgado), Amplitude (Helsi Robino), Autodesk (Jack Headley), Klaviyo (Karim El-Sayed), Personio
(Andrew Wilson), Celonis (Alice Monnet), Calm (Casey Daigle), Ørsted (Pelle Iversen), Cornerstone (Matthew Hyland), Go1
(Olivia Mitchell), Vyond (Kevin Kartono), Absorb (Sue Funke), Articulate (Sara Heegaard), Confluent (Caitlin Scholz),
Airbnb (Sarah Karlan), Brooks (Christina Harp), Patagonia (Tristan Ahern), Ramp (Karly Snajczuk), lululemon (Cameron
Aspinwall), YETI (Jesse Hill), UiPath (Carter Elkin-Paris), Robinhood (Jen Vladimirsky), Toast (Eleanor Scott), F5
(Roland Luitgaarden), TVA (Bleu Hayes).

## Follow-through, 2026-10-26 evening (Spencer: "Yes: verify the buyer at each of the 7 FAIL companies, get their emails, draft them with the same sample, and hold the crew contacts' remaining touches")
| Company | Buyer (✅ live LinkedIn /details/experience, 10-26) | Email | Draft |
|---|---|---|---|
| New Relic | Evan Chung, Sr Director Brand Experience (ran Zuora's brand video incl. vendor shoots) | echung@newrelic.com, ZB valid | r-8469365714694743265 |
| JetBrains | Melanie Shifferaw, Head of Marketing & Brand, JetBrains AI & Cloud (leads agencies; Air is an AI product) | melanie.shifferaw@jetbrains.com, ZB valid | r-3016872541390558783 |
| Docusign | Ryan Clark, Sr Creative Director, Digital Experience (🟡 weaker fit: web/product brand, not video) | ryan.clark@docusign.com, ZB valid | r-6665801472060130199 |
| Okta | Matt Maynard, VP Global Brand & Creative (Devin Cornwall's email ZB invalid again; Katie Mitchell freelance, no email) | matt.maynard@okta.com, ZB valid | r-5635825343847723744 |
| Justworks | Alexander Riezebeek, Creative Director, head of brand creative (team incl. filmmakers) | ariezebeek@justworks.com, ZB valid | r-5492047085600859125 |
| Schneider Electric | Roxanne Hughes, Head of Brand Storytelling (Sydney) | roxanne.hughes@schneider-electric.com, 🟡 ZB unknown (catch-all) + Prospeo VERIFIED | r-6550330145139093751 |
| Lonely Planet | Deepa Lakshmin, Head of Social Media & Video | deepa@lonelyplanet.com, ZB valid | r-1518952651825502691 |
Same hook and same re-voice link as the crew pitch; only To + greeting changed, except Schneider ("especially" -> "like") and Lonely Planet (rebuilt to v6 order) because those two went out in older formats. Read back from Gmail byte-for-byte, labels re-applied, draft_format_sweep all PASS (18 pitch drafts, cap 20). Crew contacts held: tracker Next Action "Hold", ledger HOLD block in memory/followups-queue.md; none had a Queue Sheet row. Apollo: 26 credits (2040 -> 2014). Not done: HashiCorp + Smithsonian NASM (no buyer found), cadence left to finish.
