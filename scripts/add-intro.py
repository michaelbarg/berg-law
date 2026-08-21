# -*- coding: utf-8 -*-
"""פוסט היכרות — הפוסט שנעוץ בראש הפרופיל.
   כל עובדה כאן מאומתת (claude/berg-open-questions.md). אין שנת הסמכה, אין
   "20+ שנים", אין "גייסתי", אין מילות שבח ואין השוואה לעורכי דין אחרים."""
import json, io, os, sys

P = sys.argv[1] if len(sys.argv) > 1 else "content/instagram-posts.json"
DISC = "האמור אינו ייעוץ משפטי ואינו תחליף לו. כל מקרה נבחן לגופו."
PROMO = ("ברג ושות׳ — המחלקה המשפטית של העסק שלך, בתשלום חודשי קבוע ומותאם לצורך.\n"
         "קישור בביו.")
TAGS = ("#עורך_דין #משפט_מסחרי #עסקים_קטנים #יזמות #ברג_ושות #דיני_עסקים "
        "#תל_אביב #חוזים #ליווי_משפטי #יזמים")
DAYTAGS = "#היכרות #שני_צידי_השולחן"

POST = {
 "day": "שישי", "pillar": "היכרות", "slug": "intro-who", "motif": "seal",
 "title": "מייקל ברג — עורך דין, ובעל עסק בעצמו",
 "slides": [
   "היכרות\nמייקל ברג",
   "אני עורך דין.\nאני גם יושב בצד השני\nשל אותו שולחן —\nמנהל עסק משלי.",
   "למדתי משפטים,\nולצידם מנהל עסקים\nבהתמחות ראיית חשבון.\nדוח כספי אני קורא\nלפני שאני קורא חוזה.",
   "ב-2020 הקמתי את פספרטו.\nהמיזם קיבל מענק\nמרשות החדשנות.",
   "ולכן כשאני מנסח סעיף,\nאני חושב על היום\nשבו תצטרכו להפעיל אותו —\nלא על היום שחותמים."],
 "cover": {"format": "portrait", "kick": "היכרות",
           "title": "מייקל ברג", "line": "עורך דין · ובעל עסק בעצמו"},
 "caption": ("רוב בעלי העסקים שאני עובד איתם לא מחפשים מישהו שיסביר להם מה כתוב בחוק. "
             "הם מחפשים מישהו שיבין למה הסעיף הזה מפריע להם לעבוד.\n\n"
             "אני עורך דין, ואני גם מנהל עסק משלי — כלומר אני מכיר את הצד שחותם, לא רק את "
             "הצד שמנסח. למדתי משפטים לצד מנהל עסקים בהתמחות ראיית חשבון, וב-2020 הקמתי את "
             "פספרטו, שקיבל מענק מרשות החדשנות.\n\n"
             "כאן בעמוד יוצא כל יום תוכן אחד: סעיף שכדאי להכיר, טעות שעולה כסף, שאלה מהשטח, "
             "ופעם בשבוע פסק דין פומבי שאפשר ללמוד ממנו משהו מעשי.\n\n"
             "אם יש סעיף שאתם לא בטוחים לגביו — כתבו לי בדיירקט."),
}
POST["tags"] = TAGS
POST["dayTags"] = DAYTAGS
POST["promo"] = PROMO
POST["firstComment"] = DAYTAGS + " " + TAGS
POST["fullCaption"] = POST["caption"] + "\n\n" + PROMO + "\n\n" + DISC

posts = json.load(io.open(P, encoding="utf8"))
if any(p["slug"] == POST["slug"] for p in posts):
    print("already present — nothing to do")
else:
    state = json.load(io.open(".ig-scheduled.json", encoding="utf8")) if os.path.exists(".ig-scheduled.json") else []
    idx = max([i for i, p in enumerate(posts) if p["slug"] in state], default=-1) + 1
    posts.insert(idx, POST)
    json.dump(posts, io.open(P, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print("intro post inserted at index %d — total now %d" % (idx, len(posts)))
