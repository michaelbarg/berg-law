#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ברג ושות׳ — הוספת 10 כתבות לתאריכים 17.08–26.08.2026

הרצה מתוך שורש הריפו (/Users/michael/berg-law):
    python3 add-articles-aug17-26.py

מה הוא עושה:
  1. קורא את content/articles.json
  2. מדלג על כל תאריך שכבר קיים (אידמפוטנטי — אפשר להריץ פעמיים בלי נזק)
  3. מוסיף את הכתבות החדשות וממיין החדש-ראשון
  4. כותב content/full/<slug>.html לכל כתבה חדשה (לא דורס קובץ קיים)
  5. מדפיס את הפקודות הבאות

אחרי ההרצה חובה:
    node scripts/build-articles.js
    node scripts/build-practice.js
"""

import json
import os
import sys
from datetime import datetime

REPO = os.path.dirname(os.path.abspath(__file__))
ARTICLES_JSON = os.path.join(REPO, "content", "articles.json")
FULL_DIR = os.path.join(REPO, "content", "full")

# ---------------------------------------------------------------- כתבות
# החדש ראשון. סכמה זהה לרשומות הקיימות.

ARTICLES = [
{
 "date": "26.08.2026",
 "slug": "nda-what-it-protects",
 "tag": {"he": "חוזים", "en": "Contracts", "ru": "Договоры", "fr": "Contrats"},
 "title": {
  "he": "הסכם סודיות: מה הוא באמת מגן עליו — ומה לא",
  "en": "An NDA: what it actually protects — and what it does not",
  "ru": "Соглашение о неразглашении: что оно защищает на самом деле",
  "fr": "Accord de confidentialité : ce qu'il protège vraiment — et ce qu'il ne protège pas"
 },
 "body": {
  "he": "הסכם סודיות מגן על מידע שהוגדר, סומן ונמסר בתנאי סודיות. הוא כמעט לא מגן על רעיון כללי, על ידע שכבר פומבי, או על מה שנאמר בפגישה שהתקיימה לפני החתימה. שלושה תיקונים שהופכים אותו ממסמך טקסי לכלי שאפשר להישען עליו.",
  "en": "A non-disclosure agreement protects information that was defined, marked and delivered in confidence. It offers little protection for a general idea, for knowledge already in the public domain, or for whatever was said in a meeting held before it was signed. Three amendments that turn it from a ceremonial document into a usable tool.",
  "ru": "Соглашение о неразглашении защищает информацию, которая была определена, помечена и передана в режиме конфиденциальности. Оно почти не защищает общую идею, уже публичные сведения или то, что прозвучало на встрече до подписания. Три правки, превращающие его в реальный инструмент.",
  "fr": "Un accord de confidentialité protège l'information définie, identifiée et transmise sous condition de confidentialité. Il ne protège guère une idée générale, un savoir déjà public, ou ce qui a été dit lors d'une réunion antérieure à sa signature. Trois correctifs qui en font un outil réel."
 },
 "gzTag": {"he": "פסיקה", "en": "Case law", "ru": "Судебная практика", "fr": "Jurisprudence"},
 "gzTitle": {
  "he": "אכיפת הסכמי סודיות — מגמות בבתי המשפט",
  "en": "Enforcing confidentiality agreements — court trends",
  "ru": "Исполнение соглашений о неразглашении — тенденции судов",
  "fr": "L'exécution des accords de confidentialité — tendances"
 }
},
{
 "date": "25.08.2026",
 "slug": "foreign-resident-starting-business-israel",
 "tag": {"he": "עולים ותושבי חוץ", "en": "Olim & Foreign Residents", "ru": "Репатрианты и нерезиденты", "fr": "Olim et résidents étrangers"},
 "title": {
  "he": "תושב חוץ שפותח עסק בישראל: עוסק, חברה או חברה זרה",
  "en": "A foreign resident opening a business in Israel: sole trader, company or foreign entity",
  "ru": "Нерезидент открывает бизнес в Израиле: ИП, компания или иностранное лицо",
  "fr": "Un non-résident ouvre une activité en Israël : entrepreneur, société ou entité étrangère"
 },
 "body": {
  "he": "הבחירה בין עוסק, חברה ישראלית או רישום חברה זרה משפיעה על אחריות אישית, על היקף הדיווח ועל היכולת לפתוח חשבון בנק ולהתקשר עם ספקים. מה נדרש בדרך כלל כשבעל השליטה אינו תושב ישראל, ומה עדיף להסדיר לפני הרישום ולא אחריו.",
  "en": "The choice between a sole trader registration, an Israeli company or registering a foreign entity affects personal liability, reporting scope and the practical ability to open a bank account and contract with suppliers. What is generally required when the controlling owner is not an Israeli resident, and what is better settled before registration rather than after.",
  "ru": "Выбор между статусом ИП, израильской компанией или регистрацией иностранной компании влияет на личную ответственность, объём отчётности и возможность открыть счёт и работать с поставщиками. Что обычно требуется, когда контролирующий владелец не является резидентом Израиля.",
  "fr": "Le choix entre le statut d'entrepreneur, une société israélienne ou l'enregistrement d'une entité étrangère influe sur la responsabilité personnelle, l'étendue des déclarations et la capacité à ouvrir un compte bancaire. Ce qui est généralement exigé lorsque le dirigeant n'est pas résident israélien."
 },
 "gzTag": {"he": "רגולציה", "en": "Regulation", "ru": "Регулирование", "fr": "Réglementation"},
 "gzTitle": {
  "he": "רישום עסקים בבעלות זרה — דרישות מתעדכנות",
  "en": "Registering foreign-owned businesses — evolving requirements",
  "ru": "Регистрация бизнеса с иностранным участием — новые требования",
  "fr": "Enregistrement d'entreprises à capitaux étrangers — exigences actualisées"
 }
},
{
 "date": "24.08.2026",
 "slug": "director-duties-small-company",
 "tag": {"he": "דיני חברות", "en": "Corporate Law", "ru": "Корпоративное право", "fr": "Droit des sociétés"},
 "title": {
  "he": "דירקטור בחברה קטנה: מה בעצם מוטל עליך",
  "en": "A director in a small company: what is actually expected of you",
  "ru": "Директор малой компании: что на вас на самом деле возложено",
  "fr": "Administrateur d'une petite société : ce qui pèse réellement sur vous"
 },
 "body": {
  "he": "חובת הזהירות וחובת האמונים חלות גם כשהדירקטוריון הוא שני שותפים סביב שולחן במטבח. מה נדרש בפועל — עיון במידע לפני החלטה, גילוי עניין אישי, והימנעות מהצבעה במצב ניגוד — ולמה פרוטוקול קצר הוא ההגנה הזולה ביותר שקיימת.",
  "en": "The duty of care and the duty of loyalty apply even when the board is two partners around a kitchen table. What is required in practice — reviewing the information before deciding, disclosing a personal interest, and abstaining where there is a conflict — and why a short set of minutes is the cheapest protection available.",
  "ru": "Обязанность осмотрительности и обязанность лояльности действуют, даже когда совет директоров — это два партнёра за кухонным столом. Что требуется на практике: изучить информацию до решения, раскрыть личный интерес и воздержаться при конфликте.",
  "fr": "Le devoir de prudence et le devoir de loyauté s'appliquent même lorsque le conseil se résume à deux associés autour d'une table. Ce qui est exigé en pratique : examiner l'information avant de décider, déclarer un intérêt personnel, s'abstenir en cas de conflit."
 },
 "gzTag": {"he": "פסיקה", "en": "Case law", "ru": "Судебная практика", "fr": "Jurisprudence"},
 "gzTitle": {
  "he": "אחריות דירקטורים בחברות פרטיות — התפתחויות",
  "en": "Director liability in private companies — developments",
  "ru": "Ответственность директоров в частных компаниях — развитие",
  "fr": "Responsabilité des administrateurs en société privée — évolutions"
 }
},
{
 "date": "23.08.2026",
 "slug": "marketing-emails-consent",
 "tag": {"he": "הגנת הפרטיות", "en": "Privacy", "ru": "Защита данных", "fr": "Vie privée"},
 "title": {
  "he": "דיוור שיווקי ללקוחות: הסכמה, הסרה ותיעוד",
  "en": "Marketing messages to customers: consent, opt-out and record-keeping",
  "ru": "Маркетинговая рассылка клиентам: согласие, отписка и учёт",
  "fr": "Prospection commerciale : consentement, désinscription et traçabilité"
 },
 "body": {
  "he": "משלוח פרסומת בדוא\"ל, ב-SMS או בוואטסאפ מחייב הסכמה מראש ואפשרות הסרה פשוטה ומיידית — והנטל להראות שההסכמה אכן ניתנה מוטל על השולח. מה נחשב הסכמה תקפה, מה לא, ואיזה שדה כדאי שיהיה בכל רשומה במאגר הלקוחות.",
  "en": "Sending promotional messages by email, SMS or WhatsApp requires prior consent and a simple, immediate opt-out — and the burden of showing consent was given rests on the sender. What counts as valid consent, what does not, and which field belongs in every record in your customer database.",
  "ru": "Отправка рекламы по электронной почте, SMS или WhatsApp требует предварительного согласия и простой мгновенной отписки, а бремя доказывания согласия лежит на отправителе. Что считается действительным согласием и какое поле должно быть в каждой записи базы.",
  "fr": "L'envoi de messages publicitaires par courriel, SMS ou WhatsApp suppose un consentement préalable et une désinscription simple et immédiate — la charge de la preuve incombant à l'expéditeur. Ce qui constitue un consentement valable, et le champ à prévoir dans chaque fiche client."
 },
 "gzTag": {"he": "חקיקה", "en": "Legislation", "ru": "Законодательство", "fr": "Législation"},
 "gzTitle": {
  "he": "דיוור פרסומי ואכיפה — מגמות רגולטוריות",
  "en": "Promotional messaging and enforcement — regulatory trends",
  "ru": "Рекламные рассылки и правоприменение — тенденции",
  "fr": "Messages promotionnels et sanctions — tendances réglementaires"
 }
},
{
 "date": "22.08.2026",
 "slug": "small-claims-what-decides",
 "tag": {"he": "תביעות קטנות", "en": "Small Claims", "ru": "Малые иски", "fr": "Petits litiges"},
 "title": {
  "he": "תביעה קטנה: מה באמת מכריע בדיון",
  "en": "Small claims: what actually decides the hearing",
  "ru": "Малый иск: что действительно решает исход слушания",
  "fr": "Petit litige : ce qui décide vraiment à l'audience"
 },
 "body": {
  "he": "בתביעות קטנות בעל הדין מופיע בעצמו, וזה בדיוק מה שהופך את ההכנה לקריטית. מה שמכריע הוא כמעט אף פעם לא רהיטות אלא סדר: כרונולוגיה ברורה, מסמכים ממוספרים ומסומנים, וסכום שאפשר להסביר במשפט אחד.",
  "en": "In small claims the party appears in person, which is exactly what makes preparation decisive. What wins is almost never eloquence but order: a clear chronology, numbered and labelled documents, and a sum you can explain in one sentence.",
  "ru": "В производстве по малым искам сторона выступает лично — именно поэтому подготовка решает всё. Побеждает не красноречие, а порядок: понятная хронология, пронумерованные документы и сумма, объяснимая одной фразой.",
  "fr": "Devant la juridiction des petits litiges, la partie comparaît en personne — c'est précisément ce qui rend la préparation décisive. Ce qui l'emporte n'est pas l'éloquence mais l'ordre : chronologie claire, pièces numérotées, montant explicable en une phrase."
 },
 "gzTag": {"he": "רגולציה", "en": "Regulation", "ru": "Регулирование", "fr": "Réglementation"},
 "gzTitle": {
  "he": "בתי משפט לתביעות קטנות — נהלי דיון ועומסים",
  "en": "Small claims courts — procedure and caseload",
  "ru": "Суды по малым искам — процедура и нагрузка",
  "fr": "Juridictions de petits litiges — procédure et charge"
 }
},
{
 "date": "21.08.2026",
 "slug": "registering-a-nonprofit-israel",
 "tag": {"he": "עמותות ומלכ\"רים", "en": "Nonprofits", "ru": "НКО", "fr": "Associations"},
 "title": {
  "he": "רישום עמותה: מטרות, ועד וניגוד עניינים — מה נקבע כבר ביום הראשון",
  "en": "Registering an Israeli nonprofit: purposes, board and conflicts — decided on day one",
  "ru": "Регистрация НКО в Израиле: цели, правление и конфликт интересов",
  "fr": "Créer une association en Israël : objets, conseil et conflits d'intérêts"
 },
 "body": {
  "he": "ניסוח המטרות בתקנון קובע מה העמותה תוכל לעשות שנים קדימה, והרכב הוועד וועדת הביקורת קובע אם יתקבל אישור ניהול תקין. שלוש טעויות נפוצות בהקמה שמתגלות רק כשמבקשים תמיכה ציבורית או תרומה משמעותית.",
  "en": "The way the purposes are drafted in the articles determines what the nonprofit may do for years to come, and the composition of the board and audit committee determines whether proper-management approval will be granted. Three common founding mistakes that surface only when applying for public funding or a significant donation.",
  "ru": "Формулировка целей в уставе определяет, чем организация сможет заниматься годы спустя, а состав правления и ревизионной комиссии — получит ли она сертификат надлежащего управления. Три частые ошибки при создании.",
  "fr": "La rédaction des objets statutaires détermine ce que l'association pourra faire des années durant, et la composition du conseil et du comité d'audit conditionne l'obtention du certificat de bonne gestion. Trois erreurs fréquentes à la création."
 },
 "gzTag": {"he": "רגולציה", "en": "Regulation", "ru": "Регулирование", "fr": "Réglementation"},
 "gzTitle": {
  "he": "רשם העמותות — דרישות ניהול תקין מתעדכנות",
  "en": "Registrar of Nonprofits — proper-management requirements updated",
  "ru": "Реестр НКО — обновление требований к управлению",
  "fr": "Registre des associations — exigences de gestion actualisées"
 }
},
{
 "date": "20.08.2026",
 "slug": "preliminary-agreement-binding",
 "tag": {"he": "מקרקעין", "en": "Real Estate", "ru": "Недвижимость", "fr": "Immobilier"},
 "title": {
  "he": "זיכרון דברים: המסמך ה\"לא מחייב\" שכן מחייב",
  "en": "The preliminary agreement: the “non-binding” document that binds",
  "ru": "Предварительное соглашение: «необязывающий» документ, который обязывает",
  "fr": "L'avant-contrat : le document « non contraignant » qui engage"
 },
 "body": {
  "he": "זיכרון דברים שמפרט צדדים, נכס, מחיר ומועד עשוי להיחשב חוזה מחייב לכל דבר — גם אם נכתב בו שייחתם הסכם מפורט בהמשך. מה הופך אותו למחייב, אילו חובות דיווח עשויות להתחיל לרוץ ממועד החתימה, ולמה במקרים רבים עדיף פשוט לא לחתום עליו.",
  "en": "A preliminary agreement that names the parties, the property, the price and the date may amount to a fully binding contract — even if it states that a detailed agreement will follow. What makes it binding, which reporting duties may start running from the signing date, and why in many cases it is better not to sign one at all.",
  "ru": "Предварительное соглашение с указанием сторон, объекта, цены и срока может быть признано полноценным договором, даже если в нём сказано, что позже будет подписан подробный контракт. Что делает его обязывающим и какие обязанности по отчётности могут начаться с момента подписания.",
  "fr": "Un avant-contrat mentionnant les parties, le bien, le prix et la date peut valoir contrat pleinement contraignant, même s'il annonce un accord détaillé à venir. Ce qui le rend contraignant, quelles obligations déclaratives peuvent courir dès la signature."
 },
 "gzTag": {"he": "פסיקה", "en": "Case law", "ru": "Судебная практика", "fr": "Jurisprudence"},
 "gzTitle": {
  "he": "זיכרון דברים בעסקאות מקרקעין — הגישה בפסיקה",
  "en": "Preliminary agreements in property deals — the judicial approach",
  "ru": "Предварительные соглашения в сделках с недвижимостью — практика",
  "fr": "Avant-contrats immobiliers — l'approche jurisprudentielle"
 }
},
{
 "date": "19.08.2026",
 "slug": "employee-or-freelancer-tests",
 "tag": {"he": "דיני עבודה", "en": "Employment Law", "ru": "Трудовое право", "fr": "Droit du travail"},
 "title": {
  "he": "עובד או פרילנסר? הכותרת בחוזה לא מכריעה",
  "en": "Employee or freelancer? The label on the contract does not decide",
  "ru": "Работник или фрилансер? Название договора ничего не решает",
  "fr": "Salarié ou indépendant ? L'intitulé du contrat ne décide de rien"
 },
 "body": {
  "he": "בית הדין בוחן את מהות היחסים בפועל ולא את שם ההסכם: מידת ההשתלבות בעסק, התלות הכלכלית, מי קובע את סדר היום ומי נושא בסיכון. הכרה בדיעבד ביחסי עובד-מעסיק יוצרת חבות רטרואקטיבית — ואיך לבנות התקשרות שמשקפת באמת את מה שקורה בשטח.",
  "en": "The labour court examines the substance of the relationship rather than the name of the agreement: how integrated the person is in the business, economic dependence, who sets the agenda and who carries the risk. A retroactive finding of employment creates retroactive liability — and how to structure an engagement that genuinely reflects reality.",
  "ru": "Суд по труду смотрит на суть отношений, а не на название договора: степень интеграции в бизнес, экономическая зависимость, кто определяет распорядок и кто несёт риск. Признание трудовых отношений задним числом порождает ретроактивные обязательства.",
  "fr": "Le tribunal du travail examine la substance de la relation, non l'intitulé du contrat : intégration dans l'entreprise, dépendance économique, qui fixe l'agenda et qui porte le risque. Une requalification rétroactive engendre une dette rétroactive."
 },
 "gzTag": {"he": "פסיקה", "en": "Case law", "ru": "Судебная практика", "fr": "Jurisprudence"},
 "gzTitle": {
  "he": "סיווג יחסי עבודה מול פרילנסרים — מגמות בבתי הדין",
  "en": "Classifying freelancers as employees — trends in the labour courts",
  "ru": "Квалификация отношений с фрилансерами — тенденции судов",
  "fr": "Requalification des indépendants — tendances des tribunaux"
 }
},
{
 "date": "18.08.2026",
 "slug": "jurisdiction-and-governing-law-clause",
 "tag": {"he": "חוזים", "en": "Contracts", "ru": "Договоры", "fr": "Contrats"},
 "title": {
  "he": "סעיף שיפוט וברירת דין: שתי שורות שקובעות כמה יעלה לכם סכסוך",
  "en": "Jurisdiction and governing law: two lines that decide what a dispute will cost you",
  "ru": "Подсудность и применимое право: две строки, определяющие цену спора",
  "fr": "Compétence et loi applicable : deux lignes qui fixent le coût d'un litige"
 },
 "body": {
  "he": "היכן יידון סכסוך ולפי דין של איזו מדינה — שתי שורות שנקבעות בשקט בסוף החוזה ומשפיעות על עלות ההליך יותר מכמעט כל סעיף אחר. מה ההבדל בין סמכות ייחודית למקבילה, מתי בוררות עדיפה, ולמה כדאי להסתכל על הסעיף הזה לפני שמסתכלים על המחיר.",
  "en": "Where a dispute will be heard and under which country's law — two lines quietly settled at the end of the contract that affect the cost of proceedings more than almost any other clause. The difference between exclusive and concurrent jurisdiction, when arbitration is preferable, and why this clause deserves attention before the price does.",
  "ru": "Где будет рассматриваться спор и по праву какой страны — две строки в конце договора, влияющие на стоимость процесса сильнее почти любого другого пункта. Разница между исключительной и альтернативной подсудностью и когда предпочтителен арбитраж.",
  "fr": "Où le litige sera jugé et selon quel droit — deux lignes discrètes en fin de contrat qui pèsent sur le coût de la procédure plus que presque toute autre clause. Compétence exclusive ou concurrente, et quand l'arbitrage est préférable."
 },
 "gzTag": {"he": "פסיקה", "en": "Case law", "ru": "Судебная практика", "fr": "Jurisprudence"},
 "gzTitle": {
  "he": "תניות שיפוט בחוזים מסחריים — לאן נוטים בתי המשפט",
  "en": "Jurisdiction clauses in commercial contracts — where courts lean",
  "ru": "Оговорки о подсудности в коммерческих договорах — позиция судов",
  "fr": "Clauses attributives de compétence — l'orientation des tribunaux"
 }
},
{
 "date": "17.08.2026",
 "slug": "trademark-search-before-launch",
 "tag": {"he": "קניין רוחני", "en": "Intellectual Property", "ru": "Интеллектуальная собственность", "fr": "Propriété intellectuelle"},
 "title": {
  "he": "בדקתם שהשם פנוי? חיפוש בגוגל הוא לא בדיקת סימן מסחר",
  "en": "Checked the name is free? A Google search is not a trademark search",
  "ru": "Проверили, свободно ли имя? Поиск в Google — не проверка товарного знака",
  "fr": "Le nom est libre ? Une recherche Google n'est pas une recherche de marque"
 },
 "body": {
  "he": "דומיין פנוי ושם משתמש פנוי ברשתות אינם אומרים שהשם פנוי לרישום. בדיקה אמיתית נעשית במאגר רשם סימני המסחר, לפי סיווג הסחורות והשירותים, ובוחנת גם דמיון מטעה ולא רק זהות. מה כדאי לבדוק לפני שמזמינים שילוט, אריזות ואתר.",
  "en": "A free domain and an available social handle do not mean the name is free to register. A real check is run against the trademark registry, by class of goods and services, and looks for confusing similarity rather than identity alone. What to verify before ordering signage, packaging and a website.",
  "ru": "Свободный домен и незанятый ник в соцсетях не означают, что имя свободно для регистрации. Настоящая проверка ведётся по реестру товарных знаков, по классам товаров и услуг, и учитывает сходство до степени смешения.",
  "fr": "Un domaine libre et un identifiant social disponible ne signifient pas que le nom est enregistrable. La vraie vérification se fait au registre des marques, par classe de produits et services, et recherche la similitude prêtant à confusion."
 },
 "gzTag": {"he": "קניין רוחני", "en": "Intellectual Property", "ru": "Интеллектуальная собственность", "fr": "Propriété intellectuelle"},
 "gzTitle": {
  "he": "רישום סימני מסחר — הליכי בחינה ומועדי התנגדות",
  "en": "Trademark registration — examination and opposition timelines",
  "ru": "Регистрация товарных знаков — экспертиза и сроки возражений",
  "fr": "Enregistrement des marques — examen et délais d'opposition"
 }
},
]

# ------------------------------------------------------- עמודי הכתבה המלאים
# ⚠️ לוודא מול קובץ קיים (למשל content/full/tabu-extract-before-signing.html)
#    אם הקבצים הקיימים הם מסמך HTML שלם ולא פרגמנט — לעטוף בהתאם.

FULL = {

"trademark-search-before-launch": """<p>הרבה עסקים בוחרים שם, בודקים שהדומיין פנוי, תופסים שם משתמש באינסטגרם — ומזמינים שילוט. שלושת הבדיקות האלה חשובות, אבל אף אחת מהן אינה בדיקת סימן מסחר.</p>

