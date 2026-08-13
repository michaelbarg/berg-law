"""מתזמן פוסטים ב-Buffer מתוך JSON של [{dueAt, text, channelId?}].
הרצה:  cd ~/berg-law && set -a && source .env && set +a && python3 scripts/push_posts.py [קובץ] [channelId]
- ברירת מחדל קובץ: /tmp/berg-posts-queue.json
- ברירת מחדל ערוץ: לינקדאין. channelId כארגומנט שני או בשדה channelId של כל פריט.
- ערוצים: לינקדאין 6a75d7bf99afb443491bfe1d · גוגל ביזנס: להריץ list_channels (למטה) אחרי החיבור בבאפר.
בדיקת ערוצים:  python3 scripts/push_posts.py --channels"""
import json, os, sys, urllib.request

TOKEN = os.environ["BUFFER_ACCESS_TOKEN"]
ORG = "6a75d6fe86d18905e5fbe108"
LINKEDIN = "6a75d7bf99afb443491bfe1d"
API = "https://api.buffer.com"

def gql(query, variables=None):
    payload = {"query": query}
    if variables: payload["variables"] = variables
    req = urllib.request.Request(API, data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

if len(sys.argv) > 1 and sys.argv[1] == "--channels":
    d = gql('{ channels(input:{organizationId:"%s"}) { id name service } }' % ORG)
    for c in d["data"]["channels"]:
        print(c["service"], c["id"], c["name"])
    sys.exit(0)

Q = ("mutation($input: CreatePostInput!) { createPost(input: $input) { __typename "
     "... on PostActionSuccess { post { id status dueAt } } ... on MutationError { message } } }")

src = sys.argv[1] if len(sys.argv) > 1 else "/tmp/berg-posts-queue.json"
default_channel = sys.argv[2] if len(sys.argv) > 2 else LINKEDIN
posts = json.load(open(src))
print("posts to schedule:", len(posts), "| default channel:", default_channel)
for p in posts:
    ch = p.get("channelId", default_channel)
    d = gql(Q, {"input": {"text": p["text"], "channelId": ch,
                "schedulingType": "automatic", "mode": "customScheduled", "dueAt": p["dueAt"]}})
    cp = d.get("data", {}).get("createPost", {})
    print(p["dueAt"], ch[-6:], "->", cp.get("__typename"), cp.get("post", {}).get("id", ""), cp.get("message", ""))
print("DONE")
