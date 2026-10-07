# House cold-pitch template

## v2, CURRENT (Spencer, 2026-10-07): congrats hook + callback, Bingo writes the whole hook
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

**Credits (v2): 3 from the verified list (MEMORY.md "Established credits"), matched to the industry, then "among others (FIFA, EuroLeague Basketball)":**
| Company type | Credits |
|---|---|
| Software, SaaS, AI, cyber, cloud, B2B, industrial, energy, corporate | Dell Technologies, Cisco, and Amazon AWS (Brave Browser for browser/privacy/AI tools) |
| Fintech, payments, banking | Venmo, Amazon AWS, and Dell Technologies |
| Fitness, sport, apparel, outdoor, wearables | NordicTrack, Fabletics, and FootJoy |
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
