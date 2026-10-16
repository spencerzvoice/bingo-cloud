# House cold-pitch template

## v6, CURRENT (Spencer, 2026-10-14 evening): his Cloudflare draft + "Audio Engineer"
Source: Spencer rewrote the Cloudflare (Jessica Liu) and 360Learning callbacks himself (Gmail draft `r-3222776882488975685`): "Instead of 'and any other content,' we're going to switch it to 'and any other news coming out of the company.'" Same evening: "capitalize 'Audio Engineer' in all first-touch drafts ... Not All Caps...Just Audio Engineer". All unsent pitch drafts rebuilt 2026-10-14. `.claude/hooks/pitch_draft_qc.py` enforces both.
**What changed vs v5:** Spencer's exact wording (2026-10-14): "My name is Spencer Pearman and I'm a professional Voiceover Artist and Audio Engineer based in Lisbon, Portugal. I'd love to voice the videos that come out of [Company], especially those spreading the word about [Event] and any other company news." So: "Audio Engineer" title case (never all caps); the intro splits into two sentences at "Portugal."; the callback is "especially those spreading the word about <event> and any other company news." (was "especially the ones that spread the word about <event> and other content."). Everything else is v5 word for word.

```
[cloud-built drafts only] <span style="background-color:#ffff00">[NOT READY: Bingo's LinkedIn check pending for <Name>, <Title>, <Company>. Bingo deletes this line once it passes]</span>

Hello <First>, hope you're doing well!

Saw <Company> just <event>. <reaction>. Congrats on the <launch>!! <span style="background-color:#ffff00">[Source: <a href="URL">Publication, Mon D, YYYY</a>. Delete this before sending]</span>     (v2 hook rules; leave out if no hook)

My name is Spencer Pearman and I'm a professional Voiceover Artist and Audio Engineer based in Lisbon, Portugal. I'd love to voice the videos that come out of <Company>, especially those spreading the word about <event, short plain words> and any other company news.
   (no hook: "...based in Lisbon, Portugal. I'd love to voice the videos that come out of <Company>.")

To give you an idea of my voice, I re-voiced your <a href="<Drive link or https://drive.google.com/REPLACE-WITH-SAMPLE-LINK>">"<exact video title>"</a> <video|spot>. I'd appreciate it if you gave it a listen!
   (no video picked yet: the title text is VIDEO TITLE PENDING)

My standard turnaround is within 24 hours and within 2-3 hours for rush projects. My recent work includes <3 credits, table below>, plus the 2026 FIFA World Cup Preview Series and the Preview of the Season for EuroLeague Basketball. You can see more of my work at spencerzvoice.com.

I'd love to get on a call and talk about working together, please don't hesitate to reach out. Hope to hear from you soon!

Best,<br>Spencer<br><a href="https://spencerzvoice.com">spencerzvoice.com</a>
```

---

### v6 NO-VIDEO variant (Spencer, 2026-10-16: "If there's not usable video for Hornet then we don't re-voice a video, we point them to my website and pass work and commercial reel"; then "Cut the repeat 'You can see more of my work' sentence")
Use only when the client's re-voice verdict in VIDEO-PICKS.md is NO GOOD MATCH. Replace the re-voice paragraph with:
```
To give you an idea of my voice, you can hear my <a href="https://spencerzvoice.com/#reel">commercial reel</a> and <a href="https://spencerzvoice.com/#spots">past work</a> on my website. I'd appreciate it if you gave it a listen!
```
and end the turnaround/credits paragraph at "...the Preview of the Season for EuroLeague Basketball." (no "You can see more of my work at spencerzvoice.com."). Everything else is v6. `pitch_draft_qc.py` enforces it (REEL_LINE). First used 2026-10-16: Hornet (Marty Geren), Nexus Studios (Kristin Glushon).

---

