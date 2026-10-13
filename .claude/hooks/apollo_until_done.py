"""Stop hook: GOAL - get the Apollo information at all costs (Spencer, 2026-10-13).

Cause: the 10-13 03:05 Morning Build sent an Apollo waterfall, polled for ~40 s, wrote
"still pending after about 4 minutes", drafted nothing and ended. Apollo finished 2 s later.
Spencer: "wait as long as you have to and retry if it doesn't work. There is no situation
where 'stopping and not doing the work' is acceptable."

On every attempt to end a turn (desktop and cloud routines alike):
1. Apollo gate. Any apollo_people_match / apollo_people_bulk_match sent with run_waterfall_*
   whose request_id has no final apollo_webhook_result_show answer (success / failed /
   unknown / expired) blocks the stop. The hook waits WAIT_S seconds itself, so the wait is
   real, then sends Bingo back to poll again. No time cap. Polls cost no credits.
2. Morning Build stage gate. A Morning Build run can't end until it has printed
   "STAGE 0 COMPLETE" ... "STAGE 3 COMPLETE" (before 12 UTC) or "STAGE 3 COMPLETE" (13:05 run).

The one exit: a session/usage-limit error, where CLAUDE.md override 7 applies (stop, commit,
push, one notification; the next run picks the PENDING request up from APOLLO-LEDGER.md).
"""
import json, os, re, sys, time

WAIT_S = 25
LIMIT_RE = re.compile(r"hit your (session|usage|weekly) limit|rate_limit_error|usage limit reached", re.I)
RID_RE = re.compile(r'request_id\\?"?\s*[:=]\s*\\?"?(-?\d{6,})')
SAVED_RE = re.compile(r"saved to (\S+\.(?:txt|json))")
TERMINAL_RE = re.compile(
    r'\\?"status\\?"\s*:\s*\\?"(success|failed)|request_id_unknown|request_id_expired|invalid_request_id')


def text_of(content):
    if isinstance(content, str):
        return content
    out = []
    for c in content or []:
        if isinstance(c, dict):
            if c.get("type") == "text":
                out.append(c.get("text", ""))
            elif "content" in c:
                out.append(text_of(c["content"]))
    return "\n".join(out)


def with_saved(txt):
    m = SAVED_RE.search(txt)
    if m:
        try:
            return txt + "\n" + open(m.group(1), encoding="utf-8", errors="replace").read()
        except Exception:
            pass
    return txt


def scan(path):
    uses, results, first_user, first_ts, said, tail = {}, {}, None, None, [], []
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            e = json.loads(line)
        except Exception:
            continue
        if first_ts is None and e.get("timestamp"):
            first_ts = e["timestamp"]
        content = (e.get("message") or {}).get("content")
        if e.get("type") == "assistant":
            for c in content or []:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "tool_use":
                    uses[c.get("id")] = (c.get("name", ""), c.get("input") or {})
                elif c.get("type") == "text":
                    said.append(c.get("text", ""))
                    tail.append(c.get("text", ""))
        elif e.get("type") == "user":
            if isinstance(content, str):
                first_user = first_user or content
                continue
            for c in content or []:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "tool_result":
                    t = text_of(c.get("content"))
                    results[c.get("tool_use_id")] = t
                    tail.append(t[:2000])
                elif c.get("type") == "text" and first_user is None:
                    first_user = c.get("text", "")
        tail = tail[-30:]
    return uses, results, first_user or "", first_ts or "", "\n".join(said), "\n".join(tail)


def pending_requests(uses, results):
    resolved, calls = set(), []
    for tid, (name, inp) in uses.items():
        res = results.get(tid)
        if res is None:
            continue
        if name.endswith("apollo_webhook_result_show"):
            if TERMINAL_RE.search(res):
                resolved.add(str(inp.get("request_id", "")).strip())
        elif name.endswith(("apollo_people_match", "apollo_people_bulk_match")) and (
                inp.get("run_waterfall_email") or inp.get("run_waterfall_phone")):
            ids = set(RID_RE.findall(with_saved(res)))
            if ids:
                calls.append(ids)
    return sorted({min(ids, key=len) for ids in calls if not ids & resolved})


def block(reason):
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


def main():
    d = json.load(sys.stdin)
    path = d.get("transcript_path") or ""
    if not path or not os.path.exists(path):
        return
    uses, results, first_user, first_ts, said, tail = scan(path)
    if LIMIT_RE.search(tail):
        return  # override 7: usage limit = stop, commit, push, one notification

    pend = pending_requests(uses, results)
    if pend:
        time.sleep(WAIT_S)
        block(
            f"GOAL: get this information at all costs. Apollo waterfall request(s) {', '.join(pend)} "
            f"have no final answer yet. This hook just waited {WAIT_S} s. Call apollo_webhook_result_show "
            f"with request_id {pend[0]} now (polls cost no credits) and keep polling for as long as it "
            f"takes, until it says success or failed. There is no time limit and no stopping before that. "
            f"Then use every valid email and draft it; any invalid/unknown/catch-all contact goes to the "
            f"backup, then an Apollo search at that company, then the next company in funnel order, "
            f"until the work is done. Never report a wait you did not measure.")

    if "Morning Build" in first_user:
        hour = int(first_ts[11:13]) if re.match(r"\d{4}-\d\d-\d\dT\d\d", first_ts) else 0
        need = ["STAGE 3 COMPLETE"] if hour >= 12 else [f"STAGE {i} COMPLETE" for i in range(4)]
        missing = [m for m in need if m not in said]
        if missing:
            block(
                f"Morning Build is not finished: {', '.join(missing)} not printed yet. Run the missing "
                f"stage(s) now, in order, reading the live draft bodies yourself (never a memory log's "
                f"claim about them). A stage that stalled or drafted nothing never skips the next one. "
                f"Print 'STAGE <n> COMPLETE: <one line of what it did>' as each one finishes.")


if __name__ == "__main__":
    main()
