/**
 * Bingo Digest Prep (Spencer, 2026-10-29: "Yes, build it"; plan: reference/automation-offload-plan.md).
 * Lives in spencer@spencerzvoice.com's own Apps Script, runs daily ~06:30 UTC (thread list ~05:00), before the 07:15 UTC
 * VO Pipeline Digest. Does the Digest's mechanical Gmail work (DIGEST-ROUTINE-PROMPT.md Steps 1-3e plus the
 * Step 0a / Prep step (0) thread list) so the Digest reads a few Sheet tabs instead of ~190 rows of
 * Gmail tool calls across 3 subagents.
 * READ-ONLY on Gmail and on the Outreach Tracker. Writes only the Prep_* tabs of the Follow-up Queue Sheet.
 * Port of scripts/digest_gmail_check.py + the Gmail half of scripts/ledger_coverage.py.
 * Needs the Gmail advanced service (Services > Gmail API v1): it enables the Gmail API for the project,
 * and the bulk reads then go through UrlFetchApp.fetchAll with the script's own token (parallel, fast).
 * Source of truth: scripts/apps-script/DigestPrep.gs in the bingo repo.
 */
const PREP_SHEET_ID = '1YVJbPnETd3gkX8dAwdHsiqijojgMlyCL_4Jaskk9aao';
const TRACKER_TITLE = 'VO Outreach Pipeline Tracker';
const ME = 'spencer@spencerzvoice.com';
const SELF = ['spencer@spencerzvoice.com', 'spencerzpearman@gmail.com'];
const INACTIVE = ['dropped', 'left company'];
const OOO = /out of (the )?office|automatic reply|auto(matic)?[- ]?reply|autoreply|away from|on leave|vacation/i;
const SKIP_NEW = /no-?reply|mailer-daemon|postmaster|notification|voices\.com|bodalgo|voice123|google\.com|calendar/i;
const ADDR = /[\w.+'-]+@[\w-]+(?:\.[\w-]+)+/g;
const API = 'https://gmail.googleapis.com/gmail/v1/users/me/';
const META = '?format=metadata&metadataHeaders=From&metadataHeaders=To&metadataHeaders=Cc' +
    '&metadataHeaders=Date&metadataHeaders=Subject&fields=id,threadId,labelIds,snippet,internalDate,payload/headers';
const BATCH = 10;  // 25 in parallel tripped Gmail's per-user concurrency limit (10-29 test: 35 lookups lost)
const UNITS_PER_S = 150;
const NEW_DAYS = 3;
const BOUNCE_DAYS = 60;  // older bounces are already in the tracker's Status
const THREAD_DAYS = 21;
const TIME_LIMIT_MS = 5 * 60 * 1000;
let TOKEN = '';
let T0 = 0;
let FAILS = {meta: 0, thread: 0, samples: []};

/** Run once from the editor: installs the daily runs (threads ~05:00 UTC, rows ~06:30 UTC; never at once)
 *  and the hourly watchdog. */
function setup() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (['run', 'runThreads', 'watchdog'].indexOf(t.getHandlerFunction()) >= 0) ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('watchdog').timeBased().everyHours(1).create();
  ScriptApp.newTrigger('runThreads').timeBased().atHour(5).nearMinute(0).everyDays(1).inTimezone('Etc/UTC').create();
  ScriptApp.newTrigger('run').timeBased().atHour(6).nearMinute(30).everyDays(1).inTimezone('Etc/UTC').create();
  return ScriptApp.getProjectTriggers().map(function (t) { return t.getHandlerFunction(); });
}

function run() {
  T0 = Date.now();
  FAILS = {meta: 0, thread: 0, samples: []};
  const out = SpreadsheetApp.openById(PREP_SHEET_ID);
  const meta = {run_utc: iso_(new Date()), status: 'RUNNING'};
  writeMeta_(out, meta);
  try {
    Gmail.Users.getProfile('me');  // fails loudly if the advanced service is missing
    TOKEN = ScriptApp.getOAuthToken();
    Object.assign(meta, prep_(out));
  } catch (e) {
    meta.status = 'ERROR';
    meta.error = String(e && e.stack || e).slice(0, 1000);
  }
  meta.finished_utc = iso_(new Date());
  meta.runtime_s = Math.round((Date.now() - T0) / 1000);
  writeMeta_(out, meta);
}

