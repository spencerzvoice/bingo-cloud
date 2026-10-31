#!/usr/bin/env python
"""Monthly rollover for Bingo's living log files (Spencer, 2026-10-31, after comparing systems with G).

Keeps the big run logs small enough for phone sessions and cloud routines to read whole, without losing
anything: old material moves, byte for byte, into an archive file next to the live one.

Per file:
  memory/followups-queue.md                      sections (## headings) dated older than KEEP_DAYS -> memory/archive/followups-queue-YYYY-MM.md
                                                 state sections (PARKED, Cadence rules, Schedule ledger, Upcoming, Flagged) always stay.
  memory/outreach-log.md                         dated sections older than KEEP_DAYS -> memory/archive/outreach-log-YYYY-MM.md
  reference/client-acquisition/FUNNEL-COHORTS.md ONLY run-log sections (Lead Batch run / Hook Sweep run / Pitch-queue count) older than
                                                 KEEP_DAYS -> reference/client-acquisition/archive/FUNNEL-COHORTS-runs-YYYY-MM.md.
                                                 Funnel sections (A..S2, the drafting order) always stay.
  reference/client-acquisition/VIDEO-PICKS.md    Log table: one row per client stays (the latest verdict); superseded rows ->
                                                 reference/client-acquisition/archive/VIDEO-PICKS-superseded.md. Rules/patterns stay.

Every live file gets a status block right under its title (In short / Status / Last updated / Open to-dos), which
sessions read first. The "Open to-dos" line is kept as sessions left it.

Usage:  python scripts/rollover.py [--dry-run] [--keep-days 30]
Safe: asserts that live lines + archived lines == original lines for every file before writing anything.
Writes local/last-rollover.txt (YYYY-MM) when it runs for real.
"""
import argparse
import datetime as dt
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = dt.date.today()
DATE_RE = re.compile(r"(20\d\d)-(\d\d)-(\d\d)")
STATUS_START = "<!-- status-block:start -->"
STATUS_END = "<!-- status-block:end -->"

FILES = [
    dict(
        path="memory/followups-queue.md",
        mode="sections",
        archive="memory/archive/followups-queue-{ym}.md",
        keep_headings=re.compile(r"^## (PARKED|Cadence rules|Schedule ledger|Upcoming|Flagged)", re.I),
        in_short="The follow-up schedule ledger (PARKED list, cadence rules, reminder dates per cohort) plus the dated run log of every "
                 "prep / remind / send pass. Cold touches 2/3 are sent offline from the Follow-up Queue Sheet; this file is the "
                 "record and the schedule, not the queue. Maintained by the `followup-drafts` skill, the Digest and Follow-up Prep.",
    ),
    dict(
        path="memory/outreach-log.md",
        mode="sections",
        archive="memory/archive/outreach-log-{ym}.md",
        keep_headings=None,
        in_short="One dated entry per outreach action (drafted, scheduled, sent, replied, bounced, dropped), newest at the bottom. "
                 "Gmail is the source of truth; this is the narrative record the Digest and Weekly Check-in read.",
    ),
    dict(
        path="reference/client-acquisition/FUNNEL-COHORTS.md",
        mode="sections",
        archive="reference/client-acquisition/archive/FUNNEL-COHORTS-runs-{ym}.md",
        only_headings=re.compile(r"^## .*(Lead Batch run|Hook Sweep run|Pitch-queue count)", re.I),
        in_short="The canonical funnel letters (A..S2): who is in each send cohort, its status, the DRAFTING ORDER, and the "
                 "reserved YouTube-channel funnels (S, S1, S2). Routine run logs (Lead Batch, Hook Sweep, queue counts) sit at "
                 "the bottom and roll into archive/ after 30 days.",
    ),
    dict(
        path="reference/client-acquisition/VIDEO-PICKS.md",
        mode="table-latest-per-client",
        archive="reference/client-acquisition/archive/VIDEO-PICKS-superseded.md",
        in_short="Spencer's hard rules and the good/bad patterns for picking a re-voice source video, then a Log with ONE row per "
                 "client: its current verdict (built / NO GOOD MATCH / swap). Earlier verdicts for the same client live in "
                 "archive/VIDEO-PICKS-superseded.md. Read the rules and patterns before any pick; read a client's row before "
                 "re-checking it.",
    ),
]


def read(p):
    with io.open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read().split("\n")


