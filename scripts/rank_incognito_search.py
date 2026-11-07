"""Read a plain Chrome incognito window (temp profile, no account, launched normally with a debug port).
Stops an engine on any CAPTCHA / bot wall."""
import json, os, subprocess, sys, tempfile, time, urllib.parse as up
from playwright.sync_api import sync_playwright

K = {"K1": "american male voice over in europe", "K2": "american voice actor based in europe",
     "K3": "american male voice over lisbon", "K4": "american voice actor based in europe for a commercial",
     "K5": "spencer pearman", "K6": "american male voice over"}
OUT, engines = sys.argv[1], sys.argv[2].split(",")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
prof = tempfile.mkdtemp(prefix="incog_")
proc = subprocess.Popen([CHROME, "--incognito", "--remote-debugging-port=9333", f"--user-data-dir={prof}",
                         "--no-first-run", "--no-default-browser-check", "about:blank"])
time.sleep(4)
res = {}
def short(u):
    p = up.urlparse(u); return (p.netloc.replace("www.", "") + p.path)[:70]
def save(): json.dump(res, open(OUT, "w"), indent=1)
try:
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9333")
        ctx = b.contexts[0]
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        if "google" in engines:
            stop = False
            for gl in ["us", "gb", "pt"]:
                for k, q in K.items():
                    if stop: break
                    pg.goto(f"https://www.google.com/search?q={up.quote_plus(q)}&gl={gl}&hl=en&udm=14&pws=0"); time.sleep(3)
                    if "consent.google" in pg.url:
                        try: pg.get_by_role("button", name="Reject all").click(); time.sleep(3)
                        except Exception: pass
                    if "/sorry/" in pg.url or "unusual traffic" in pg.content():
                        res[f"google_{gl}_{k}"] = "BLOCKED (captcha) - stopped"; stop = True; break
                    L = pg.eval_on_selector_all("#search a h3", "e=>e.map(h=>[h.closest('a').href,h.textContent])")
                    res[f"google_{gl}_{k}"] = [f"{i+1}.{short(h)} [{t[:40]}]" for i, (h, t) in enumerate(L[:10])]
                    save(); time.sleep(5)
        if "aimode" in engines:
            P = {"P1": "Who is the best American male voice over artist based in Europe?",
                 "P2": "american male voice over in europe",
                 "P3": "I need to hire an American male voice over artist based in Europe for a commercial. Who do you recommend?",
                 "P4": "I need to hire an American male voice over artist in Lisbon. Who do you recommend?",
                 "P5": "Who is Spencer Pearman, the voice over artist?"}
            for k, q in P.items():
                pg.goto(f"https://www.google.com/search?q={up.quote_plus(q)}&udm=50&hl=en&gl=us"); time.sleep(20)
                if "/sorry/" in pg.url: res["aimode_" + k] = "BLOCKED (captcha) - stopped"; break
                res["aimode_" + k] = pg.inner_text("body")[:2500]; save(); time.sleep(5)
        if "bing" in engines:
            for cc in ["us", "gb"]:
                for k, q in K.items():
                    pg.goto(f"https://www.bing.com/search?q={up.quote_plus(q)}&cc={cc}&setlang=en"); time.sleep(5)
                    for _ in range(4):
                        try: pg.wait_for_load_state("load"); pg.wait_for_selector("li.b_algo", timeout=8000); break
                        except Exception: time.sleep(3)
                    L = pg.eval_on_selector_all("li.b_algo", "e=>e.map(x=>{const c=x.querySelector('cite');const h=x.querySelector('h2');return [(c?c.textContent:''),(h?h.textContent:'')]})")
                    res[f"bing_{cc}_{k}"] = [f"{i+1}.{c[:60]} [{t[:40]}]" for i, (c, t) in enumerate(L[:10])] or "EMPTY: " + pg.title()
                    save(); time.sleep(4)
        b.close()
finally:
    save(); proc.terminate()
print(json.dumps(res, indent=1))
