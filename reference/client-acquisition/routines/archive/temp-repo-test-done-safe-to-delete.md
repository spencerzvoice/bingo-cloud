# TEMP - repo test (done, safe to delete)

Archived 2026-10-07 before deletion. id `trig_013H7XsfJExExsDrVgmeZ8gj`, cron ``, env `env_01VPYwj9nwzjzGqdxm4fRQFY`, connectors: Google_Drive, Gmail, FGAC_ai, Claude_Code_Remote.

## Prompt (verbatim)

One-off YouTube test #2 for Spencer's cloud routines. Do NOT commit or push. NEVER print env var values or cookie contents. Do NOT modify any certificate/trust store and do NOT use --no-check-certificates - if something needs that, just report it.
Put every command in a script file and run it with bash (avoid inline parentheses).
1. `python -m pip install -q -U "yt-dlp[default]" deno curl_cffi` - the [default] extra installs yt-dlp-ejs, the JS-challenge solver scripts, locally, so yt-dlp does NOT need to fetch them from GitHub. Report `python -m pip show yt-dlp-ejs | head -2` and `python -m yt_dlp --version`.
2. `echo "$YT_COOKIES_B64" | base64 -d > /tmp/yt_cookies.txt`.
3. Download: `python -m yt_dlp --cookies /tmp/yt_cookies.txt -f "best[height<=480]/best" -o "/tmp/t1.%(ext)s" "https://www.youtube.com/watch?v=ivvw5uBvTh4"` - OK + file size (ls -la), or the exact ERROR line plus any [jsc] warning lines. If it fails, retry once adding `--extractor-args youtube:player_client=web_embedded,tv`, and once adding `--extractor-args youtube:player_client=mweb`.
4. Captions: `python -m yt_dlp --cookies /tmp/yt_cookies.txt --skip-download --write-auto-subs --sub-langs en -o /tmp/c1 "https://www.youtube.com/watch?v=ivvw5uBvTh4"` - OK (ls /tmp/c1*) or error.
5. `rm -f /tmp/yt_cookies.txt`.
Finish with a short OK/FAIL summary and the exact winning command.
