#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ממלא ימים חסרים בתור האינסטגרם ומסנכרן את קובץ המצב מול מה שבאמת פורסם.
   --topup הרגיל ממשיך מהתאריך האחרון בתור, ולכן הוא לא רואה חור באמצע."""
import os, json, io, re, time, urllib.request, urllib.error
from datetime import datetime, timedelta, timezone

T = os.environ["BUFFER_ACCESS_TOKEN"]
ORG = "6a75d6fe86d18905e5fbe108"
IG = "6a7f6bf6b2d9d577437ac2f9"
SITE = "https://berg-law.co.il"
HOUR = 16                     # 19:00 שעון ישראל
DAYS = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
CAP = 10
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def gq(q, v=None):
    b = {"query": q}
    if v:
        b["variables"] = v
    r = urllib.request.Request("https://api.buffer.com/", data=json.dumps(b).encode(),
                               headers={"Authorization": "Bearer " + T, "Content-Type": "application/json"})
    for a in range(5):
        try:
            return json.loads(urllib.request.urlopen(r).read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(70 * (a + 1)); continue
            return {"HTTP": e.code, "body": e.read().decode()[:300]}
    return {}


def head(u):
    try:
        return urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=10).status
    except Exception as e:
        return getattr(e, "code", 0)


Q = """query($i:PostsInput!){ posts(input:$i){ edges{ node{ status dueAt sentAt
 assets{ ... on ImageAsset { source } } } } } }"""
MUT = ("mutation($input: CreatePostInput!){ createPost(input:$input){ __typename "
       "... on PostActionSuccess { post { id dueAt } } ... on MutationError { message } } }")

ns = [x["node"] for x in gq(Q, {"i": {"organizationId": ORG, "filter": {"channelIds": [IG]}}})
      ["data"]["posts"]["edges"]]


def slug(n):
    for a in n["assets"]:
        m = re.search(r"/ig/([^/]+)/", a.get("source") or "")
        if m:
            return m.group(1)
    return None


sched = sorted((n for n in ns if n["status"] == "scheduled"), key=lambda n: n["dueAt"])
sent = [n for n in ns if n.get("sentAt")]

# 1. סנכרון מצב: כל מה שפורסם או מתוזמן חייב להיות מסומן כמנוצל, אחרת יתוזמן שוב
state = set(json.load(io.open(".ig-scheduled.json", encoding="utf8")))
live = {s for s in (slug(n) for n in ns) if s}
added = live - state
if added:
    state |= added
    json.dump(sorted(state), io.open(".ig-scheduled.json", "w", encoding="utf8"), ensure_ascii=False)
    print("סונכרן קובץ המצב — נוספו: %s" % ", ".join(sorted(added)))

# 2. איתור ימים חסרים בין היום למחרת הפוסט האחרון
have = {n["dueAt"][:10] for n in sched}
today = datetime.now(timezone.utc).date()
last = datetime.strptime(sched[-1]["dueAt"][:10], "%Y-%m-%d").date() if sched else today
gaps = []
d = today + timedelta(days=1)
while d <= last:
    if d.isoformat() not in have:
        gaps.append(d)
    d += timedelta(days=1)
print("בתור: %d · חורים: %s" % (len(sched), ", ".join(g.isoformat() for g in gaps) or "אין"))
if not gaps:
    raise SystemExit(0)

posts = json.load(io.open("content/instagram-posts.json", encoding="utf8"))
room = CAP - len(sched)
print("מקום פנוי במכסה: %d\n" % room)

for g in gaps:
    if room <= 0:
        print("  המכסה מלאה — שאר החורים יטופלו בהשלמה הבאה"); break
    name = DAYS[(g.weekday() + 1) % 7]
    pool = [p for p in posts if p["day"] == name and p["slug"] not in state]
    if not pool:
        print("  ✗ %s (%s) — אין פוסט פנוי ליום הזה" % (g, name)); continue
    p = pool[0]
    files = sorted(f for f in os.listdir("ig/" + p["slug"]) if f.endswith(".jpg"))
    imgs = ["%s/ig/%s/%s" % (SITE, p["slug"], f) for f in files]
    bad = [u for u in imgs if head(u) != 200]
    if bad:
        print("  ✗ %s — %d תמונות לא חיות, מדלג" % (p["slug"], len(bad))); continue
    d = gq(MUT, {"input": {
        "channelId": IG, "text": p["fullCaption"] + "\n\n" + p["firstComment"],
        "schedulingType": "automatic", "mode": "customScheduled",
        "dueAt": "%sT%02d:00:00.000Z" % (g.isoformat(), HOUR),
        "assets": [{"image": {"url": u, "metadata": {"altText": p["title"]}}} for u in imgs],
        "metadata": {"instagram": {"type": "post", "shouldShareToFeed": True}}}})
    cp = (d.get("data") or {}).get("createPost") or d
    if cp.get("__typename") == "PostActionSuccess":
        print("  ✓ %s (%s)  %s" % (g, name, p["slug"]))
        state.add(p["slug"]); room -= 1
        json.dump(sorted(state), io.open(".ig-scheduled.json", "w", encoding="utf8"), ensure_ascii=False)
    else:
        print("  ✗ %s — %s" % (p["slug"], json.dumps(cp, ensure_ascii=False)[:160]))
    time.sleep(12)
