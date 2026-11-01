"""Stop hook: AGENTS.md hard rule 0 (Spencer, 2026-10-05: "So follow it").
Blocks a reply that hands Spencer a manual step (sign in, click, paste, export...) unless the reply
also shows what Bingo tried first, on a line starting "Tried:". Bingo gets sent back to try its own
tools (Chrome, built-in browser, FGAC, Carly, API keys, repo scripts) before asking.

Tightened 2026-11-01 (Spencer: "You've been answering twice, why?") after three false positives in
one day: the hook now ignores quoted drafts, code blocks and the verification footer, needs a real
object after a bare imperative ("Upload counts..." is not an ask), and stands down when Spencer's own
last message asked for the thing (a prompt, a draft, a reply, wording to paste).
"""
import json, re, sys

ASK = re.compile(
    r"\b(you(?:'ll| will)? (?:need|have) to|you need to|can you|could you|please|you should|"
    r"you'd have to|on your end|your move)\b[^.\n]{0,80}\b(sign ?in|log ?in|log back|click|paste|copy|"
    r"open|export|upload|download|drag|install|enable|approve|authori[sz]e|connect|add the|set (?:it|them|the)|share|run)\b"
    r"|\b(sign in|log in) (?:once|again|yourself)\b"
    r"|(?:^|[.!]\s+|^\s*[-*]\s+(?:\*\*[^*]+\*\*:?\s*)?)(?:make sure|sign in|log in|click|paste|copy|export|"
    r"upload|set (?:it|them|all|the|both|each)|share|approve|enable|install|connect|drag)"
    r"\s+(?:it|them|this|that|these|those|the|your|a|an|me|to|into|on|in|up|with|from|yourself|once|again)\b[^.\n]{0,80}",
    re.I | re.M)

# Spencer asked for text he will paste or send himself: a prompt, a draft, a reply, wording.
USER_ASKED = re.compile(
    r"\b(prompt|paste|give me|write (?:me|up|the|a)|draft|rewrite|re-?word|reply|response|message|script|"
    r"template|wording|what (?:should|do) i (?:say|send|write)|instructions? for)\b", re.I)


def strip_noise(text):
    """Drop what is not Bingo talking to Spencer: fenced code, quoted drafts, the verification footer."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    keep = []
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith(">") or re.match(r"^[—-]\s*(Verified|Bracketed|Unknown|Tried)\b", s, re.I):
            continue
        keep.append(line)
    return "\n".join(keep)


def transcript(path):
    """Return (last user message text, Bingo's reply after it)."""
    user, texts = "", []
    try:
        lines = open(path, encoding="utf-8")
    except Exception:
        return user, ""
    for line in lines:
        try:
            e = json.loads(line)
        except Exception:
            continue
        content = e.get("message", {}).get("content") or []
        if e.get("type") == "user":
            if isinstance(content, str):
                user, texts = content, []
            elif not any(isinstance(c, dict) and c.get("type") == "tool_result" for c in content):
                user = "\n".join(c.get("text", "") for c in content if isinstance(c, dict))
                texts = []
        elif e.get("type") == "assistant":
            for c in content:
                if isinstance(c, dict) and c.get("type") == "text":
                    texts.append(c["text"])
    return user, "\n".join(texts)


def main():
    d = json.load(sys.stdin)
    if d.get("stop_hook_active"):
        return
    user, reply = transcript(d.get("transcript_path", ""))
    text = d.get("last_assistant_message") or reply
    if USER_ASKED.search(user or ""):
        return
    m = ASK.search(strip_noise(text or ""))
    if not m or re.search(r"^\s*\**Tried:", text, re.M | re.I):
        return
    print(json.dumps({"decision": "block", "reason": (
        f'Hard rule 0 (AGENTS.md *****): your reply asks Spencer to do something manual ("{m.group(0)}"). '
        "Before asking, try every tool you have: his Chrome (Claude in Chrome, signed in), the built-in "
        "browser, FGAC, Carly, local/api-keys.env, repo scripts. If one works, do it yourself and drop the ask. "
        "If none can (e.g. only he can record a take or approve a payment), keep the ask and add a line "
        "starting 'Tried:' naming what you checked.")}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