## v5 (Spencer, 2026-10-14) - history, superseded by v6 (callback + "Audio Engineer" only): his Docebo send
Source: Spencer's Docebo pitch to Manny Gonzalez, sent 2026-10-14 17:36 Lisbon (Gmail `1a13b45f68359792`): "Check out the format for Docobo and apply that to all first touches. The link to the re-voice comes directly after the intro and before I talk about my 24-hour turnaround, my credits, and all that stuff." All 43 unsent pitch drafts (Funnels I, J, K, L, P) were rebuilt to v5 the same afternoon. `.claude/hooks/pitch_draft_qc.py` enforces it.
**What changed vs v4:** the re-voice paragraph moves up to sit right after the intro sentence, and its opener is now "To give you an idea of my voice, I re-voiced your ..." (the v4 "Also, so you can hear how my voice meshes well with your content" opener is retired). Everything else is v4 word for word.

```
[cloud-built drafts only] <span style="background-color:#ffff00">[NOT READY: Bingo's LinkedIn check pending for <Name>, <Title>, <Company>. Bingo deletes this line once it passes]</span>

Hello <First>, hope you're doing well!

Saw <Company> just <event>. <reaction>. Congrats on the <launch>!! <span style="background-color:#ffff00">[Source: <a href="URL">Publication, Mon D, YYYY</a>. Delete this before sending]</span>     (v2 hook rules; leave out if no hook)

My name is Spencer Pearman and I'm a professional Voiceover Artist and audio engineer based in Lisbon, Portugal, and I'd love to voice the videos that come out of <Company>, especially the ones that spread the word about <event, short plain words> and other content.
   (no hook: "...based in Lisbon, Portugal. I'd love to voice the videos that come out of <Company>.")

To give you an idea of my voice, I re-voiced your <a href="<Drive link or https://drive.google.com/REPLACE-WITH-SAMPLE-LINK>">"<exact video title>"</a> <video|spot>. I'd appreciate it if you gave it a listen!
   (no video picked yet: the title text is VIDEO TITLE PENDING)

My standard turnaround is within 24 hours and within 2-3 hours for rush projects. My recent work includes <3 credits, table below>, plus the 2026 FIFA World Cup Preview Series and the Preview of the Season for EuroLeague Basketball. You can see more of my work at spencerzvoice.com.

I'd love to get on a call and talk about working together, please don't hesitate to reach out. Hope to hear from you soon!

Best,<br>Spencer<br><a href="https://spencerzvoice.com">spencerzvoice.com</a>
```
Paragraphs are separated by `<br><br>`. Sports variant, credits table, hook rules and exceptions: as v4/v2 below.

---

## v4 (Spencer, 2026-10-13) - history, superseded by v5 (re-voice line position + opener only): his own Calm + Premier Padel drafts
Source: Spencer rewrote the Calm (Daniel Szeto) and Premier Padel (Yasmine Akki) pitches himself, then said: "copy that format over to the other drafts in Funnel Q and the Ramp draft and save this as the newest pitch in our memory." He confirmed the rush line reads "2-3 hours". All 9 Funnel Q + Ramp drafts and all 10 Funnel I drafts were rebuilt to v4 on 2026-10-13; the 11 Funnel Q/Ramp/Calm/Premier Padel pitches were scheduled for Tue 10-13, 8:32 AM recipient-local. `.claude/hooks/pitch_draft_qc.py` enforces v4 and rejects the v3 lines.
**What changed vs v3:** intro back to "professional Voiceover Artist and audio engineer based in Lisbon, Portugal"; callback "especially the ones that spread the word about <event> and other content"; turnaround line "My standard turnaround is within 24 hours and within 2-3 hours for rush projects."; FIFA/EuroLeague named in full ("the 2026 FIFA World Cup Preview Series and the Preview of the Season for EuroLeague Basketball"); website line "You can see more of my work at spencerzvoice.com."; re-voice line opens "Also, so you can hear how my voice meshes well with your content, I re-voiced your ..."; close "I'd love to get on a call and talk about working together, please don't hesitate to reach out. Hope to hear from you soon!"
**Unchanged:** greeting, hook paragraph and its v2 rules (below), "!!" on the congrats line, the credits table, "meshes well with your content", no em/en dashes, the yellow [NOT READY], [VERIFY EMPLOYMENT] and [Source] marker lines, the Pushkin exception. Spencer's own hook/take text stays word for word. He often personalises the callback per draft ("...and any other news you might have coming up!"); keep his version.

