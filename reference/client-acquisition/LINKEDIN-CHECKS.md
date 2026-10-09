# LinkedIn final checks

Every final employment check on a live LinkedIn profile page, done by the `linkedin-final-check` skill (desktop, built-in browser). A contact is ready to send only after a PASS here within the last 14 days. Apollo/search results never go in this file.

Format: `date | name | company | profile URL | "headline / current title as shown" | PASS / LEFT / UNRESOLVED (+why)`

Pending as of 2026-10-05 (Apollo-confirmed today; LinkedIn not yet opened): Janet Klinke (Hitachi Rail) linkedin.com/in/janet-klinke · Nicholas Dahl (Coinbase) linkedin.com/in/nicholas-dahl-a3144017 · Kelly Bonner (SoFi) linkedin.com/in/kellyannebonner · Cameron Aspinwall (lululemon) linkedin.com/in/cameron-aspinwall-700715b2 · Jesse Hill (YETI) linkedin.com/in/jessenicholashill


Pending Funnel G2 (Apollo-confirmed 2026-10-05; built-in browser hit LinkedIn authwall, Spencer to sign in): Roland Luitgaarden (F5) linkedin.com/in/rolandluit · Sergio Manzo (Siemens) linkedin.com/in/sergio-ricardez-manzo · Natascha Ladstaetter (Siemens Energy) linkedin.com/in/nataschaladstaetter · Bleu Hayes (TVA) linkedin.com/in/bleuhayes · Mito Habe-Evans (NPR) linkedin.com/in/mitohabeevans · Ariana Lilligren (Smithsonian) linkedin.com/in/ariana-lilligren-30740a48
2026-10-05 | Roland Luitgaarden | F5 | linkedin.com/in/rolandluit | "Lead Creative Producer, F5, Jun 2026 - Present" | PASS
2026-10-05 | Sergio Manzo | Siemens | linkedin.com/in/sergio-ricardez-manzo | "Marketing Video Studio Production Manager, Siemens, Oct 2023 - Present" | PASS
2026-10-05 | Natascha Ladstaetter | Siemens Energy | linkedin.com/in/nataschaladstaetter | "Marketing Manager, Siemens Energy, Oct 2023 - Present, Linz" | PASS
2026-10-05 | Bleu Hayes | Tennessee Valley Authority | linkedin.com/in/bleuhayes | "Video Producer, Tennessee Valley Authority, Mar 2017 - Present" | PASS
2026-10-05 | Mito Habe-Evans | NPR | linkedin.com/in/mitohabeevans | "Creative Director/Supervising Producer, NPR Video, Jan 2018 - Present" | PASS
2026-10-05 | Ariana Lilligren | Smithsonian Institution | linkedin.com/in/ariana-lilligren-30740a48 | "Head of Production, Smithsonian Institution, May 2022 - Present: oversees Smithsonian Exhibits production shops (fabrication, mount making, 3D printing)" | PASS on employment, WRONG FIT (physical exhibits, not video) - draft left NOT READY, needs a video contact
2026-10-05 | Jesse Hill | YETI | linkedin.com/in/jessenicholashill | "Manager, Content Production, YETI, Nov 2021 - Present" | PASS
2026-10-05 | Eleanor Scott | Toast | linkedin.com/in/eleanor-scott | "International Content Marketing Manager, Toast, Nov 2024 - Present, London" | PASS
2026-10-05 | Taylor Erin | Instacart | linkedin.com/in/taylor-erin-11b53921 | "Executive Creative Director / Head of Creative, Instacart, Jan 2024 - Present" | PASS
2026-10-05 | Cameron Aspinwall | lululemon | linkedin.com/in/cameron-aspinwall-700715b2 | "Producer, Global Brand Creative, lululemon (Contract), May 2026 - Present" | PASS
2026-10-05 | Jose Monrabal | ABB | linkedin.com/in/jimonrabal | "Head of Global Brand Communications, ABB, Jun 2021 - Present, Zurich" | PASS
2026-10-05 | Jen Vladimirsky | Robinhood | linkedin.com/in/jenvladimirsky | "Creative Producer, Robinhood, Apr 2025 - Present" | PASS
2026-10-05 | Kelly Bonner | SoFi | linkedin.com/in/kellyannebonner | "Creative Director, SoFi, Mar 2025 - Present" | PASS
2026-10-05 | Hannah Brozek | Gong | linkedin.com/in/hannahbrozek | "Senior Content Marketing Manager, Gong, Aug 2025 - Present" | PASS
2026-10-05 | Carter Elkin-Paris | UiPath | linkedin.com/in/carterep | "Senior Producer, Global Brand Studio, UiPath, Nov 2018 - Present" | PASS
2026-10-05 | Andrew Linsk | Psyop | linkedin.com/in/andrew-linsk-04bb95 | "Executive Producer, Psyop, Jan 2018 - Present" | PASS

