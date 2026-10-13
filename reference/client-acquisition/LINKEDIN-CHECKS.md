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
2026-10-09 | Ivana Milovanovic | Tripadvisor | linkedin.com/in/ivanamilovanovic | "no public company shown (13:05 rerun)" | API-HIDDEN
2026-10-12 | Ivana Milovanovic | Tripadvisor | linkedin.com/in/ivanamilovanovic | "no public company shown (03:05 run)" | API-HIDDEN
2026-10-12 | Ivana Milovanovic | Tripadvisor | linkedin.com/in/ivanamilovanovic | "no public company shown (13:05 run)" | API-HIDDEN
2026-10-12 | Ivana Milovanovic | Tripadvisor | linkedin.com/in/ivanamilovanovic | "Executive Producer, Tripadvisor, Aug 2026 - Present (desktop Chrome, /details/experience/)" | PASS (NOT READY cleared 2026-10-12)
2026-10-13 | Karly Snajczuk | Ramp | linkedin.com/in/karly-snajczuk | "Lead Creative Producer at Ramp" (experience: Lead Creative Producer Oct 2026-Present; Senior Creative Producer Nov 2025-; desktop Chrome) | PASS
2026-10-13 | Cameron Robertson | Maersk | linkedin.com/in/cameronrobertson5 | "Senior Producer & Videographer, A.P. Moller - Maersk, Jan 2019 - Present (desktop Chrome, /details/experience/, pre-draft)" | PASS
2026-10-13 | Deepika Upadhyay | Schneider Electric | linkedin.com/in/deepika-upadhyay-31900b161 | "Web Content Producer, Schneider Electric, Nov 2016 - Present, Gurugram (desktop Chrome, pre-draft)" | PASS (weak title fit: web content, not video)
2026-10-13 | Raven Kenemer | HashiCorp (IBM) | linkedin.com/in/ravenbrajdic | "Senior Product Marketing Manager, Content Strategy, IBM, Jan 2026 - Present + Senior Editorial and Content Manager, HashiCorp, Sep 2024 - Present (desktop Chrome, pre-draft)" | PASS (content strategy, not video)
2026-10-13 | Jack Headley | Autodesk | linkedin.com/in/jack-headley | "Senior Video Producer, Autodesk, Jul 2025 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Alice Monnet | Celonis | linkedin.com/in/alicemonnet | "Lead Video Producer, Celonis, Oct 2026 - Present (Senior Video Producer Sep 2025-) (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Matthew Moresco | Docusign | linkedin.com/in/matthew-moresco-38780239 | "Video Producer/Editor, Docusign, Sep 2025 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Jonathan Lopez | Justworks | linkedin.com/in/iamjonathanlopez | "Video Producer & Editor, Justworks, Dec 2023 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Karim El-Sayed | Klaviyo | linkedin.com/in/karimaudiovideo | "Principal Video Producer, Klaviyo, Sep 2024 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Reed Jones | Okta | linkedin.com/in/reed-jones | "Keynote Producer, Okta, May 2026 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Andrew Wilson | Personio | linkedin.com/in/andrew-wilson-1189a231 | "Senior Video Producer, Personio, Oct 2026 - Present (Video Producer May 2023-) (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Yichun Hsieh | Elastic | linkedin.com/in/yichun-hsieh-bb06935 | "Creative Director, Elastic, Nov 2021 - Jun 2026 (ended; no current Elastic role) (desktop Chrome)" | LEFT (not drafted; Elastic -> Shelby Khan)
2026-10-13 | Shelby Khan | Elastic | linkedin.com/in/shelbykhan | "Senior Director of Brand and Creative, Elastic, May 2026 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Adam Mittner | GitLab | linkedin.com/in/adammittner | "Sr. Director of Brand Creative, GitLab, Apr 2026 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Mitch Rymeski | Harness | linkedin.com/in/mitch-rymeski-49757826 | "Creative Director, Harness, May 2026 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Alex Gauermann | JetBrains | linkedin.com/in/alex-gauermann-a98751131 | "Broadcast Engineer / Video Producer, JetBrains, Aug 2023 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Jamal Farley | LaunchDarkly | linkedin.com/in/jamalfarley | "Senior Video Producer, LaunchDarkly, Sep 2026 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Pablo Zubieta | MongoDB | linkedin.com/in/pablo-zubieta | "Senior Video Producer, MongoDB, Feb 2025 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Colin Goheen | Postman | linkedin.com/in/colin-goheen | "Head of Video, Postman, Feb 2025 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Riley West | Twilio | linkedin.com/in/riley-west | "Senior Creative Producer, Twilio Inc., Mar 2021 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Eddie Russell | Unity | linkedin.com/in/eddie-russell-996572109 | "Manager, Content Production (Professional Training team), Unity, Apr 2024 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Moe Hung | New Relic | linkedin.com/in/moe-hung-559a463b | "Lead Brand Designer, New Relic, Sep 2026 - Present (was Creative Director Jul 2024 - Sep 2026) (desktop Chrome, pre-draft)" | PASS (current at New Relic; title changed to brand design)
2026-10-13 | Janssen Weeks | Qualtrics | linkedin.com/in/janssenweeks | "Head Of Production + Executive Producer, Qualtrics, Jun 2022 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Daniel Koga | ServiceNow | linkedin.com/in/daniel-koga-471bab8 | "Producer / Sr. Program Manager - Global Brand Film & Video, ServiceNow, Mar 2017 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Joe Gagliardi | ServiceNow | linkedin.com/in/joegagliardi | "Executive Video Producer, ServiceNow, Dec 2024 - Present" | PASS (email unknown, not drafted)
2026-10-13 | Jess Peterson | Shopify | linkedin.com/in/jessjpeterson | "Executive Producer, Brand Studio Video, Shopify, Jun 2025 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Jim Johnson | Workday | linkedin.com/in/jimjohnsonjimsbookdotcom | "sr. executive producer, Workday Studios, Oct 2012 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Liz Colanto | Pegasystems | linkedin.com/in/liz-colanto11 | "Head of Post, Lead Video Editor, Pegasystems, May 2024 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Georgina Lipovac | Anaplan | linkedin.com/in/georginabrown1 | "Senior Creative Director, Anaplan, Jul 2026 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Pete Anderson | Freshworks | linkedin.com/in/pete-anderson-a689106 | "Global Video Lead, Freshworks, Aug 2022 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Gus Teixeira | Darktrace | linkedin.com/in/gteixeira-d | "Video Producer, Darktrace, Dec 2024 - Present" | PASS (email catch-all, not drafted)
2026-10-13 | Kevin Ginosian | Darktrace | linkedin.com/in/kvginosian | "Senior Manager Content Strategy, Orca Security, Sep 2026 - Present" | LEFT
2026-10-13 | Ryan Catlett | Darktrace | linkedin.com/in/ryancatlett | "Senior Creative Director, Darktrace, Feb 2024 - Present" | PASS (email catch-all, not drafted)
2026-10-13 | Garrett Goeckner | EC-Council | linkedin.com/in/garrett-goeckner-24a956b9 | "Video Producer, EC-Council, Feb 2018 - Present" | PASS (email unknown, not drafted)
2026-10-13 | Swati Salian | EC-Council | linkedin.com/in/swati-salian | "Content Manager, EC-Council, Jun 2021 - Oct 2026 (ended)" | LEFT
2026-10-13 | Tanya Mukundan | EC-Council | linkedin.com/in/tanyamukundan | "Assistant Director - Marketing, EC-Council, Sep 2025 - Present (desktop Chrome, pre-draft)" | PASS
2026-10-13 | Ashish Verma | EC-Council | linkedin.com/in/motiondesignbyash | "Video and Motion Content Designer, Skysun, Mar 2026 - Aug 2026 (no current EC-Council role shown)" | LEFT