<h2>מה בעצם בודקים</h2>
<p>בדיקה אמיתית נעשית מול מאגר רשם סימני המסחר, והיא מתבצעת <strong>לפי סיווג</strong>: אותו שם עשוי להיות רשום לתחום אחד ופנוי לחלוטין בתחום אחר. לכן השאלה הראשונה היא לא "האם השם תפוס" אלא "האם השם תפוס בסיווג שבו אני פועל".</p>
<p>הבדיקה גם רחבה יותר מזהות מוחלטת. סימן קיים עשוי לחסום שם חדש כאשר קיים <strong>דמיון מטעה</strong> — צליל דומה, משמעות דומה, או מראה חזותי שעלול לבלבל צרכן סביר. שינוי אות אחת אינו פותר את הבעיה.</p>

<h2>שם חברה, דומיין וסימן מסחר הם שלושה דברים שונים</h2>
<p>רישום שם חברה ברשם החברות אינו מקנה זכות בשם מול מתחרים. דומיין הוא חוזה שירות מול רשם הדומיינים. סימן מסחר רשום הוא זכות קניינית — והוא היחיד מבין השלושה שמאפשר למנוע מאחר להשתמש בשם.</p>

<h2>מה כדאי לעשות, ובאיזה סדר</h2>
<ul>
  <li>לבצע בדיקת כשירות וזמינות <em>לפני</em> ההשקעה בעיצוב, שילוט, אריזות ואתר — לא אחריה.</li>
  <li>לבחור סיווגים לפי הפעילות בפועל ולפי מה שמתוכנן בשנתיים הקרובות, לא רק לפי היום.</li>
  <li>לשמור תיעוד של מועד תחילת השימוש בשם: חשבוניות, פרסומים, צילומי מסך מתוארכים.</li>
  <li>אם קיים סימן דומה — לשקול שינוי מהותי בשם מוקדם ככל האפשר. מיתוג מחדש בשנה השנייה יקר בהרבה.</li>
