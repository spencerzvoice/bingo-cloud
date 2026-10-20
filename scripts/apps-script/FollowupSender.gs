/**
 * Bingo Follow-up Sender (Spencer, 2026-10-20: "This needs to be done offline").
 * Lives in spencer@spencerzvoice.com's own Apps Script, runs on Google's servers.
 * The cloud routines never make touch 2/3 drafts: they append a row to the queue Sheet.
 * Every minute tick() sends each QUEUED row at its local send time (touch 2 = 09:04,
 * touch 3 = 10:13 contact-local) as a reply in the original thread, after a last
 * no-contact check. Anything held or failed = instant alert email.
 * Source of truth: scripts/apps-script/FollowupSender.gs in the bingo repo.
 */
const SHEET_ID = '1YVJbPnETd3gkX8dAwdHsiqijojgMlyCL_4Jaskk9aao';
const ME = 'spencer@spencerzvoice.com';
const FROM = 'Spencer Pearman <spencer@spencerzvoice.com>';
const ALERT_TO = 'spencer@spencerzvoice.com';
const WINDOW_START = '08:32';
const WINDOW_END = '15:00';
const C = {status: 0, touch: 1, name: 2, company: 3, to: 4, tz: 5, date: 6, time: 7,
           thread: 8, draft: 9, body: 10, lastTouch: 11, queuedBy: 12, sentAt: 13,
           sentId: 14, note: 15};

/** Run once from the editor: installs the every-minute sender and the evening preview. */
function setup() {
  ScriptApp.getProjectTriggers().forEach(function (t) { ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('tick').timeBased().everyMinutes(1).create();
  ScriptApp.newTrigger('eveningPreview').timeBased().atHour(19).nearMinute(0)
      .everyDays(1).inTimezone('Europe/Lisbon').create();
  log_('setup', 'triggers installed: tick every 1 min, eveningPreview 19:00 Lisbon');
  return ScriptApp.getProjectTriggers().map(function (t) { return t.getHandlerFunction(); });
}

function tick() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) return;
  try {
    const ss = SpreadsheetApp.openById(SHEET_ID);
    ss.getSheetByName('Log').getRange('E1:F1').setValues([['last tick (UTC)', iso_(new Date())]]);
    const sh = ss.getSheetByName('Queue');
    const rows = sh.getDataRange().getDisplayValues();
    for (let r = 1; r < rows.length; r++) {
      const row = rows[r];
      if (String(row[C.status]).trim().toUpperCase() !== 'QUEUED') continue;
      try {
        if (row[C.draft] && !row[C.body]) absorbDraft_(sh, r, row);
        else maybeSend_(sh, r, row);
      } catch (e) {
        set_(sh, r, {status: 'ERROR', note: String(e).slice(0, 400)});
        alert_('Follow-up FAILED: ' + row[C.name] + ' (' + row[C.company] + ')',
               'Touch ' + row[C.touch] + ' to ' + row[C.to] + ' did not send.\n\nError: ' + e +
               '\n\nQueue: https://docs.google.com/spreadsheets/d/' + SHEET_ID);
      }
    }
  } finally {
    lock.releaseLock();
  }
}

/** Moves an existing Gmail draft into the queue row (body + thread) and deletes the draft. */
function absorbDraft_(sh, r, row) {
  const d = GmailApp.getDraft(row[C.draft]);
  const m = d.getMessage();
  const body = m.getPlainBody().replace(/\s+$/, '');
  if (!body) throw new Error('draft ' + row[C.draft] + ' has an empty body');
  set_(sh, r, {body: body, thread: m.getThread().getId(), to: row[C.to] || m.getTo()});
  d.deleteDraft();
  log_('absorbed', row[C.name] + ' draft ' + row[C.draft] + ' -> queue, draft deleted');
}

function maybeSend_(sh, r, row) {
  const tz = zone_(row[C.tz]);
  if (!tz) throw new Error('unknown time zone "' + row[C.tz] + '"');
  const sendTime = hhmm_(row[C.time]);
  if (sendTime < WINDOW_START || sendTime >= WINDOW_END) throw new Error('send time ' + sendTime + ' is outside 08:32-15:00');
  if (!row[C.thread] || !row[C.body]) throw new Error('row missing thread_id or body');
  const now = new Date();
  const zones = row[C.tz].trim().toUpperCase() === 'US' ? ['America/New_York', 'America/Los_Angeles'] : [tz];
  const localDate = Utilities.formatDate(now, tz, 'yyyy-MM-dd');
  const localTime = Utilities.formatDate(now, tz, 'HH:mm');
  const day = Utilities.formatDate(now, tz, 'EEE');
  if (day === 'Sat' || day === 'Sun') return;
  if (localDate < String(row[C.date]).trim()) return;
  if (localTime < sendTime) return;
  for (let i = 0; i < zones.length; i++) {
    const t = Utilities.formatDate(now, zones[i], 'HH:mm');
    if (t < WINDOW_START || t >= WINDOW_END) return; // wait for the next weekday
  }

  const hold = noContactCheck_(row);
  if (hold) {
    set_(sh, r, {status: 'HELD', note: hold});
    log_('held', row[C.name] + ': ' + hold);
    alert_('Follow-up HELD: ' + row[C.name] + ' (' + row[C.company] + ')',
           'Touch ' + row[C.touch] + ' to ' + row[C.to] + ' was NOT sent.\nReason: ' + hold +
           '\n\nQueue: https://docs.google.com/spreadsheets/d/' + SHEET_ID);
    return;
  }

  const id = sendReply_(row);
  set_(sh, r, {status: 'SENT', sentAt: iso_(new Date()), sentId: id,
               note: 'sent ' + localDate + ' ' + Utilities.formatDate(new Date(), tz, 'HH:mm') + ' ' + tz});
  log_('sent', row[C.name] + ' (' + row[C.company] + ') touch ' + row[C.touch] + ' msg ' + id);
}

