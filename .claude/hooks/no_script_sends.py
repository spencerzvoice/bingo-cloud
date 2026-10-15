# No email sends from scripts. Spencer, 2026-10-15, after 11 follow-ups were sent at 4-7am local by a script
# using a temporary FGAC key: a script call skips every Gmail hook (send window, pitch QC, queue cap).
# Every send goes through FGAC google_api_modify, where send_window_guard.py checks the recipient's local time.
#
# PreToolUse on Bash / PowerShell: block when the command, or a script file it runs (.py .sh .ps1 .js .mjs .ts),
# contains a Gmail send endpoint (messages/send, drafts/send) AND an HTTP client (urllib, requests, httpx, curl,
# wget, fetch, Invoke-RestMethod, Invoke-WebRequest). Reading or grepping for the text is fine.
import json, os, re, sys

SEND = re.compile(r"(messages|drafts)/send\b")
HTTP = re.compile(r"urllib|requests\.|httpx|http\.client|\bcurl\b|\bwget\b|\bfetch\(|Invoke-RestMethod|Invoke-WebRequest|\birm\b|\biwr\b", re.I)
EXT = re.compile(r"""["']?([^\s"'|;&<>]+\.(?:py|sh|ps1|js|mjs|ts))["']?""", re.I)

data = json.load(sys.stdin)
if data.get("hook_event_name") != "PreToolUse":
    sys.exit(0)
cmd = str((data.get("tool_input") or {}).get("command", ""))
cwd = data.get("cwd") or os.getcwd()
sources = [cmd]
for m in EXT.finditer(cmd):
    p = os.path.expanduser(m.group(1))
    for cand in (p, os.path.join(cwd, p)):
        try:
            if os.path.isfile(cand):
                sources.append(open(cand, encoding="utf-8", errors="ignore").read())
                break
        except Exception:
            pass
for s in sources:
    if SEND.search(s) and HTTP.search(s):
        sys.stderr.write(
            "BLOCKED by no_script_sends: this would send email from a script, which skips the send-window guard "
            "(Spencer, 2026-10-15: nothing lands before 8:32AM or after 3PM local). Send each email with FGAC "
            "google_api_modify (gmail/v1/users/me/drafts/send or messages/send) so the guard checks it, or schedule it.\n")
        sys.exit(2)
sys.exit(0)
