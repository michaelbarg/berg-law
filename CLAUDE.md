# פרוטוקול עבודה - ברג ושות׳

- קלוד (אפליקציה) = ארכיטקט. אתה (Claude Code) = מבצע. מייקל = הגשר.
- תחילת כל סשן: קרא docs/STATUS.md
- סוף כל סשן: עדכן docs/STATUS.md והדפס בלוק "📋 העבר לקלוד":
  מה בוצע / מצב / בעיות / שאלות לארכיטקט

## חוקים קדושים (שינוי רק באישור מייקל):
- מבנה מפתחות i18n וארבעת המילונים ב-index.html
- גרש עברי U+05F3 ב"ושות׳" (ASCII שובר JS)
- מחירים הוסרו מהאתר (16.08.2026). דיסקליימר משפטי, תמונה מוטמעת
- נקודות תצורה: const DOCS, const PAY_LINKS, const PHONE
- פריסה תמיד: netlify deploy --prod --dir .  (או git push אחרי חיבור CI)
- הריפו ציבורי - אסור להכניס אליו סיסמאות, טוקנים או מפתחות בשום קובץ
- כל הודעה לארכיטקט חייבת להסתיים ב-git push (הוא קורא מ-GitHub)

## רצף בילד (חובה בכל בילד, בסדר):
```
node scripts/build-articles.js
node scripts/build-practice.js
node scripts/build-state.js
```
build-state.js חייב לרוץ אחרון — הארכיטקט קורא ops/state.json.

## קבצי תפעול
ראה docs/PROTOCOL.md לפורמט מלא.
- ops/state.json — נבנה אוטומטית, לא לערוך ידנית
- ops/tasks.json — משימות פתוחות, לעדכן סטטוס אחרי אימות
- ops/buffer.json — מצב Buffer, לעדכן אחרי push_posts
- docs/LEDGER.md — יומן append-only, רשומה בסוף כל סשן