/** Returns a reason to hold, or '' if clear. Spencer's rule: any email or LinkedIn contact since the last touch = don't send. */
function noContactCheck_(row) {
  const email = String(row[C.to]).trim().toLowerCase();
  const domain = email.split('@')[1] || '';
  const thread = GmailApp.getThreadById(row[C.thread]);
  if (!thread) return 'thread ' + row[C.thread] + ' not found';
  const msgs = thread.getMessages();
  let last = null;
  for (let i = 0; i < msgs.length; i++) {
    const m = msgs[i];
    if (m.isDraft()) continue;
    const fromMe = m.getFrom().toLowerCase().indexOf(ME) !== -1;
    if (fromMe) { last = m.getDate(); continue; }
    if (isAutoReply_(m)) continue; // out-of-office is not contact (Prep 10-19: Brooks OOO "not a hold")
    return 'they wrote in the thread on ' + iso_(m.getDate()) + ' (' + m.getFrom() + ')';
  }
  if (!last) return 'no earlier message from Spencer in the thread';
  const after = Math.floor(last.getTime() / 1000) + 60;
  const generic = /^(gmail|googlemail|yahoo|hotmail|outlook|icloud|me|aol|proton|protonmail)\./.test(domain);
  const fromQ = generic ? email : domain;
  const inbound = GmailApp.search('from:' + fromQ + ' after:' + after, 0, 20);
  for (let i = 0; i < inbound.length; i++) {
    const ms = inbound[i].getMessages();
    for (let j = 0; j < ms.length; j++) {
      const m = ms[j];
      if (m.getDate().getTime() / 1000 < after || m.getFrom().toLowerCase().indexOf(fromQ) === -1) continue;
      if (!isAutoReply_(m)) return 'inbound mail from ' + m.getFrom() + ' on ' + iso_(m.getDate());
    }
  }
  if (GmailApp.search('in:sent to:' + email + ' after:' + after, 0, 1).length) return 'Spencer already emailed them since the last touch';
  if (GmailApp.search('in:scheduled to:' + email, 0, 1).length) return 'another email to them is already in Scheduled';
  const name = String(row[C.name]).trim();
  if (name && GmailApp.search('from:linkedin.com "' + name + '" after:' + after, 0, 1).length) return 'LinkedIn notification naming ' + name + ' since the last touch';
  return '';
}

/** Sends the body as a threaded reply through the Gmail REST API (keeps In-Reply-To/References). */
function sendReply_(row) {
  // Gmail advanced service (Services > Gmail API, identifier "Gmail"); plain REST calls got 403 "Gmail API not enabled" (self-test 10-20).
  const tr = Gmail.Users.Threads.get('me', row[C.thread],
      {format: 'metadata', metadataHeaders: ['Message-ID', 'References', 'Subject']});
  const msgs = (tr.messages || []).filter(function (m) { return (m.labelIds || []).indexOf('DRAFT') === -1; });
  if (!msgs.length) throw new Error('thread has no messages');
  const h = function (m, n) {
    const x = (m.payload.headers || []).filter(function (y) { return y.name.toLowerCase() === n.toLowerCase(); })[0];
    return x ? x.value : '';
  };
  const lastMsg = msgs[msgs.length - 1];
  const msgId = h(lastMsg, 'Message-ID');
  const refs = (h(lastMsg, 'References') + ' ' + msgId).trim();
  const subj = h(msgs[0], 'Subject').replace(/^(re:\s*)+/i, '');
  const mime = [
    'From: ' + FROM,
    'To: ' + row[C.to],
    'Subject: =?UTF-8?B?' + Utilities.base64Encode('Re: ' + subj, Utilities.Charset.UTF_8) + '?=',
    'In-Reply-To: ' + msgId,
    'References: ' + refs,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset="UTF-8"',
    'Content-Transfer-Encoding: base64',
    '',
    Utilities.base64Encode(String(row[C.body]), Utilities.Charset.UTF_8)
  ].join('\r\n');
  const sent = Gmail.Users.Messages.send(
      {raw: Utilities.base64EncodeWebSafe(mime, Utilities.Charset.UTF_8), threadId: row[C.thread]}, 'me');
  if (!sent || !sent.id) throw new Error('Gmail send returned no message id');
  return sent.id;
}