</ul>

<p>שם הוא אחד הנכסים היקרים של עסק, והוא גם אחד הבודדים שאפשר לאבד בבת אחת. שעה של בדיקה בתחילת הדרך חוסכת את הדילמה של החלפת שם אחרי שהלקוחות כבר מכירים אותו.</p>""",

"jurisdiction-and-governing-law-clause": """<p>בסוף כל חוזה מסחרי יש שתי שורות שכמעט אף אחד לא מתמקח עליהן: היכן יידון סכסוך, ולפי איזה דין. הן נראות טכניות. בפועל הן קובעות כמה יעלה לכם סכסוך — לפעמים יותר מכל סעיף אחר בחוזה.</p>

<h2>סמכות שיפוט: איפה מתדיינים</h2>
<p>תניית שיפוט קובעת את בית המשפט שידון בסכסוך. ההבחנה המרכזית היא בין <strong>סמכות ייחודית</strong> — רק בית משפט אחד מוסמך — לבין <strong>סמכות מקבילה</strong>, שמאפשרת לפנות גם לערכאות אחרות. ניסוח לא ברור מייצר הליך מקדמי שלם רק כדי להכריע היכן יתנהל ההליך העיקרי.</p>
<p>המרחק הוא לא עניין של נוחות בלבד. התדיינות בעיר אחרת, ובוודאי במדינה אחרת, משנה את עלות הייצוג, את זמינות העדים ואת הכדאיות הכלכלית של התביעה. צד חזק שמכניס תניית שיפוט רחוקה יודע בדיוק מה הוא עושה.</p>

