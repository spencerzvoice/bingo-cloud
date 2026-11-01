"""HHM revenue history by month.

Joins the public video list (memory/hhm-videos-2026-10-31.txt: id|views|duration|approx_date|title)
with real upload dates the desktop pulls (dates file: one `id,YYYYMMDD` per line) and prints
uploads, lifetime views and an ad-revenue band per upload month.

Usage:
  python scripts/hhm_monthly.py memory/hhm-videos-2026-10-31.txt memory/hhm-upload-dates.csv [out.md]

RPM band = AIR Media-Tech Entertainment P25 / median / P75 (May 2025-May 2026, Studio data):
$0.88 / $2.43 / $5.02 per 1,000 views. Views are lifetime, so a month's figure is what that
month's uploads have earned to date, not cash received in that month.
"""
import collections
import sys

RPM = (0.88, 2.43, 5.02)


def main():
    vids_path, dates_path = sys.argv[1], sys.argv[2]
    out_path = sys.argv[3] if len(sys.argv) > 3 else None
    dates = {}
    for line in open(dates_path, encoding="utf8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        vid, d = [x.strip() for x in line.split(",")[:2]]
        if len(d) == 8 and d.isdigit():
            dates[vid] = d
    rows = []
    missing = 0
    for line in open(vids_path, encoding="utf8"):
        p = line.rstrip("\n").split("|", 4)
        if len(p) < 5:
            continue
        vid, views, dur, approx, title = p
        d = dates.get(vid)
        if not d:
            missing += 1
            d = approx  # year-level fallback, flagged below
        rows.append((d, vid in dates, int(views or 0), title))
    by = collections.defaultdict(lambda: [0, 0, 0])
    for d, real, v, _ in rows:
        k = d[:4] + "-" + d[4:6]
        by[k][0] += 1
        by[k][1] += v
        by[k][2] += 0 if real else 1
    lines = ["| Month | Uploads | Lifetime views | Ad rev low | mid | high | approx-dated |",
             "|---|---|---|---|---|---|---|"]
    tot = 0
    peak = ("", 0)
    for k in sorted(by):
        n, v, ap = by[k]
        tot += v
        if v > peak[1]:
            peak = (k, v)
        lines.append(f"| {k} | {n} | {v:,} | ${v*RPM[0]/1000:,.0f} | ${v*RPM[1]/1000:,.0f} | ${v*RPM[2]/1000:,.0f} | {ap or ''} |")
    lines.append(f"| **Total** | {len(rows)} | {tot:,} | ${tot*RPM[0]/1000:,.0f} | ${tot*RPM[1]/1000:,.0f} | ${tot*RPM[2]/1000:,.0f} | {missing} |")
    lines.append("")
    lines.append(f"Peak upload month by lifetime views: {peak[0]} ({peak[1]:,} views -> "
                 f"${peak[1]*RPM[0]/1000:,.0f} / ${peak[1]*RPM[1]/1000:,.0f} / ${peak[1]*RPM[2]/1000:,.0f}).")
    lines.append(f"Videos without a real upload date (year-level only): {missing}.")
    text = "\n".join(lines)
    print(text)
    if out_path:
        open(out_path, "w", encoding="utf8").write(text + "\n")


if __name__ == "__main__":
    main()
