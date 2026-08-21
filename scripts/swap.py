#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""מחליף תוכן של פוסט מתוזמן, בלי לוותר על החלון שלו.
   שימוש: python3 scripts/swap.py <dueAtPrefix> <slug-חדש>
   דוגמה: python3 scripts/swap.py 2026-08-21T13:00 case-one-star"""
import os, sys, json, io, re, urllib.request, urllib.error

T = os.environ["BUFFER_ACCESS_TOKEN"]
ORG = "6a75d6fe86d18905e5fbe108"
IG = "6a7f6bf6b2d9d577437ac2f9"
SITE = "https://berg-law.co.il"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
WHEN, NEW = sys.argv[1], sys.argv[2]


def gq(q, v=None):
    b = {"query": q}
    if v:
        b["variables"] = v
    r = urllib.request.Request("https://api.buffer.com/", data=json.dumps(b).encode(),
                               headers={"Authorization": "Bearer " + T, "Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(r).read())
    except urllib.error.HTTPError as e:
        return {"HTTP": e.code, "body": e.read().decode()[:300]}


def head(u):
    try:
        return urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=10).status
    except Exception as e:
        return getattr(e, "code", 0)


Q = """query($i:PostsInput!){ posts(input:$i){ edges{ node{ id status dueAt
 assets{ ... on ImageAsset { source } } } } } }"""
EDIT = """mutation($input: EditPostInput!){ editPost(input:$input){ __typename
 ... on PostActionSuccess { post { id dueAt } } ... on MutationError { message } } }"""

ns = [x["node"] for x in gq(Q, {"i": {"organizationId": ORG, "filter": {"channelIds": [IG]}}})
      ["data"]["posts"]["edges"]]


def slug(n):
    for a in n["assets"]:
        m = re.search(r"/ig/([^/]+)/", a.get("source") or "")
        if m:
            return m.group(1)


target = [n for n in ns if n["status"] == "scheduled" and n["dueAt"].startswith(WHEN)]
if not target:
    sys.exit("לא נמצא פוסט מתוזמן ב-%s" % WHEN)
t = target[0]
old = slug(t)

posts = {p["slug"]: p for p in json.load(io.open("content/instagram-posts.json", encoding="utf8"))}
p = posts.get(NEW)
if not p:
    sys.exit("אין פוסט בשם %s" % NEW)

imgs = ["%s/ig/%s/%s" % (SITE, NEW, f)
        for f in sorted(f for f in os.listdir("ig/" + NEW) if f.endswith(".jpg"))]
bad = [u for u in imgs if head(u) != 200]
if bad:
    sys.exit("תמונות לא חיות (%d) — לפרוס קודם" % len(bad))

# editPost הוא החלפה מלאה, לא patch — הכול נשלח מחדש
d = gq(EDIT, {"input": {
    "id": t["id"], "mode": "customScheduled", "dueAt": t["dueAt"],
    "schedulingType": "automatic", "text": p["fullCaption"] + "\n\n" + p["firstComment"],
    "assets": [{"image": {"url": u, "metadata": {"altText": p["title"]}}} for u in imgs],
    "metadata": {"instagram": {"type": "post", "shouldShareToFeed": True}}}})
ep = (d.get("data") or {}).get("editPost") or d
if ep.get("__typename") != "PostActionSuccess":
    sys.exit("נכשל: " + json.dumps(ep, ensure_ascii=False)[:200])

state = set(json.load(io.open(".ig-scheduled.json", encoding="utf8")))
state.add(NEW)
state.discard(old)                      # מחזיר את הישן לבריכה כדי שיתוזמן מחדש
json.dump(sorted(state), io.open(".ig-scheduled.json", "w", encoding="utf8"), ensure_ascii=False)
print("✓ %s  %s → %s   (%s חזר לבריכה)" % (t["dueAt"][:16], old, NEW, old))