<h2>ברירת דין: לפי איזה חוק</h2>
<p>בהתקשרות בין־לאומית זו שאלה נפרדת לחלוטין. אפשר להתדיין בישראל לפי דין זר, ולהפך. דין זר מחייב הוכחה בבית המשפט באמצעות מומחה — הוצאה שנוספת לכל הליך.</p>

<h2>בוררות — מתי היא באמת עדיפה</h2>
<p>בוררות מהירה יותר וחסויה יותר, ולעיתים מאפשרת בורר בעל מומחיות בתחום. מנגד, היא כרוכה בעלות מיידית, וערעור עליה מוגבל מאוד. ככלל, היא מתאימה יותר להתקשרויות ארוכות טווח בין צדדים שממשיכים לעבוד יחד, ופחות לגבייה פשוטה.</p>

<h2>שלוש שאלות לפני שחותמים</h2>
<ul>
  <li>אם אני אצטרך לתבוע, כמה יעלה לי להגיע לשם — ומה זה עושה לכדאיות של תביעה קטנה יחסית?</li>
  <li>האם הסעיף סימטרי, או שהוא נוח רק לצד שניסח את החוזה?</li>
  <li>אם נקבעה בוררות — מי ממנה את הבורר, ומי נושא בעלות?</li>
</ul>

