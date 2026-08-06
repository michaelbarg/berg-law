# STATUS - עדכון אחרון: 2026-08-06

## מצב נוכחי
v8 + מנגנון מאמרים + תמונת פרופיל + סטודיו פנימי. האתר חי ב-https://berg-law.co.il (SSL פעיל).

## בוצע בסשן האחרון
- תמונת פרופיל אמיתית הוחלפה (base64 מוטמע + גיבוי ב-assets/michael-berg.jpg)
- studio/index.html — מחולל קרוסלות ממותג (כלי פנימי, berg-law.co.il/studio/)
- robots.txt חוסם /studio/, noindex meta tag נוסף
- בדיקת Buffer API (ראה למטה)

## בעיות פתוחות
- אין

## שאלות לארכיטקט

### ממצאי בדיקת Buffer API (תוכנית חינמית)

**כן, ה-API זמין בתוכנית החינמית:**
- 1 API key, 3,000 requests/חודש
- עד 3 ערוצים (channels)
- עד 10 פוסטים מתוזמנים לכל ערוץ (מתמלא מחדש כשמתפרסמים)

**אופן העבודה:**
- API מסוג GraphQL בכתובת https://api.buffer.com
- אימות: Bearer token (מפתח מ-publish.buffer.com/settings/api)
- יצירת פוסט: mutation createPost עם text, channelId, mode: addToQueue
- תמונות: אין העלאה ישירה — צריך לתת URL ציבורי לתמונה (חייב להישאר נגיש עד הפרסום)
- קרוסלות: נתמך דרך מערך assets עם מספר תמונות

**מסקנה:** מתאים לאוטומציה יומית של מאמרים. צריך לארח תמונות (Netlify/GitHub) ולספק URL ציבורי. 3,000 requests בחודש מספיקים בשפע לפוסט יומי.

## הוראות אחרונות מהארכיטקט
- סטודיו פנימי (בוצע)
- בדיקת Buffer API (בוצע)
