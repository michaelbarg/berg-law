#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""מעלה לאוויר פוסטים היום: פוסט ההיכרות מיד, ועוד שניים מוקדמים יותר.
   editPost בבאפר הוא החלפה מלאה ולא patch — חובה לשלוח מחדש text+assets+metadata."""
import os, json, re, time, sys, urllib.request, urllib.error

T = os.environ["BUFFER_ACCESS_TOKEN"]
ORG = "6a75d6fe86d18905e5fbe108"
IG = "6a7f6bf6b2d9d577437ac2f9"


def gq(q, v=None):
    b = {"query": q}
    if v:
        b["variables"] = v
    r = urllib.request.Request("https://api.buffer.com/", data=json.dumps(b).encode(),
                               headers={"Authorization": "Bearer " + T,
                                        "Content-Type": "application/json"})
    for a in range(5):
        try:
            return json.loads(urllib.request.urlopen(r).read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(70 * (a + 1)); continue
            return {"HTTP": e.code, "body": e.read().decode()[:300]}
    return {"error": "rate limited"}


Q = """query($i:PostsInput!){ posts(input:$i){ edges{ node{ id status dueAt sentAt externalLink text
 assets{ ... on ImageAsset { source } } } } } }"""
EDIT = """mutation($input: EditPostInput!){ editPost(input:$input){ __typename
 ... on PostActionSuccess { post { id status dueAt } } ... on MutationError { message } } }"""


def snap():
    d = gq(Q, {"i": {"organizationId": ORG, "filter": {"channelIds": [IG]}}})
    return [x["node"] for x in d["data"]["posts"]["edges"]]


def slug(n):
    for a in n["assets"]:
        m = re.search(r"/ig/([^/]+)/", a.get("source") or "")
        if m:
            return m.group(1)
    return "?"


def payload(n, extra):
    imgs = [a["source"] for a in n["assets"] if a.get("source")]
    p = {"id": n["id"], "schedulingType": "automatic", "text": n["text"],
         "assets": [{"image": {"url": u, "metadata": {"altText": "ברג ושות׳ — משרד עורכי דין"}}}
                    for u in imgs],
         "metadata": {"instagram": {"type": "post", "shouldShareToFeed": True}}}
    p.update(extra)
    return p


# slug -> חלון היעד היום (UTC). None = לפרסם מיד.
PLAN = [("intro-who", None),
        ("w-boring-docs", "2026-08-21T13:00:00.000Z"),
        ("clause-personal-guarantee", "2026-08-21T14:30:00.000Z")]

by = {slug(n): n for n in snap() if n["status"] == "scheduled"}
for s, when in PLAN:
    n = by.get(s)
    if not n:
        print("  ✗ %s לא בתור — דילוג" % s); continue
    extra = {"mode": "shareNow"} if when is None else {"mode": "customScheduled", "dueAt": when}
    d = gq(EDIT, {"input": payload(n, extra)})
    ep = (d.get("data") or {}).get("editPost") or d
    ok = ep.get("__typename") == "PostActionSuccess"
    print("  %s %-28s %s" % ("✓" if ok else "✗", s,
                             ("מתפרסם עכשיו" if when is None else when[11:16] + "Z")
                             if ok else json.dumps(ep, ensure_ascii=False)[:160]))
    time.sleep(6)

print("\nממתין לאישור פרסום…")
for i in range(14):
    time.sleep(15)
    cur = [n for n in snap() if slug(n) == "intro-who"]
    if not cur:
        print("  יצא מהתור"); break
    n = cur[0]
    print("  t+%03ds  %-10s %s" % ((i + 1) * 15, n["status"], n.get("externalLink") or ""))
    if n["status"] in ("sent", "error"):
        break

print("\n═══ מצב סופי ═══")
for n in sorted(snap(), key=lambda n: n.get("sentAt") or n["dueAt"]):
    mark = "פורסם" if n.get("sentAt") else n["status"]
    when = (n.get("sentAt") or n["dueAt"])[:16]
    print("  %-18s %-10s %-26s %s" % (when, mark, slug(n), n.get("externalLink") or ""))
