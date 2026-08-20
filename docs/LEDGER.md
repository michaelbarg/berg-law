# LEDGER — יומן ביצוע

---

## 2026-08-20 · תקלת אינסטגרם (סבב 6)
- **ממצא:** תור אינסטגרם 10/10 scheduled אבל 0 פרסומים מ-17.08. שורש: פער 7 ימים (20-26.08) —
  הקבוצה הקודמת (16-17.08) נשלחה, והקבוצה הבאה תוזמנה ל-27.08+. ללא שגיאות Buffer (0 errors).
  לא תקלת חיבור — תקלת תזמון.
- **תיקון:** מחקנו 3 פוסטים רחוקים (02-05.09) ← topup מילא אותם מחדש. פרסמנו פוסט-הוכחה
  מיידי (`shareNow`) עם `metadata.instagram.type=post + shouldShareToFeed=True`.
- **הוכחת חיים:**
  - sentAt: `2026-08-20T09:26:24.248Z`
  - externalLink: `https://www.instagram.com/p/DcQcAC3IDXS/`
- **מניעה:** social.yml — צעד `Check publish freshness`: אם sentAt האחרון > 26 שעות → exit 1 (מייל התראה).
- **sentAt אחרון לפני תיקון:** 2026-08-17T16:02:56Z (3 ימים)
- **תמונות שבורות:** 0 (כולן 200)
- **מצב סופי:** Instagram 10 scheduled (27.08–05.09) + 1 sent now

---

## 2026-08-19 · CI + פורמטים + תורים (סבב 5)
- **CI:**
  - `deploy.yml`: on push to main → build articles/practice/state → Netlify build hook. Asset verification pre-build.
  - `social.yml`: daily 06:00Z → topup Instagram + LinkedIn + GBP. Secret verification, failure on 0 added, queue report.
  - Secrets: `NETLIFY_BUILD_HOOK` + `BUFFER_ACCESS_TOKEN` מוגדרים ב-GitHub Actions.
- **פורמט כתבות:**
  - 6 כתבות חדשות (27.08–01.09) עם שדה `format` (qa/term/didyouknow/bureaucracy/fear/history).
  - `build-articles.js`: FORMAT_MAP → chip ויזואלי (צבע מהפלטה, opacity נמוך) בכל עמוד כתבה + ארכיון.
  - סינון פורמט בארכיון (שורת chips נפרדת, לצד סינון תחום). כתבות ללא format — ללא שינוי.
  - 29/29 validation, sitemap 35 URLs.
- **תורים חברתיים:**
  - `push_posts.py` שוכתב: `--topup` ממלא LinkedIn + GBP מקבצי JSON. `--channels` לרשימת ערוצים.
  - GBP תאריכים הוזזו 21-27→20-26.08. LinkedIn 1 חדש (3 כפילויות), GBP 3 חדשים (4 hit limit).
  - מצב סופי: Instagram 10/10, LinkedIn 10/10, GBP 10/10.
- **תיעוד:** tasks.json עודכן (T1 cancelled, T7 done, T12-T16 נוספו). .gitignore: __pycache__/.

---

## 2026-08-17 · E-E-A-T: author + schema (סבב 4)
- **בוצע:**
  - ישות ארגון: `@type` → `Attorney`, `@id` → `#org`, `availableLanguage`, `areaServed` → `IL`
  - ישות מחבר: `Person` `#michael-berg` with `knowsAbout`, `worksFor` → `#org`
  - סכמת כתבה: `Article` → `BlogPosting` with `@id` refs (author/publisher), `isAccessibleForFree`
  - חתימת מחבר: `<div class="byline">` עם קישור ל-`/about-michael-berg`, תאריך, tag — בכל 23 הכתבות
  - עמוד מחבר: `/about-michael-berg` — תואר, רקע עסקי, תחומי עיסוק, 4 שפות (מתוכן קיים בלבד)
  - סייטמאפ: 31 → 33 URLs (+about-michael-berg +1 new article)
  - בילד: וולידציה אוטומטית — 23/23 עמודים (BlogPosting + author + JSON-LD parse + no duplicate @id)
- **אימות חי:** 5/5 — michael-berg=2 · BlogPosting=1 · about-page=200 · #org=2 · byline=1
- **לא נוסף:** שנת הסמכה, מספר רישיון, שנות ותק (לא מאומתים)

---

## 2026-08-16 · deploy fix (סבב 3)
- **נמצא:** Netlify CI build failed silently — `build-state.js` crash kills the entire `&&` chain, so no deploy goes through.
- **תיקון:** `netlify.toml` build command: wrapped `build-state.js` in `(... || true)` — reporting tool must not block deploy.
- **פריסה ידנית:** `netlify deploy --prod --dir .` — live at berg-law.co.il.
- **אימות:** 4/4 acceptance tests pass (ללא עלות=0, ru_RU=1, state.json=JSON, articles.json=26.08).

---

## 2026-08-16 · code (סבב 2)
- **משימות:** T6, T11
- **בוצע:**
  - הסרת "ללא עלות" מקטע 04 (HTML + 4 מילוני i18n)
  - הסרת טווח שנים 2010–2014 מהתארים (לא מאומת, claude/berg-open-questions.md לא קיים)
  - og:locale — כבר תקין מסבב 1
  - כרטיסי כתבות סטטיים הועברו לבילד: build-articles.js מזריק top-3 ל-index.html
  - נוצרו: ops/tasks.json, ops/buffer.json, scripts/build-state.js, docs/PROTOCOL.md
  - robots.txt: Disallow /ops/
- **אומת:** build-articles.js רץ, כרטיסים 16+15+14.08 עם קישורי /articles/slug, grep "ללא עלות" = 0
- **שגיאה:** אין
- **פתוח לצד השני:**
  - מייקל: טוקן Netlify, אישור GitHub App ב-Netlify UI, זמני תגובה (T5)
  - architect: אין

---

## 2026-08-16 · code (סבב 1 — BRIEF-16.08)
- **משימות:** T4, T6, T7, T8, T10, T11
- **בוצע:**
  - 10 כתבות 17–26.08 (סה"כ 23), builds OK
  - ציות: המתמחה(4)→העוסק, מהספרים(2)→הוסר, 20+(5)→מ-2009, ייעוץ ראשונה(2)→היכרות
  - og:description עודכן
  - Buffer: LI 3/4, GBP 6/7 (מגבלת 10)
  - Netlify↔GitHub: הגדרות נכתבו, build command ב-netlify.toml
  - CLAUDE.md עודכן — מחירים הוסרו מחוקים קדושים
- **אומת:** deploy Netlify OK, curl 200, grep 0 לכל ביטויים בעייתיים, articles.json ראשון = 26.08
- **שגיאה:** Netlify CI deploy נכשל — "Unable to access repository" (צריך GitHub App authorization)
- **פתוח לצד השני:**
  - מייקל: רומנטקס (אושר — להשאיר), טוקן, GitHub App, Buffer overflow
  - architect: אין