<p>זו אחת הנקודות שבהן שינוי של מילה אחת בשלב המשא ומתן שווה יותר מכל טיעון מבריק בשלב הסכסוך.</p>""",

"employee-or-freelancer-tests": """<p>"הוא עובד אצלנו כפרילנסר, יש חוזה." המשפט הזה נשמע מרגיע, והוא כמעט חסר משמעות. בית הדין לעבודה לא בוחן את שם ההסכם אלא את מה שקרה בפועל.</p>

<h2>מה נבחן בפועל</h2>
<p>המבחן המרכזי הוא מידת ההשתלבות בעסק: האם אותו אדם היה חלק מהמערך הרגיל של הפעילות, או ספק חיצוני שנתן שירות מוגדר. סביבו נבחנים סימנים נוספים — תלות כלכלית באותו מזמין, מי קובע את שעות העבודה וסדר העדיפויות, מי מספק את הכלים, מי נושא בסיכון הכלכלי, והאם הייתה אפשרות אמיתית לעבוד עבור אחרים.</p>
<p>אף סימן אחד אינו מכריע לבדו. התמונה המצטברת היא שקובעת, ולכן שני הסדרים שנראים דומים על הנייר עשויים להסתיים אחרת לגמרי.</p>

<h2>למה זה מסוכן דווקא בעסק קטן</h2>
<p>כשמכירים ביחסי עובד-מעסיק בדיעבד, ההכרה חלה על כל התקופה. מדובר בחשיפה מצטברת לרכיבים סוציאליים שלא שולמו לאורך שנים — הוצאה שמתגלה בבת אחת, בדרך כלל בדיוק ברגע שבו העסק הכי פחות מוכן אליה.</p>

<h2>איך בונים התקשרות שמחזיקה</h2>
<ul>
  <li>להגדיר תוצר ולא נוכחות. "אספקת X עד תאריך Y" ולא "זמינות בימים א'–ה'".</li>
  <li>לא לשלב את נותן השירות במבנה הניהולי — בלי מנהל ישיר, בלי הערכת ביצועים, בלי כפיפות בארגון.</li>
  <li>להימנע מבלעדיות בפועל. ספק שכל הכנסתו ממזמין אחד לאורך שנים נראה כמו עובד.</li>
  <li>לתמחר את הפער. תעריף שזהה לעלות שכר של עובד מחליש את הטענה שמדובר בהתקשרות עסקית.</li>
  <li>לבדוק את ההסדר מחדש כל שנה. התקשרות מתחילה כשירות חיצוני ונשחקת לאט לתוך העסק.</li>
</ul>

<p>השורה התחתונה פשוטה: אם ההתנהלות היומיומית נראית כמו העסקה, שם ההסכם לא ישנה את זה. עדיף לבחור מודל אחד ולעמוד בו באמת.</p>""",

"preliminary-agreement-binding": """<p>זיכרון דברים נחתם בדרך כלל בסוף ערב, בהתלהבות, כדי "לסגור את זה" לפני שמישהו אחר יגיע. זו בדיוק הסיבה שהוא מסוכן.</p>

