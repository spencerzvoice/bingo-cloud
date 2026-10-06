# GEO off-site work: 2026-10-06

Everything below was checked live in Spencer's Chrome or via FGAC Gmail this run.

## Done

**1. Search engines**
- Google Search Console: `sc-domain:spencerzvoice.com` exists and is verified. Before: `https://spencerzvoice.com/sitemap.xml` was submitted earlier today with status "Couldn't fetch". The URL serves 200 / application/xml with 3 URLs (/, /pt/, /es/). I resubmitted it and got "Sitemap submitted successfully". The old `https://www.spencerzvoice.com/sitemap.xml` (Carrd, 2024) is still listed as "Couldn't fetch". It's harmless and I left it.
- Bing Webmaster Tools: the site `https://spencerzvoice.com/` was already added and verified (imported from GSC earlier today). The new sitemap showed "Success, 1 URL discovered" from the first submit, so I resubmitted it and it's now "Processing". The old www sitemap (2024 import, 32 URLs) is still listed. Its URLs are all dead Carrd pages.

**2. Cloudflare (personal account, zone spencerzvoice.com): no change needed. Everything was already allowed.**

| Setting | Before | After |
|---|---|---|
| AI Crawl Control > Security, per-crawler "Block" toggles (ClaudeBot, Claude-SearchBot, Claude-User, GPTBot, OAI-SearchBot, ChatGPT-User, PerplexityBot, Perplexity-User, Googlebot, BingBot, Applebot, all others) | all OFF (allowed) | unchanged |
| Security > Settings > Configure AI bot policies: Search / Agent / Training | Allow / Allow / Allow | unchanged |
| Bot Preference Sync (managed robots.txt) | OFF | unchanged (robots.txt = site's own: `User-agent: * / Allow: /` + sitemap) |
| Bot fight mode | OFF | unchanged |
| AI Labyrinth | OFF | unchanged |
| Custom security rules | none | unchanged |

Note: Google-Extended has no separate toggle. It is a robots.txt token, and robots.txt allows everyone. Over the last 7 days, AI Crawl Control logged 2.63k "unsuccessful" requests, which are 404s (old Carrd paths). They are not blocks. With crawler user agents, the homepage returns 200.

**3. Directories**
- Voquent: Spencer is logged in. Profile #23219 does NOT appear on the Lisbon page (/studios/portugal/lisbon/ lists 11 talents, filtered by the public location). The public location still reads "Oakland, United States". No location field can be edited in Profile, My Experience, My Studio, Availability or Account. The billing address is already Rua Regedor 11, Lisboa. The fix is Voquent support. See handoff 4 (the draft from earlier today is no longer in Drafts). I also removed Joshua Alexander from the Voquent About ("Coached by Elaine Craig and Scott Burns.").
- Outspoken Voices: no account (Chrome is signed out, and Gmail shows only a 2024 reel email to info@outspokenvoices.com). It needs a new account, so that's Spencer's step (below).
- great-voices.com: no talent-submission page or address. The only contact is `hello@great-voices.com` (on /voice-over-lisbon and /quote). The "About us" page says they hold a database of 2000+ actors. I did NOT create the Gmail draft. The repo's `pitch_draft_qc.py` hook blocks any new (non-reply) FGAC draft that doesn't follow the client-pitch template, and a roster submission can't follow it. The text is below for Spencer to paste.

**4. Bios** (full before/after in `reports/profile-bios-2026-10-06.md`)
- LinkedIn About: replaced with the site About text plus "Hear samples at spencerzvoice.com." Saved. There was no share-with-network option in that dialog.
- Bodalgo: replaced the long description with the site About text. Training now reads "Coached by Elaine Craig and Scott Burns..." (Joshua Alexander removed). Saved and confirmed.
- Intch: signed out. That's Spencer's step (below).

**5. YouTube credit drafts** (Gmail drafts in spencer@spencerzvoice.com, both thread replies with In-Reply-To/References set)
- Primal Space → Ewan, `spaceprimal@gmail.com`. Draft `r6174903323294945585` (message 1a1128f909ab3407) in thread 19e45d7ba7d29629 ("Re: Narration Rate Adjustment..."). This is the latest thread with them, May 20 2026. It's Spencer's rate notice, and there's no reply in it. Finding: the "Why Inventing Color TV Was So Difficult" description ALREADY credits "Narrator: Spencer Pearman" (no link). The draft asks them to change that line to "Narrated by Spencer Z. Pearman, spencerzvoice.com".
- Noah Media Group → Neil Housley, `neil.housley@noahmediagroup.com`. Draft `r-3679035919524481658` (message 1a1128f9604946b5) in thread 1a058a09e07bb4b3 ("Re: Checking in after the Preview Series"). Neil replied there warmly on Sep 4. Dan Shaw's thread (Sep 11) never got an answer, so I chose Neil's. Finding: the episodes live on FIFA's own channel (Ep 1, PBXkGP2CEFs, uploaded by "FIFA"), and that description has no narrator credit. Noah likely can't edit it, so the draft asks Neil to add the credit or point Spencer to whoever handles FIFA's uploads.

## Handed to Spencer (exact steps)
1. **Intch bio:** go to intch.org > Sign In > enter your email > enter the code from your inbox > Profile > edit bio. Paste the text in `reports/profile-bios-2026-10-06.md` (Intch section).
2. **Outspoken Voices listing (free account):** go to https://www.outspokenvoices.com/voice-actor/register. Sign up (this needs a password, so it's yours to do). Set city = Lisboa, country = Portugal, language = American English, gender = Male. Add the reels and paste the site About text as the bio. The Lisboa page lists artists by profile city.
3. **great-voices.com submission:** create a new email from spencer@spencerzvoice.com to hello@great-voices.com.
   Subject: `Voiceover talent submission: Spencer Pearman (American English, Lisbon)`
   ```
   Hi Great Voices team,

   I'm Spencer Pearman, an American English voiceover artist based in Lisbon. I saw your Lisbon voice over page and would love to be on your roster for English-language projects.

   I record in a fully treated studio here in Portugal, and recent work includes FIFA, Amazon Web Services, NordicTrack, FootJoy and EuroLeague Basketball. You can hear my reels at spencerzvoice.com.

   Happy to send anything else you need.

   Best,
   Spencer
   spencerzvoice.com
   ```
4. **Voquent location:** the earlier draft r4540827422879882096 is no longer in spencer@spencerzvoice.com Drafts (404 this run), and nothing to talent@voquent.com is in that mailbox. So either Spencer sent it from spencerzpearman@gmail.com (his Voquent login email) or it was deleted. If not sent: email talent@voquent.com from spencerzpearman@gmail.com, subject "Location update for profile #23219 (Spencer Pearman)": "Hi Voquent team, my profile #23219 still shows Oakland, United States, but I'm now based in Lisbon, Portugal (my account address is already updated). Could you update my public location to Lisbon, Portugal? Thanks! Spencer". This is the only route onto the Lisbon page.
5. **Review + send** the two credit drafts (Primal Space / Ewan, Noah / Neil).

## Flags (not changed)
- Voquent public profile shows Pronouns "ae / aer / aers / aerself" (Account & Settings > Pronouns). It looks like a default dropdown pick. Spencer should set or clear it.
- The LinkedIn banner image includes a Workday logo. I didn't touch it.
- Bodalgo Experience still says "voicing 6 of 12 episodes of the 2026 FIFA World Cup Preview Series" and "iFit/NordicTrack's 2023 Holiday Campaign where I voiced 4 separate spots". These were left as they were (not on the site; I didn't verify them).
- Bing/GSC still hold the 2024 www/Carrd sitemap. You can remove it in each tool once the new one is indexed.

— Verified: GSC + Bing sitemap state (live dashboards) · Cloudflare bot settings (live dashboard) · site About text (spencerzvoice.com, live) · Primal Space description credit (YouTube hyjCmIbRRvs) · FIFA Ep 1 description has no credit (YouTube PBXkGP2CEFs) · contact addresses/threads (FGAC Gmail) · great-voices contact (site pages)
— Bracketed (you fill): none
— Unknown: whether Voquent will change the city on request; whether Noah can influence FIFA's YouTube descriptions
