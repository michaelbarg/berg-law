#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""בדיקת בריאות לכל צינורות התוכן של ברג ושות׳.
   הרצה:  set -a && . ./.env && set +a && python3 scripts/health.py
   יוצא עם קוד 1 אם יש ממצא חוסם — כדי שאפשר יהיה לתלות בו משימה מתוזמנת."""
import os, sys, json, re, datetime, urllib.request, urllib.error

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
os.chdir(ROOT)
SITE = "https://berg-law.co.il"
ORG = "6a75d6fe86d18905e5fbe108"
CH = {"אינסטגרם": "6a7f6bf6b2d9d577437ac2f9",
      "לינקדאין": "6a75d7bf99afb443491bfe1d",
      "גוגל ביזנס": "6a7dc920b2d9d577436d768d"}
TOKEN = os.environ.get("BUFFER_ACCESS_TOKEN")
problems = []


def gql(query, variables=None):
    body = {"query": query}
    if variables:
        body["variables"] = variables
    req = urllib.request.Request(
        "https://api.buffer.com/", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + TOKEN})
    return json.loads(urllib.request.urlopen(req).read())


def head(url, timeout=10):
    try:
        r = urllib.request.Request(url, method="HEAD")
        return urllib.request.urlopen(r, timeout=timeout).status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


POSTS_Q = """query($i:PostsInput!){ posts(input:$i){ edges{ node{ status dueAt sentAt text
 error{ ... on PostPublishingError { message } }
 assets{ ... on ImageAsset { source } } } } } }"""

print("═══ תורי הפרסום ═══")
if not TOKEN:
    problems.append("BUFFER_ACCESS_TOKEN חסר — לא ניתן לבדוק את התורים")
    print("  ⛔ אין טוקן")
else:
    ig_urls = []
    for name, cid in CH.items():
        d = gql(POSTS_Q, {"i": {"organizationId": ORG, "filter": {"channelIds": [cid]}}})
        ns = [x["node"] for x in d["data"]["posts"]["edges"]]
        sched = sorted((n for n in ns if n["status"] == "scheduled"), key=lambda n: n["dueAt"])
        errs = [n for n in ns if n.get("error")]
        # חובה לסנן status=sent במפורש — בלי זה מוחזר חלון חלקי בלבד
        ds = gql(POSTS_Q, {"i": {"organizationId": ORG,
                                 "filter": {"channelIds": [cid], "status": ["sent"]}}})
        sent = sorted((x["node"] for x in ds["data"]["posts"]["edges"]
                       if x["node"].get("sentAt")), key=lambda n: n["sentAt"])
        through = sched[-1]["dueAt"][:10] if sched else "—"
        print("  %-12s בתור %-3d עד %-11s שגיאות %d" % (name, len(sched), through, len(errs)))
        for n in errs:
            problems.append("%s: פוסט ב-%s נכשל — %s" % (name, n["dueAt"][:16], n["error"]["message"][:120]))
        if len(sched) < 3:
            problems.append("%s: רק %d פוסטים בתור — למלא" % (name, len(sched)))
        # שתק = תקלה. תור מלא שלא מפרסם נראה בריא עד שמסתכלים על sentAt.
        if sent:
            last = datetime.datetime.strptime(sent[-1]["sentAt"][:19], "%Y-%m-%dT%H:%M:%S")
            age = (datetime.datetime.utcnow() - last).total_seconds() / 3600
            print("               פורסם לאחרונה לפני %.0f שעות" % age)
            if age > 48 and sched:
                problems.append("%s: לא פורסם דבר %.0f שעות למרות שיש תור" % (name, age))
            # רק 14 הימים האחרונים — פוסט ישן מ-2020 בתור ייתן "חור של 2334 ימים"
            cutoff = (datetime.datetime.utcnow() - datetime.timedelta(days=14)).strftime("%Y-%m-%d")
            days = sorted({n["sentAt"][:10] for n in sent if n["sentAt"][:10] >= cutoff})
            if len(days) > 1:
                gaps = [(datetime.datetime.strptime(days[i], "%Y-%m-%d")
                         - datetime.datetime.strptime(days[i - 1], "%Y-%m-%d")).days
                        for i in range(1, len(days))]
                print("               ימי פרסום אחרונים: %s" % " ".join(d[5:] for d in days))
                if max(gaps) > 2:
                    problems.append("%s: חור של %d ימים בפרסום בשבוע האחרון" % (name, max(gaps)))
        elif sched:
            problems.append("%s: מעולם לא פורסם פוסט" % name)
        seen = {}
        for n in sched:
            k = (n["dueAt"], (n.get("text") or "")[:120])
            if k in seen:
                problems.append("%s: פוסט כפול ב-%s — יתפרסם פעמיים" % (name, n["dueAt"][:16]))
            seen[k] = 1
        if name == "אינסטגרם":
            for n in sched:
                ig_urls += [a["source"] for a in n["assets"] if a.get("source")]

    print("\n═══ תמונות הקרוסלות בתור ═══")
    bad = [(u, head(u)) for u in ig_urls]
    bad = [(u, c) for u, c in bad if c != 200]
    print("  %d תמונות · תקינות %d · שבורות %d" % (len(ig_urls), len(ig_urls) - len(bad), len(bad)))
    for u, c in bad[:8]:
        problems.append("תמונה מחזירה %s — הפוסט ייכשל בשקט: %s" % (c, u))

print("\n═══ מאגרי התוכן ═══")
arts = json.load(open("content/articles.json", encoding="utf8"))
today = datetime.date.today()
future = [a for a in arts if datetime.datetime.strptime(a["date"], "%d.%m.%Y").date() > today]
print("  מאמרים: %d סה\"כ · %d עתידיים" % (len(arts), len(future)))
if len(future) < 3:
    problems.append("מאמרים: רק %d עתידיים — לכתוב חדשים" % len(future))
orphan = [a.get("slug") for a in arts if not os.path.exists("content/full/%s.html" % a.get("slug", ""))]
if orphan:
    problems.append("מאמרים בלי טקסט מלא (הכרטיס לא יוביל לשום מקום): %s" % ", ".join(map(str, orphan)))

ig = json.load(open("content/instagram-posts.json", encoding="utf8"))
used = json.load(open(".ig-scheduled.json", encoding="utf8")) if os.path.exists(".ig-scheduled.json") else []
left = len(ig) - len(used)
print("  אינסטגרם: %d בספרייה · %d נוצלו · %d נותרו (~%d ימים)" % (len(ig), len(used), left, left))
if left < 7:
    problems.append("אינסטגרם: נותרו %d פוסטים בלבד — לכתוב חדשים" % left)

# פוסטי פסיקה חייבים מקור מאומת. שער הבנייה תופס את זה, אבל עדיף לדעת מוקדם.
for p in ig:
    if p.get("pillar") == "מן הפסיקה":
        miss = [k for k in ("court", "docketNo", "holding", "source_url", "verified_at")
                if not (p.get("cover") or {}).get(k)]
        if miss:
            problems.append("פסיקה '%s' חסר: %s" % (p["slug"], ", ".join(miss)))

# ── כלל מייקל: הפנים שלו פעם בשבוע. לא פעמיים, ולא יומיים ברצף. ──
# הכלל הזה נשבר פעם אחת בלי שאיש שם לב, כי הזזת פוסט קדימה נראית תמימה.
print("\n═══ תדירות הדיוקן ═══")
FACE_FMT = {"portrait", "portraitfull"}
ig_lib = {q["slug"]: q for q in ig}


def has_face(sl):
    q = ig_lib.get(sl) or {}
    fmt = (q.get("cover") or {}).get("format") or ("portraitfull" if q.get("day") == "שבת" else "")
    return fmt in FACE_FMT


if TOKEN:
    d = gql(POSTS_Q, {"i": {"organizationId": ORG, "filter": {"channelIds": [CH["אינסטגרם"]]}}})
    nodes = [x["node"] for x in d["data"]["posts"]["edges"]]
    dated = []
    for n in nodes:
        when = n.get("sentAt") or n["dueAt"]
        sl = None
        for a in n["assets"]:
            m = re.search(r"/ig/([^/]+)/", a.get("source") or "")
            if m:
                sl = m.group(1); break
        if sl and has_face(sl):
            dated.append((when[:10], sl))
    dated.sort()
    if not dated:
        print("  אין פוסט־דיוקן בחלון הנוכחי")
    for day, sl in dated:
        print("  %s  %s" % (day, sl))
    # שני פוסטי־פנים בתוך פחות מ-7 ימים = הפרה
    for i in range(1, len(dated)):
        d0 = datetime.datetime.strptime(dated[i - 1][0], "%Y-%m-%d")
        d1 = datetime.datetime.strptime(dated[i][0], "%Y-%m-%d")
        gap = (d1 - d0).days
        if gap < 7:
            problems.append("דיוקן פעמיים תוך %d ימים (%s ו-%s) — הכלל הוא פעם בשבוע"
                            % (gap, dated[i - 1][1], dated[i][1]))
    if len(dated) >= 2:
        print("  מרווח מינימלי בפועל: %d ימים" % min(
            (datetime.datetime.strptime(dated[i][0], "%Y-%m-%d")
             - datetime.datetime.strptime(dated[i - 1][0], "%Y-%m-%d")).days
            for i in range(1, len(dated))))


print("\n═══ האתר ═══")
for path in ("/", "/practice/", "/articles/", "/sitemap.xml", "/og.jpg"):
    c = head(SITE + path)
    print("  %-16s %s" % (path, c))
    if c != 200:
        problems.append("האתר: %s מחזיר %s" % (path, c))

print("\n" + "═" * 46)
if problems:
    print("⛔ %d ממצאים:" % len(problems))
    for p in problems:
        print("   · " + p)
    sys.exit(1)
print("✅ הכול תקין.")