<h2>מתי הוא מחייב</h2>
<p>מסמך מחייב כשמתקיימים בו שני תנאים: גמירת דעת — הצדדים התכוונו להתקשר — ומסוימות, כלומר הפרטים המהותיים סוכמו. זיכרון דברים שמזהה את הצדדים, את הנכס, את המחיר ואת מועד המסירה עשוי לקיים את שני התנאים במלואם.</p>
<p>המשפט "ייחתם הסכם מפורט בהמשך" אינו מבטל זאת מאליו. הוא ראיה לכוונה, אבל כשהמסמך עצמו כבר מסדיר את העיקר, הוא עשוי להיחשב חוזה שלם שהמסמך הבא רק ירחיב.</p>

<h2>מה נשאר בחוץ — ועולה כסף</h2>
<p>זיכרון דברים כמעט אף פעם אינו מסדיר את מה שבאמת מסבך עסקאות: מנגנון תשלומים מול הסרת שעבודים, ערבויות, מועד קבלת החזקה, טיפול בליקויים, וחלוקת אחריות לתשלומי חובה. הצדדים מגלים את הפערים האלה אחרי שהם כבר קשורים זה לזה.</p>

<h2>חובות דיווח</h2>
<p>עסקה במקרקעין מחייבת דיווח לרשויות, והמועד נגזר ממועד ההתקשרות המחייבת — לא ממועד ההסכם המפורט. חתימה על זיכרון דברים עשויה אפוא להתחיל מרוץ של מועדים בלי שהצדדים מודעים לכך.</p>

<h2>מה עושים במקום</h2>
<ul>
  <li>עדיף לא לחתום כלל, ולהיערך לחתימה על הסכם מלא תוך ימים ספורים.</li>
  <li>אם בכל זאת חותמים — לציין מפורשות אילו נושאים מהותיים <em>טרם</em> סוכמו, בשמם.</li>
  <li>לא להעביר תשלום כלשהו לפני בדיקת נסח עדכני ואימות זהות הבעלים הרשום.</li>
  <li>לתעד את הכוונה: אם המסמך נועד להיות בלתי מחייב, זה צריך להיות ברור מהנוסח ומההתנהגות כאחד.</li>
</ul>

<p>הכלל הפשוט: מה שחותמים עליו בערב אחד יכול לחייב שנים. עדיף להשקיע כמה ימים בהסכם אמיתי.</p>""",

"registering-a-nonprofit-israel": """<p>רוב מי שמקים עמותה מתמקד בשלב הראשון בשם ובלוגו. שני הדברים שיקבעו את גורל העמותה נמצאים בשני מקומות אחרים לגמרי: ניסוח המטרות, והרכב האנשים.</p>

<h2>המטרות בתקנון — התקרה של הפעילות</h2>
<p>עמותה רשאית לפעול רק במסגרת מטרותיה הרשומות. מטרות צרות מדי יחייבו הליך שינוי תקנון כשהפעילות תתפתח; מטרות רחבות ומעורפלות מדי עלולות לעורר שאלות ברישום ובבקשות תמיכה. הנוסח הנכון הוא ממוקד אך מנוסח ברמת עיקרון, כך שיכיל התפתחות סבירה.</p>

<h2>האנשים — כאן נופלות רוב הבקשות</h2>
<p>לעמותה נדרשים מוסדות נפרדים: אסיפה כללית, ועד, וגוף ביקורת. עקרון היסוד הוא הפרדה — מי שמכהן בוועד אינו יכול לשמש גם כמבקר, וקרבה משפחתית בין נושאי משרה מעוררת קושי. בעמותות משפחתיות זו הסיבה השכיחה ביותר לעיכוב באישור ניהול תקין.</p>

<h2>ניגוד עניינים ותשלומים</h2>
<p>תשלום לנושא משרה, התקשרות עם עסק בבעלות חבר ועד, או שכירת נכס מקרוב משפחה — כל אלה דורשים גילוי מלא, אישור מסודר ותיעוד. לא בהכרח אסור; אבל לא מתועד, זה נראה גרוע.</p>

<h2>שלוש טעויות שחוזרות</h2>
<ul>
  <li>העתקת תקנון מעמותה אחרת בלי להתאים את המטרות לפעילות בפועל.</li>
  <li>מינוי ועד שכולו בני משפחה אחת, ואז ניסיון "לתקן" זאת רק כשמבקשים אישור.</li>
  <li>תחילת גיוס תרומות לפני שקיימת התשתית לניהול כספי מסודר ולדיווח.</li>
</ul>

<p>אישור ניהול תקין הוא המפתח לתמיכות ולתרומות משמעותיות, והוא נבנה מהיום הראשון — לא ברגע שמגישים את הבקשה.</p>""",

"small-claims-what-decides": """<p>ההליך בתביעות קטנות נועד להיות פשוט ומהיר, ובעל הדין מופיע בו בעצמו. דווקא בגלל זה, ההכנה — ולא הכישרון הרטורי — היא מה שמכריע.</p>

<h2>מה השופט באמת צריך</h2>
<p>הדיון קצר. השופט צריך להבין בתוך דקות מה קרה, מתי, ומה הסכום המבוקש ועל בסיס מה חושב. תיק שמאורגן היטב עונה על שלוש השאלות האלה לבד; תיק מבולגן מבזבז את הזמן על שחזור העובדות במקום על המחלוקת עצמה.</p>

<h2>שלושה דברים שמייצרים את ההבדל</h2>
<ul>
  <li><strong>כרונולוגיה בעמוד אחד.</strong> תאריך, מה קרה, לאיזה מסמך זה מפנה. בלי פרשנות ובלי רגש.</li>
  <li><strong>מסמכים ממוספרים.</strong> נספח 1, נספח 2, ובכתב התביעה הפניה מפורשת לכל אחד. עותק לבית המשפט ועותק לצד השני.</li>
  <li><strong>סכום שאפשר להסביר במשפט אחד.</strong> "שילמתי X, קיבלתי Y, ההפרש הוא Z." סכום שנשמע מנופח פוגע באמינות כל התביעה.</li>
</ul>

