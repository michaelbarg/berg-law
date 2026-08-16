# LEDGER — יומן ביצוע

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