```
[cloud-built drafts only] <span style="background-color:#ffff00">[NOT READY: Bingo's LinkedIn check pending for <Name>, <Title>, <Company>. Bingo deletes this line once it passes]</span>

Hello <First>, hope you're doing well!

Saw <Company> just <event>. <reaction>. Congrats on the <launch>!! <span style="background-color:#ffff00">[Source: <a href="URL">Publication, Mon D, YYYY</a>. Delete this before sending]</span>     (v2 hook rules; leave out if no hook)

My name is Spencer Pearman and I'm a professional Voiceover Artist and audio engineer based in Lisbon, Portugal, and I'd love to voice the videos that come out of <Company>, especially the ones that spread the word about <event, short plain words> and other content.
   (no hook: the sentence ends "...videos that come out of <Company>.")

My standard turnaround is within 24 hours and within 2-3 hours for rush projects. My recent work includes <3 credits, table below>, plus the 2026 FIFA World Cup Preview Series and the Preview of the Season for EuroLeague Basketball. You can see more of my work at spencerzvoice.com.

Also, so you can hear how my voice meshes well with your content, I re-voiced your <a href="<Drive link or https://drive.google.com/REPLACE-WITH-SAMPLE-LINK>">"<exact video title>"</a> <video|spot>. I'd appreciate it if you gave it a listen!
   (no video picked yet: the title text is VIDEO TITLE PENDING)

I'd love to get on a call and talk about working together, please don't hesitate to reach out. Hope to hear from you soon!

Best,<br>Spencer<br><a href="https://spencerzvoice.com">spencerzvoice.com</a>
```
Paragraphs are separated by `<br><br>`.