<h2>מה פוגע דווקא בצד הצודק</h2>
<p>הרחבה לסיפורים שאינם רלוונטיים, התקפה אישית על הצד השני, וניסיון לטעון טענות רבות מדי במקביל. שלוש טענות חזקות עדיפות על עשר טענות בינוניות. גם הצגת מסמך בפעם הראשונה בדיון עצמה פוגעת — עדיף להגיש מראש.</p>

<h2>לפני הדיון</h2>
<p>כדאי לעבור על התיק בקול רם מול מישהו שאינו מכיר את הסיפור, ולראות אם הוא מבין את המחלוקת בתוך שתי דקות. אם לא — הבעיה אינה בשופט.</p>

<p>הליך פשוט אינו הליך שלא צריך להתכונן אליו. הוא הליך שבו ההכנה היא היתרון היחיד שיש.</p>""",

"marketing-emails-consent": """<p>עסק שאוסף כתובות דוא"ל ומספרי טלפון בונה נכס שיווקי אמיתי — ובמקביל, אחריות. הכללים לגבי דיוור פרסומי בישראל ברורים יחסית, והחשיפה בגינם מצטברת לפי מספר ההודעות שנשלחו.</p>

<h2>שלושת התנאים</h2>
<p>ככלל, משלוח פרסומת בדוא"ל, במסרון או בהודעה מיידית מחייב <strong>הסכמה מראש</strong> של הנמען, <strong>זיהוי ברור</strong> של השולח ושל אופי ההודעה, ו<strong>דרך הסרה פשוטה ומיידית</strong> באותו ערוץ שבו נשלחה ההודעה. הנטל להראות שההסכמה ניתנה מוטל על השולח — לא על הלקוח להוכיח שלא הסכים.</p>

<h2>מה נחשב הסכמה תקפה</h2>
<p>סימון יזום של הנמען, בשדה שאינו מסומן מראש, בסמוך למלל שמסביר למה בדיוק הוא מסכים. מה שאינו נחשב: תיבה מסומנת כברירת מחדל, הסכמה שנבלעת בתוך תנאי שימוש ארוכים, או כרטיס ביקור שנמסר בכנס.</p>
<p>לקוח קיים שרכש מוצר עשוי לקבל דיוור על מוצרים דומים בתנאים מסוימים — אך גם אז נדרשת אפשרות סירוב ברורה כבר במועד איסוף הפרטים.</p>

<h2>מה לשמור בכל רשומה</h2>
<ul>
  <li>מועד ההסכמה המדויק, מקורה (טופס, עמוד נחיתה, חנות), וגרסת הנוסח שהוצג.</li>
  <li>כתובת IP או מזהה טכני אחר, כשהאיסוף מקוון.</li>
  <li>מועד הסרה, אם בוצעה — וחסימה אפקטיבית מכל רשימות התפוצה, לא רק מזו שממנה הוסר.</li>
</ul>

<h2>הטעות התפעולית הנפוצה</h2>
<p>ייצוא רשימה לכלי דיוור חדש בלי להעביר איתה את נתוני ההסכמה. מרגע זה אין למי שמפעיל את המערכת שום דרך להראות מה הלקוח אישר. שדה אחד בקובץ מונע את זה מראש.</p>

<p>מעבר לחשיפה המשפטית, רשימה שנבנתה בהסכמה אמיתית פשוט עובדת טוב יותר.</p>""",

"director-duties-small-company": """<p>ברוב החברות הקטנות בישראל, הדירקטוריון הוא שני אנשים שממילא מדברים כל יום. זה לא משנה את העובדה שהחוק מטיל עליהם חובות אישיות.</p>

<h2>שתי החובות</h2>
<p><strong>חובת זהירות</strong> — לפעול ברמת מיומנות סבירה, ובעיקר לקבל החלטות על בסיס מידע. דירקטור שמאשר התקשרות משמעותית בלי לעיין בה מפר את החובה גם אם ההחלטה עצמה התבררה כנכונה.</p>
<p><strong>חובת אמונים</strong> — לפעול לטובת החברה ולא לטובת עצמו. כאן נמצאים ניגוד עניינים, ניצול הזדמנות עסקית של החברה, ותחרות בה.</p>

<h2>המקומות שבהם זה נשבר בחברה קטנה</h2>
<ul>
  <li>התקשרות של החברה עם עסק אחר בבעלות אחד השותפים, בלי גילוי ובלי אישור מסודר.</li>
  <li>העברת כספים בין החברה לבעליה בלי הסכם הלוואה ובלי תיעוד.</li>
  <li>המשך פעילות והתחייבות לספקים חדשים כשברור שהחברה מתקשה לעמוד בהתחייבויותיה.</li>
  <li>החלטות מהותיות שהתקבלו בשיחת טלפון ולא תועדו בשום מקום.</li>
</ul>

<h2>ההגנה הזולה ביותר</h2>
<p>פרוטוקול. לא מסמך משפטי — חצי עמוד: מה הוצג, מי היה נוכח, מי גילה עניין אישי, מה הוחלט ומדוע. ההשקעה היא עשר דקות אחרי כל החלטה משמעותית, והיא ההבדל בין "התקבלה החלטה עסקית מנומקת" לבין "אין תיעוד".</p>
<p>לצד זה כדאי לבדוק אם קיים ביטוח נושאי משרה, ומה הוא מכסה בפועל.</p>

<p>אחריות אישית אינה שאלה של גודל החברה. היא שאלה של האם אפשר להראות, בדיעבד, שההחלטה התקבלה כראוי.</p>""",

"foreign-resident-starting-business-israel": """<p>תושב חוץ שרוצה לפעול עסקית בישראל עומד בפני שלוש אפשרויות עיקריות, וההבדל ביניהן אינו טכני — הוא משפיע על אחריות אישית, על היקף הדיווח ועל היכולת הבסיסית לפתוח חשבון בנק.</p>

<h2>שלושת המסלולים</h2>
<p><strong>עוסק</strong> — פשוט וזול, אבל אין הפרדה בין העסק לאדם: כל חבות עסקית היא חבות אישית. מתאים לפעילות מצומצמת ובעלת סיכון נמוך.</p>
<p><strong>חברה ישראלית</strong> — ישות נפרדת עם אחריות מוגבלת. זהו המסלול הנפוץ ביותר, והוא גם המסלול שספקים ולקוחות עסקיים מצפים לו. דורש דירקטוריון, כתובת רשומה בישראל ודיווח שנתי.</p>
<p><strong>רישום חברה זרה</strong> — כאשר קיימת כבר חברה בחו"ל שרוצה לפעול בישראל ישירות. מחייב הגשת מסמכי ההתאגדות הזרים, מתורגמים ומאומתים, ומינוי מיופה כוח מקומי.</p>

