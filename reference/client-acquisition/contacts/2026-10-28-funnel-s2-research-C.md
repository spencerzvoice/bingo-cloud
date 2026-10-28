# Funnel S2 research, Group C (re-approach of 2024 channels)

Research date: 2026-10-28. Read-only: nothing sent, no Gmail/Drive touched.

**Sources and method (all this session):**
- Channel lists, subscriber counts, upload dates, durations and descriptions: yt-dlp 2026.08.19 (`/videos` tab + `--print upload_date|channel_follower_count|duration` per video + channel `/about` description). Upload dates are the per-video `upload_date` field (✅).
- **Captions were blocked.** Every `--write-auto-subs` call returned HTTP 429 (timedtext), including the one retry after a 60 s wait. vidIQ transcripts weren't an option (2 credits left). **Excerpt timings come from a local Whisper transcript instead** (faster-whisper small.en on the first 180 s of each pick's audio, downloaded with `--download-sections *0-180`). Timestamps are Whisper segment times. They're good to about ±1 s, but a few segments that absorbed music beds are wider (flagged where it matters). Transcripts: `scratchpad/s2_research/C/audio/<id>.txt`.
- I did not listen by ear, so "human vs AI voice" is ❓ throughout. The tool can't judge it.
- ACTIVE = at least one long-form upload (over 4 min) on or after 2026-07-30.

Tags: ✅ = seen this session (source named). 🟡 = unverified or inferred. ❓ = unknown.

---

## Summary table

