"""Latest-video check (Spencer, 2026-10-13: "Finding the latest video is a part of the discovery. Write this into
your code, you don't need me to prompt you to find the latest video this is already a part of your task and your job.")

Why: the 10-08 latest-launch check and the 10-13 hook sweep both kept Confluent on "The 2025 Data Streaming Report"
while Confluent's newest upload (Oct 6, "Confluent X VCARB: Every Second Means Everything") was a narrated F1 spot,
i.e. both the best hook and the right re-voice. Nobody had listed the channel's newest uploads.

What it does: for every client in a funnel, reads the latest WINNER line in that funnel's `_candidates` doc, finds the
YouTube channel of the winning video, and lists EVERY upload on that channel that is newer than the winner (the uploads
tab is newest-first, so everything above the winner is newer). Those are the videos you must watch/judge before keeping
the pick or writing a hook. It doesn't decide for you: talking heads, music-only, webinars and >5 min videos still fail
the narrator rules (`narrator_check.py`, VIDEO-PICKS.md).

Usage: set K to a FGAC temporary API key (create_temporary_api_key, purpose bulk_calls), then
    python scripts/latest_video_check.py "Funnel I" [Client ...]
Exit code 0 always; read the report. Lines:
    CURRENT  <client>: winner is the channel's newest upload
    NEWER    <client>: N newer uploads -> each listed with id, duration, title (short ones flagged CHECK)
    BLOCKED  <client>: YouTube refused (cloud IP) -> desktop relay
    NO PICK  <client>: no WINNER line / not a YouTube URL
Run it in EVERY hook sweep and every re-voice pick (CLAUDE.md 5c, Morning Build Stage 1 step 2h, revoice-material Step 1).
"""
import json, os, re, shutil, subprocess, sys, urllib.parse, urllib.request

K = os.environ["K"]
API = "https://fgac.ai/api/proxy/"
MAXLIST = 120  # uploads to scan before giving up on finding the winner
SHORT = 240    # seconds; longer uploads are usually webinars/keynotes


def get(path, raw=False):
    r = urllib.request.urlopen(urllib.request.Request(API + path, headers={"Authorization": "Bearer " + K}))
    return r.read().decode("utf-8", "replace") if raw else json.load(r)


def drive_q(q):
    return get("drive/v3/files?fields=files(id,name)&q=" + urllib.parse.quote(q)).get("files", [])


def winners(funnel):
    f = drive_q(f"name='{funnel}' and mimeType='application/vnd.google-apps.folder' and trashed=false")
    if not f:
        sys.exit(f"no Drive folder named {funnel!r}")
    c = drive_q(f"name='_candidates' and '{f[0]['id']}' in parents and trashed=false")
    if not c:
        sys.exit(f"no _candidates doc in {funnel}")
    text = get(f"drive/v3/files/{c[0]['id']}/export?mimeType=text/plain", raw=True)
    out, client = {}, None
    for line in text.splitlines():
        m = re.match(r"##\s+(.+?)\s+\(Funnel", line.strip())
        if m:
            client = m.group(1)
        m = re.match(r"WINNER:\s*(.+?)\s+-\s+(https?://\S+)", line.strip())
        if m and client:
            out[client] = (m.group(1), m.group(2))  # later lines win = latest WINNER
    return out


def ytdlp(*args):
    exe = [sys.executable, "-m", "yt_dlp", "--no-warnings"]
    if shutil.which("node") and not shutil.which("deno"):
        exe += ["--js-runtimes", "node"]
    r = subprocess.run(exe + list(args), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout, r.stderr


def vid_id(url):
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", url)
    return m.group(1) if m else None


def check(client, title, url):
    vid = vid_id(url)
    if not vid:
        return f"NO PICK  {client}: winner is not a YouTube video ({url})"
    rc, out, err = ytdlp("--skip-download", "--print", "%(channel_url)s|%(upload_date)s", url)
    if rc or not out.strip():
        return f"BLOCKED  {client}: could not read {url} ({err.strip()[-160:]})"
    chan, up = out.strip().splitlines()[-1].split("|")
    rc, out, err = ytdlp("--flat-playlist", "--playlist-end", str(MAXLIST), "--print", "%(id)s|%(duration)s|%(title)s", chan + "/videos")
    if rc or not out.strip():
        return f"BLOCKED  {client}: could not list {chan} ({err.strip()[-160:]})"
    rows = [l.split("|", 2) for l in out.strip().splitlines()]
    ids = [r[0] for r in rows]
    if vid not in ids:  # very old / Short / unlisted winner: every recent upload is newer, show the newest 20
        newer = rows[:20]
        head = (f"NEWER    {client}: winner \"{title}\" ({up}) is not in the channel's last {MAXLIST} uploads ({chan});"
                f" the newest 20 are listed")
    else:
        newer = rows[:ids.index(vid)]
        head = f"NEWER    {client}: {len(newer)} upload(s) newer than \"{title}\" ({up}) on {chan}"
    if not newer:
        return f"CURRENT  {client}: \"{title}\" ({up}) is the newest upload on {chan}"
    lines = [head]
    for i, d, t in newer:
        try:
            short = float(d) <= SHORT
        except ValueError:
            short = True
        lines.append(f"    {'CHECK' if short else 'long '} https://www.youtube.com/watch?v={i} | {d}s | {t}")
    return "\n".join(lines)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    funnel, only = sys.argv[1], set(sys.argv[2:])
    w = winners(funnel)
    if not w:
        print(f"no WINNER lines in {funnel}/_candidates")
    for client in sorted(w):
        if only and client not in only:
            continue
        print(check(client, *w[client]), flush=True)
    for client in sorted(only - set(w)):
        print(f"NO PICK  {client}: no WINNER line in {funnel}/_candidates")
    print("\nEvery CHECK line must be watched (frames + transcript) and judged before the pick is kept or a hook is"
          " written. Log the verdicts in VIDEO-PICKS.md.")


if __name__ == "__main__":
    main()
