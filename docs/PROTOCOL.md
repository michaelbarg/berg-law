# פרוטוקול תקשורת — ברג ושות׳

## קבצי מצב

| קובץ | כותב | מתי | פורמט |
|---|---|---|---|
| `ops/state.json` | `build-state.js` (אוטומטי) | כל בילד | JSON — git, articles, pages, buffer, tasks |
| `ops/tasks.json` | code / architect | כשמשימה מתווספת או משתנה | JSON array — id, title, status, owner, note |
| `ops/buffer.json` | code (מהמק) | אחרי כל push_posts | JSON — לכל ערוץ: queued, lastSentAt, lastCheckedAt |
| `docs/LEDGER.md` | code / architect | אחרי כל סשן | append-only, החדש למעלה |
| `docs/STATUS.md` | code | סוף כל סשן | סיכום מצב נוכחי |
| `CLAUDE.md` | code באישור מייקל | שינויי פרוטוקול | חוקים קדושים + הגדרות עבודה |

## סטטוסים ב-tasks.json

`todo` → `doing` → `done` | `blocked` | `cancelled`

**כלל:** status עובר ל-`done` רק אחרי אימות בפועל, לא אחרי שפקודה רצה.

## owner

- `code` — Claude Code על המק
- `architect` — סשן Claude.ai
- `michael` — מייקל (פעולה ידנית)

## רצף בילד

**חובה בכל בילד, בסדר הזה:**

```bash
node scripts/build-articles.js
node scripts/build-practice.js
node scripts/build-state.js
```

**`build-state.js` חייב לרוץ בכל בילד, אחרי build-articles ו-build-practice. בלעדיו הארכיטקט עיוור.**

## Netlify CI

Build command ב-`netlify.toml`:
```
node scripts/build-articles.js && node scripts/build-practice.js && node scripts/build-state.js
```

`git push` = פריסה אוטומטית (אחרי שמייקל מאשר GitHub App ב-Netlify UI).

## LEDGER.md — פורמט רשומה

```
## YYYY-MM-DD · [code|architect]
- **משימות:** T1, T3, ...
- **בוצע:** ...
- **אומת:** ...
- **שגיאה:** [ציטוט מדויק | אין]
- **פתוח לצד השני:** ...
```

יומן append-only. החדש למעלה. לעולם לא למחוק רשומות קודמות.