<h2>מה בדרך כלל נדרש כשהבעלים אינו תושב</h2>
<ul>
  <li>אימות זהות ומסמכים באמצעות אפוסטיל או בקונסוליה — זה השלב שלוקח הכי הרבה זמן, וכדאי להתחיל בו ראשון.</li>
  <li>כתובת למסירת מסמכים בישראל.</li>
  <li>ייפוי כוח לחתימה ולהגשות, כשהבעלים אינו נוכח.</li>
  <li>היערכות לתהליך פתיחת החשבון בבנק, שהוא לרוב הצוואר הצר האמיתי ולא הרישום עצמו.</li>
</ul>

<h2>מה כדאי להסדיר לפני ולא אחרי</h2>
<p>מבנה ההחזקות ומיהו בעל השליטה, זכויות חתימה, ומי מוסמך לפעול בישראל בהיעדר הבעלים. שינוי של אלה אחרי הרישום אפשרי — אך הוא כרוך בהליך, ולעיתים בבדיקה מחודשת מול הבנק.</p>

<p>הכלל המעשי: לבחור מסלול לפי רמת הסיכון ולפי מי הלקוחות הצפויים, ולהתחיל באיסוף המסמכים המאומתים מוקדם ככל האפשר.</p>""",

"nda-what-it-protects": """<p>הסכם סודיות הוא אחד המסמכים שנחתמים הכי הרבה והכי מעט נקראים. בפועל, רובם מגנים על פחות ממה שהצדדים מדמיינים.</p>

<h2>מה NDA באמת מכסה</h2>
<p>הוא מגן על <strong>מידע</strong> — כלומר על משהו שהוגדר, נמסר, וניתן להצביע עליו. הוא כמעט לא מגן על רעיון כללי, על כיוון עסקי, או על "החזון". הוא גם אינו מגן על מידע שכבר פומבי, על מידע שהצד השני החזיק בו קודם, או על מידע שהגיע אליו כדין ממקור אחר.</p>
<p>נקודה שנשכחת: הוא לא חל למפרע. מה שנאמר בפגישת ההיכרות, לפני שנחתם, נשאר מחוץ להגנה — ולכן כדאי לחתום לפני שנפגשים, לא אחרי.</p>

<h2>שלושת התיקונים שמשנים אותו</h2>
<ul>
  <li><strong>הגדרה שאפשר לאכוף.</strong> "כל מידע שנמסר" רחב מדי ולכן חלש. עדיף להגדיר קטגוריות — מחירונים, רשימות לקוחות, מפרטים טכניים, תנאי התקשרות — ולנהוג בהתאם: לסמן מסמכים ולשלוח דרך ערוץ אחד מזוהה.</li>
  <li><strong>תקופה ריאלית.</strong> סודיות "לנצח" נראית חזקה ונוטה להיחלש בבחינה. תקופה מוגדרת וסבירה, ארוכה יותר עבור סוד מסחרי מובהק, מחזיקה טוב יותר.</li>
  <li><strong>סעד שאפשר להפעיל.</strong> חובת השבה או השמדה של החומר בתום ההתקשרות, והתייחסות מפורשת לסעד של צו מניעה — כי בהפרת סודיות הנזק לרוב אינו ניתן לכימוי מדויק.</li>
</ul>

<h2>מה שהסכם סודיות לא יעשה בשבילכם</h2>
<p>הוא לא מונע מאדם להשתמש בידע ובניסיון הכלליים שרכש, והוא אינו תחליף להסדרת בעלות בקניין רוחני. מי שמעביר פיתוח לספק חיצוני זקוק לסעיף העברת זכויות מפורש — NDA לבדו לא יקנה לו בעלות בתוצר.</p>

<p>השאלה המעשית לפני חתימה היא פשוטה: אם הצד השני יפר את זה מחר, מה בדיוק אוכל להראות שנמסר, ומתי? אם אין תשובה — הבעיה אינה בנוסח אלא בהתנהלות.</p>"""
}

# ---------------------------------------------------------------- ביצוע

def main():
    if not os.path.isfile(ARTICLES_JSON):
        sys.exit("לא נמצא %s — להריץ מתוך שורש הריפו." % ARTICLES_JSON)

    with open(ARTICLES_JSON, encoding="utf-8") as f:
        existing = json.load(f)

    have_dates = {a.get("date") for a in existing}
    have_slugs = {a.get("slug") for a in existing}

    added = []
    for art in ARTICLES:
        if art["date"] in have_dates:
            print("דילוג — %s כבר קיים" % art["date"])
            continue
        if art["slug"] in have_slugs:
            print("דילוג — slug כבר קיים: %s" % art["slug"])
            continue
        added.append(art)

    if not added:
        print("\nאין מה להוסיף. הקובץ כבר מעודכן.")
        return

    merged = added + existing
    merged.sort(key=lambda a: datetime.strptime(a["date"], "%d.%m.%Y"), reverse=True)

    os.makedirs(FULL_DIR, exist_ok=True)
    written = []
    for art in added:
        path = os.path.join(FULL_DIR, art["slug"] + ".html")
        if os.path.exists(path):
            print("קיים כבר, לא נדרס: %s" % path)
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(FULL[art["slug"]].strip() + "\n")
        written.append(path)

    with open(ARTICLES_JSON, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=1)
        f.write("\n")

    print("\n✓ נוספו %d כתבות (%s → %s)" % (
        len(added), added[-1]["date"], added[0]["date"]))
    print("✓ נכתבו %d עמודים מלאים ב-content/full/" % len(written))
    print("✓ סה\"כ כתבות בקובץ: %d" % len(merged))
    print("""
הצעד הבא:
    node scripts/build-articles.js
    node scripts/build-practice.js
    npx -y netlify-cli deploy --prod --dir .

ואז לאמת:  https://berg-law.co.il/content/articles.json
""")


if __name__ == "__main__":
    main()
