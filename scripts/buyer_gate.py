"""Buyer gate (Spencer, 2026-10-26, after Maersk: "Tell me why we reached out to the wrong person").

Cause: on 10-13 both researched Maersk targets had dead emails, so the build pitched the first video-titled person
with a valid email: Cameron Robertson, Senior Producer & Videographer. He works there (every gate passed) but he
doesn't hire voice talent; Maersk's in-house video mostly uses interviewee voices and the brand films go through
outside production companies, so the buyer was Sam Poulter, Global Head of Marketing & Branding. The employment gate
only asks "do they work there". This gate asks "do they hire VO".

Every new-client pitch recipient needs a PASS row in reference/client-acquisition/BUYER-GATE.json before a draft is
created or edited; .claude/hooks/buyer_gate_guard.py blocks the draft otherwise.

Usage:
  python scripts/buyer_gate.py check "<title>" [--company-type inhouse|studio|agency] [--practice ...]
  python scripts/buyer_gate.py record <email> "<Name>" "<Company>" "<title>" --company-type inhouse|studio|agency
        --practice in-house-vo|agency|interviewee|unknown --source "<where the title was read, today>"
        [--evidence "<why this person hires VO / who more senior was checked>"]
  python scripts/buyer_gate.py keep <email> "<Spencer's words, date>"     (Spencer's own call overrides a FAIL)
  python scripts/buyer_gate.py show <email>

Verdicts:
  PASS           decision-maker title (head / director / VP / chief / EP / creative director / production manager)
  PASS-EVIDENCE  a producer-level title with written evidence they commission talent (see REVIEW)
  REVIEW         a producer or marketing-manager title: passes only with --evidence (they booked VO before, they are
                 the senior-most video owner and you name who you checked, or they are a producer at a studio/agency,
                 where producers cast talent)
  FAIL           crew or adjacent roles (videographer, editor, designer, keynote/event/web producer, content strategy,
                 product marketing, coordinator...). Never fall back to one: go up the org (LinkedIn People tab,
                 theorg.com), take the buyer's email through Apollo, or mark the company BLOCKED.
  KEEP-SPENCER   Spencer chose to pitch this person anyway (his words recorded).
Company practice: when research says the brand films are agency-made or the in-house video uses interviewee/on-camera
voices, the video team is not the door. Only brand/marketing leadership (or the agency) passes.
"""
import argparse, datetime, json, os, re, sys

LEDGER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "client-acquisition", "BUYER-GATE.json")

# Order matters: buyer words win over crew words ("Head of Post, Lead Video Editor" = a buyer).
BUYER = [
    r"\bhead of\b", r"\bheads?\b(?= ?(of|,))", r"\bdirector\b", r"\bvp\b", r"\bvice president\b", r"\bchief\b",
    r"\bcmo\b", r"\bceo\b", r"\bfounder\b", r"\bco-founder\b", r"\bowner\b", r"\bpartner\b", r"\bmanaging director\b",
    r"\bexecutive producer\b", r"\bexec(utive)? producer\b", r"\bep\b", r"\bproduction manager\b",
    r"\bmanager,? (video|content|creative|studio|post)[ -]?production\b", r"\bvideo production manager\b",
    r"\bpost[- ]production manager\b", r"\bstudio (lead|manager)\b", r"\bhead\b",
]
BRAND_LEAD = [r"\b(head|director|vp|chief|cmo|vice president)\b.*\b(brand|marketing|creative|communications)\b",
              r"\b(brand|marketing|creative|communications)\b.*\b(head|director|vp|chief|lead)\b", r"\bcmo\b",
              r"\bcreative director\b"]
CREW = [
    r"videographer", r"\beditor\b", r"\bediting\b", r"motion", r"animator", r"\bdesigner\b", r"camera", r"\bdp\b",
    r"cinematographer", r"photographer", r"colou?rist", r"engineer", r"keynote", r"\bevent", r"web content",
    r"content strateg", r"product marketing", r"\bpmm\b", r"social", r"coordinator", r"assistant", r"\bintern\b",
    r"copywriter", r"specialist", r"\banalyst\b", r"webcast",
]
REVIEW = [r"producer", r"content marketing manager", r"brand marketing manager", r"marketing manager",
          r"content manager", r"creative lead", r"brand lead", r"video lead", r"content lead"]


