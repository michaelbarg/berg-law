"""מתזמן פוסטים ב-Buffer מתוך JSON של [{dueAt, text}].
הרצה:  cd ~/berg-law && set -a && source .env && set +a && python3 scripts/push_posts.py [קובץ]
ברירת מחדל: /tmp/berg-posts-queue.json"""
import json, os, sys, urllib.request

TOKEN = os.environ["BUFFER_ACCESS_TOKEN"]
CHANNEL = "6a75d7bf99afb443491bfe1d"          # LinkedIn — michael-barg-passparto
Q = ("mutation($input: CreatePostInput!) { createPost(input: $input) { __typename "
     "... on PostActionSuccess { post { id status dueAt } } ... on MutationError { message } } }")

src = sys.argv[1] if len(sys.argv) > 1 else "/tmp/berg-posts-queue.json"
posts = json.load(open(src))
print("posts to schedule:", len(posts))
for p in posts:
    payload = {"query": Q, "variables": {"input": {
        "text": p["text"], "channelId": CHANNEL,
        "schedulingType": "automatic", "mode": "customScheduled", "dueAt": p["dueAt"]}}}
    req = urllib.request.Request("https://api.buffer.com",
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read().decode())
    cp = d.get("data", {}).get("createPost", {})
    print(p["dueAt"], "->", cp.get("__typename"), cp.get("post", {}).get("id", ""), cp.get("message", ""))
print("DONE")
