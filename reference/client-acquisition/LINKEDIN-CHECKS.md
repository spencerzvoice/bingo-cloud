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