def classify(title, company_type="inhouse", practice="unknown"):
    t = (title or "").lower().strip()
    if not t:
        return "FAIL", "no title on file: read it on their live LinkedIn first"
    has = lambda pats: next((p for p in pats if re.search(p, t)), None)
    buyer, crew, review = has(BUYER), has(CREW), has(REVIEW)
    if practice in ("agency", "interviewee"):
        if has(BRAND_LEAD):
            return "PASS", "brand/marketing lead, and this company's video goes through %s" % (
                "agencies" if practice == "agency" else "interviewee voices in-house")
        return "FAIL", ("company practice = %s: the in-house video team doesn't buy VO. Pitch the head of "
                        "brand/marketing (or the agency) instead" % practice)
    if buyer:
        return "PASS", "decision-maker title (%s)" % re.sub(r"\\b|\(\?.*?\)", "", buyer)
    if crew:
        return "FAIL", "crew/adjacent role (%s), not a VO buyer. Go up the org or BLOCK the company" % crew.replace("\\b", "")
    if review:
        if company_type in ("studio", "agency") and "producer" in t:
            return "PASS", "producer at a %s (producers cast talent there)" % company_type
        return "REVIEW", ("IC producer/marketing title (%s). Passes only with --evidence: VO they've booked, or "
                          "they're the senior-most video owner (name who you checked)" % review)
    return "REVIEW", "title doesn't match a known pattern: needs --evidence"


def load():
    try:
        return json.load(open(LEDGER, encoding="utf-8"))
    except Exception:
        return {}


def save(d):
    with open(LEDGER, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "record", "keep", "show"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--company-type", default="inhouse", choices=["inhouse", "studio", "agency"])
    ap.add_argument("--practice", default="unknown", choices=["in-house-vo", "agency", "interviewee", "unknown"])
    ap.add_argument("--source", default="")
    ap.add_argument("--evidence", default="")
    a = ap.parse_args()
    today = datetime.date.today().isoformat()

    if a.cmd == "check":
        v, why = classify(" ".join(a.args), a.company_type, a.practice)
        print("%s: %s" % (v, why))
        return 0 if v == "PASS" else 1

    d = load()
    if a.cmd == "show":
        print(json.dumps(d.get(a.args[0].lower()), indent=1, ensure_ascii=False))
        return 0

    if a.cmd == "keep":
        email, words = a.args[0].lower(), " ".join(a.args[1:])
        if not words or email not in d:
            print("keep needs an existing row and Spencer's own words + date")
            return 2
        d[email].update(verdict="KEEP-SPENCER", spencer=words, date=today)
        save(d)
        print("KEEP-SPENCER recorded for", email)
        return 0

    if len(a.args) != 4 or not a.source:
        print('record needs: <email> "<Name>" "<Company>" "<title>" --source "<where you read the title today>"')
        return 2
    email, name, company, title = a.args
    v, why = classify(title, a.company_type, a.practice)
    if v == "REVIEW" and len(a.evidence.strip()) >= 25:
        v, why = "PASS-EVIDENCE", why.split(".")[0] + ". Evidence: " + a.evidence.strip()
    elif v == "FAIL" and a.evidence.strip().lower().startswith("senior-most:") and a.practice not in ("agency", "interviewee"):
        v, why = "PASS-EVIDENCE", "crew title but the senior-most video owner. Evidence: " + a.evidence.strip()
    d[email.lower()] = dict(name=name, company=company, title=title, verdict=v, why=why, date=today,
                            company_type=a.company_type, practice=a.practice, source=a.source)
    save(d)
    print("%s: %s %s, %s (%s)" % (v, name, company, title, why))
    return 0 if v.startswith("PASS") else 1


if __name__ == "__main__":
    sys.exit(main())