function prep_(out) {
  // Step 1: exactly one tracker of that title in the root of My Drive.
  const it = DriveApp.searchFiles("title = '" + TRACKER_TITLE + "' and 'root' in parents and trashed = false" +
      " and mimeType = 'application/vnd.google-apps.spreadsheet'");
  const found = [];
  while (it.hasNext()) found.push(it.next().getId());
  if (found.length !== 1) return {status: 'ERROR', error: found.length + ' trackers named "' + TRACKER_TITLE + '" in My Drive root'};

  // Step 2: active rows = an email and Status not Dropped / Left Company.
  const vals = SpreadsheetApp.openById(found[0]).getSheetByName('Outreach Tracker').getRange('A1:L1000').getDisplayValues();
  const rows = [], known = {};
  for (let n = 1; n < vals.length; n++) {
    const r = vals[n];
    const emails = (String(r[3]).toLowerCase().match(ADDR) || []);
    emails.forEach(function (a) { known[a] = true; });
    if (!emails.length || INACTIVE.indexOf(String(r[6]).trim().toLowerCase()) >= 0) continue;
    rows.push({row: n + 1, name: r[0], company: r[1], emails: emails, status: r[6], last: r[8], flag: r[10]});
  }
  const addrs = Object.keys(rows.reduce(function (m, r) { r.emails.forEach(function (a) { m[a] = 1; }); return m; }, {})).sort();

  // Step 3a: per address, latest inbound (5) and latest outbound (2), both directions, no date limit.
  const lists = getAll_([].concat.apply([], addrs.map(function (a) {
    return [list_('from:' + a + ' -in:drafts', 5), list_('from:me to:' + a + ' -in:drafts', 1)];
  })));
  const want = {};
  lists.forEach(function (l) { (l.messages || []).forEach(function (m) { want[m.id] = 1; }); });

  // Step 3 extras: bounces (300 latest delivery failures), drafts (3b), new contacts (3c).
  const bl = getAll_([list_('newer_than:' + BOUNCE_DAYS + 'd (from:(mailer-daemon OR postmaster) OR subject:(undeliverable OR "delivery status notification"))', 300)])[0];
  const dl = getAll_(['drafts?maxResults=500&fields=drafts(id,message(id))'])[0];
  const nl = getAll_([list_('newer_than:' + NEW_DAYS + 'd (in:inbox OR in:sent) -in:drafts -category:promotions -category:social', 200)])[0];
  [bl, nl].forEach(function (l) { (l.messages || []).forEach(function (m) { want[m.id] = 1; }); });
  (dl.drafts || []).forEach(function (d) { want[d.message.id] = 1; });
  const M = metas_(Object.keys(want));

  const res = {}, errors = {};
  addrs.forEach(function (a, i) {
    const li = lists[2 * i], lo = lists[2 * i + 1];
    if (li.error || lo.error) { errors[a] = li.error || lo.error; return; }
    // A listed message whose metadata failed must not silently fall back to an older one (Tim Eger, 10-29 test).
    if ((li.messages || []).concat(lo.messages || []).some(function (m) { return !M[m.id]; })) {
      errors[a] = 'metadata missing'; return;
    }
    const inbound = (li.messages || []).map(function (m) { return M[m.id]; }).filter(Boolean);
    const outbound = (lo.messages || []).map(function (m) { return M[m.id]; }).filter(Boolean);
    const ooo = inbound.filter(function (m) { return OOO.test(m.subject) || OOO.test(m.snippet.slice(0, 200)); });
    const real = inbound.filter(function (m) { return ooo.indexOf(m) < 0; });
    res[a] = {inb: real[0], out: outbound[0], ooo: ooo[0]};
  });
  const bounces = {};
  (bl.messages || []).forEach(function (x) {
    const m = M[x.id]; if (!m) return;
    const text = (m.snippet + ' ' + m.subject).toLowerCase();
    addrs.forEach(function (a) { if (text.indexOf(a) >= 0 && (!bounces[a] || m.date > bounces[a].date)) bounces[a] = m; });
  });
  const drafts = {};
  (dl.drafts || []).forEach(function (d) {
    const m = M[d.message.id]; if (!m) return;
    ((m.to + ' ' + m.cc).toLowerCase().match(ADDR) || []).forEach(function (a) { (drafts[a] = drafts[a] || []).push(d.id); });
  });
  const fresh = {};
  (nl.messages || []).forEach(function (x) {
    const m = M[x.id]; if (!m) return;
    const outgoing = m.from.toLowerCase().indexOf(ME) >= 0;
    ((outgoing ? m.to + ' ' + m.cc : m.from).toLowerCase().match(ADDR) || []).forEach(function (a) {
      if (a !== ME && !known[a] && !SKIP_NEW.test(a) && !fresh[a]) fresh[a] = [a, outgoing ? 'out' : 'in', m.date, m.subject];
    });
  });

  // One line per tracker row; a cell with several addresses takes the latest of each field across them.
  let checked = 0, onRows = 0;
  const notChecked = [];
  const table = rows.map(function (r) {
    const g = r.emails.map(function (a) { return res[a]; }).filter(Boolean);
    const err = r.emails.map(function (a) { return errors[a]; }).filter(Boolean).join('; ');
    if (g.length === r.emails.length) checked++; else notChecked.push('r' + r.row + ' ' + r.name + ' (' + (err || 'not reached') + ')');
    const pick = function (k) { return g.map(function (x) { return x[k]; }).filter(Boolean).sort(byDate_)[0]; };
    const inb = pick('inb'), out = pick('out'), ooo = pick('ooo');
    const b = r.emails.map(function (a) { return bounces[a]; }).filter(Boolean).sort(byDate_)[0];
    const d = [].concat.apply([], r.emails.map(function (a) { return drafts[a] || []; }));
    if (d.length) onRows++;
    return [r.row, r.name, r.company, r.emails.join('; '), r.status, r.last, r.flag,
            inb ? inb.date : '', inb ? inb.subject : '', inb ? inb.thread : '',
            out ? out.date : '', out ? out.subject : '', out ? out.thread : '',
            ooo ? ooo.date : '', ooo ? ooo.subject : '', ooo ? ooo.snippet.slice(0, 240) : '',
            b ? b.date : '', b ? b.subject : '', d.length, d.join(' '), err];
  });
  writeTab_(out, 'Prep_Rows', ['row', 'name', 'company', 'email', 'status', 'sheet_last_contact', 'flag',
      'in_date', 'in_subject', 'in_thread', 'out_date', 'out_subject', 'out_thread',
      'ooo_date', 'ooo_subject', 'ooo_snippet', 'bounce_date', 'bounce_subject', 'drafts', 'draft_ids', 'error'], table);
  writeTab_(out, 'Prep_New', ['address', 'direction', 'date', 'subject'], Object.keys(fresh).map(function (a) { return fresh[a]; }));

  const partial = checked < rows.length || FAILS.meta > 0 || Date.now() - T0 > TIME_LIMIT_MS;
  return {status: partial ? 'PARTIAL' : 'OK', tracker_id: found[0], ACTIVE: rows.length, CHECKED: checked,
          meta_failed: FAILS.meta, fail_samples: FAILS.samples.join(' | '),
          not_checked: notChecked.join(' | '), drafts_total: (dl.drafts || []).length, drafts_on_rows: onRows,
          new_contacts_days: NEW_DAYS, new_contacts: Object.keys(fresh).length};
}