API test 2026-10-05 (cloud_check.py, desktop, ZenRows; Bright Data returned 502 for that batch): 16/16 PASS on company, matching the live-page checks above; control Lauren Jackson (Nat Geo role ended per Apollo) = HIDDEN, correctly not passed. Spencer approved API clearing 2026-10-05.
API lines use: `date | Name | Company | URL | "public profile company: X (source)" | API-PASS / API-MISMATCH / API-HIDDEN`
2026-10-05 | Amanda Baumgart | National Geographic | linkedin.com/in/amanda-baumgart-3b5a697 | "Production Manager, National Geographic & Disney CreativeWorks, Apr 2022 - Present (branded content + social video campaigns)" | PASS
2026-10-05 | Brett Reinke | National Geographic | linkedin.com/in/brett-reinke-a73581125 | "Post Production Supervisor, National Geographic Partners" (no dates shown) | PASS (backup)
2026-10-05 | Jonathan Ray | Smithsonian Institution | linkedin.com/in/jonathan-m-ray | "Producer Webcast, Smithsonian, Aug 2023 - Present (producer, sound engineer, video/audio editor)" | PASS
2026-10-05 | Emily Frost | Smithsonian Institution | linkedin.com/in/emily-frost-1b27a19 | "Web and Digital Content Producer, Smithsonian, Feb 2023 - Present" | PASS (backup)
2026-10-06 | Steven Watson | Airwallex | linkedin.com/in/stevenwatson3 | "public profile company: Airwallex (brightdata)" | API-PASS
2026-10-06 | Sue Funke | Absorb Software | linkedin.com/in/thesuefunke | "Senior Brand Marketing Manager, Absorb Software, Feb 2025 - Present (leads video production)" | PASS
2026-10-06 | Marta Lisboa | 360Learning | linkedin.com/in/martalisboa | "Creative Director, 360Learning, May 2026 - Present, Paris" | PASS
2026-10-06 | Heather Mounsey | Plaid | linkedin.com/in/heathermounsey | "Head of Brand and Creative, Plaid, Jan 2024 - Present" | PASS
2026-10-06 | Martijn Savenije | Booking.com | linkedin.com/in/martijnsavenije | "Senior Manager Content Studio, Booking.com, Oct 2025 - Present (headline: Head of Content Studio)" | PASS
2026-10-06 | Liv Moloney | The Economist | linkedin.com/in/livmoloney | "Head of Video, The Economist, Feb 2024 - Present" | PASS
2026-10-06 | Anne Gaynor | Peloton Interactive | linkedin.com/in/anne-marie-gaynor-a1bb9928 | "Senior Executive Producer, Peloton Interactive, Aug 2021 - Present" | PASS
2026-10-06 | Maggie Wasserman | Garmin | linkedin.com/in/maggie-wasserman | "Global Executive Producer, Garmin International, 2017 - Present" | PASS
2026-10-06 | Jordan Howes | BUCK | linkedin.com/in/jordan-howes-7094b347 | "Head of Production, BUCK, Oct 2023 - Present, Sydney" | PASS
2026-10-06 | Constanza Gallardo | Pushkin Industries | linkedin.com/in/constanzagp | "Head of Production & Executive Producer, Pushkin Industries, Aug 2025 - Present" | PASS
2026-10-07 | Sarah Karlan | Airbnb | linkedin.com/in/sarah-karlan-8aa438102 | top card "Creative for hire, currently @airbnb", company Airbnb | PASS
2026-10-07 | Jessica Liu | Cloudflare | linkedin.com/in/jessica-jliu | "Video Production Manager @ Cloudflare", Amsterdam | PASS
2026-10-07 | Thao Ngo | Litmos | linkedin.com/in/thaongo | top card company Litmos | PASS
2026-10-07 | Kevin Kartono | Vyond | linkedin.com/in/kevin-adiyanto-kartono-4a0831130 | "Senior Video Producer at Vyond" | PASS
2026-10-07 | Olivia Mitchell | Go1 | linkedin.com/in/olivia-mitchell-mktg | "Content Marketing Manager At Go1" | PASS
2026-10-07 | Manny Gonzalez | Docebo | linkedin.com/in/mannygonzalez | "Sr. Creative Director @ Docebo" | PASS
2026-10-07 | Matthew Hyland | Cornerstone OnDemand | linkedin.com/in/matthew-hyland | top card company Cornerstone OnDemand | PASS
2026-10-07 | Sara Heegaard | Articulate | linkedin.com/in/saraheegaard | "Senior Content Marketing Manager at Articulate" | PASS
2026-10-07 | Daniel Yoo | Confluent | linkedin.com/in/danielyoomedia | experience: "Senior Creative Producer, Confluent, Sep 2024 - Apr 2026" (linkedin.com/in/danyoo is a different person) | LEFT - To cleared, backup Marissa Schneider pending Spencer
2026-10-07 | Jesse Holden | Confluent | linkedin.com/in/jessejholden | experience "Director of Video, Confluent, Jan 2024 - Apr 2026" (Apollo still says current) | LEFT - not used
2026-10-07 | Caitlin Scholz | Confluent | linkedin.com/in/caitlin-scholz | experience "Brand Marketing Senior Content Manager, Confluent, Jun 2024 - Present" | PASS - new Confluent contact
2026-10-08 | Christina Harp | Brooks Running | linkedin.com/in/christinaharp | "URL on file (apollo)" | URL-ON-FILE
2026-10-08 | Daniel Szeto | Calm | linkedin.com/in/daniel-szeto-34272468 | "URL on file (apollo)" | URL-ON-FILE
2026-10-08 | Allison Straughan | Columbia Sportswear | linkedin.com/in/allison-straughan-12270332 | "URL on file (apollo)" | URL-ON-FILE
2026-10-08 | Max Dickson | Lonely Planet | linkedin.com/in/maxdickson3 | "URL on file (apollo)" | URL-ON-FILE
2026-10-08 | Ivana Milovanovic | Tripadvisor | linkedin.com/in/ivanamilovanovic | "URL on file (apollo)" | URL-ON-FILE
2026-10-08 | Naotaka Aogaki | Wilson Sporting Goods | linkedin.com/in/naotakaaogaki | "URL on file (apollo)" | URL-ON-FILE
2026-10-08 | Freddie Young | On | linkedin.com/in/freddieyoung | "URL on file (apollo)" | URL-ON-FILE
2026-10-08 | Tristan Ahern | Patagonia | linkedin.com/in/tristancimini | "URL on file (apollo)" | URL-ON-FILE
2026-10-08 | Paul Jun | Ramp | linkedin.com/in/paul-jun-3544a167 | "URL on file (apollo)" | URL-ON-FILE
2026-10-08 | Christina Harp | Brooks Running | linkedin.com/in/christinaharp | "public profile company: Brooks Running (zenrows)" | API-PASS
2026-10-08 | Daniel Szeto | Calm | linkedin.com/in/daniel-szeto-34272468 | "public profile company: Calm (zenrows)" | API-PASS
2026-10-08 | Allison Straughan | Columbia Sportswear | linkedin.com/in/allison-straughan-12270332 | "public profile company: Columbia Sportswear Company (zenrows)" | API-PASS
2026-10-08 | Max Dickson | Lonely Planet | linkedin.com/in/maxdickson3 | "public profile company: Lonely Planet (zenrows)" | API-PASS
2026-10-08 | Ivana Milovanovic | Tripadvisor | linkedin.com/in/ivanamilovanovic | "no public company shown" | API-HIDDEN
2026-10-08 | Naotaka Aogaki | Wilson Sporting Goods | linkedin.com/in/naotakaaogaki | "public profile company: Wilson Sporting Goods Co. (zenrows)" | API-PASS
2026-10-08 | Freddie Young | On | linkedin.com/in/freddieyoung | "public profile company: On (zenrows)" | API-PASS
2026-10-08 | Tristan Ahern | Patagonia | linkedin.com/in/tristancimini | "public profile company: Patagonia (zenrows)" | API-PASS
2026-10-08 | Paul Jun | Ramp | linkedin.com/in/paul-jun-3544a167 | "public profile company: Ramp (zenrows)" | API-PASS
2026-10-09 | Ivana Milovanovic | Tripadvisor | linkedin.com/in/ivanamilovanovic | "no public company shown" | API-HIDDEN
