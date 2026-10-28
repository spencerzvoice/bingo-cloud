# Funnel S2 research, Group A (2024 re-approach channels), 2026-10-28

Research only: nothing sent, no Gmail/Drive touched. Every ✅ fact was read this session from yt-dlp output: channel About JSON (`description`, `channel_follower_count`), per-video `-J` (`upload_date`, `duration`, `description`), and auto-caption VTT files (`en` / `en-orig`). Raw data: `scratchpad/s2_research/A/*.json` and `scratchpad/s2_research/A/subs/*.vtt`.

Caveats that apply to every row:
- **Emails:** yt-dlp only sees the About *text* and video descriptions. YouTube's hidden "View email address" business-email button (needs sign-in and a CAPTCHA) was NOT checked. "None found" means "not printed in About/description text", not "the channel has no email".
- **Excerpt times** come from auto-caption cue starts, so they're accurate to about ±1 s. End times are the end of the closing sentence. Check them by ear before cutting.
- **Narrator verdicts** come from credits and captions only. I heard no audio, so AI vs. human voice can't be judged unless the channel says so.
- ACTIVE = a long-form (>4 min) upload since 2026-07-30 (90 days before 2026-10-28).

## Summary table

| # | Channel (handle, subs ✅) | Last 5 long-form uploads ✅ (cadence) | Active | Narrator | Email printed today vs 2024 | Re-voice pick ✅ | Excerpt (s) | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Be Smart, [@besmart](https://www.youtube.com/@besmart), 5.89M | 10-22, 09-15, 08-18, 07-16, 07-02 (~monthly) | ✅ yes | ON-CAMERA HOST ✅ ("hosted and produced by Joe Hanson, PhD", desc + About; first-person "I've spent the last couple of months…" captions) | `biz@itsokaytobesmart.com` ✅ (desc "SPONSORSHIP INQUIRIES") = **different** from itsokaytobesmart@gmail.com | [YgoiujmwLKI](https://www.youtube.com/watch?v=YgoiujmwLKI) "The Real Cost of AI Will Shock You", 2026-10-22, 42:43, THE newest | 34.4–91.9 (57.5) | **ON-CAMERA** |
| 2 | Real Science, [@realscience](https://www.youtube.com/@realscience), 2.09M | 2025-12-06, 2025-11-22, 2025-10-25, 2025-09-27, 2025-08-30 (biweekly to monthly, then stopped) | ❌ no (last upload 326 days ago) | Credited ✅: "Editing, Writing, Narration: Stephanie Sammann" (latest desc). Owner or hire ❓ | none found; realscience@standard.tv not printed | [2KpNwcpAAd8](https://www.youtube.com/watch?v=2KpNwcpAAd8) "Why Studying Sloths Is Basically Impossible", 2025-12-06, 17:10, THE newest | 33.2–76.1 (43, interview cuts in) | **INACTIVE** |
| 3 | Newsthink, [@Newsthink](https://www.youtube.com/@Newsthink), 1.24M | 10-19, 10-01, 09-20, 08-31, 08-04 (every 2–3 wks) | ✅ yes | FOUNDER ✅ ("Newsthink is produced and presented by Cindy Pom", every desc; About "Hi, I'm Cindy Pom… before starting Newsthink") | none found; hello@newsthink.ca not printed | [FrmDpOtkR0I](https://www.youtube.com/watch?v=FrmDpOtkR0I) "Why Isaac Newton Quit Science", 2026-10-19, 11:46, THE newest | 0.6–62.4 (61.8) | **FOUNDER-VOICED** |
| 4 | Animagraffs, [@animagraffs](https://www.youtube.com/@animagraffs), 1.94M | 2026-08-21, 06-09, 03-25, 2025-10-01, 2025-09-19 (every 2–3 months) | ✅ yes (68 days) | FOUNDER ✅ (desc "Jacob O'Neal - Research, script, narration…"; caption 0:02 "I'm Jake O'Neal, creator of Animagraffs") | none found; animagraffs@gmail.com not printed | [n9-5G4bS0X4](https://www.youtube.com/watch?v=n9-5G4bS0X4) "How the Grumman F-14 Tomcat Works", 2026-08-21, 46:00, THE newest | 12.2–71.1 (59) | **FOUNDER-VOICED** |
| 5 | Lesics, **renamed "Sabin Civil Engineering"**, [@SabinCivil](https://www.youtube.com/@SabinCivil), 6.96M | 09-29, 08-08, 07-02, 06-19 (course promo, 4:47), 05-30 (~monthly) | ✅ yes | ❓ unknown (no credit in any desc; captions don't name the narrator) | none found; sabin@lesics.com not printed | [nyjI97MuUBI](https://www.youtube.com/watch?v=nyjI97MuUBI) "Marina Bay Sands \| The Most Dangerous Building Gamble in History", 2026-09-29, 12:55, THE newest | 0.4–57.0 (56.6) | **NO EMAIL** |
| 6 | Branch Education, [@BranchEducation](https://www.youtube.com/@BranchEducation), 2.77M | 09-21, 08-21, 05-28, 02-17, 2025-11-15 (monthly to quarterly) | ✅ yes | **HIRED ✅** ("Voice Over: Phil Lee" in all 5 descs; founder Teddy Tablante writes/edits) | none found; brancheducation@nebula.tv not printed | [N_6k_jd5pnA](https://www.youtube.com/watch?v=N_6k_jd5pnA) "How does Tap to Pay Work?", 2026-09-21, 30:18, THE newest | 0.3–62.8 (62.5) | **NO EMAIL** (strong fit: they hire VO) |
| 7 | Real Engineering, [@RealEngineering](https://www.youtube.com/@RealEngineering), 5.12M | 09-26, 08-29, 08-22, 08-02, 08-01 (every 1–4 wks) | ✅ yes | FOUNDER ✅ ("Producer/Writer/Narrator: Brian McManus", desc) | none found; mcmanus.brian1@gmail.com not printed | [6B96xetwrqI](https://www.youtube.com/watch?v=6B96xetwrqI) "The Plane That's 38% Nose", 2026-09-26, 20:16, THE newest | 0.2–59.5 (59, includes ~5 s title beat at 45–51) | **FOUNDER-VOICED** |
| 8 | Smart Tech, [@smarttechus](https://www.youtube.com/@smarttechus), 256K | 10-26, 10-24, 10-22, 10-18, 10-16 (every 2–4 days) | ✅ yes | ❓ narrated, uncredited (captions: "Hello tech enthusiasts. Join us on Smart Tech…"). AI vs human ❓ | `surfingukr@gmail.com` ✅ (About text) = **same** | [em3I43eFVHQ](https://www.youtube.com/watch?v=em3I43eFVHQ) "45 Unbelievable Heavy Machinery That Are At Another Level!", 2026-10-26, 38:08, THE newest | 19.3–80.0 (61) | **READY** (see notes: low-quality compilation channel) |
| 9 | Bloomberg Originals, [@business](https://www.youtube.com/@business), 5.18M | 10-28, 10-27, 10-26, 10-25, 10-23 (daily) | ✅ yes | Mixed: host-led shows ✅ (e.g. "Hosted by… Emily Chang", The Circuit). Pick has an uncredited narrator ❓ | none found; digitalvid@bloomberg.net not printed | [3kGQ7gsrOeA](https://www.youtube.com/watch?v=3kGQ7gsrOeA) "The Most Profitable Subway on Earth", 2026-10-27, 11:20, **one of the latest** (newer: 10-28 Circuit episode, host-led) | 4.1–48.7 (44.6, then an interviewee) | **NO EMAIL** |
| 10 | Crime Dynasty, [@crimedynasty](https://www.youtube.com/@crimedynasty), 431K | 10-27, 10-22, 10-17, 10-12, 10-05 (every ~5 days) | ✅ yes | In-house ✅ (desc: "We thoroughly research every video, do our own editing and narrating"); who ❓ | none found; partnerships@crimedynasty.com not printed | [g0FhaAUL6v8](https://www.youtube.com/watch?v=g0FhaAUL6v8) "7 Men Who Slept With A Cartel Boss's Wife", 2026-10-27, 27:05, THE newest | 0.0–64.6 (64.6) | **NO EMAIL** |
| 11 | Billion Dollar Builds, [@billiondollarbuilds](https://www.youtube.com/@billiondollarbuilds), 143K | 10-28, 10-13, 09-24, 09-04, 08-29 (biweekly) | ✅ yes | ❓ unknown (no credit; desc says "our team produces…") | none found; billiondollarbuilds@gmail.com not printed | [IgGNvA5Qodg](https://www.youtube.com/watch?v=IgGNvA5Qodg) "Hoover Dam Is Running Out Of Power And It's Only Going To Get WORSE!", 2026-10-28, 12:28, THE newest | 0.6–59.5 (59) | **NO EMAIL** |
| 12 | The Impossible Build, [@TheImpossibleBuild](https://www.youtube.com/@TheImpossibleBuild), 152K | 2026-01-13, 01-10, 01-06, 01-02, 2025-12-01 (bursts, then stopped) | ❌ no (last upload 288 days ago) | ❓ unknown | none found; theimpossiblebuild@gmail.com not printed | [aH2K7qNY4tg](https://www.youtube.com/watch?v=aH2K7qNY4tg) "Inside the Artificial Islands Engineers Are Racing to Keep Afloat", 2026-01-13, 12:59, THE newest | 0.2–59.5 (59) | **INACTIVE** |
| 13 | Rare Cars, [@rarecars3336](https://www.youtube.com/@rarecars3336), 122K | 10-24, 10-17, 10-13, 10-03, 10-01 (1–2/week) | ✅ yes | ❓ human, not named (About: "NO AI Voices Used"; captions are first person: "that I have been able to find") | `rarecarsmedia@gmail.com` ✅ (every desc: "For business inquiries…") = **different** from rarecarsmedia@fearlessotter.com | [M7y0dM_W37k](https://www.youtube.com/watch?v=M7y0dM_W37k) "The History Of The HEMI Engine From 1900 to 2026", 2026-10-24, 31:18, THE newest | 0.3–59.7 (59.4) | **READY** (channel identity 🟡, see notes) |
| 14a | Wendover Productions, [@Wendoverproductions](https://www.youtube.com/@Wendoverproductions), 4.92M | 10-21, 09-30, 09-04, 08-25, 08-08 (every 2–3 wks; About "every other Tuesday") | ✅ yes | 🟡 FOUNDER (Sam Denby). No narrator credit seen this session; this comes from prior knowledge | `wendover@standard.tv` ("Sponsorship Enquiries") + `sam@wendover.productions` ("Other emails") ✅ = **same** as 2024 | [vIGub9r4a2o](https://www.youtube.com/watch?v=vIGub9r4a2o) "America's Most Illegal Military Base", 2026-10-21, 23:49, THE newest | 0.7–57.8 (57) | **FOUNDER-VOICED 🟡** |
| 14b | Half as Interesting, [@halfasinteresting](https://www.youtube.com/@halfasinteresting), 2.95M | 10-19, 10-14, 10-07, 09-30, 09-23 (weekly) | ✅ yes | 🟡 FOUNDER (Sam Denby, prior knowledge). Desc credits writers only ("Video written by Ben Doyle" / "Amy Muller") | none printed on HAI; 2024 used sam@wendover.productions (shared with Wendover) | [ju1OZStv2eI](https://www.youtube.com/watch?v=ju1OZStv2eI) "How Planes Fly Without Air Traffic Control", 2026-10-19, 7:18, THE newest | 0.6–56.3 (55.7) | **FOUNDER-VOICED 🟡** |
| 15 | Neo, [@neoexplains](https://www.youtube.com/@neoexplains), 3.05M | 2026-07-13, 04-14, 02-24, 2025-11-18, 2025-09-16 (every ~2–3 months) | ❌ no (last upload 107 days ago; borderline) | Credited ✅ "Animations and Narration: Leon Herres" (02-24 desc); first person "I digitally reconstructed…" (captions). Founder 🟡 | none found; neo@standard.tv not printed | [krSePO1QsDI](https://www.youtube.com/watch?v=krSePO1QsDI) "How the U.S. Doomsday Plane Works", 2026-07-13, 15:19, THE newest | 1.1–58.5 (57.4) | **INACTIVE** (also founder-voiced 🟡) |

Status counts: READY 2 (Smart Tech, Rare Cars) · ON-CAMERA 1 (Be Smart) · FOUNDER-VOICED 5 (Newsthink, Animagraffs, Real Engineering, Wendover 🟡, HAI 🟡) · NO EMAIL 5 (Sabin Civil/Lesics, Branch Education, Bloomberg Originals, Crime Dynasty, Billion Dollar Builds) · INACTIVE 3 (Real Science, The Impossible Build, Neo) · BLOCKED 0 · NOT FOUND 0.

---

## Per-channel notes and excerpt quotes

### 1. Be Smart (PBS, Joe Hanson): ON-CAMERA
- Channel ID UCH4BNI0-FOK2dMXoFtViWHw ✅. Description: "Produced by Least Square Media and Spotzen for PBS Digital Studios" ✅.
- Excerpt 34.4–91.9 s skips the 0–34 s cold open ("Do you hate AI?…"). First: "AI technology has become one of the most contentious issues of our time." Last: "So I sat down with these scientists and researchers who study this stuff every day so that we could get the real answers." Interview soundbites start at 91.96.
- Notes: Joe Hanson hosts and speaks in first person. I didn't watch frames, so how much of this is on camera vs VO is ❓. Low fit for a narrator pitch. The new sponsorship address (biz@) is a sponsor inbox.

### 2. Real Science: INACTIVE
- Channel ID UC176GAQozKKjhz62H8u9vQQ ✅. Nebula partner (desc links nebula.tv/videos/realscience-…) ✅.
- Excerpt 33.2–76.1 s (only 43 s of continuous narration; an interviewee, Dr. Becky Cliff's segment, starts at 76.2). First: "All across Costa Rica, scientists and conservationists are working tirelessly to understand and protect some of the world's most peculiar creatures, two-toed and three-toed sloths." Last: "And on top of this, for a long time, sloths were woefully misunderstood." The 0–31 s opening is an interview cold open.
- Notes: no long-form upload since 2025-12-06. Narration credited to Stephanie Sammann on the latest video only. Earlier descs don't credit a narrator.

### 3. Newsthink: FOUNDER-VOICED
- Channel ID UCIlU5KDHKFSaebYviKfOidw ✅.
- Excerpt 0.6–62.4 s. First: "In February 1699, a prisoner was brought to a London pub to meet a government official." Last: "He filled his notebooks with everything from instructions on how 'to make birds drunk' to questions about light and colour."
- Notes: sponsor read at 7:17 (UPDF) per chapter list ✅, outside the excerpt. Cindy Pom (ex-CBS/CBC correspondent) presents her own channel. Low fit.

### 4. Animagraffs: FOUNDER-VOICED
- Channel ID UCnZeeKO8qVdtkrA4-uKhtTw ✅.
- Excerpt 12.2–71.1 s skips the host intro ("I'm Jake O'Neal, creator of Animagraffs. And this is how the Grumman F-14 Tomcat works."). First: "Its design phase began in the 1960's, and it was officially deployed in 1974, in the midst of the cold war." Last: "The iconic variable sweep wings can shift from 20 degrees at their widest angle, to 68 degrees sharp rearward rake, forming a perfect delta or triangle shape ideal for supersonic speeds."
- Notes: one person makes everything (research, script, narration, music) per desc ✅. Low fit.

### 5. Lesics → Sabin Civil Engineering: NO EMAIL
- Channel ID UCqZQJ4600a9wIfMPbYc60OQ ✅. The rename is confirmed by the channel's own video "Lesics is getting renamed!" (ytsearch result, same channel) ✅. `@Lesics` / `@lesics` / `@LesicsOfficial` return 404 ✅.
- About ✅: "This channel is currently in the brink of a shutdown. Your support at Patreon is valuable to us… Cheers Sabin Mathew."
- Excerpt 0.4–57.0 s. First: "The unique architectural shape of Marina Bay Sands in Singapore is incredible, but you'll be astonished to learn about the challenges engineers had to overcome to achieve it." Last: "How do you fix this issue?"
- Notes: Lovable sponsor link in desc ✅ (where the read sits in the video ❓). A channel near shutdown and asking for Patreon money is a budget red flag. Email: check the About "View email address" button by hand.

### 6. Branch Education: NO EMAIL (best-fit lead in this group)
- Channel ID UCdp4_l1vPmpN-gDbUwhaRUQ ✅. About: "Founder of Branch Education: Theodore J Tablante" ✅.
- Excerpt 0.3–62.8 s. First: "Let's say you're at your favorite coffee shop." Last: "…the exact cryptographic algorithms used to securely transmit your bank details, and everything else involved in near field communication or NFC, which is the technology behind contactless payments."
- Notes: they **hire their narrator** (Phil Lee on all 5 latest). They're a real VO buyer, but the pitch would be asking them to switch or add a voice. Sponsors: IEEE Spectrum, Micron, Brilliant (descs) ✅. No email printed. The 2024 address was @nebula.tv. Get the About-button email before drafting.

### 7. Real Engineering: FOUNDER-VOICED
- Channel ID UCR1IuLEqb6UEA_zQ81kwXfg ✅. Standard/Nebula network ✅ (desc: standard.tv merch link, Nebula links).
- Excerpt 0.2–59.5 s. First: "This is the X59, NASA's latest X-plane and the newest creation from Lockheed Martin's secretive Skunk Works in Palmdale, California." Last: "From tip to nose wheel, it takes up over half the plane." The title line "This is the insane engineering of the X59 Quest." ends ~45 s, followed by ~5 s of music before 51 s.
- Notes: Brian McManus narrates his own channel. The team includes a Head of Production (Mike Ridolfi) and a writer (Josi Gold) ✅. Desc also plugs throttle.media, which builds 3D animation for clients ✅. That could be a separate production-company lead 🟡.

### 8. Smart Tech: READY (with caveats)
- Channel ID UCn9PDlPz01u9OCpb4scwY4A ✅. About ✅: "curating captivating moments featuring colossal machines… inquiries regarding copyright… surfingukr@gmail.com".
- Excerpt 19.3–80.0 s skips the channel greeting (8.3–15.9 s). First: "The Python 5000 is designed for use in regions outside of North America and Europe where access to ultra-low sulfur diesel fuel may be limited." Last: "To ensure ultimate off-road capability, the Praetorian is fitted with a drivetrain from a MAN four-wheel drive truck with differential locks and stabilizers."
- Notes: this is a fair-use compilation of other companies' footage, posted every 2–4 days. The video descriptions contain odd boilerplate (a fake-looking "Mother's maiden name… Birthday Date…" block and an empty "contact:" line) ✅. Narrator voice could be AI ❓. Low budget and low credibility. Spencer should decide whether it's worth a slot.

### 9. Bloomberg Originals: NO EMAIL
- Channel ID UCUMZ7gohGI9HcU9VNsr2FJQ ✅, handle @business.
- Excerpt 4.1–48.7 s (44.6 s; an interviewee speaks 48.8–57.8, then the narrator resumes 57.8–73.7). First: "It's 2 a.m. and an army of high-skilled mechanics has descended into the tunnels of Hong Kong's subway." Last: "It's driven by predictive AI and thousands of sensors catching mechanical faults before trains even break down." For ~60 s, join 4.1–48.7 and 57.8–73.7.
- Notes: corporate newsroom. Most shows are fronted by Bloomberg journalists (Emily Chang, Francine Lacqua). The narrator of the pick is uncredited ❓. digitalvid@bloomberg.net isn't printed anywhere. A cold YouTube-channel pitch is the wrong door here. Buyer-gate it like a company (Bloomberg Media video EP).

### 10. Crime Dynasty: NO EMAIL
- Channel ID UC_iDeVHuxSAScwmyqiQDYjw ✅.
- Excerpt 0.0–64.6 s (includes a ~5 s music beat at 19–25). First: "1989, a cartel boss opens a box." Last: "Together they had two small children, but the world around him was about to crack open."
- Notes: desc says "scripts written and checked by real humans" and "do our own editing and narrating" ✅. That suggests an in-house narrator. True crime, uploads every ~5 days. No email printed.

### 11. Billion Dollar Builds: NO EMAIL
- Channel ID UCJjHHlKlx9e-heapJ_Rwa6Q ✅.
- Excerpt 0.6–59.5 s. First: "For nearly a century, one of America's greatest engineering marvels has stood against the immense force of the Colorado River." Last: "Its seasonal floods threatened settlements and farmland while unpredictable flows made reliable irrigation difficult."
- Notes: fair-use footage, "our team produces well-researched…" ✅. Narrator ❓ (could be AI, not judged). Smallest channel in the group (143K).

### 12. The Impossible Build: INACTIVE
- Channel ID UCfAU3Cacu8v-qJJ4dSoe7zw ✅. About links theimpossiblebuild.org/newsletter ✅.
- Excerpt 0.2–59.5 s. First: "Did you know that in the last century, engineers have moved more earth and rock than all the natural rivers in the world combined?" Last: "We begin with the most famous shape in ocean engineering."
- Notes: no long-form upload since 2026-01-13. Skip.

### 13. Rare Cars: READY (identity 🟡)
- Channel ID UCOdITIW6-5_FZYyYGaTuPOw ✅, handle @rarecars3336. About ✅: "Unique automotive documentaries on history's rare cars… NO AI Voices Used."
- **Identity check:** `@rarecars` (247K) is a different channel, a car *marketplace* ("Dealers: 30 days free, then $99/mo") ✅. Don't use it. `@rarecars3336` matches the 2024 mailbox name (rarecarsmedia@), but nothing seen this session names Fearless Otter. The desc email is now @gmail.com. Whether this is the same channel and owner as 2024 is 🟡.
- Excerpt 0.3–59.7 s. First: "Hemi is a name that almost every car enthusiast knows." Last: "And Chrysler itself even experimented with hemispherical combustion chambers during World War II."
- Notes: the narrator speaks in the first person ("the earliest record… that I have been able to find"), so this may be founder-narrated ❓. Uploads 1–2/week.

### 14. Wendover Productions + Half as Interesting (Sam Denby): FOUNDER-VOICED 🟡
- Wendover channel ID UC9RM-iSvTu1uPJb8X5yp3EQ, HAI UCuCkxoKLYO_EQ2GeFtbM_bw ✅. Standard/Nebula network ✅ (wendover@standard.tv, Nebula links).
- Wendover excerpt 0.7–57.8 s. First: "The British government does its best to maintain the fiction of the British Indian Ocean Territory, but it's a flimsy one." Last: "But bizarrely, it's not even a British base, it's an American one."
- HAI excerpt 0.6–56.3 s. First: "On September 29th, the day that this video was written, Air France flight 256 from Paris to Ho Chi Minh City lost contact with air traffic control, flying completely blind over the Middle East for almost a full hour." Last: "Flying major commercial routes through this uncontrolled airspace is actually kind of a new thing and it's mostly out of necessity."
- Notes: neither channel credits a narrator in its descs, and I didn't hear audio, so "Sam Denby narrates" is 🟡 (not verified this session). Storyblocks and Chime sponsor reads are in descs, placement ❓. HAI's script is full of jokes that rely on Sam's delivery, so it's a weaker re-voice demo than Wendover.

### 15. Neo: INACTIVE
- Channel ID UCtYKe7-XbaDjpUwcU5x0bLg ✅. Nebula partner ✅.
- Excerpt 1.1–58.5 s. First: "The Boeing VC-25 is perhaps the most iconic plane in the world, and it is of course the aircraft that the US president most often uses while traveling, giving it the call sign Air Force One." Last: "And for this video, I digitally reconstructed and mapped out the inside of the aircraft to understand how the Doomsday Plane actually works."
- Notes: last long-form upload was 2026-07-13, 107 days ago, so it misses the 90-day line by 17 days. Narration credited to Leon Herres, who also animates. Likely founder-voiced 🟡. Low fit either way.

---
— Verified: subscriber counts, upload dates, durations and titles (yt-dlp `-J` / flat playlist, this session) · descriptions and credits quoted above (yt-dlp `description`) · excerpt quotes and times (auto-caption VTT, this session) · Lesics rename (channel's own "Lesics is getting renamed!" video) · @rarecars is a marketplace (About text)
— Bracketed (you fill): hidden About-button business emails for Sabin Civil, Branch, Crime Dynasty, Billion Dollar Builds, Newsthink, Animagraffs, Real Engineering, Neo, Real Science, Impossible Build (needs a signed-in browser + CAPTCHA, not attempted)
— Unknown: AI vs human voice on Smart Tech / Billion Dollar Builds / Impossible Build · whether @rarecars3336 is still the Fearless Otter channel · whether Sam Denby narrates Wendover/HAI (🟡, not verified this session) · sponsor-read placement in Sabin, Wendover, HAI videos
