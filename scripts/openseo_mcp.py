"""Minimal MCP-over-HTTP client for Spencer's own OpenSEO account (token from Claude's stored OAuth)."""
import json, os, sys, time, urllib.request, urllib.error

d = json.load(open(os.path.expanduser('~/.claude/.credentials.json')))
e = next(v for k, v in d['mcpOAuth'].items() if k.startswith('plugin:openseo'))
URL, TOK = e['serverUrl'], e['accessToken']
print('token expires in min:', round((e.get('expiresAt', 0) / 1000 - time.time()) / 60), file=sys.stderr)
sid = None

def rpc(method, params=None, id_=1):
    global sid
    body = {"jsonrpc": "2.0", "method": method, "params": params or {}}
    if id_ is not None: body["id"] = id_
    h = {"Authorization": "Bearer " + TOK, "Content-Type": "application/json",
         "Accept": "application/json, text/event-stream", "MCP-Protocol-Version": "2025-06-18", "User-Agent": "claude-code/2.0 (bingo)"}
    if sid: h["Mcp-Session-Id"] = sid
    try:
        r = urllib.request.urlopen(urllib.request.Request(URL, json.dumps(body).encode(), h), timeout=180)
    except urllib.error.HTTPError as x:
        print("HTTP", x.code, x.read()[:300], file=sys.stderr); raise SystemExit(1)
    sid = r.headers.get("Mcp-Session-Id") or sid
    raw = r.read().decode("utf-8", "replace")
    if not raw.strip(): return None
    if raw.lstrip().startswith("{"): return json.loads(raw)
    msgs = [json.loads(l[5:]) for l in raw.splitlines() if l.startswith("data:")]
    return msgs[-1] if msgs else raw

rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "bingo", "version": "1"}})
rpc("notifications/initialized", None, None)
cmd = sys.argv[1]
if cmd == "list":
    for t in rpc("tools/list", {}, 2)["result"]["tools"]:
        print(t["name"], "::", json.dumps(t.get("inputSchema", {}).get("properties", {}))[:3000])
else:
    args = json.loads(sys.argv[2])
    out = rpc("tools/call", {"name": cmd, "arguments": args}, 3)
    print(json.dumps(out)[:int(sys.argv[3]) if len(sys.argv) > 3 else 20000])
