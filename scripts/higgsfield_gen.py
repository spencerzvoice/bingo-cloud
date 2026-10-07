"""Generate a clip with the Higgsfield API and save it locally.

Key: put ONE of these in local/api-keys.env
    HF_KEY=<key-id>:<key-secret>
    or HF_API_KEY_ID=... and HF_API_KEY_SECRET=...

Usage:
    python scripts/higgsfield_gen.py "prompt" [--model kling-video/v2.6/pro/text-to-video]
        [--duration 5|10] [--aspect 16:9|9:16|1:1] [--sound off|on] [--name shot01]

Output: local/content/higgsfield/<name>.mp4 (+ .json with the request record).
Default sound is OFF: Spencer's own VO goes on top, never generated audio.
Cost (Higgsfield API page, 2026-10-07): Kling 2.6 ~$0.07/s, so 5 s ~ $0.35, 10 s ~ $0.70.
"""
import argparse
import json
import os
import pathlib
import sys
import time
import uuid

import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "local" / "content" / "higgsfield"
BASE = "https://api.higgsfield.ai"
TERMINAL = {"completed", "failed", "nsfw", "canceled"}


def load_key():
    env = {}
    f = ROOT / "local" / "api-keys.env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    env.update({k: v for k, v in os.environ.items() if k.startswith("HF_")})
    if env.get("HF_KEY"):
        return env["HF_KEY"]
    if env.get("HF_API_KEY_ID") and env.get("HF_API_KEY_SECRET"):
        return f"{env['HF_API_KEY_ID']}:{env['HF_API_KEY_SECRET']}"
    sys.exit("No Higgsfield key: add HF_KEY=<id>:<secret> to local/api-keys.env")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--model", default="kling-video/v2.6/pro/text-to-video")
    ap.add_argument("--duration", type=int, default=5)
    ap.add_argument("--aspect", default="16:9")
    ap.add_argument("--sound", default="off")
    ap.add_argument("--name", default=time.strftime("hf_%Y%m%d_%H%M%S"))
    a = ap.parse_args()

    headers = {
        "Authorization": f"Key {load_key()}",
        "Content-Type": "application/json",
        "Idempotency-Key": str(uuid.uuid4()),
    }
    body = {"prompt": a.prompt, "duration": a.duration,
            "aspect_ratio": a.aspect, "sound": a.sound}
    r = requests.post(f"{BASE}/{a.model}", headers=headers, json=body, timeout=60)
    if r.status_code >= 400:
        sys.exit(f"Submit failed {r.status_code}: {r.text[:500]}")
    job = r.json()
    print("submitted", job.get("request_id"))

    status_url = job["status_url"]
    wait = 5
    while True:
        time.sleep(wait)
        s = requests.get(status_url, headers=headers, timeout=60).json()
        st = s.get("status")
        print("status", st)
        if st in TERMINAL:
            break
        wait = min(wait * 1.5, 30)

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{a.name}.json").write_text(
        json.dumps({"model": a.model, "request": body, "response": s}, indent=2),
        encoding="utf-8")
    if st != "completed":
        sys.exit(f"Ended {st}: {s.get('error')}")

    url = s["video"]["url"]
    dest = OUT / f"{a.name}.mp4"
    with requests.get(url, stream=True, timeout=300) as v:
        v.raise_for_status()
        with open(dest, "wb") as fh:
            for chunk in v.iter_content(1 << 20):
                fh.write(chunk)
    print("saved", dest)


if __name__ == "__main__":
    main()
