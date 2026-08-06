# STATUS - עדכון אחרון: 2026-08-06

## מצב נוכחי
v7.5 + מנגנון מאמרים דינמי נפרסו. האתר חי ב-https://berg-law.netlify.app.
הריפו ציבורי: github.com/michaelbarg/berg-law

## בוצע בסשן האחרון
- יצירת content/articles.json עם 3 מאמרים ב-4 שפות (he/en/ru/fr)
- הוספת renderArticles() ל-index.html: fetch מה-JSON, מיון לפי תאריך, הצגת 3 אחרונים בכרטיסים ובגזט
- fallback שקט: אם fetch נכשל — ה-HTML הסטטי נשאר
- חיבור אוטומטי להחלפת שפה (hook על applyLang)
- id="articlesGrid" ו-id="gazetteAside" נוספו ל-HTML
- ריפו הפך לציבורי + חוק קדוש: אסור סיסמאות/טוקנים
- README + INDEX עודכנו

## בעיות פתוחות
- DNS של berg-law.co.il — ממתין ל-NS propagation (הוחלף ב-DomainTheNet)

## שאלות לארכיטקט
- אין כרגע — מנגנון המאמרים עובד, מוכנים לתוכן חדש

## הוראות אחרונות מהארכיטקט
- מנגנון מאמרים יומי (בוצע)
