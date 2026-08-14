#!/usr/bin/env python3
"""
מתזמן קרוסלות אינסטגרם בבאפר, פוסט אחד ליום.

דורש:  BUFFER_ACCESS_TOKEN בסביבה, וערוץ אינסטגרם מחובר בבאפר.
התמונות נלקחות מהאתר החי (Netlify) — לכן צריך לפרוס לפני ההרצה.

  python3 scripts/push_instagram.py --dry                 # רק מראה מה יתוזמן
  python3 scripts/push_instagram.py --from 2026-08-17     # מתזמן מהתאריך הזה, יום אחרי יום
  python3 scripts/push_instagram.py --from 2026-08-17 --count 14
"""
import os, json, sys, argparse, urllib.request, urllib.error
from datetime import datetime, timedelta, timezone

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SITE = "https://berg-law.co.il"
ORG  = "6a75d6fe86d18905e5fbe108"
TOKEN = os.environ.get("BUFFER_ACCESS_TOKEN")
POST_HOUR_UTC = 16          # 19:00 בישראל (UTC+3) — שעת שיא באינסטגרם
DAYS = ["ראשון","שני","שלישי","רביעי","חמישי","שישי","שבת"]   # 0=ראשון

def gql(query, variables=None):
    if not TOKEN:
        sys.exit("BUFFER_ACCESS_TOKEN חסר. הרץ:  set -a && . ./.env && set +a")
    body = {"query": query}
    if variables: body["variables"] = variables
    req = urllib.request.Request(
        "https://api.buffer.com/", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + TOKEN})
    try:
        return json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e:
        sys.exit("Buffer HTTP %s: %s" % (e.code, e.read().decode()[:400]))

def instagram_channel():
    d = gql('{ channels(input:{organizationId:"%s"}) { id name service } }' % ORG)
    chans = (d.get("data") or {}).get("channels") or []
    for c in chans:
        if c["service"] == "instagram":
            return c
    print("ערוצים מחוברים כרגע:")
    for c in chans: print("   %-16s %s  %s" % (c["service"], c["id"], c["name"]))
    sys.exit("\n❌ אין ערוץ אינסטגרם בבאפר.\n"
             "   1. להפוך את החשבון ל-Instagram Business ולקשר אותו לעמוד פייסבוק\n"
             "   2. בבאפר: Channels → Connect → Instagram\n"
             "   3. להריץ שוב.")

MUT = ("mutation($input: CreatePostInput!) { createPost(input: $input) { __typename "
       "... on PostCreateSuccess { post { id dueAt status } } "
       "... on CoreWebPostCreateError { message } "
       "... on UnauthorizedError { message } } }")

def schedule(post, channel_id, when, dry=False):
    imgs = post["_images"]
    inp = {
        "channelId": channel_id,
        "text": post["fullCaption"],
        "mode": "customScheduled",
        "dueAt": when.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "assets": [{"image": {"url": u, "metadata": {"altText": post["title"]}}} for u in imgs],
        "metadata": {"instagram": {
            "type": "carousel" if len(imgs) > 1 else "post",
            "firstComment": post["firstComment"],
            "shouldShareToFeed": True,
        }},
    }
    if dry:
        print("  [dry] %s  %s  %d תמונות  |  %s" %
              (when.strftime("%d.%m %H:%MZ"), post["day"], len(imgs), post["title"][:46]))
        return True
    d = gql(MUT, {"input": inp})
    cp = (d.get("data") or {}).get("createPost") or {}
    if cp.get("__typename") == "PostCreateSuccess":
        print("  ✓ %s  %s" % (when.strftime("%d.%m %H:%MZ"), post["title"][:52]))
        return True
    print("  ✗ %s  %s" % (post["slug"], cp.get("message") or json.dumps(d)[:220]))
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", help="YYYY-MM-DD — היום הראשון לפרסום")
    ap.add_argument("--count", type=int, default=0, help="כמה פוסטים לתזמן (0 = הכול)")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    posts = json.load(open(os.path.join(ROOT, "content/instagram-posts.json"), encoding="utf8"))
    # לכל פוסט — התמונות שנמצאות בפועל על הדיסק, לפי סדר
    for p in posts:
        d = os.path.join(ROOT, "ig", p["slug"])
        files = sorted(f for f in os.listdir(d)) if os.path.isdir(d) else []
        p["_images"] = ["%s/ig/%s/%s" % (SITE, p["slug"], f) for f in files if f.endswith(".jpg")][:10]
    missing = [p["slug"] for p in posts if not p["_images"]]
    if missing: sys.exit("חסרות תמונות ל: " + ", ".join(missing))

    start = datetime.strptime(a.start, "%Y-%m-%d").replace(tzinfo=timezone.utc) if a.start \
            else datetime.now(timezone.utc) + timedelta(days=1)
    # מסדרים לפי יום בשבוע: כל פוסט יוצא ביום שהוא נכתב עבורו
    by_day = {}
    for p in posts: by_day.setdefault(p["day"], []).append(p)
    queue, cursor, guard = [], start, 0
    while len(queue) < (a.count or len(posts)) and guard < 400:
        guard += 1
        # weekday(): שני=0 … ראשון=6  →  ממירים לאינדקס שבו ראשון=0
        name = DAYS[(cursor.weekday() + 1) % 7]
        pool = by_day.get(name) or []
        if pool:
            queue.append((pool.pop(0), cursor.replace(hour=POST_HOUR_UTC, minute=0, second=0, microsecond=0)))
        cursor += timedelta(days=1)

    ch = instagram_channel() if not a.dry else {"id": "DRY", "name": "(dry run)"}
    print("ערוץ: %s  ·  %d פוסטים  ·  החל מ-%s  ·  %02d:00Z (19:00 שעון ישראל)\n"
          % (ch["name"], len(queue), start.strftime("%d.%m.%Y"), POST_HOUR_UTC))
    ok = sum(schedule(p, ch["id"], w, a.dry) for p, w in queue)
    print("\n%d/%d תוזמנו." % (ok, len(queue)))
    if a.dry: print("זו הרצה יבשה. להסיר --dry כדי לתזמן באמת.")

if __name__ == "__main__":
    main()
