#!/usr/bin/env python3
"""Keep every Bingo (desktop, cloud, phone) on one shared memory: origin/main.

  start  (SessionStart hook): pull origin/main into whatever branch this session is on.
  stop   (Stop hook): commit MEMORY.md + memory/ + reference/ changes, merge origin/main, push to main.

Only memory files are auto-committed; other work in progress is left alone.
Never fails the session: every problem is reported and the script exits 0.
"""
import os
import subprocess
import sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
MEMORY_PATHS = ["MEMORY.md", "memory", "reference"]


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=90)
    except Exception as e:  # git missing, timeout, ...
        return subprocess.CompletedProcess(args, 1, "", str(e))


def fetch_and_merge_main():
    """Merge origin/main into HEAD. Returns an error message, or None on success."""
    if git("fetch", "-q", "origin", "main").returncode != 0:
        return "couldn't reach GitHub"
    if git("merge-base", "--is-ancestor", "origin/main", "HEAD").returncode == 0:
        return None  # already up to date
    if git("merge", "--no-edit", "-q", "origin/main").returncode != 0:
        git("merge", "--abort")
        return "merging origin/main hit a conflict"
    return None


def start():
    err = fetch_and_merge_main()
    if err:
        print(f"Bingo memory sync: {err}. MEMORY.md may be out of date; run `git merge origin/main` "
              "and resolve it (keep both sides' facts) before relying on memory.")
    else:
        print("Bingo memory sync: up to date with origin/main (the shared memory).")


def stop():
    if git("status", "--porcelain", "--", *MEMORY_PATHS).stdout.strip():
        git("add", "--", *MEMORY_PATHS)
        git("commit", "-q", "-m", "memory: auto-sync", "--", *MEMORY_PATHS)
    err = fetch_and_merge_main()
    if err:
        print(f"Bingo memory sync: {err}; memory not pushed to main.", file=sys.stderr)
        return
    if git("rev-list", "--count", "origin/main..HEAD").stdout.strip() in ("", "0"):
        return  # nothing new for main
    if git("push", "-q", "origin", "HEAD:main").returncode != 0:
        print("Bingo memory sync: push to main failed; run `git push origin HEAD:main`.", file=sys.stderr)
        return
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if branch and branch not in ("HEAD", "main"):
        git("push", "-q", "-u", "origin", branch)


if __name__ == "__main__":
    {"start": start, "stop": stop}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: None)()
    sys.exit(0)
