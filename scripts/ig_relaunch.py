#!/usr/bin/env python3
"""
מריץ מחדש את תור האינסטגרם אחרי שהחשבון הפך לעסקי.
בודק שבאפר באמת רואה business, מוחק את מה שתוזמן במצב תזכורת, ומתזמן הכול מחדש אוטומטי.

  python3 scripts/ig_relaunch.py --from 2026-08-16
"""
import os, sys, json, time, argparse, subprocess, urllib.request, urllib.error

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ORG = "6a75d6fe86d18905e5fbe108"
TOKEN = os.environ.get("BUFFER_ACCESS_TOKEN")
STATE = os.path.join(ROOT, ".ig-scheduled.json")

def gql(q, v=None):
    if not TOKEN: sys.exit("BUFFER_ACCESS_TOKEN חסר.  set -a && . ./.env && set +a")
    b = {"query": q}
    if v: b["variables"] = v
    r = urllib.request.Request("https://api.buffer.com/", data=json.dumps(b).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + TOKEN})
    for i in range(6):
        try: return json.loads(urllib.request.urlopen(r).read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                w = 70 * (i + 1); print("   … מגבלת קצב, ממתין %ds" % w, flush=True); time.sleep(w); continue
            sys.exit("Buffer HTTP %s: %s" % (e.code, e.read().decode()[:300]))
    sys.exit("מגבלת קצב לא התפנתה.")

ap = argparse.ArgumentParser(); ap.add_argument("--from", dest="start", required=True)
ap.add_argument("--force", action="store_true", help="להמשיך גם אם באפר עדיין מדווח profile")
a = ap.parse_args()

ch = next((c for c in gql('{channels(input:{organizationId:"%s"}){id name service type isDisconnected}}' % ORG)
           ["data"]["channels"] if c["service"] == "instagram"), None)
if not ch: sys.exit("אין ערוץ אינסטגרם בבאפר.")
print("ערוץ: %s  ·  id %s  ·  type=%s  ·  מנותק=%s" % (ch["name"], ch["id"], ch["type"], ch["isDisconnected"]))

if ch["type"] != "business" and not a.force:
    sys.exit("\n❌ באפר עדיין רואה את החשבון כ-profile ולא כ-business.\n"
             "   סוג החשבון נשמר ברגע החיבור, ולכן צריך לחבר מחדש:\n"
             "   Buffer → Channels → אינסטגרם → Disconnect/Remove → Connect → Instagram\n"
             "   ולבחור את החשבון העסקי (יעבור דרך פייסבוק).\n"
             "   אחר כך להריץ שוב את הפקודה הזו.")

# 1. מוחקים כל פוסט אינסטגרם קיים (הם תוזמנו במצב תזכורת)
d = gql('{posts(input:{organizationId:"%s",filter:{channelIds:["%s"]}}){edges{node{id status}}}}'
        % (ORG, ch["id"]))
edges = (((d.get("data") or {}).get("posts") or {}).get("edges")) or []
old = [e["node"]["id"] for e in edges]
print("\nנמצאו %d פוסטים קיימים בערוץ — מוחק." % len(old))
DEL = "mutation($id: PostId!){ deletePost(input:{id:$id}){ __typename ... on MutationError { message } } }"
for i, pid in enumerate(old, 1):
    r = gql(DEL, {"id": pid})
    t = ((r.get("data") or {}).get("deletePost") or {}).get("__typename", "?")
    print("  %2d/%d  %s" % (i, len(old), t))
    time.sleep(3)

# 2. מאפסים מצב ומריצים את המתזמן הרגיל
if os.path.exists(STATE): os.remove(STATE)
print("\nמתזמן מחדש את כל 30 הפוסטים במצב אוטומטי…\n")
subprocess.call([sys.executable, "-u", os.path.join(ROOT, "scripts/push_instagram.py"), "--from", a.start])