/**
 * Step 0a thread list, its own daily run (~05:00 UTC) so the row check keeps the whole 6-min budget:
 * every thread Spencer STARTED (Sent last 21 days + Scheduled) to an external address.
 * The Digest reconciles it against memory/followups-queue.md (that lives in the repo, not here).
 * Status goes to Prep_ThreadMeta.
 */
function runThreads() {
  T0 = Date.now();
  FAILS = {meta: 0, thread: 0, samples: []};
  const out = SpreadsheetApp.openById(PREP_SHEET_ID);
  const meta = {run_utc: iso_(new Date()), status: 'RUNNING'};
  writeMeta_(out, meta, 'Prep_ThreadMeta');
  try {
    Gmail.Users.getProfile('me');
    TOKEN = ScriptApp.getOAuthToken();
    const threads = threads_();
    writeTab_(out, 'Prep_Threads', ['thread', 'date', 'to', 'subject', 'messages', 'inbound', 'scheduled'], threads);
    const partial = FAILS.thread > 0 || Date.now() - T0 > TIME_LIMIT_MS;
    Object.assign(meta, {status: partial ? 'PARTIAL' : 'OK', thread_days: THREAD_DAYS, threads: threads.length,
                         thread_failed: FAILS.thread, fail_samples: FAILS.samples.join(' | ')});
  } catch (e) {
    meta.status = 'ERROR';
    meta.error = String(e && e.stack || e).slice(0, 1000);
  }
  meta.finished_utc = iso_(new Date());
  meta.runtime_s = Math.round((Date.now() - T0) / 1000);
  writeMeta_(out, meta, 'Prep_ThreadMeta');
}

