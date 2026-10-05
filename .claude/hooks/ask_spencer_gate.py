"""Stop hook: AGENTS.md hard rule 0 (Spencer, 2026-10-05: "So follow it").
Blocks a reply that hands Spencer a manual step (sign in, click, paste, export...) unless the reply
also shows what Bingo tried first, on a line starting "Tried:". Bingo gets sent back to try its own
tools (Chrome, built-in browser, FGAC, Carly, API keys, repo scripts) before asking.
"""
import json, re, sys

ASK = re.compile(
    r"\b(you(?:'ll| will)? (?:need|have) to|you need to|can you|could you|please|you should|"
    r"you'd have to|on your end|your move)\b[^.\n]{0,80}\b(sign ?in|log ?in|log back|click|paste|copy|"
    r"open|export|upload|download|drag|install|enable|approve|authori[sz]e|connect|add the|set (?:it|them|the)|share|run)\b"
    r"|\b(sign in|log in) (?:once|again|yourself)\b"
    r"|(?:^|[.!:]\s+|^\s*[-*]\s+(?:\*\*[^*]+\*\*:?\s*)?)(?:make sure|sign in|log in|click|paste|copy|export|"
    r"upload|set (?:it|them|all|the|both|each)|share|approve|enable|install|connect|drag)\b[^.\n]{0,80}",
    re.I)


def last_reply(path):
    texts = []
    for line in open(path, encoding="utf-8"):
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("type") == "user" and not any(
                isinstance(c, dict) and c.get("type") == "tool_result"
                for c in (e.get("message", {}).get("content") or []) if isinstance(c, dict)):
            texts = []
        elif e.get("type") == "assistant":
            for c in e.get("message", {}).get("content") or []:
                if isinstance(c, dict) and c.get("type") == "text":
                    texts.append(c["text"])
    return "\n".join(texts)


def main():
    d = json.load(sys.stdin)
    if d.get("stop_hook_active"):
        return
    text = d.get("last_assistant_message") or last_reply(d.get("transcript_path", ""))
    m = ASK.search(text or "")
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
