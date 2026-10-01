# PreToolUse hook: block whole-file Write on the project's MEMORY.md.
# Several Bingo chats share this folder; a stale chat rewriting the whole
# file wipes newer entries. Edit (targeted, fails if the file changed
# since it was read) is still allowed.
import json, os, sys

data = json.load(sys.stdin)
path = (data.get("tool_input") or {}).get("file_path", "")
project = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()

def norm(p):
    return os.path.normcase(os.path.abspath(p))

if path and norm(path) == norm(os.path.join(project, "MEMORY.md")):
    sys.stderr.write(
        "Blocked: never rewrite MEMORY.md wholesale (parallel Bingo chats share it). "
        "git pull, Read MEMORY.md from disk, then use Edit for targeted changes.\n"
    )
    sys.exit(2)
sys.exit(0)