| # | Channel | URL / handle | Subs ✅ | Last 5 long-form (upload_date ✅) / cadence | Narrator verdict | Email printed today vs 2024 address | Re-voice pick | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | TLDR News Global | youtube.com/@TLDRnewsGLOBAL | 1,180,000 | 10-28, 10-27, 10-26, 10-23, 10-22 · **daily** | ❓ Unnamed staff presenter. Descriptions say the channel "is run by a small group of young people". On-camera ❓ | **None found** (About description empty in yt-dlp; not in 2 descriptions). 2024 tldr@standard.tv not seen | Rousymf8Iqo, newest | **NO EMAIL** |
| 2 | Odd Compass | youtube.com/@OddCompass | 412,000 | 2026-10-23, 2026-03-15, 2025-07-26, 2025-02-18, 2024-11-30 · **slower (every 4-7 months)** | ❓ Not credited. Description: "Everything here was human-made: the voiceover..." | ✅ oddcompasshistory@gmail.com (About), **same** | b4Ig1a4cjOY, newest | **READY** |
| 3 | Isaac Arthur (SFIA) | youtube.com/@isaacarthurSFIA | 1,170,000 | 10-25, 10-22, 10-17, 10-15, 10-11 · **2+/week** | **FOUNDER** ✅ "Written, Produced & Narrated by: Isaac Arthur" (descriptions) | ✅ isaacarthur@standard.tv (About), **same** | bI9ac94cWDc, newest | **FOUNDER-VOICED** |
| 4 | TechAltar | youtube.com/@TechAltar | 805,000 | 09-16, 08-25, 08-18, 07-28, 06-30 · **every 1-4 weeks (about monthly)** | **FOUNDER/host** ✅ About: "Host: Marton Barcza". First-person transcript ("I definitely thought so"). On-camera ❓ | **None found** (About names Tarsier Media GmbH, no email). 2024 techaltar@standard.tv not seen | GyxYEYsNUn4, newest | **FOUNDER-VOICED** |
| 5 | Ridddle | youtube.com/channel/UC9Ep0Y4T5rvUuIfjKN1wqTw (@ridddlen, which 404'd on the /videos path) | 5,740,000 | 10-27, 10-20, 10-12, 10-02, 09-25 · **weekly** | ❓ Not credited. Narrated VO doc | **None printed.** The About text says "we had some email issues. Everything's working now, so feel free to message us again." 2024 ad@eldddir.com not seen | hqx_7RvHnOY, newest | **NO EMAIL** (printed). Strong fit otherwise |
| 6 | The Intel Report | youtube.com/@TheIntelReport | 280,000 | 07-24, 06-14, 05-28, 05-02, 02-28 · monthly, **last one 96 days ago** | ❓ Narrator reads the sponsor in first person ("I've been playing...") | None printed (Patreon only). 2024 theoperationsroom@gmail.com not seen | vw63IoVD9mk, newest | **INACTIVE** (just past 90 days) |
| 6b | ↳ The Operations Room (same team ✅: both link patreon.com/TheOperationsRoom) | youtube.com/@TheOperationsRoom | 1,450,000 | 10-03, 09-13, 08-22, 08-20, 08-15 · **every 1-3 weeks** | ❓ Not credited. Narrated (transcript), with veteran archive audio cut in | None printed | EU-nV5FxKf0, newest | **NO EMAIL** (printed); 2024 gmail likely the route 🟡 |
| 7 | Mafia Side | youtube.com/@mafiaside | 177,000 | 2026-03-07, 01-08, 2025-12-25, 12-03, 11-24 · monthly until March | ❓ Not credited | None printed. 2024 mafiasideoffice@gmail.com not seen | zfWijjSudjQ, newest | **INACTIVE** |
| 8 | Vox | youtube.com/@Vox | 12,700,000 | 10-28, 10-27, 10-27, 10-26, 10-24 · **daily** | **ON-CAMERA / staff hosts** ✅. Newest: "Hosted by Kahlil Greene" (description, first-person transcript). Others are podcast-style shows (America, Actually; The Gray Area; Vox Conversations transcript) | ✅ voxvideo@vox.com (About), **same** | none (no narrated explainer among the newest) | **ON-CAMERA** |
| 9 | What's the Dirt? | youtube.com/@whatsthedirt | 396,000 | 08-08, 06-16, 04-16, 04-03, 02-25 · **every 2-8 weeks**; last one 81 days ago | **FOUNDER** ✅ transcript opens "repeated copyright claims on my content, I've started a Patreon"; description "my sponsor" | ✅ matt@whatsthedirt.org (About "Personal Email" + description "General Inquiries"), **same**. Brand deals: whatsthedirt@rightclick.gg | Wkj8AGe3-mo, newest | **FOUNDER-VOICED** |
| 10 | CaspianReport | youtube.com/@CaspianReport | 1,850,000 | 10-28, 10-18, 10-13, 10-05, 09-21 · **weekly** | 🟡 Probably the founder: the narrator reads the BetterHelp ad in first person ("For me, the hardest part is disconnecting from work"), and the description says "My bookshelf". No credit line | None printed. 2024 caspianreport@lighthouseagents.com not seen | cNzEpeYlYeo, newest | **NO EMAIL** (printed); the agency thread exists |
| 11 | The Present Past | youtube.com/@ThePresentPast_ | 466,000 | 10-09, 08-31, 07-23, 07-07, 06-30 · **every 1-6 weeks** | 🟡 FOUNDER. ✅ About: "My name is Jochem. I make the show". Description: "Video by: Jochem Boodt". That the voice is his is 🟡 | None printed (only a Dropbox file-request link). 2024 ThePresentPast@lighthouseagents.com not seen | kV42lYbOjbo, newest | **FOUNDER-VOICED** 🟡 |
| 12 | Economics Explained | youtube.com/@EconomicsExplained | 2,890,000 | 10-28, 10-21, 10-18, 10-14, 10-05 · **1-2/week** | ❓ Not credited | ✅ hello@economicsexplained.com ("Business Enquiries", descriptions). **Different** from the warm contact clara@lunar-x.com | vQodCxq7b9g, newest | **READY** (warm, via Clara) |
| 12b | ↳ Context Matters | youtube.com/@context.matters | 114,000 | 2025-12-30, 2025-09-14, 08-04, 07-20, 07-02 | ❓ Not credited. ✅ "Context Matters is produced by @EconomicsExplained" (descriptions); "Writer credits: Hugh O'Reilly" | None printed | 8IZuOb2R0Tw, newest | **INACTIVE** (10 months) |
| 13 | Academy of Ideas | youtube.com/@academyofideas | 2,030,000 | 10-24, 10-04, 09-13, 08-14, 07-19 · **every ~3 weeks** | 🟡 FOUNDER (per the brief/FUNNEL-COHORTS: Michael narrates himself; no credit line seen this session) | None printed (About links membership only). 2024 academyofideas@gmail.com not seen | L2PHH59F_1g, newest | **FOUNDER-VOICED** 🟡 |
| 14 | Volksgeist | youtube.com/@Volksgeist | 922,000 | 10-19, 09-27, 09-19, 08-31, 08-19 · **every 1-3 weeks** | **FOUNDER** ✅ About: "created, hosted and written by Philip D'Amico". First-person transcript ("I'm going to tell you a story", "that was just me riffing") | ✅ philip@volksgeist.org (descriptions), **same** | _ptPuYVfNUM, newest | **FOUNDER-VOICED** |
| 15 | The Tesla Space (Creator Mill) | youtube.com/@TheTeslaSpace | 539,000 | 10-21, 10-14, 10-07, 09-30, 09-23 · **weekly** | ❓ Not credited. First-person narration ("the most insane vehicle demo I have ever seen") | ✅ sean@creatormill.com ("Business Email", descriptions), **same** | IiWPDRNm_Vs, newest | **READY** (past client) |
| 15b | ↳ The Space Race (Creator Mill ✅: Tesla Space descriptions say "our other channel, The Space Race") | youtube.com/channel/UCeMcDx6-rOq_RlKSPehk2tQ | 909,000 | 10-24, 10-17, 10-10, 09-29, 09-26 · **weekly** | **FOUNDER** ✅ "Narration: Sean Callaghan" (descriptions) | ✅ sean@creatormill.com, same | _I3KAaI__-M, newest | **FOUNDER-VOICED** |
| 16 | MagnatesMedia | youtube.com/@MagnatesMedia | 1,860,000 | 2025-09-12, 08-22, 08-08, 07-13, 06-25 | 🟡 FOUNDER. ✅ About: "My name is John". Transcript: "trust me, this story gets crazy" | ✅ support@magnatesmedia.com ("Paid sponsorship enquiries", descriptions), **different** from john@magnatesmedia.com | Qbe0I3X6R-o, newest | **INACTIVE** (still dark, 13+ months) |

---

## Per-channel notes and excerpts

Excerpt times are seconds from the video start (Whisper, first 180 s).

### 1. TLDR News Global
- Pick ✅: **Rousymf8Iqo**, https://www.youtube.com/watch?v=Rousymf8Iqo, "Israel's Election Results Explained", 2026-10-28, 9:37. The newest upload.
- Excerpt **70.2 → 129.1 s (59 s)**, after the cold open (0-52 s) and the subscribe plug (59.7-63.9 s).
  - First: "First off, Israel's elections are parliamentary."
  - Last: "...and national security minister Itamar Ben-Gvir's far-right Jewish power."
  - Alternative: the cold open alone, 0.0-52.2 s (52 s): "On Tuesday, Israel went to the polls..." to "...why Israel might be going back to the polls in short order."
- Notes: part of the Standard network (2024 address was @standard.tv). It's a staff-presenter news outfit with a daily cadence, and the narration is the house presenter's identity. 🟡 a low-odds buyer of outside VO.

### 2. Odd Compass
- Pick ✅: **b4Ig1a4cjOY**, https://www.youtube.com/watch?v=b4Ig1a4cjOY, "INDIA & CHINA: 2000 years of connected history", 2026-10-23, 36:13. The newest upload.
- Excerpt **73.9 → 130.9 s (57 s)**:
  - First: "And so our story begins."
  - Last: "In truth, a caravan could only carry a small amount of precious cargo."
  - (The cold open runs 0.3-31.3 s, "India and China. What if their history..." to "Thousands of years of untold history." It's followed by a music bed that Whisper merged into one 37.8-67.9 s segment, so the start of "Historically, it was trade..." isn't timed precisely. The pick above avoids that segment.)
- Notes: the narration addresses viewers as "adventurer". Uploads are rare (one every few months), so this is a big-production, low-volume channel. No sponsor read in the first 3 min.

### 3. Isaac Arthur (SFIA)
- Pick ✅: **bI9ac94cWDc**, https://www.youtube.com/watch?v=bI9ac94cWDc, "The Fermi Paradox: Civilization Extinction Cycles", 2026-10-25, 36:19. The newest upload.
- Excerpt **0.9 → 59.0 s (58 s)**:
  - First: "Maybe the galaxy isn't empty, it's just caught in a loop of rise, ruin, and rebirth..."
  - Last: "And maybe, just maybe, that silence is the answer."
- Notes: Isaac narrates his own videos (✅ credit line), and the voice is his brand. On the Nebula/Standard network. Not a buyer.

### 4. TechAltar
- Pick ✅: **GyxYEYsNUn4**, https://www.youtube.com/watch?v=GyxYEYsNUn4, "Apple "Audio Intelligence" is real bad", 2026-09-16, 17:32. The newest long-form.
- Excerpt **54.3 → 115.1 s (61 s)**, after the cold open and the "sponsored by Obscura VPN" line at ~43-53.6 s:
  - First: "Okay let's first recap what Apple has actually launched."
  - Last: "...but this is where things get more delicate."
- Notes: hosted by Marton Barcza (About). Operated by Tarsier Media GmbH. Nebula creator. Host-voiced. Not a buyer.

### 5. Ridddle
- Pick ✅: **hqx_7RvHnOY**, https://www.youtube.com/watch?v=hqx_7RvHnOY, "We Might Have a Black Hole in Our Solar System", 2026-10-27, 18:34. The newest upload.
- Excerpt **0.0 → 65.4 s (65 s)**:
  - First: "Right now, there might be a black hole orbiting our sun."
  - Last: "...yet we haven't been able to find an entire planet right under our noses for over a decade."
- Notes: the biggest channel in this group (5.74M), weekly, and a fully narrated space doc. No narrator credit and no sponsor read in the first 3 min. The About text says they had email problems and asks people to message again. No address is printed (YouTube's hidden business-email button may hold one; I can't read it with yt-dlp). The 2024 address ad@eldddir.com ("ridddle" reversed) is ❓ still valid. Run a deliverability check before using it.

### 6. The Intel Report (+ 6b The Operations Room)
- Intel Report pick ✅: **vw63IoVD9mk**, https://www.youtube.com/watch?v=vw63IoVD9mk, "How The US Navy Became The Best In The World At Damage Control In WW2 (No AI)", 2026-07-24, 19:48. The newest upload, 96 days old.
  - Excerpt **1.6 → 58.5 s (57 s)**, before the Freecash read (58.5-133.7 s). First: "In October of 1942, the navies of the United States and the Japanese Empire clashed in the battle of the Santa Cruz Islands." Last: "...some of the most intense battles of the Pacific War."
- Operations Room pick ✅: **EU-nV5FxKf0**, https://www.youtube.com/watch?v=EU-nV5FxKf0, "Pearl Harbor (3/3) - US Fighters Strike Back - Animated", 2026-10-03, 37:12. The newest upload.
  - Excerpt **9.5 → 65.7 s (56 s)**. First: "The second wave of 167 Japanese strike aircraft arrives to the east of Oahu's Kahuku Point at 8.40am." Last: "Like the earlier wave, Kaneohe Naval Air Station is one of the first locations to be attacked." (It's part 3 of a series, so a part-1 opening may read better.)
- Notes: same outfit ✅ (identical Patreon link, and both promote "The War Office" podcast). The 2024 address theoperationsroom@gmail.com belongs to them. The Intel Report has been tagging titles "(No AI)". The 1.45M Operations Room is the better target, since it's active and twice the size, but no email is printed on either channel. 🟡 the narrator could be the in-house team that hosts the podcast.

### 7. Mafia Side
- Pick ✅: **zfWijjSudjQ**, https://www.youtube.com/watch?v=zfWijjSudjQ, "10 CRAZY Mass Prison Escapes Caught on Camera", 2026-03-07, 7:02. The newest upload, 235 days old.
- Excerpt **2.0 → 63.0 s (61 s)**. First: "Often, we hear of prison escapes involving just one or a small number of inmates." Last: "...leaving behind a scene of confusion and chaos."
- Notes: INACTIVE since March. A top-10 list format. Low priority.

### 8. Vox
- Newest long-form ✅: KVYNwthBcgM, "The HBCU renaissance, explained", 2026-10-28, 8:38. It's hosted on camera by creator Kahlil Greene (description: "Hosted by Kahlil Greene"; transcript: "I'm Kahlil Greene"). The next long-form uploads are talk shows or podcasts (America, Actually; The Gray Area; Best of Luck), and NB93ARM7GVY is a two-person Vox Conversations interview (transcript).
- **No narrated pick.** None of the newest uploads is a voice-over explainer.
- Notes: a newsroom with staff and creator hosts. The pitch email is still voxvideo@vox.com (same). 🟡 a poor fit for a re-voice sample.

### 9. What's the Dirt?
- Pick ✅: **Wkj8AGe3-mo**, https://www.youtube.com/watch?v=Wkj8AGe3-mo, "Untangling Jay Z's Evil Plan To Destroy Drake", 2026-08-08, 40:43. The newest upload.
- Excerpt **19.5 → 80.0 s (60.5 s)**, after the Patreon intro (0-19.5 s). First: "Over the last 12 months something very strange has been happening in the music business." Last: "...Drake had realized his own power and was chasing something bigger with more control and leverage."
- Notes: Matt narrates his own channel, in first person, and reads the Zocdoc ad himself. Brand deals go through RightClick (whatsthedirt@rightclick.gg). Not a buyer.

### 10. CaspianReport
- Pick ✅: **cNzEpeYlYeo**, https://www.youtube.com/watch?v=cNzEpeYlYeo, "Something is rotten in Germany", 2026-10-28, 14:09. The newest upload.
- Excerpt **0.2 → 63.5 s (63 s)**, inside the cold open, which ends at 84 s; the BetterHelp read runs 87.7-179.7 s. First: "Germany had it all figured out." Last: "But Germany's problems run deeper."
- Notes: sponsor-heavy. BetterHelp, plus a paid stock promo on 10-18 whose disclosure says "compensated twelve thousand five hundred dollars". The narrator does the sponsor reads in first person. Lighthouse Agents (their agency, which replied "will be in touch" in 2024) is the route. No email is printed on the channel.

### 11. The Present Past
- Pick ✅: **kV42lYbOjbo**, https://www.youtube.com/watch?v=kV42lYbOjbo, "The Israeli Plane Crash Conspiracy", 2026-10-09, 38:38. The newest upload.
- Excerpt **36.2 → 98.3 s (62 s)**. First: "Officials said the plane was just carrying flowers and perfume, but after the crash mysterious men in white suits were seen scavenging through the debris." Last: "Boeing's 747 is a cargo plane with just 4 people on board." (Music beds sit inside 1.3-23.1 s and 51.2-69.8 s; Whisper merged them into the segments, so treat the internal timings as ±2 s.)
- Notes: Jochem Boodt's personal show ("I make the show"), with a hired edit/2D/3D team. Odoo sponsor. Same agency as Caspian (Lighthouse).

### 12. Economics Explained (+ 12b Context Matters)
- EE pick ✅: **vQodCxq7b9g**, https://www.youtube.com/watch?v=vQodCxq7b9g, "How China Is Restarting Its Economy", 2026-10-28, 13:50. The newest upload.
  - Excerpt **0.0 → 59.6 s (60 s)**. First: "It's fair to say that there has been something of a vibe shift in the perception of the Chinese economy over the last few years." Last: "...and yet people are talking about its economic miracle." (The Pasqal sponsor read starts at 112.6 s.)
- Context Matters pick ✅: **8IZuOb2R0Tw**, https://www.youtube.com/watch?v=8IZuOb2R0Tw, "The Invisible War for The Internet", 2025-12-30, 16:14. The newest upload, but the channel has been dark for 10 months.
  - Excerpt **0.0 → 61.0 s (61 s)**. First: "Over 99% of the world's internet traffic flows through about 600 fiber-optic cables just like this." Last: "But these incidents aren't limited to China and Taiwan." (The Incogni read starts at ~123.9 s, in first person.)
- Notes: the EE network also runs WirtschaftsWissen (German) and L'Économie Expliquée (French) ✅ (EE descriptions). The Context Matters About text also names a sister channel, "The Red Line" ✅; I didn't resolve its handle. A newer EE network channel may be where a "new voice" trial would happen 🟡. Warm route: Clara Salles Ackermann (clara@lunar-x.com, per the brief, not reopened).

### 13. Academy of Ideas
- Pick ✅: **L2PHH59F_1g**, https://www.youtube.com/watch?v=L2PHH59F_1g, "Kakistocracy - Are We Ruled By the Worst?", 2026-10-24, 11:51. The newest upload.
- Excerpt **0.0 → 56.9 s (57 s)**. First: "Is ours a government of the people, by the people, for the people, or a kakistocracy, rather, for the benefit of knaves at the cost of fools?" Last: "...and satisfy their desires for wealth, power, and control."
- Notes: no sponsor reads; it runs on memberships and Substack. The founder narrates (warm, but per the brief, not a buyer). No email printed today.

### 14. Volksgeist
- Pick ✅: **_ptPuYVfNUM**, https://www.youtube.com/watch?v=_ptPuYVfNUM, "The Israel Situation is Insane", 2026-10-19, 55:18. The newest upload.
- The narration is broken up by archival clips (22.0-26.5, 33.6-41.0 and 57.5-71.6 s). The longest clean stretch is **71.6 → 116.4 s (45 s)**: "Now AIPAC isn't the only lobbying organization in America that advocates for a foreign nation." to "It sounds like conspiracy slop." (Shorter than 55 s; the clips make a full minute of clean narration impossible in the first 3 min.)
- Notes: Philip hosts and writes it himself. It's on Nebula and Spotify, sponsored by Straight Arrow News and Trainwell. Not a buyer.

### 15. The Tesla Space / Creator Mill
- Tesla Space pick ✅: **IiWPDRNm_Vs**, https://www.youtube.com/watch?v=IiWPDRNm_Vs, "What Everyone Got Wrong About The New Tesla Roadster", 2026-10-21, 11:33. The newest upload.
  - Excerpt **0.0 → 57.7 s (58 s)**. First: "In this week's episode we find out what's really going on with Tesla's flying car..." Last: "...a limited edition race car that does it in under 0.9 seconds using four compressed air thrusters in the back."
- Space Race pick ✅: **_I3KAaI__-M**, https://www.youtube.com/watch?v=_I3KAaI__-M, "Jupiter isn't a planet", 2026-10-24, 16:19. The newest upload. Excerpt **2.5 → ~65.8 s (63 s)**. First: "What if Jupiter wasn't a planet?" Last: "...even less of us really know what's going on with the other 111 moons of Jupiter."
- **Creator Mill channels found:**
  - ✅ The Tesla Space: its own narrator is ❓ (first person, uncredited).
  - ✅ The Space Race: narrated by Sean Callaghan.
  - ✅ creatormill.com also features "What Life In Elon Musk's Mars Colony Will Be Like" (2021, a Tesla Space video) and an ItsYeBoi video (2.65M subs; 🟡 Sean's own on-camera channel; I didn't check its format).
  - ❓ **The Fallout channel Spencer narrated (Nov 2024-Apr 2025): name not found.** The site doesn't list it, and the Fallout channels I checked (Uranium Fever, Kateri Lore, The Vault Lore, Explainatron) show no Creator Mill email. Spencer knows the name.
- Notes: the creatormill.com contact address today is ✅ **creators@creatormill.com**. sean@creatormill.com is still printed on both channels. Spencer's past-client thread is the route. 🟡 Sean may narrate Tesla Space too (same production company), which would make it a founder-voiced channel. I couldn't confirm by ear.

### 16. MagnatesMedia
- Newest ✅: **Qbe0I3X6R-o**, https://www.youtube.com/watch?v=Qbe0I3X6R-o, "The INSANE Truth About YouTube", 2025-09-12, 39:34. Nothing has gone up since then.
- Excerpt (in case it wakes up) **51.7 → 114.7 s (63 s)**. First: "The story of YouTube begins in a surprising place, the headquarters of PayPal." Last: "...and Steve eventually left for Facebook."
- Notes: **still inactive** (13.5 months). John sells a "YouTube Millionaire System" course (magnatesmedia.com). The printed email today is support@magnatesmedia.com (sponsorship). Skip for S2.

---

— Verified (this session): subs, upload dates, durations and descriptions — yt-dlp 2026-10-28 · About texts — yt-dlp `/about` description · narrator credits: Isaac Arthur, Space Race (Sean Callaghan), Volksgeist About, TechAltar About (host), Vox (Kahlil Greene) — video descriptions / About · first-person narration (What's the Dirt, Volksgeist, TechAltar, Caspian sponsor read, Tesla Space) — Whisper transcripts of the first 180 s · creators@creatormill.com and the Tesla Space Mars video — creatormill.com page + yt-dlp · Intel Report = Operations Room — shared Patreon link in both channels' About/descriptions
— Bracketed (Spencer fills): name of the Creator Mill Fallout channel
— Unknown: human vs AI voice on every channel (not checked by ear) · narrator identity for TLDR, Odd Compass, Ridddle, Intel Report/Operations Room, Mafia Side, EE, Context Matters, Tesla Space · whether hidden YouTube business emails exist for TLDR, TechAltar, Ridddle, Caspian, Present Past, AoI, Operations Room · whether the 2024 addresses not printed today still deliver · Academy of Ideas founder-narration (inherited from the brief, not reverified)
