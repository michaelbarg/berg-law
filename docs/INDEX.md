# ברג ושות׳ - אינדקס פרויקט ראשי
עדכון אחרון: 2026-08-07 | עודכן ע"י: Claude (ארכיטקט, Cowork + Desktop Commander)

## 1. נכסים חיים
| נכס | מיקום/כתובת | סטטוס |
|---|---|---|
| אתר ייצור | https://berg-law.co.il | חי — SSL פעיל, DNS של Netlify (אומת 7.8) |
| URL זמני Netlify | https://berg-law.netlify.app | חי |
| ריפו | github.com/michaelbarg/berg-law | ציבורי |
| דומיין | DomainTheNet, בתוקף עד 8/2027 | פעיל |

## 2. קבצי הפרויקט
| קובץ | תפקיד |
|---|---|
| index.html | האתר כולו - 4 שפות, אשף נסחים, i18n, renderArticles() |
| legal.html | תנאי שימוש + מדיניות פרטיות (4 קישורים מהפוטר) |
| studio/index.html | סטודיו ניהול — חסום לאינדוקס |
| robots.txt | חוסם /studio/ |
| content/articles.json | מאמרים יומיים - נטען דינמית ע"י renderArticles() |
| netlify.toml | תצורת פריסה + headers |
| CLAUDE.md | פרוטוקול העבודה - נקרא אוטומטית |
| docs/STATUS.md | מצב שוטף - גשר לארכיטקט |
| docs/INDEX.md | הקובץ הזה |
| README.md | תצורה + חוקים קדושים |

## 3. נקודות תצורה (בתוך index.html)
| קבוע | שולט על | ערך נוכחי |
|---|---|---|
| DOCS | מחירי נסחים | reg:59 hist:69 merged:79 company:69 |
| PAY_LINKS.docs | קישור סליקה | ריק (fallback וואטסאפ) |
| PHONE | וואטסאפ/חיוג | 972546665615 |
| מייל | טפסים ופוטר | michael@passparto.com |

## 4. מסמכים אצל מייקל (מהשיחה עם הארכיטקט)
נבדק בדיסק וב-Drive ב-7.8 — ארבעת הראשונים לא נמצאו (כנראה קיימים רק בשיחת קלוד):
- berg-co-social-strategy.md - אסטרטגיה שנתית + PROMPT שבועי — ❌ לא בדיסק
- berg-co-week1-content.md - תוכן שבוע 1 ל-Buffer — ❌ לא בדיסק
- berg-law-claude-code-handoff.md - חבילת ההעברה המקורית — ❌ לא בדיסק
- berg-launch-board.html - לוח משימות חי — ❌ לא בדיסק
- berg-co-brand-guide.md - מדריך השפה המיתוגית — ✅ ~/Downloads/berg-co-brand-guide.md
- berg-carousel-maker.html - כלי יצירת קרוסלות — ✅ ~/Downloads/berg-carousel-maker.html
- תיקיית קמפיין: ~/berg-campaign/ — הוקמה 7.8: brand-directive-v2.md (שחור-זהב, סאנס-סריף), mood-images-shortlist.md, michael-berg-portrait-2026.png (הפורטרט הרשמי), berg-carousel-maker.html v2 (שחור-זהב, Heebo+IBM Plex, 1080×1350; v1 נשמר ב-Downloads)

## 5. חשבונות ושירותים
| שירות | תפקיד | סטטוס |
|---|---|---|
| DomainTheNet | רשם דומיין | פעיל |
| Netlify | אחסון ופריסה | חי (berg-law.netlify.app) |
| GitHub | קוד | פעיל (michaelbarg/berg-law) |
| Buffer | תזמון רשתות | ✅ פעיל — לינקדאין מחובר, API עובד (GraphQL, טוקן ב-.env) |
| Grow | סליקה | ממתין הקמה |

## 6. משימות פתוחות (נכון ל-7.8)
1. ✅ מאמר יומי 07.08 — נכתב ע"י הארכיטקט, שולב ונפרס ע"י Claude Code (7.8, קומיט 7c2fa89)
2. הקמת Grow (סליקה) → הדבקת הקישור ב-PAY_LINKS.docs (כרגע הזמנות נסחים נופלות לוואטסאפ)
3. ✅ Buffer הוקם ועובד — פוסט ערך ראשון (ערבות אישית) פורסם ללינקדאין 7.8 דרך ה-API. נותר: טעינת תוכן שבוע 1 (דורש שחזור berg-co-week1-content.md)
4. שחזור 4 מסמכי הארכיטקט משיחת קלוד ושמירתם בדיסק/ריפו
5. רשות: העברת berg-co-brand-guide.md ו-berg-carousel-maker.html מה-Downloads לריפו
6. ✅ אוטומציה יומית פעילה — תוקנה 9.8: הריצות דיווחו "דולג" כי כלי Desktop Commander דחויים בסשן מתוזמן ולא נטענו. הפרומפט עודכן (טעינת כלים ב-ToolSearch + 3 ניסיונות + חובת ציטוט שגיאה + תור תוכן במקום ויתור), נוספה בדיקת אידמפוטנטיות, ונוסף טריגר גיבוי ב-11:00 (trig_01EFWipi4pWSr6yDNUYWP1yE) שמסיים מיד אם המאמר כבר פורסם. טריגר ראשי (7:30): trig_01LHv4G35X7hTBV7f9ByNVf7: כל יום 07:30 — מאמר לאתר; א'/ג'/ה' — גם פוסט ערך לבאפר מתוזמן ל-09:00. ריצה ראשונה: ראשון 9.8. ספר הפעלה: פרויקט קלוד claude/berg-pipeline.md. תנאי: המק דלוק עם אפליקציית קלוד פתוחה