function threads_() {
  const ids = {};
  ['in:sent newer_than:' + THREAD_DAYS + 'd', 'in:scheduled'].forEach(function (q) {
    let tok = '';
    do {
      const l = getAll_([list_(q, 500) + (tok ? '&pageToken=' + tok : '')])[0];
      if (l.error) throw new Error('thread list: ' + l.error);
      (l.messages || []).forEach(function (m) { ids[m.threadId] = 1; });
      tok = l.nextPageToken || '';
    } while (tok);
  });
  const keys = Object.keys(ids);
  const got = getAll_(keys.map(function (t) {
    return 'threads/' + t + '?format=metadata&metadataHeaders=From&metadataHeaders=To&metadataHeaders=Cc' +
        '&metadataHeaders=Subject&metadataHeaders=Date&fields=messages(labelIds,payload/headers)';
  }));
  const rows = [];
  keys.forEach(function (t, i) {
    if (got[i].error) {
      FAILS.thread++;
      if (FAILS.samples.length < 3) FAILS.samples.push(String(got[i].error).slice(0, 160));
      return;
    }
    const msgs = got[i].messages || [];
    if (!msgs.length) return;
    const h = heads_(msgs[0]);
    if ((h.from || '').toLowerCase().indexOf(ME) < 0) return;  // not started by Spencer
    const rc = ((h.to || '') + ' ' + (h.cc || '')).toLowerCase().match(ADDR) || [];
    const ext = rc.filter(function (a, k) { return SELF.indexOf(a) < 0 && rc.indexOf(a) === k; });
    if (!ext.length) return;  // only to himself
    const inbound = msgs.some(function (m) { return (heads_(m).from || '').toLowerCase().indexOf(ME) < 0; });
    const scheduled = msgs.some(function (m) { return (m.labelIds || []).indexOf('SCHEDULED') >= 0; });
    rows.push([t, h.date || '', ext.join('; '), h.subject || '', msgs.length, inbound, scheduled]);
  });
  return rows;
}

function list_(q, n) {
  return 'messages?q=' + encodeURIComponent(q) + '&maxResults=' + n + '&fields=messages(id,threadId),nextPageToken';
}

/** Metadata for many message ids, as {id: {date, thread, from, to, cc, subject, snippet}}. */
function metas_(ids) {
  const got = getAll_(ids.map(function (id) { return 'messages/' + id + META; }));
  const out = {};
  ids.forEach(function (id, i) {
    const m = got[i];
    if (!m || m.error) {
      FAILS.meta++;
      if (FAILS.samples.length < 3) FAILS.samples.push(String(m && m.error).slice(0, 160));
      return;
    }
    const h = heads_(m);
    const ms = Number(m.internalDate) || Date.parse(h.date || '') || 0;
    out[id] = {date: Utilities.formatDate(new Date(ms), 'Etc/UTC', 'yyyy-MM-dd'), ts: ms, thread: m.threadId,
               from: h.from || '', to: h.to || '', cc: h.cc || '', subject: h.subject || '', snippet: m.snippet || ''};
  });
  return out;
}

function heads_(m) {
  const h = {};
  ((m.payload || {}).headers || []).forEach(function (x) { h[x.name.toLowerCase()] = x.value; });
  return h;
}

