"""Cloud LinkedIn employment check (no login, public profile only).

Usage:  python cloud_check.py contacts.json
contacts.json = [{"name": "...", "company": "...", "url": "https://www.linkedin.com/in/<slug>/"}, ...]

Reads BRIGHTDATA_API_KEY / ZENROWS_API_KEY from the environment (cloud) or local/api-keys.env (desktop).
Bright Data first (batches of 20), ZenRows as fallback for anything Bright Data couldn't read.
Prints one JSON line per contact: {"name","company","url","result","shown_company","source"}
result: PASS (public profile's current company matches) | MISMATCH (shows another company) | HIDDEN (no company shown / fetch failed)
The public (logged-out) profile shows the current COMPANY only; titles and dates are masked by LinkedIn.
"""
import json, os, re, sys, urllib.request, urllib.parse, urllib.error

def keys():
    k = {n: os.environ.get(n, "") for n in ("BRIGHTDATA_API_KEY", "ZENROWS_API_KEY")}
    p = os.path.join(os.path.dirname(__file__), "..", "..", "..", "local", "api-keys.env")
    if os.path.exists(p):
        for l in open(p, encoding="utf-8"):
            m = re.match(r"^([A-Z_]+)=(.*)$", l.strip())
            if m and not k.get(m.group(1)):
                k[m.group(1)] = m.group(2).strip()
    return k

def norm(s):
    s = (s or "").lower()
    s = re.sub(r"\b(inc|llc|ltd|plc|corp|corporation|company|co|gmbh|ag|the|group|holdings)\b\.?", " ", s)
    return re.sub(r"[^a-z0-9]+", "", s)

def same(a, b):
    a, b = norm(a), norm(b)
    return bool(a and b) and (a == b or a in b or b in a)

def slug(u):
    m = re.search(r"linkedin\.com/in/([^/?#]+)", u or "")
    return m.group(1).lower() if m else None

def brightdata(key, urls):
    out = {}
    for i in range(0, len(urls), 20):
        body = json.dumps({"input": [{"url": u} for u in urls[i:i + 20]]}).encode()
        req = urllib.request.Request(
            "https://api.brightdata.com/datasets/v3/scrape?dataset_id=gd_l1viktl72bvl7bjuj0&format=json&include_errors=true",
            data=body, method="POST",
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        try:
            data = json.loads(urllib.request.urlopen(req, timeout=300).read().decode())
        except Exception as e:
            sys.stderr.write("brightdata error: %s\n" % e)
            continue
        if isinstance(data, dict):
            sys.stderr.write("brightdata non-list reply (async snapshot?): %s\n" % str(data)[:300])
            continue
        for p in data:
            s = slug((p.get("input") or {}).get("url") or p.get("input_url") or p.get("url"))
            if s:
                out[s] = p.get("current_company_name") or (p.get("current_company") or {}).get("name")
    return out

def zenrows(key, url):
    q = urllib.parse.urlencode({"apikey": key, "url": url, "premium_proxy": "true", "js_render": "true"})
    try:
        raw = urllib.request.urlopen("https://api.zenrows.com/v1/?" + q, timeout=180).read().decode("utf-8", "replace")
    except Exception as e:
        sys.stderr.write("zenrows error: %s\n" % e)
        return None
    for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        try:
            d = json.loads(ld)
        except Exception:
            continue
        for g in (d.get("@graph") or [d]):
            if g.get("@type") == "Person":
                w = [x.get("name") for x in (g.get("worksFor") or []) if x.get("name") and "*" not in x.get("name")]
                if w:
                    return w[0]
    t = re.search(r"<title>[^<-]+-\s*([^<|]+?)\s*\|\s*LinkedIn</title>", raw)
    return t.group(1).strip() if t else None

def main():
    contacts = json.load(open(sys.argv[1], encoding="utf-8"))
    k = keys()
    bd = brightdata(k["BRIGHTDATA_API_KEY"], [c["url"] for c in contacts]) if k["BRIGHTDATA_API_KEY"] else {}
    for c in contacts:
        shown, src = bd.get(slug(c["url"])), "brightdata"
        if not shown and k["ZENROWS_API_KEY"]:
            shown, src = zenrows(k["ZENROWS_API_KEY"], c["url"]), "zenrows"
        res = "HIDDEN" if not shown else ("PASS" if same(shown, c["company"]) else "MISMATCH")
        print(json.dumps({"name": c["name"], "company": c["company"], "url": c["url"],
                          "result": res, "shown_company": shown, "source": src if shown else None}))

if __name__ == "__main__":
    main()
