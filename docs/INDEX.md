# ברג ושות׳ - אינדקס פרויקט ראשי
עדכון אחרון: 2026-08-19 | עודכן ע"י: Claude Code

## 1. נכסים חיים
| נכס | מיקום/כתובת | סטטוס |
|---|---|---|
| אתר ייצור | https://berg-law.co.il | חי — SSL, DNS Netlify, CI deploy on push |
| URL זמני Netlify | https://berg-law.netlify.app | חי |
| ריפו | github.com/michaelbarg/berg-law | ציבורי |
| דומיין | DomainTheNet, בתוקף עד 8/2027 | פעיל |
| CI: deploy | `.github/workflows/deploy.yml` | on push → build → Netlify hook |
| CI: social | `.github/workflows/social.yml` | daily 06:00Z → topup IG+LI+GBP |

## 2. קבצי הפרויקט
| קובץ | תפקיד |
|---|---|
| index.html | האתר כולו — 4 שפות, i18n, top-3 article cards, org+person schema |
| legal.html | תנאי שימוש + מדיניות פרטיות |
| about-michael-berg | עמוד מחבר (E-E-A-T) — תואר, רקע, תחומים, 4 שפות |
| robots.txt | חוסם /studio/, /ops/ |
| content/articles.json | 29 כתבות — 6 עם format (qa/term/didyouknow/bureaucracy/fear/history) |
| content/instagram-posts.json | 30 פוסטים לאינסטגרם (20 scheduled, 10 remaining) |
| netlify.toml | build command + headers |
| scripts/build-articles.js | בונה עמודי כתבות + ארכיון + sitemap + author page + validation |
| scripts/build-practice.js | בונה עמודי תחומי עיסוק |
| scripts/build-state.js | בונה ops/state.json (non-fatal) |
| scripts/push_instagram.py | --topup לתור אינסטגרם (Buffer API) |
| scripts/push_posts.py | --topup לתורי לינקדאין + GBP (Buffer API) |
| CLAUDE.md | פרוטוקול העבודה — נקרא אוטומטית |
| docs/LEDGER.md | יומן append-only |
| docs/INDEX.md | הקובץ הזה |

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

## 4ב. תשתית SEO (נבנתה 11.8)
| רכיב | מיקום | מצב |
|---|---|---|
| מחולל עמודי מאמר + sitemap | scripts/build-articles.js | פעיל — `node scripts/build-articles.js` |
| טקסטים מלאים | content/full/<slug>.html | 3 מאמרים |
| עמודים אינדקסביליים | articles/<slug>.html | 3 חיים (200 OK) |
| sitemap.xml | שורש | 5 כתובות, מוצהר ב-robots.txt |
| canonical + Article/BreadcrumbList schema | index.html + עמודי מאמר | פעיל |
| Google Search Console | — | ❌ ממתין למייקל |
| Google Business Profile | — | ❌ ממתין למייקל (הכי משפיע) |

## 5. חשבונות ושירותים
| שירות | תפקיד | סטטוס |
|---|---|---|
| DomainTheNet | רשם דומיין | פעיל |
| Netlify | אחסון ופריסה | חי (berg-law.netlify.app) |
| GitHub | קוד | פעיל (michaelbarg/berg-law) |
| Buffer | תזמון רשתות | ✅ פעיל — לינקדאין מחובר, API עובד (GraphQL, טוקן ב-.env) |
| Grow | סליקה | ממתין הקמה |

## 6. משימות פתוחות (נכון ל-10.8)
1. ✅ מאמר יומי 07.08 — נכתב ע"י הארכיטקט, שולב ונפרס ע"י Claude Code (7.8, קומיט 7c2fa89)
2. הקמת Grow (סליקה) → הדבקת הקישור ב-PAY_LINKS.docs (כרגע הזמנות נסחים נופלות לוואטסאפ)
3. ✅ Buffer הוקם ועובד — פוסט ערך ראשון (ערבות אישית) פורסם ללינקדאין 7.8 דרך ה-API. נותר: טעינת תוכן שבוע 1 (דורש שחזור berg-co-week1-content.md)
4. שחזור 4 מסמכי הארכיטקט משיחת קלוד ושמירתם בדיסק/ריפו
5. רשות: העברת berg-co-brand-guide.md ו-berg-carousel-maker.html מה-Downloads לריפו
6. ✅ אוטומציית תוכן — הועברה 10.8 לארכיטקטורת **תור** אחרי שהריצות היומיות המשיכו לדווח "דולג" (הגשר למק מתנתק לסירוגין; סשן מתוזמן לא מצליח להסתמך עליו). כעת: מאמרים עם תאריכים עתידיים יושבים ב-articles.json ו-renderArticles מסנן לפי `_todayEnd` — האתר מפרסם מאמר לבד כל בוקר, בלי מק ובלי אוטומציה; פוסטים מתוזמנים מראש ב-Buffer ומתפרסמים משם. שני הטריגרים היומיים נמחקו, ובמקומם טריגר **שבועי** למילוי התור (ראשון 10:00, trig_01RU8NBByXmUCKrfCdviu88P). מלאי נוכחי: מאמרים עד 16.08, פוסטים עד 23.08. ספר הפעלה: claude/berg-pipeline.md בפרויקט