/** 19:00 Lisbon: email Spencer who gets followed up next (his alert, works with the PC off). */
function eveningPreview() {
  const rows = SpreadsheetApp.openById(SHEET_ID).getSheetByName('Queue').getDataRange().getDisplayValues().slice(1)
      .filter(function (r) { return String(r[C.status]).trim().toUpperCase() === 'QUEUED'; });
  if (!rows.length) return;
  const lines = rows.map(function (r) {
    return '- ' + r[C.name] + ' (' + r[C.company] + '), touch ' + r[C.touch] + ', ' + r[C.date] + ' ' + hhmm_(r[C.time]) + ' ' + r[C.tz];
  });
  alert_(rows.length + ' follow-up' + (rows.length === 1 ? '' : 's') + ' queued to send automatically',
         'These go out at their local send time. Nothing for you to do.\n\n' + lines.join('\n') +
         '\n\nQueue: https://docs.google.com/spreadsheets/d/' + SHEET_ID);
}

/** Self-test: starts a thread to Spencer's own address, then sends a threaded reply through sendReply_. Logs both ids. */
function selfTest() {
  const subj = 'Bingo sender self-test ' + iso_(new Date());
  GmailApp.sendEmail(ME, subj, 'Thread starter for the follow-up sender self-test. Safe to delete.');
  Utilities.sleep(4000);
  const t = GmailApp.search('subject:"' + subj + '"', 0, 1)[0];
  if (!t) throw new Error('self-test thread not found');
  const row = [];
  row[C.to] = ME; row[C.thread] = t.getId();
  row[C.body] = 'Self-test reply from the Bingo Follow-up Sender. If this sits in the same thread as the starter, threading works. Safe to delete.';
  const id = sendReply_(row);
  Utilities.sleep(3000);
  const n = GmailApp.getThreadById(t.getId()).getMessageCount();
  log_('selftest', 'thread ' + t.getId() + ' reply ' + id + ' messages in thread: ' + n);
  return 'thread ' + t.getId() + ', reply ' + id + ', messages in thread ' + n;
}

/** Writes dryRun() to the Log sheet so it can be read remotely. */
function dryRunLog() {
  dryRun().forEach(function (l) { log_('dryrun', l); });
}

/** Debug helper: what tick() would do for every QUEUED row right now, without sending. */
function dryRun() {
  const rows = SpreadsheetApp.openById(SHEET_ID).getSheetByName('Queue').getDataRange().getDisplayValues();
  const out = [];
  for (let r = 1; r < rows.length; r++) {
    const row = rows[r];
    if (String(row[C.status]).trim().toUpperCase() !== 'QUEUED') continue;
    const tz = zone_(row[C.tz]);
    out.push(row[C.name] + ' | ' + tz + ' local now ' + (tz ? Utilities.formatDate(new Date(), tz, 'EEE yyyy-MM-dd HH:mm') : '?') +
             ' | send ' + row[C.date] + ' ' + hhmm_(row[C.time]) + ' | body ' + (row[C.body] ? 'ok' : (row[C.draft] ? 'draft to absorb' : 'MISSING')) +
             ' | check: ' + (row[C.thread] ? (noContactCheck_(row) || 'clear') : 'n/a'));
  }
  return out;
}

function isAutoReply_(m) {
  const auto = String(m.getHeader('Auto-Submitted') || '').toLowerCase();
  if (auto && auto !== 'no') return true;
  return /automatic reply|auto-?reply|out of (the )?office|abwesenheit|fuera de la oficina/i.test(m.getSubject());
}
function zone_(z) {
  z = String(z || '').trim();
  if (!z) return '';
  if (z.toUpperCase() === 'US') return 'America/Los_Angeles';
  try { Utilities.formatDate(new Date(), z, 'HH:mm'); return z; } catch (e) { return ''; }
}
function hhmm_(t) {
  const m = String(t).trim().match(/^(\d{1,2}):(\d{2})/);
  return m ? ('0' + m[1]).slice(-2) + ':' + m[2] : String(t);
}
function iso_(d) { return Utilities.formatDate(d, 'UTC', "yyyy-MM-dd'T'HH:mm:ss'Z'"); }
function set_(sh, r, f) {
  Object.keys(f).forEach(function (k) { sh.getRange(r + 1, C[k] + 1).setNumberFormat('@').setValue(f[k]); });
}
function log_(event, detail) {
  SpreadsheetApp.openById(SHEET_ID).getSheetByName('Log').appendRow([iso_(new Date()), event, detail]);
}
function alert_(subject, body) {
  GmailApp.sendEmail(ALERT_TO, '[Bingo] ' + subject, body, {name: 'Bingo follow-ups'});
}
