"""Incognito (temp profile, no account) checks: Brave, Bing K1 US retry, ChatGPT, Gemini, Perplexity, Copilot."""
import json, subprocess, sys, tempfile, time, urllib.parse as up
from playwright.sync_api import sync_playwright

P = {"P1": "Who is the best American male voice over artist based in Europe?",
     "P2": "american male voice over in europe",
     "P3": "I need to hire an American male voice over artist based in Europe for a commercial. Who do you recommend?",
     "P4": "I need to hire an American male voice over artist in Lisbon. Who do you recommend?",
     "P5": "Who is Spencer Pearman, the voice over artist?"}
K = {"K1": "american male voice over in europe", "K2": "american voice actor based in europe",
     "K3": "american male voice over lisbon", "K4": "american voice actor based in europe for a commercial",
     "K5": "spencer pearman", "K6": "american male voice over"}
OUT, engines = sys.argv[1], sys.argv[2].split(",")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
res = {}
def save(): json.dump(res, open(OUT, "w"), indent=1)
def short(u):
    p = up.urlparse(u); return (p.netloc.replace("www.", "") + p.path)[:70]

def fresh(p, port):
    prof = tempfile.mkdtemp(prefix="incog_")
    proc = subprocess.Popen([CHROME, "--incognito", f"--remote-debugging-port={port}", f"--user-data-dir={prof}",
                             "--no-first-run", "--no-default-browser-check", "about:blank"])
    time.sleep(4)
    b = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
    ctx = b.contexts[0]
    return proc, b, (ctx.pages[0] if ctx.pages else ctx.new_page())

def body(pg): return pg.inner_text("body")

with sync_playwright() as p:
    port = 9340
    for eng in engines:
        for k in (K if eng in ("brave", "bingk1") else P):
            if eng == "bingk1" and k != "K1": continue
            if eng == "brave" and k not in ("K5", "K6"): continue
            port += 1
            proc, b, pg = fresh(p, port)   # new incognito profile per prompt: no carry-over
            key = f"{eng}_{k}"
            try:
                if eng == "brave":
                    pg.goto(f"https://search.brave.com/search?q={up.quote_plus(K[k])}&source=web"); time.sleep(5)
                    L = pg.eval_on_selector_all("main a[href^=http]", "e=>[...new Set(e.map(a=>a.href))]")
                    L = [x for x in L if "brave.com" not in x]
                    res[key] = [f"{i+1}.{short(h)}" for i, h in enumerate(L[:14])] or "EMPTY: " + body(pg)[:200]
                elif eng == "bingk1":
                    for cc in ["us"]:
                        pg.goto(f"https://www.bing.com/search?q={up.quote_plus(K[k])}&cc={cc}&setlang=en"); time.sleep(6)
                        pg.wait_for_selector("li.b_algo", timeout=15000)
                        L = pg.eval_on_selector_all("li.b_algo", "e=>e.map(x=>{const c=x.querySelector('cite');return c?c.textContent:''})")
                        res[key] = [f"{i+1}.{c[:60]}" for i, c in enumerate(L[:10])]
                elif eng == "chatgpt":
                    pg.goto(f"https://chatgpt.com/?q={up.quote_plus(P[k])}&hints=search"); time.sleep(45)
                    res[key] = body(pg)[:3000]
                elif eng == "perplexity":
                    pg.goto(f"https://www.perplexity.ai/search?q={up.quote_plus(P[k])}"); time.sleep(40)
                    res[key] = body(pg)[:3000]
                elif eng == "gemini":
                    pg.goto("https://gemini.google.com/app"); time.sleep(6)
                    for name in ["Reject all", "Accept all"]:
                        pass
                    try: pg.get_by_role("button", name="Reject all").click(timeout=3000); time.sleep(2)
                    except Exception: pass
                    box = pg.locator("rich-textarea [contenteditable]").first
                    box.click(); box.type(P[k], delay=20); pg.keyboard.press("Enter"); time.sleep(40)
                    r = pg.locator("model-response")
                    res[key] = (r.last.inner_text() if r.count() else "NO RESPONSE: " + body(pg)[:600])[:3000]
                elif eng == "copilot":
                    pg.goto("https://copilot.microsoft.com/"); time.sleep(8)
                    import re as _re
                    try: pg.get_by_role("button", name=_re.compile("Reject", _re.I)).first.click(timeout=5000); time.sleep(3)
                    except Exception: pass
                    try: pg.get_by_text("Go to Chat").first.click(timeout=5000); time.sleep(6)
                    except Exception: pass
                    try: pg.get_by_role("button", name=_re.compile("Reject", _re.I)).first.click(timeout=3000); time.sleep(2)
                    except Exception: pass
                    box = pg.locator("textarea, [contenteditable=true]").first
                    box.click(); box.type(P[k], delay=20); pg.keyboard.press("Enter"); time.sleep(40)
                    res[key] = body(pg)[:3000]
            except Exception as ex:
                res[key] = f"ERROR {type(ex).__name__}: {str(ex)[:150]} | PAGE: " + (body(pg)[:400] if pg else "")
            save()
            b.close(); proc.terminate(); time.sleep(2)
print(json.dumps(res, indent=1))
