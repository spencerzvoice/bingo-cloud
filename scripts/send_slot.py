"""Send slot: when may a pitch / follow-up go to this contact? Run it before every Schedule send.

Spencer, 2026-10-15: "Nothing goes out before 8:32AM or after 3PM" / "Its scheduled, otherwise."
Spencer, 2026-10-27, after Bingo scheduled 3 US pitches for the next morning at 17:12 Lisbon (13:12 NY):
"Why are the ones in the US scheduled to go out tomorrow when they can go out today? Its before 3pm no?"
Rule: inside 08:32-15:00 contact-local RIGHT NOW = it goes TODAY (a few minutes from now). Only outside the
window does it wait for the next weekday 08:32 local. "US" = inside the window in both New York and Los Angeles.
Never pick "next 08:32" by habit: this script decides from the live clock.

Usage:
  python scripts/send_slot.py <email or IANA zone or US> [...]
Prints, per contact: local time(s) now, then TODAY <slot> or NEXT <slot>, with the slot in UTC
(= Gmail's "Greenwich Mean Time" schedule dialog on u/3) and Lisbon.
"""
import datetime, json, os, sys
from zoneinfo import ZoneInfo

OPEN, CLOSE = (8, 32), (15, 0)
US = ["America/New_York", "America/Los_Angeles"]
LEAD = datetime.timedelta(minutes=5)  # time to finish the Gmail schedule dialog
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ = json.load(open(os.path.join(ROOT, "reference", "client-acquisition", "CONTACT-TZ.json"), encoding="utf-8"))
UTC, LIS = ZoneInfo("UTC"), ZoneInfo("Europe/Lisbon")


def inside(t_utc, zones):
    for z in zones:
        l = t_utc.astimezone(ZoneInfo(z))
        if l.weekday() >= 5 or not (OPEN <= (l.hour, l.minute) < CLOSE):
            return False
    return True


def next_open(t_utc, zones):
    # earliest weekday 08:32 (in the latest-opening zone) at or after t_utc that is inside every zone's window
    cands = []
    for z in zones:
        l = t_utc.astimezone(ZoneInfo(z))
        d = l.date()
        for _ in range(8):
            o = datetime.datetime(d.year, d.month, d.day, *OPEN, tzinfo=ZoneInfo(z)).astimezone(UTC)
            if o >= t_utc and inside(o, zones):
                cands.append(o)
                break
            d += datetime.timedelta(days=1)
    return min(cands) if cands else None


def slot(arg, now=None):
    now = (now or datetime.datetime.now(UTC)).replace(second=0, microsecond=0)
    zone = TZ.get(arg.lower(), arg) if "@" in arg else arg
    if "@" in arg and arg.lower() not in TZ:
        return arg, None, "NO ZONE in CONTACT-TZ.json: add it first (live LinkedIn / YouTube About)", None
    zones = US if zone == "US" else [zone]
    t = now + LEAD
    if inside(t, zones):
        return arg, zone, "TODAY", t
    return arg, zone, "NEXT", next_open(t, zones)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    now = datetime.datetime.now(UTC)
    print("now: %s UTC / %s Lisbon" % (now.strftime("%a %H:%M"), now.astimezone(LIS).strftime("%H:%M")))
    for a in sys.argv[1:]:
        who, zone, verdict, s = slot(a, now)
        if s is None:
            print("%s: %s" % (who, verdict)); continue
        zs = US if zone == "US" else [zone]
        local = ", ".join("%s %s" % (z.split("/")[-1], now.astimezone(ZoneInfo(z)).strftime("%H:%M")) for z in zs)
        print("%s [%s, now %s]: %s %s UTC (Gmail GMT) = %s Lisbon" % (
            who, zone, local, verdict, s.strftime("%a %Y-%m-%d %H:%M"), s.astimezone(LIS).strftime("%H:%M")))
