"""Upload the rendered digest to Gmail as a draft, so the routine never has to copy the raw by hand.

Why (2026-10-19): the routine used to paste the whole local/digest-<date>.raw (~20-40 KB of base64) into one
FGAC call. On 10-19 the raw was 28.8 KB, the run judged it "too large to relay by hand" and sent plain text.
Now the bytes go up from this script and the routine sends the draft by its id: a call of ~30 characters,
whatever the digest's size. The send itself still goes through FGAC google_api_modify, so the send hooks see it.

Usage: set K to a FGAC temporary API key (create_temporary_api_key), then
    python scripts/digest_upload.py local/digest-<date>.raw
Prints: DRAFT_ID=<id> THREAD_ID=<threadId>. Exits non-zero on any error.
Only ever addressed to Spencer's own mailbox (the renderer sets To), and this script refuses anything else.
"""
import base64, email, json, os, sys, urllib.request
from email import policy

K = os.environ["K"]
B = "https://fgac.ai/api/proxy/gmail/v1/users/me/"
SELF = {"spencer@spencerzvoice.com"}

raw = open(sys.argv[1], encoding="ascii").read().strip()
msg = email.message_from_bytes(base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4)), policy=policy.default)
to = {a.addr_spec.lower() for a in msg["To"].addresses} if msg["To"] else set()
if not to or not to <= SELF or msg["Cc"] or msg["Bcc"]:
    sys.exit(f"REFUSED: digest drafts go to spencer@spencerzvoice.com only, got To={sorted(to)}")
if not str(msg["Subject"]).startswith("VO Pipeline Digest"):
    sys.exit("REFUSED: not a digest (subject must start 'VO Pipeline Digest')")

req = urllib.request.Request(
    B + "drafts", data=json.dumps({"message": {"raw": raw}}).encode(), method="POST",
    headers={"Authorization": "Bearer " + K, "Content-Type": "application/json"})
d = json.load(urllib.request.urlopen(req, timeout=60))
print(f"DRAFT_ID={d['id']} THREAD_ID={d['message']['threadId']}")
