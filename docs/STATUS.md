# STATUS - עדכון אחרון: 2026-08-11

## מצב נוכחי
האתר חי ב-https://berg-law.co.il. ארכיטקטורת תור: 13 מאמרים בקובץ, renderArticles מסנן עתידיים (_todayEnd) — האתר מפרסם לבד עד 16.08. 6 פוסטים מתוזמנים ב-Buffer עד 23.08.

## בוצע בסשן האחרון (11.08 — תשתית SEO)
- scripts/build-articles.js — מחולל עמודי מאמר אינדקסביליים + sitemap.xml (מדלג על מאמרים עתידיים)
- 3 עמודי מאמר עם טקסט מלא בעברית (~550-650 מילים כל אחד): נסח טאבו, ערבות אישית, התכתבות כחוזה
- content/full/ — מאגר הטקסטים המלאים
- sitemap.xml (5 כתובות) + robots.txt עם Sitemap: + canonical ב-index.html
- סכמת Article + BreadcrumbList בכל עמוד מאמר
- קישור פנימי: כרטיס מאמר בדף הבית מוביל לעמוד המאמר כשקיים slug
- אימות חי: sitemap 200, שלושת העמודים 200, robots כולל Sitemap, canonical באוויר

## בעיות פתוחות
- Claude Code ב-CLI על המק מנותק (Not logged in) — הפריסה בוצעה ידנית עם npx netlify-cli. צריך להריץ `claude` ולהתחבר מחדש כדי שהמסירות ל-Claude Code יעבדו שוב.
- הגשר לענן (Desktop Commander) מתנתק לסירוגין — הסיבה למעבר לארכיטקטורת תור.

## ממתין למייקל
- Google Business Profile — פתיחה ואימות (הכי משפיע על נראות מקומית)
- Google Search Console — אימות בעלות והגשת sitemap
- Grow (סליקה) — קישור ל-PAY_LINKS.docs

## שאלות לארכיטקט
- אין