def write(p, lines):
    full = os.path.join(ROOT, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with io.open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def append(p, header_lines, body_lines):
    full = os.path.join(ROOT, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    new = not os.path.exists(full)
    with io.open(full, "a", encoding="utf-8", newline="\n") as f:
        if new:
            f.write("\n".join(header_lines) + "\n")
        f.write("\n".join(body_lines) + "\n")


def split_status(lines):
    """Return (title_lines, existing_status_lines or None, rest)."""
    if not lines or not lines[0].startswith("# "):
        return [], None, lines
    title = [lines[0]]
    rest = lines[1:]
    if rest and rest[0] == STATUS_START:
        end = rest.index(STATUS_END)
        return title, rest[: end + 1], rest[end + 1:]
    return title, None, rest


def build_status(spec, status_line, old_status):
    todo = "> **Open to-dos:** none logged here (live actions live in the Follow-up Queue Sheet, the tracker and Gmail Drafts)."
    if old_status:
        for l in old_status:
            if l.startswith("> **Open to-dos:**"):
                todo = l
    return [
        STATUS_START,
        "> **In short:** " + spec["in_short"],
        "> **Status:** " + status_line,
        "> **Last updated:** %s (rollover). Sessions append below as before; this block is refreshed by `scripts/rollover.py`." % TODAY.isoformat(),
        todo,
        STATUS_END,
        "",
    ]


def section_date(heading):
    m = DATE_RE.search(heading)
    if not m:
        return None
    try:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def roll_sections(spec, lines, keep_days):
    title, old_status, body = split_status(lines)
    cutoff = TODAY - dt.timedelta(days=keep_days)
    # split body into preamble + sections at "## " headings
    idx = [i for i, l in enumerate(body) if l.startswith("## ")]
    pre = body[: idx[0]] if idx else body
    sections = []
    for n, i in enumerate(idx):
        j = idx[n + 1] if n + 1 < len(idx) else len(body)
        sections.append(body[i:j])
    live, archived = [], {}
    dates = []
    for sec in sections:
        h = sec[0]
        d = section_date(h)
        keep = True
        if spec.get("only_headings") and not spec["only_headings"].search(h):
            keep = True
        elif spec.get("keep_headings") and spec["keep_headings"].search(h):
            keep = True
        elif d is None:
            keep = True
        elif d < cutoff:
            keep = False
        if keep:
            live.append(sec)
            if d:
                dates.append(d)
        else:
            archived.setdefault(d.strftime("%Y-%m"), []).append(sec)
    live_lines = [l for s in live for l in s]
    n_arch = sum(len(v) for v in archived.values())
    span = ("%s to %s" % (min(dates).isoformat(), max(dates).isoformat())) if dates else "no dated sections"
    adir = os.path.dirname(spec["archive"])
    status = "%d live sections (%s); %d archived this run to `%s/` (sections older than %d days roll over monthly)." % (
        len(live), span, n_arch, adir, keep_days)
    new_lines = title + build_status(spec, status, old_status) + pre + live_lines
    return new_lines, archived, (len(pre) + sum(len(s) for s in sections), len(pre) + len(live_lines), n_arch and sum(len(l) for v in archived.values() for l in v))


def roll_table(spec, lines):
    title, old_status, body = split_status(lines)
    # Log table = rows starting with "| 20" after the "## Log" heading
    try:
        log_i = next(i for i, l in enumerate(body) if l.strip().lower() == "## log")
    except StopIteration:
        raise SystemExit("VIDEO-PICKS: no '## Log' heading")
    head = body[: log_i + 1]
    rest = body[log_i + 1:]
    tbl_hdr = [l for l in rest[:3] if l.startswith("|") and not re.match(r"^\| 20\d\d-", l)]
    rows = [l for l in rest if re.match(r"^\| 20\d\d-", l)]
    others = [l for l in rest if l not in tbl_hdr and not re.match(r"^\| 20\d\d-", l)]
    latest = {}
    for i, r in enumerate(rows):
        cells = [c.strip() for c in r.split("|")]
        key = re.sub(r"\s+", " ", cells[2]).lower() if len(cells) > 2 else r
        latest[key] = i  # later row wins (rows are appended chronologically)
    keep_idx = set(latest.values())
    live_rows = [r for i, r in enumerate(rows) if i in keep_idx]
    sup_rows = [r for i, r in enumerate(rows) if i not in keep_idx]
    status = "%d live rows, one per client; %d superseded rows moved this run to `%s`." % (
        len(live_rows), len(sup_rows), spec["archive"])
    new_lines = title + build_status(spec, status, old_status) + head + tbl_hdr + live_rows + others
    return new_lines, tbl_hdr, sup_rows, (len(body), len(head) + len(tbl_hdr) + len(live_rows) + len(others), len(sup_rows))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--keep-days", type=int, default=30)
    a = ap.parse_args()
    report = []
    for spec in FILES:
        lines = read(spec["path"])
        title = lines[0] if lines else "# " + os.path.basename(spec["path"])
        if spec["mode"] == "sections":
            new_lines, archived, (orig, live, arch) = roll_sections(spec, lines, a.keep_days)
            assert orig == live + arch, (spec["path"], orig, live, arch)
            report.append("%s: %d lines -> %d live, %d archived" % (spec["path"], orig, live, arch))
            if not a.dry_run:
                for ym, secs in sorted(archived.items()):
                    body = [l for s in secs for l in s]
                    append(spec["archive"].format(ym=ym),
                           [title + " - archive " + ym, "", "> Rolled over from `%s` by `scripts/rollover.py`. Read-only history; the live file keeps the last 30 days." % spec["path"], ""],
                           body)
                write(spec["path"], new_lines)
        else:
            new_lines, tbl_hdr, sup_rows, (orig, live, arch) = roll_table(spec, lines)
            assert orig == live + arch, (spec["path"], orig, live, arch)
            report.append("%s: %d body lines -> %d live, %d superseded rows archived" % (spec["path"], orig, live, arch))
            if not a.dry_run and sup_rows:
                append(spec["archive"],
                       [title + " - superseded verdicts", "", "> Earlier rows for clients that have a newer row in `%s`. Moved by `scripts/rollover.py`, nothing deleted." % spec["path"], ""] + tbl_hdr,
                       sup_rows)
                write(spec["path"], new_lines)
            elif not a.dry_run:
                write(spec["path"], new_lines)
    if not a.dry_run:
        os.makedirs(os.path.join(ROOT, "local"), exist_ok=True)
        with io.open(os.path.join(ROOT, "local", "last-rollover.txt"), "w", encoding="utf-8") as f:
            f.write(TODAY.strftime("%Y-%m") + "\n")
    print(("DRY RUN\n" if a.dry_run else "") + "\n".join(report))


if __name__ == "__main__":
    main()