/** GETs Gmail REST paths in parallel batches; retries 429/5xx with backoff; never writes. */
function getAll_(paths) {
  const out = new Array(paths.length);
  const last = {};
  let todo = paths.map(function (p, i) { return i; });
  // Gmail's quota is per minute, so backoff runs past a full minute (2+4+8+16+30+30 s) before giving up.
  for (let attempt = 0; attempt < 7 && todo.length; attempt++) {
    if (attempt) Utilities.sleep(1000 * Math.min(30, Math.pow(2, attempt)));
    const retry = [];
    for (let s = 0; s < todo.length; s += BATCH) {
      if (Date.now() - T0 > TIME_LIMIT_MS) { todo.slice(s).forEach(function (i) { out[i] = {error: 'time limit'}; }); break; }
      const chunk = todo.slice(s, s + BATCH);
      const started = Date.now();
      const units = chunk.reduce(function (u, i) { return u + (paths[i].indexOf('threads/') === 0 ? 10 : 5); }, 0);
      const res = UrlFetchApp.fetchAll(chunk.map(function (i) {
        return {url: API + paths[i], method: 'get', muteHttpExceptions: true, headers: {Authorization: 'Bearer ' + TOKEN}};
      }));
      res.forEach(function (r, k) {
        const code = r.getResponseCode(), i = chunk[k];
        if (code === 200) out[i] = JSON.parse(r.getContentText());
        else if (code === 204) out[i] = {};  // partial response with nothing in it = zero matches
        else if (code === 429 || code >= 500 || (code === 403 && /quota|rateLimit/i.test(r.getContentText()))) {
          retry.push(i);
          last[i] = code + ' ' + r.getContentText().replace(/\s+/g, ' ').slice(0, 120);
        }
        else out[i] = {error: code + ' ' + r.getContentText().slice(0, 200)};
      });
      // Pace to UNITS_PER_S, under Gmail's 15,000 units/min per user (get/list = 5 units, threads.get = 10).
      const wait = units * 1000 / UNITS_PER_S - (Date.now() - started);
      if (wait > 0) Utilities.sleep(wait);
    }
    todo = retry;
  }
  todo.forEach(function (i) { out[i] = {error: 'retries exhausted: ' + last[i]}; });
  return out;
}

/**
 * Watchdog (2026-10-29, replaces the Morning Build 13:05 UTC cloud run; plan step 2). Hourly, weekdays
 * 08-18 UTC, from this separate project so it still fires when the Follow-up Sender itself is down.
 * Read-only; emails Spencer once a day per problem:
 *  1. Sender heartbeat (Queue Sheet Log!F1) older than 15 min.
 *  2. A QUEUED row more than 30 min past its local send time.
 *  3. A cold touch 2/3 reply sitting in Gmail Drafts (thread has only Spencer's 1-2 sent messages,
 *     started in the last 30 days). Warm drafts (any inbound) and LT touches (3+ sent) are left alone.
 * Ledger gaps (a due touch nobody queued) stay with the 04:05 Morning Build Stage 4, the Digest and Prep.
 */
function watchdog() {
  const now = new Date();
  const h = now.getUTCHours(), dow = now.getUTCDay();
  if (dow === 0 || dow === 6 || h < 8 || h > 18) return;
  const issues = watchIssues_(now);
  const props = PropertiesService.getScriptProperties();
  const day = Utilities.formatDate(now, 'Etc/UTC', 'yyyy-MM-dd');
  const fresh = issues.filter(function (i) { return props.getProperty('wd_' + day + '_' + i[0]) === null; });
  if (!fresh.length) return;
  MailApp.sendEmail(ME, '[Bingo] Watchdog: ' + fresh.length + ' follow-up problem' + (fresh.length > 1 ? 's' : ''),
      fresh.map(function (i) { return '- ' + i[1]; }).join('\n') +
      '\n\nQueue: https://docs.google.com/spreadsheets/d/' + PREP_SHEET_ID +
      '\n(Bingo Digest Prep watchdog; one email per problem per day.)', {name: 'Bingo watchdog'});
  fresh.forEach(function (i) { props.setProperty('wd_' + day + '_' + i[0], '1'); });
}

