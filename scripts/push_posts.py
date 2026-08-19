"""מתזמן פוסטים ב-Buffer מתוך JSON של [{dueAt, text, channelId?}].
הרצה:  cd ~/berg-law && set -a && source .env && set +a && python3 scripts/push_posts.py [קובץ] [channelId]
- ברירת מחדל קובץ: /tmp/berg-posts-queue.json
- ברירת מחדל ערוץ: לינקדאין. channelId כארגומנט שני או בשדה channelId של כל פריט.
- ערוצים: לינקדאין 6a75d7bf99afb443491bfe1d · גוגל ביזנס 6a7dc920b2d9d577436d768d
בדיקת ערוצים:  python3 scripts/push_posts.py --channels
השלמת תור:     python3 scripts/push_posts.py --topup"""
import argparse, json, os, sys, time, urllib.request
from datetime import datetime, timedelta, timezone

TOKEN = os.environ.get("BUFFER_ACCESS_TOKEN")
ORG = "6a75d6fe86d18905e5fbe108"
LINKEDIN = "6a75d7bf99afb443491bfe1d"
GBP = "6a7dc920b2d9d577436d768d"
API = "https://api.buffer.com"

def gql(query, variables=None):
    if not TOKEN:
        sys.exit("BUFFER_ACCESS_TOKEN חסר. הרץ:  set -a && . ./.env && set +a")
    payload = {"query": query}
    if variables: payload["variables"] = variables
    for attempt in range(6):
        try:
            req = urllib.request.Request(API, data=json.dumps(payload).encode(),
                headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = min(2 ** attempt * 5, 60)
                print("   … מגבלת קצב, ממתין %ds" % wait, flush=True)
                time.sleep(wait)
                continue
            body = e.read().decode("utf-8", errors="replace")[:200]
            sys.exit("Buffer HTTP %s: %s" % (e.code, body))
    sys.exit("Buffer: מגבלת קצב לא התפנתה אחרי 6 ניסיונות.")

Q = ("mutation($input: CreatePostInput!) { createPost(input: $input) { __typename "
     "... on PostActionSuccess { post { id status dueAt } } ... on MutationError { message } } }")

def list_channels():
    d = gql('{ channels(input:{organizationId:"%s"}) { id name service } }' % ORG)
    for c in d["data"]["channels"]:
        print(c["service"], c["id"], c["name"])

def pending_count(channel_id):
    d = gql('{posts(input:{organizationId:"%s",filter:{channelIds:["%s"]}}){edges{node{status dueAt}}}}' % (ORG, channel_id))
    edges = (d.get("data", {}).get("posts", {}).get("edges") or [])
    return len([e for e in edges if e["node"]["status"] in ("scheduled", "draft", "pending")])

def schedule_post(post, channel_id):
    inp = {"text": post["text"], "channelId": channel_id,
           "schedulingType": "automatic", "mode": "customScheduled", "dueAt": post["dueAt"]}
    if channel_id == GBP:
        inp["metadata"] = {"google": {"type": "whats_new",
            "detailsWhatsNew": {"button": post.get("button", "learn_more"),
                                "link": post.get("link", "https://berg-law.co.il")}}}
    d = gql(Q, {"input": inp})
    cp = d.get("data", {}).get("createPost", {})
    typename = cp.get("__typename", "?")
    return typename == "PostActionSuccess", typename, cp.get("message", "")

def topup(limit=10):
    """Topup LinkedIn and GBP queues from their queue JSON files."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    channels = [
        ("LinkedIn", LINKEDIN, os.path.join(root, "linkedin-queue-2026-09.json")),
        ("GBP",      GBP,      os.path.join(root, "gbp-queue-21-27.08.json")),
    ]
    total_added = 0
    for name, ch_id, queue_file in channels:
        if not os.path.exists(queue_file):
            print(f"[{name}] אין קובץ {os.path.basename(queue_file)} — מדלג")
            continue
        posts = json.load(open(queue_file))
        current = pending_count(ch_id)
        free = max(0, limit - current)
        print(f"[{name}] בתור: {current} · מכסה: {limit} · מקום: {free}")
        if free == 0:
            print(f"[{name}] התור מלא.")
            continue
        # Filter to future posts only
        now = datetime.now(timezone.utc)
        future = [p for p in posts if datetime.fromisoformat(p["dueAt"].replace("Z", "+00:00")) > now]
        to_push = future[:free]
        if not to_push:
            print(f"[{name}] אין פוסטים עתידיים לתזמן.")
            continue
        ok = 0
        for i, p in enumerate(to_push):
            success, typename, msg = schedule_post(p, ch_id)
            if success:
                ok += 1
                print(f"  ✓ {p['dueAt'][:16]}")
            elif "LimitReached" in typename:
                print(f"  ⛔ מכסה מלאה — עוצר")
                break
            elif "already" in msg.lower():
                print(f"  ↺ {p['dueAt'][:16]} כבר קיים — מדלג")
            else:
                print(f"  ✗ {p['dueAt'][:16]} {typename}: {msg[:80]}")
            if i < len(to_push) - 1:
                time.sleep(5)
        print(f"[{name}] {ok} נוספו.\n")
        total_added += ok
    return total_added

def push_file(src, default_channel):
    posts = json.load(open(src))
    print("posts to schedule:", len(posts), "| default channel:", default_channel)
    for p in posts:
        ch = p.get("channelId", default_channel)
        success, typename, msg = schedule_post(p, ch)
        pid = ""
        if success:
            d = gql(Q, {"input": {"text": p["text"], "channelId": ch,
                         "schedulingType": "automatic", "mode": "customScheduled", "dueAt": p["dueAt"]}})
        print(p["dueAt"], ch[-6:], "->", typename, msg)
    print("DONE")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", default=None)
    ap.add_argument("channel", nargs="?", default=LINKEDIN)
    ap.add_argument("--channels", action="store_true")
    ap.add_argument("--topup", action="store_true")
    ap.add_argument("--limit", type=int, default=10)
    a = ap.parse_args()

    if a.channels:
        list_channels()
        return
    if a.topup:
        added = topup(a.limit)
        # Report
        for name, ch_id in [("LinkedIn", LINKEDIN), ("GBP", GBP)]:
            n = pending_count(ch_id)
            print(f"[{name}] scheduled now: {n}")
        if added == 0:
            print("⚠ 0 posts added across all channels")
        return
    if a.file:
        push_file(a.file, a.channel)
    else:
        print("Usage: push_posts.py <file> [channelId]  OR  push_posts.py --topup")

if __name__ == "__main__":
    main()
