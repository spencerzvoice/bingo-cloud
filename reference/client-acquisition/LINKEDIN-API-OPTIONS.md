# LinkedIn profile-data APIs for a cloud employment check (priced 2026-10-05)

Purpose: let a cloud routine confirm a contact's current employer/title/start date from their LinkedIn URL with NO login (Spencer, 2026-10-05: wants the check to run without his computer). Volume ~150-300 lookups/month. Pricing pages opened 2026-10-05 by Bingo's research run, named per row. Not adopted yet. Spencer decides.

| Provider | Model | ~150/mo | ~300/mo | Live? | Start date | Free | Cookie | Source |
|---|---|---|---|---|---|---|---|---|
| Bright Data LinkedIn Profiles | PAYG $1.5/1K records | ~$0.23 | ~$0.45 | Live, by URL (async) | not stated (unknown) | "5K records/mo" (one-off vs recurring unclear) | No | brightdata.com/pricing/web-scraper |
| Apify HarvestAPI profile scraper | $4/1K + Apify plan (Free $5/mo, Starter $19) | ~$0.60 | ~$1.20 | Live | Yes | Apify free $5 (unclear if it covers) | No | apify.com/harvestapi/linkedin-profile-scraper |
| RapidAPI Fresh LinkedIn Profile Data | Basic $10/mo = 500 requests | $10 | $10 | Live (~14s) | not checked | none | No | rapidapi.com (freshdata) |
| ZenRows LinkedIn | Free 5K credits/mo; Build $16 | $0-16 | $0-16 | Live, public view | Yes (date ranges) | 5K credits/mo | No | zenrows.com/pricing |
| Scrapingdog | Lite $40/mo | $40 | $40 | Live | Yes | 100 credits | No | scrapingdog.com/pricing |
| Enrich Layer | credit packs; live fetch = 10 credits | ~$40 | ~$79 | Cache <=29d or forced live | Yes | none | not stated | enrichlayer.com/pricing |
| People Data Labs | Pro from $98/mo | $98 | $98 | DATABASE (fails freshness) | ? | 100/mo | No | peopledatalabs.com/pricing/person |
| Coresignal | Starter $199/mo | $199 | $199 | DATABASE (fails freshness) | ? | 7-day trial | No | coresignal.com/pricing |

Dead: Proxycurl ("no longer in service", nubela.co/proxycurl/ → NinjaPear). No LinkedIn endpoint found: ScraperAPI, Oxylabs (unverified).
Caveats: all live scrapers read the LOGGED-OUT public profile, so some profiles hide experience. A miss = [VERIFY EMPLOYMENT], never a pass. All are scraping against LinkedIn's ToS; the risk sits with the vendor, not Spencer's account (no login used).
Recommendation: Bright Data (cheapest, established, live). Runner-up Apify HarvestAPI. Before adopting: free-tier bake-off on 10 known profiles (incl. a known job-changer) vs the live-page results in LINKEDIN-CHECKS.md.