/** Test from the editor: writes what watchdog() would report to tab Prep_Watchdog, sends nothing. */
function watchdogDryRun() {
  const issues = watchIssues_(new Date());
  writeTab_(SpreadsheetApp.openById(PREP_SHEET_ID), 'Prep_Watchdog', ['key', 'issue', 'checked_utc'],
      (issues.length ? issues : [['none', 'no problems found']]).map(function (i) { return [i[0], i[1], iso_(new Date())]; }));
}

function watchIssues_(now) {
  const issues = [];
  const ss = SpreadsheetApp.openById(PREP_SHEET_ID);

  const beat = String(ss.getSheetByName('Log').getRange('F1').getDisplayValue());
  const age = (now - new Date(beat)) / 60000;
  if (!(age <= 15)) issues.push(['sender-down', 'Follow-up sender down since ' + beat + ' (heartbeat ' +
      (isNaN(age) ? 'unreadable' : Math.round(age) + ' min old') + '). Queued follow-ups will not go out until it runs again.']);

  const q = ss.getSheetByName('Queue').getDataRange().getDisplayValues();
  for (let r = 1; r < q.length; r++) {
    if (String(q[r][0]).trim().toUpperCase() !== 'QUEUED' || !q[r][6] || !q[r][7]) continue;
    let tz = String(q[r][5]).trim();
    if (tz.toUpperCase() === 'US' || !tz) tz = 'America/Los_Angeles';
    let local;
    try { local = Utilities.formatDate(new Date(now.getTime() - 30 * 60000), tz, 'yyyy-MM-dd HH:mm'); }
    catch (e) { local = Utilities.formatDate(new Date(now.getTime() - 30 * 60000), 'Etc/UTC', 'yyyy-MM-dd HH:mm'); }
    if (q[r][6] + ' ' + q[r][7] < local) {
      issues.push(['stuck-' + (r + 1), 'Queue row ' + (r + 1) + ' still QUEUED past its send time: touch ' + q[r][1] +
          ' to ' + q[r][2] + ' (' + q[r][3] + '), due ' + q[r][6] + ' ' + q[r][7] + ' ' + q[r][5] + '.']);
    }
  }

  const drafts = (Gmail.Users.Drafts.list('me', {maxResults: 100}).drafts || []);
  drafts.forEach(function (d) {
    const m = Gmail.Users.Messages.get('me', d.message.id, {format: 'metadata', metadataHeaders: ['In-Reply-To', 'Subject', 'To']});
    const hm = heads_(m);
    if (!hm['in-reply-to']) return;  // not a reply
    const t = Gmail.Users.Threads.get('me', m.threadId, {format: 'metadata', metadataHeaders: ['From']});
    const sent = (t.messages || []).filter(function (x) { return (x.labelIds || []).indexOf('DRAFT') < 0; });
    const allMine = sent.every(function (x) { return (heads_(x).from || '').toLowerCase().indexOf(ME) >= 0; });
    const recent = sent.length && now - Number(sent[0].internalDate) < 30 * 86400000;
    if (allMine && recent && sent.length <= 2) {
      issues.push(['draft-' + d.id, 'Cold touch ' + (sent.length + 1) + ' sitting in Drafts (should be a Queue row): "' +
          (hm.subject || '') + '" to ' + (hm.to || '') + ' (draft ' + d.id + ').']);
    }
  });
  return issues;
}

function byDate_(a, b) { return b.ts - a.ts; }

function writeTab_(ss, name, header, rows) {
  const sh = ss.getSheetByName(name) || ss.insertSheet(name);
  sh.clearContents();
  const data = [header].concat(rows).map(function (r) {
    return r.map(function (v) { return typeof v === 'string' ? v.slice(0, 500) : v; });
  });
  const range = sh.getRange(1, 1, data.length, header.length);
  range.setNumberFormat('@');
  range.setValues(data);
}

function writeMeta_(ss, meta, tab) {
  writeTab_(ss, tab || 'Prep_Meta', ['key', 'value'], Object.keys(meta).map(function (k) { return [k, String(meta[k])]; }));
  SpreadsheetApp.flush();  // RUNNING must be visible at once, not buffered until the run ends
}

function iso_(d) { return Utilities.formatDate(d, 'Etc/UTC', "yyyy-MM-dd'T'HH:mm:ss'Z'"); }