**Sports variant (Spencer's Premier Padel draft; leagues, tours, teams, federations, sports media/events):**
- Reaching-out: "...and I'd love to be the voice for the videos that <Company> produce, especially the ones that spread the word about <event> ..." (Spencer's own PP line: "...that Premier Padel produce - ones that spread the word about new tournaments and cities, events and news!").
- Credits: "My recent work includes the 2026 FIFA World Cup Preview Series and the Preview of the Season for EuroLeague Basketball, NordicTrack and Altra Running among others. You can see more of my work at spencerzvoice.com."

---

## v3 (Spencer approved 2026-10-12) - history, superseded by v4: humanizer pass on v2
Source: Bingo ran the `humanizer` skill (`.claude/skills/humanizer`) over v2 and proposed this version; Spencer approved it the same afternoon ("Update the pitch and emails in my draft folder starting now"). All 21 unsent pitch drafts were rebuilt to it on 2026-10-12 (`memory/2026-10-12.md`). `.claude/hooks/pitch_draft_qc.py` enforces it and rejects the v2 lines.
**What changed vs v2 and why:** "I hope this message finds you well" (stock opener) → "hope you're doing well!"; "My work is high quality" (claim with no detail) cut; the "bringing the news of X to the world" callback (inflated) → "starting with the ones about <event>"; intro + reaching-out merged into one sentence; "among others (FIFA, EuroLeague Basketball)" → "plus FIFA and EuroLeague Basketball"; "you can hear my work at" → "my reels are at"; "Also, I put together a re-voice of your" → "I also re-voiced your"; the stock "Feel free to reach out or schedule a call" close → "If you'd like to work together, just reply here and we can set up a call."
**Unchanged from v2:** the hook paragraph and its rules (below), the "!!" on the congrats line, the 3-credit table, "meshes well with your content" (Spencer's voice, never change it), no em/en dashes, the yellow [NOT READY: ...], [VERIFY EMPLOYMENT: ...] and [Source: ...] marker lines, and the Pushkin exception. Spencer's own hook/take text stays word for word.

```
[cloud-built drafts only] <span style="background-color:#ffff00">[NOT READY: Bingo's LinkedIn check pending for <Name>, <Title>, <Company>. Bingo deletes this line once it passes]</span>

Hello <First>, hope you're doing well!          (casual, younger men: "Hi <First>, hope you're doing well!")

Saw <Company> just <event>. <reaction>. Congrats on the <launch>!! <span style="background-color:#ffff00">[Source: <a href="URL">Publication, Mon D, YYYY</a>. Delete this before sending]</span>     (v2 hook rules; leave out if no hook)

My name is Spencer Pearman. I'm a voiceover artist and audio engineer in Lisbon, and I'd love to voice the videos that come out of <Company>, starting with the ones about <event, short plain words>.
   (no hook: the sentence ends "...videos that come out of <Company>.")

I turn work around within 24 hours and run my own sessions, so it's one less thing for you to manage. My recent work includes <3 credits, table below>, plus FIFA and EuroLeague Basketball, and my reels are at spencerzvoice.com.
   (credits already name FIFA or EuroLeague: drop the "plus ..." part)

I also re-voiced your <a href="<Drive link or https://drive.google.com/REPLACE-WITH-SAMPLE-LINK>">"<exact video title>"</a> <video|spot> so you can hear how my voice meshes well with your content. I'd appreciate it if you gave it a listen!
   (no video picked yet: the title text is VIDEO TITLE PENDING)

If you'd like to work together, just reply here and we can set up a call. Hope to hear from you soon!

Best,<br>Spencer<br><a href="https://spencerzvoice.com">spencerzvoice.com</a>
```
Paragraphs are separated by `<br><br>`. **Callback (v3):** "starting with the ones about <event>", where <event> is the hook's news in a few plain words ("the Fall Update", "the double 1-2 in Copenhagen", "Nova and Frontline"). Never "to the world" / "with the world". The v2 hook rules, double "!!" rule and credits table below still apply; ignore v2's callback list and its intro/quality/close lines.

---

## v2 (Spencer, 2026-10-07) - history, superseded by v3: congrats hook + callback, Bingo writes the whole hook
Source: Spencer's own sends and edits of 2026-10-07 (Toast, UiPath, Psyop, Robinhood, SoFi, Gong, Instacart, BUCK sent; ABB, Garmin, Peloton, Booking.com, Plaid, The Economist edited in Drafts). His brief: "read the source that we're choosing for the hook and say, if it makes sense, 'Congratulations on the release', 'on this product', 'on this new collaboration', 'on this technology that you've developed'. Then we do a callback when we're talking about the reason why I'm reaching out: 'I'd love to be your voiceover artist ... to help bring the news of this accomplishment to the world'." His answers the same night: Bingo writes the whole hook but still gives him the source link; the quality line gets its own paragraph when there's a callback; credits are 3 matched to the industry.
**v2 replaces, where they conflict:** the 10-03 "Bingo writes the event line only, Spencer writes [YOUR TAKE]" rule and the 10-05 default bridge ", starting with the videos that will tell this story" / "never bring this to the world" (Spencer now writes "bring the news ... to the world" himself). Everything else below (intro, quality line, re-voice line, close, no em dashes) is unchanged.

```
[cloud-built drafts only] <span style="background-color:#ffff00">[NOT READY: Bingo's LinkedIn check pending for <Name>, <Title>, <Company>. Bingo deletes this line once it passes]</span>

Hello <First>, I hope this message finds you well!          (casual, younger men: "Hi <First>, hope you're doing well!")

Saw <Company> just <event, from the source>. <ONE short, plain reaction sentence grounded in a specific detail from the source>. Congrats on the <launch | release | new collaboration | new technology | news | recognition>!! <span style="background-color:#ffff00">[Source: <a href="URL">Publication, Mon D, YYYY</a>. Delete this before sending]</span>

My name is Spencer Pearman and I'm a professional Voiceover Artist and audio engineer based in Lisbon, Portugal.

I'm reaching out because I'd love to be your go-to Voiceover Artist for the projects that come through <Company>, <CALLBACK>.

My work is high quality, my turnaround is within 24 hours, and I run self-directed sessions, so it's one less thing to manage on a job.

My recent work includes <3 credits matched to the industry, table below>, among others (FIFA, EuroLeague Basketball), and you can hear my work at spencerzvoice.com.

Also, I put together a re-voice of your <a href="<Drive link or https://drive.google.com/REPLACE-WITH-SAMPLE-LINK>">"<exact video title>"</a> <video|spot> so you can hear how my voice meshes well with your content. I'd appreciate it if you gave it a listen!

Feel free to reach out or schedule a call if you'd like to talk about working together. I hope to hear from you soon!

Best,<br>Spencer<br><a href="https://spencerzvoice.com">spencerzvoice.com</a>
```

**Double exclamation point (Spencer, 2026-10-07: "use the double exclamation point where applicable. It's something that I do frequently, and it adds a bit more of my personality"):** the hook's Congrats line ends in "!!" ("Congrats on the launch!!"), and so does any other excited line in the hook or callback (his YETI "great call!!", Gong "very exciting news!!"). The fixed template lines (greeting, re-voice line, close) keep a single "!" so every pitch reads the same at the edges.

**Hook rules (v2):**
- Read the source first (watch the video if it's a video). The congrats word fits the event: a product/feature = "launch" or "release", a partnership = "new collaboration", R&D = "new technology", an award/ranking = "recognition", anything else = "news". If no congrats makes sense, there is no hook.
- The reaction is one plain sentence about something specific in the source (Spencer's: "Looks like this new piece has a lot of exclusive capabilities." / "Agentic traders and Robinhood Agents is a big game changer." / "That's a huge, Avenger-style, collaboration you guys got going on."). No jargon, no technical detail an outsider wouldn't get, no jokes, no praise of their marketing strategy.
- Topic rules unchanged (VO/video/creative news or a plain business milestone, never technical/regulatory; CLAUDE.md 5). Product brands: new product + its launch video first, and the re-voice is that video (CLAUDE.md 5c).
- The yellow `[Source: ...]` marker always carries the clickable source link so Spencer can check it; it must be deleted before sending (the pre-schedule check flags it).

**Callback (v2):** names the hook's news and ties it to telling the world, in Spencer's words. Pick the one that fits:
- "like bringing the news of <the event> to the world" (Toast, UiPath)
- "and help bring news like <the event> out to the world" (SoFi, Robinhood)
- "especially ones that will communicate your latest launches and achievements to the world" (Garmin)
- "especially the ones that will help share the exciting news of <Company> with the world" (ABB)
- "like the ones that will share this news about <the event>" (BUCK)
No hook = no callback: the sentence ends at "<Company>." and the quality line stays in the SAME paragraph (Spencer's Booking.com, Plaid, Economist).

**Credits (v2, still current in v3): 3 from the verified list (MEMORY.md "Established credits"), matched to the industry, then (v3) "plus FIFA and EuroLeague Basketball":**
| Company type | Credits |
|---|---|
| Software, SaaS, AI, cyber, cloud, B2B, industrial, energy, corporate | Dell Technologies, Cisco, and Amazon AWS (Brave Browser for browser/privacy/AI tools) |
| Fintech, payments, banking | Venmo, Amazon AWS, and Dell Technologies |
| **Sports organisations: leagues, tours, teams, federations, sports media and sports events** (Spencer, 2026-10-12: "make it the default for sports clients") | v4 (Spencer's Premier Padel draft, 10-13): "My recent work includes the 2026 FIFA World Cup Preview Series and the Preview of the Season for EuroLeague Basketball, NordicTrack and Altra Running among others." (v3 had FIFA and EuroLeague only) |
| Fitness, sporting goods, apparel, outdoor, wearables (brands) | NordicTrack, Fabletics, and FootJoy |
| Travel, hospitality, luggage | Travelpro, Dell Technologies, and Cisco |
| Creative/production/animation studios, media, music | Venmo, Dell Technologies, and Artlist.io |
| Consumer apps, retail, food, delivery | Venmo, Amazon AWS, and Artlist.io |
Never cite an ES/PT credit. Spencer may swap credits per draft; never change his choice.

**Per-client exceptions = Spencer's own call, listed in `NO_SAMPLE_DOMAINS` / `CUSTOM_REACHING_OUT_DOMAINS` in `.claude/hooks/pitch_draft_qc.py`:** Pushkin Industries (no re-voice sample; his own reaching-out line about audiobooks/podcasts and narration + commercial VO), 2026-10-07.

---

## v1 (2026-10-05, Hitachi Rail) - history, superseded where v2 differs

Source: Spencer's own Hitachi Rail email to Janet Klinke, sent 2026-10-05 11:54 Lisbon (Gmail `1a10bb33cf02b312`). He rewrote it himself, then said: "read the wording and format of the Hitachi draft and copy across all other drafts now and moving forward." This replaces the earlier 6-part template. `.claude/hooks/pitch_draft_qc.py` enforces it on every FGAC draft write.

**Spencer's TVA send (scheduled 2026-10-05 night for Tue 10-06 13:32, Gmail `1a111330a0779b60`) is the voice model from here on ("look at the scheduled email that I sent to TVA to get an idea of how I want these to be voiced"):**
- His take after the event line is short, warm, a congratulation: "From what I read that's history in the making. Congrats to you and TVA!" (still Spencer-written, never Bingo's).
- "My work is high quality", not "reliable".
- **Default bridge (Spencer, 2026-10-05 night: "make that bridge the default"):** when the hook is a launch, award, premiere or milestone, `<BRIDGE>` = ", starting with the videos that will tell this story" ("...for the projects that come through TVA, starting with the videos that will tell this story."). No hook, or a hook that isn't news a video would be made about = no bridge, the sentence ends at the company name. The pitch is: congrats on the news, I want to voice the videos that share it. Tie it to the video, never "bring this to the world" or "everybody should hear about". Spencer may rewrite the bridge per draft (his TVA send: ", and hopefully ones that will spread the word about the history you all just made").
- Credits end with "among others (FIFA, EuroLeague Basketball)" when FIFA/EuroLeague aren't already named.
- Close: "Feel free to reach out or schedule a call if you'd like to talk about working together. I hope to hear from you soon!"

**Voice line CUT (Spencer, 2026-10-05 night):** "I have a warm bass/baritone voice, and I record and produce everything myself." is gone from every pitch. The samples show the voice, and self-producing is irrelevant to the buyer. The intro paragraph ends at "Lisbon, Portugal." The QC hook now rejects the old line.

**Spencer's 10-05 edits to his own email (applied):** cut "so turnaround is fast" from the intro (the turnaround line already covers it), "24hrs" → "24 hours", "Voiceover Artist" capitalized in both places. **"meshes well with your content" is his voice. Keep it, never "improve" it.**

Paragraphs are separated by `<br><br>`. Fill only the `<...>` slots and leave every other word as it is.

```
[cloud-built drafts only] <span style="background-color:#ffff00">[NOT READY: Bingo's LinkedIn check pending for <Name>, <Title>, <Company>. Bingo deletes this line once it passes]</span>

Hello <First>, I hope this message finds you well!          (casual, younger men: "Hi <First>, hope you're doing well!")

<hook paragraph: event line + <span style="background-color:#ffff00">[YOUR TAKE] Source: <a href="URL">Publication, Mon D, YYYY</a></span>, or Spencer's own written hook; leave it out if there is none>

My name is Spencer Pearman and I'm a professional Voiceover Artist and audio engineer based in Lisbon, Portugal.

I'm reaching out because I'd love to be your go-to Voiceover Artist for the projects that come through <Company><BRIDGE>. My work is high quality, my turnaround is within 24 hours, and I run self-directed sessions, so it's one less thing to manage on a job.

My recent work includes <2-4 relevant credits, e.g. Dell Technologies, Cisco, and Amazon AWS>, among others (FIFA, EuroLeague Basketball), and you can hear my work at spencerzvoice.com.

Also, I put together a re-voice of your <a href="<Drive link or https://drive.google.com/REPLACE-WITH-SAMPLE-LINK>">"<exact video title>"</a> <video|spot> so you can hear how my voice meshes well with your content. I'd appreciate it if you gave it a listen!
   (no video picked yet: use the title text VIDEO TITLE PENDING)

Feel free to reach out or schedule a call if you'd like to talk about working together. I hope to hear from you soon!

Best,<br>Spencer<br><a href="https://spencerzvoice.com">spencerzvoice.com</a>
```

Credits naming: write "Artlist.io" (Spencer's spelling) and "Dell Technologies". Never "American" or "low-register". No em/en dashes.

Hook placement: Spencer's Hitachi send had no hook paragraph. Drafts that carry a hook keep it between the greeting and "My name is". **Hooks stay (Spencer, 10-05).** The Hitachi send had none only because "there just wasn't anything to say compelling about the Hook Source without it sounding like it was reaching too much." Rule: if the source gives nothing real to react to, leave the hook out rather than force one.
