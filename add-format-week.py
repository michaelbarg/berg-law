#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ברג ושות׳ — שבוע פיילוט פורמטים: 6 כתבות (27.08–01.09), שדה format חדש.

הרצה משורש הריפו:  python3 add-format-week.py
אחר כך:            node scripts/build-articles.js && node scripts/build-practice.js
אידמפוטנטי — מדלג על תאריך/slug קיים, לא דורס content/full.
"""

import json, os, sys
from datetime import datetime

REPO = os.path.dirname(os.path.abspath(__file__))
AJ   = os.path.join(REPO, "content", "articles.json")
FULL = os.path.join(REPO, "content", "full")

# פורמטים: qa=שאלות ששואלים · term=מושג במשפט · didyouknow=הידעת
# bureaucracy=בירוקרטיה מפורקת · fear=ממה מפחדים · history=היסטוריה משפטית

ARTICLES = [
{
 "date": "01.09.2026", "slug": "history-of-the-tabu",
 "format": "history",
 "tag": {"he": "היסטוריה משפטית", "en": "Legal History", "ru": "История права", "fr": "Histoire du droit"},
 "title": {
  "he": "למה קוראים לזה \"טאבו\"? מסע קצר של מילה עות'מאנית",
  "en": "Why is it called \"Tabu\"? The short journey of an Ottoman word",
  "ru": "Почему это называется «Табу»? Краткая история османского слова",
  "fr": "Pourquoi dit-on « Tabou » ? Le bref voyage d'un mot ottoman"
 },
 "body": {
  "he": "כל ישראלי שקנה דירה מכיר את המילה \"טאבו\" — ומעטים יודעים שהיא ירושה עות'מאנית. רישום המקרקעין המודרני בארץ נשען על רפורמות הקרקעות של האימפריה העות'מאנית מהמאה ה-19, עבר דרך המנדט הבריטי שהקים את מפעל הסדר הזכויות, והגיע עד מרשם ממוחשב שמנפיק נסח בתוך דקות. סיפור קצר על איך שלוש אימפריות בנו את המסמך שאתם מזמינים היום אונליין.",
  "en": "Every Israeli who has bought an apartment knows the word \"Tabu\" — few know it is an Ottoman inheritance. Israel's modern land registry rests on 19th-century Ottoman land reforms, passed through the British Mandate's title-settlement project, and arrived at a computerized registry that issues an extract within minutes. A short story of how three empires built the document you now order online.",
  "ru": "Каждый израильтянин, покупавший квартиру, знает слово «Табу» — но мало кто знает, что это османское наследие. Современный земельный реестр Израиля опирается на османские земельные реформы XIX века, прошёл через британский мандат с его проектом урегулирования прав и дошёл до компьютеризированного реестра, выдающего выписку за минуты. Краткая история о том, как три империи создали документ, который вы сегодня заказываете онлайн.",
  "fr": "Tout Israélien ayant acheté un appartement connaît le mot « Tabou » — peu savent qu'il s'agit d'un héritage ottoman. Le registre foncier israélien moderne repose sur les réformes agraires ottomanes du XIXe siècle, est passé par le projet de règlement des titres du Mandat britannique, et a abouti à un registre informatisé délivrant un extrait en quelques minutes. La brève histoire de trois empires derrière le document que vous commandez aujourd'hui en ligne."
 },
 "gzTag": {"he": "מקרקעין", "en": "Real Estate", "ru": "Недвижимость", "fr": "Immobilier"},
 "gzTitle": {
  "he": "מהאימפריה העות'מאנית לנסח אונליין",
  "en": "From the Ottoman Empire to an online extract",
  "ru": "От Османской империи до выписки онлайн",
  "fr": "De l'Empire ottoman à l'extrait en ligne"
 }
},
{
 "date": "31.08.2026", "slug": "fear-demand-letter-first-hour",
 "format": "fear",
 "tag": {"he": "ממה מפחדים", "en": "Facing Your Fears", "ru": "Чего боятся", "fr": "Vaincre ses peurs"},
 "title": {
  "he": "קיבלתם מכתב התראה? מה עושים בשעה הראשונה — ומה אסור",
  "en": "Received a demand letter? What to do in the first hour — and what not to",
  "ru": "Получили письмо-предупреждение? Что делать в первый час — и чего не делать",
  "fr": "Vous avez reçu une mise en demeure ? Que faire la première heure — et que ne pas faire"
 },
 "body": {
  "he": "מכתב התראה נועד להלחיץ — זה חלק מהתפקיד שלו. אבל הוא גם רק מכתב: הוא אינו פסק דין, אינו עיקול, ולרוב הוא פתיחת משא ומתן ולא סופו. מה עושים: קוראים בנחת, בודקים מועדים, אוספים את המסמכים הרלוונטיים ולא נפטרים משום דבר. מה לא עושים: לא מתקשרים לצד השני בסערת רגשות, לא עונים מיד בכתב, ולא מתעלמים — התעלמות היא הטעות היקרה מכולן. תשובה עניינית ושקולה, לרוב בליווי מקצועי, משנה את מאזן הכוחות.",
  "en": "A demand letter is designed to pressure you — that is part of its job. But it is also just a letter: not a judgment, not a lien, and usually the opening of a negotiation rather than its end. What to do: read it calmly, note the deadlines, gather the relevant documents and discard nothing. What not to do: don't call the other side in the heat of the moment, don't fire back an immediate written reply, and don't ignore it — ignoring is the most expensive mistake. A measured, substantive response, usually with professional guidance, shifts the balance.",
  "ru": "Письмо-предупреждение создано, чтобы давить — это часть его задачи. Но это всего лишь письмо: не судебное решение и не арест, а чаще всего начало переговоров, а не их конец. Что делать: спокойно прочитать, отметить сроки, собрать документы и ничего не выбрасывать. Чего не делать: не звонить другой стороне на эмоциях, не отвечать письменно сгоряча и не игнорировать — игнорирование обходится дороже всего. Взвешенный ответ по существу, как правило при профессиональном сопровождении, меняет баланс сил.",
  "fr": "Une mise en demeure est conçue pour faire pression — c'est son rôle. Mais ce n'est qu'une lettre : ni un jugement, ni une saisie, et le plus souvent l'ouverture d'une négociation plutôt que sa fin. À faire : lire calmement, noter les délais, rassembler les documents pertinents et ne rien jeter. À ne pas faire : ne pas appeler l'autre partie sous le coup de l'émotion, ne pas répondre par écrit dans l'instant, et ne pas ignorer — l'ignorance est l'erreur la plus coûteuse. Une réponse mesurée et substantielle, généralement accompagnée d'un professionnel, change le rapport de force."
 },
 "gzTag": {"he": "גבייה וסכסוכים", "en": "Disputes", "ru": "Споры", "fr": "Litiges"},
 "gzTitle": {
  "he": "מכתב התראה הוא פתיחת משא ומתן, לא גזר דין",
  "en": "A demand letter opens a negotiation — it is not a verdict",
  "ru": "Письмо-предупреждение — начало переговоров, а не приговор",
  "fr": "La mise en demeure ouvre une négociation, ce n'est pas un verdict"
 }
},
{
 "date": "30.08.2026", "slug": "bureaucracy-opening-osek-murshe",
 "format": "bureaucracy",
 "tag": {"he": "בירוקרטיה מפורקת", "en": "Bureaucracy Decoded", "ru": "Бюрократия без страха", "fr": "Bureaucratie décodée"},
 "title": {
  "he": "פותחים עוסק מורשה: שלוש תחנות, ומה באמת לוקח זמן",
  "en": "Registering as a licensed dealer in Israel: three stops, and what actually takes time",
  "ru": "Открываем «осек мурше»: три инстанции — и что действительно занимает время",
  "fr": "S'enregistrer comme indépendant en Israël : trois guichets, et ce qui prend vraiment du temps"
 },
 "body": {
  "he": "הקמת עוסק מורשה עוברת דרך שלוש תחנות: מע\"מ (פתיחת התיק והקצאת מספר העוסק), מס הכנסה (פתיחת תיק וקביעת מקדמות), וביטוח לאומי (סיווג ותשלומים). הרישום עצמו מהיר — מה שלוקח זמן הוא ההחלטות שכדאי לקבל לפניו: עוסק מורשה או פטור, איזה סיווג פעילות, והאם בכלל עדיפה חברה. סדר נכון חוסך תיקונים בדיעבד, ותיעוד מסודר מהיום הראשון חוסך כאב ראש בדוח השנתי הראשון.",
  "en": "Setting up as a licensed dealer (osek murshe) runs through three stops: VAT (opening the file and receiving your dealer number), Income Tax (opening a file and setting advance payments), and National Insurance (classification and contributions). The registration itself is quick — what takes time are the decisions best made beforehand: licensed or exempt dealer, which activity classification, and whether a company is the better fit altogether. The right order saves retroactive corrections, and orderly records from day one save headaches at the first annual report.",
  "ru": "Оформление статуса «осек мурше» проходит через три инстанции: НДС (открытие дела и получение номера), подоходный налог (открытие дела и установление авансов) и Битуах Леуми (классификация и взносы). Сама регистрация быстрая — время занимают решения, которые лучше принять заранее: «мурше» или «патур», какая классификация деятельности, и не выгоднее ли вообще компания. Правильный порядок избавляет от исправлений задним числом, а аккуратный учёт с первого дня — от головной боли при первом годовом отчёте.",
  "fr": "S'enregistrer comme indépendant (osek murshe) passe par trois guichets : la TVA (ouverture du dossier et numéro d'assujetti), l'impôt sur le revenu (dossier et acomptes), et l'assurance nationale (classification et cotisations). L'enregistrement lui-même est rapide — ce qui prend du temps, ce sont les décisions à prendre avant : assujetti ou exonéré, quelle classification d'activité, et si une société ne serait pas préférable. Le bon ordre évite les corrections rétroactives, et une comptabilité ordonnée dès le premier jour épargne bien des maux de tête au premier bilan annuel."
 },
 "gzTag": {"he": "עסקים קטנים", "en": "Small Business", "ru": "Малый бизнес", "fr": "Petites entreprises"},
 "gzTitle": {
  "he": "עוסק מורשה בשלוש תחנות — המדריך המהיר",
  "en": "Licensed dealer in three stops — the quick guide",
  "ru": "«Осек мурше» за три шага — быстрый гид",
  "fr": "Indépendant en trois guichets — le guide rapide"
 }
},
{
 "date": "29.08.2026", "slug": "didyouknow-oral-contract-binding",
 "format": "didyouknow",
 "tag": {"he": "הידעת", "en": "Did You Know", "ru": "А вы знали", "fr": "Le saviez-vous"},
 "title": {
  "he": "הידעת? חוזה בעל־פה מחייב — הבעיה היא להוכיח אותו",
  "en": "Did you know? An oral contract is binding — the problem is proving it",
  "ru": "А вы знали? Устный договор обязывает — проблема в том, как его доказать",
  "fr": "Le saviez-vous ? Un contrat oral engage — le problème est de le prouver"
 },
 "body": {
  "he": "בניגוד לאינטואיציה של רובנו, חוזה נכרת ברוב המקרים גם בעל־פה ואף בהתנהגות — לחיצת יד, אישור בטלפון, תחילת ביצוע. רק סוגי עסקאות מסוימים, ובראשם עסקאות במקרקעין, דורשים מסמך בכתב כתנאי לתוקפם. הבעיה המעשית היא ההוכחה: כשאין כתב, כל צד זוכר גרסה אחרת. ולכן הכלל הפרקטי פשוט — אחרי כל סיכום בעל־פה, מייל קצר: \"כפי שסיכמנו: א', ב', ג'\". שתי דקות שהופכות זיכרון לראיה.",
  "en": "Contrary to most people's intuition, a contract is in most cases formed orally and even by conduct — a handshake, a phone confirmation, starting performance. Only certain transaction types, chiefly real estate, require a written document as a condition of validity. The practical problem is proof: with nothing in writing, each side remembers a different version. Hence the simple rule — after every oral agreement, a short email: \"As agreed: A, B, C.\" Two minutes that turn memory into evidence.",
  "ru": "Вопреки интуиции большинства, договор в большинстве случаев заключается и устно, и даже поведением — рукопожатие, подтверждение по телефону, начало исполнения. Лишь отдельные виды сделок, прежде всего с недвижимостью, требуют письменной формы как условия действительности. Практическая проблема — доказательство: без письма каждая сторона помнит свою версию. Отсюда простое правило: после каждой устной договорённости — короткое письмо: «Как договорились: А, Б, В». Две минуты, превращающие память в доказательство.",
  "fr": "Contrairement à l'intuition commune, un contrat se forme dans la plupart des cas oralement, voire par le comportement — une poignée de main, une confirmation téléphonique, un début d'exécution. Seuls certains types de transactions, l'immobilier en tête, exigent un écrit comme condition de validité. Le problème pratique est la preuve : sans écrit, chacun se souvient d'une version différente. D'où la règle simple — après chaque accord oral, un court courriel : « Comme convenu : A, B, C ». Deux minutes qui transforment un souvenir en preuve."
 },
 "gzTag": {"he": "חוזים", "en": "Contracts", "ru": "Договоры", "fr": "Contrats"},
 "gzTitle": {
  "he": "לחיצת יד היא חוזה — מייל אחד הופך אותה לראיה",
  "en": "A handshake is a contract — one email makes it evidence",
  "ru": "Рукопожатие — это договор; одно письмо делает его доказательством",
  "fr": "Une poignée de main est un contrat — un courriel en fait une preuve"
 }
},
{
 "date": "28.08.2026", "slug": "term-heart-azhara",
 "format": "term",
 "tag": {"he": "מושג במשפט", "en": "Legal Term", "ru": "Юридический термин", "fr": "Terme juridique"},
 "title": {
  "he": "מושג: הערת אזהרה — המנעול הזול ביותר בעסקת נדל\"ן",
  "en": "The term: cautionary note — the cheapest lock in a property deal",
  "ru": "Термин: предупредительная запись — самый дешёвый замок в сделке с недвижимостью",
  "fr": "Le terme : mention d'avertissement — le verrou le moins cher d'une transaction immobilière"
 },
 "body": {
  "he": "הערת אזהרה היא רישום במרשם המקרקעין שמודיע לעולם: על הנכס הזה יש התחייבות. היא אינה מעבירה בעלות — היא חוסמת. מרגע רישומה, עסקה סותרת לא תירשם, וכל מי שבודק את הנסח רואה שהנכס \"תפוס\". בעסקת רכישה היא ההגנה המרכזית של הקונה בתקופה שבין חתימת החוזה לרישום הבעלות: היא מונעת מהמוכר למכור פעמיים או לשעבד את הנכס בינתיים. רישומה מהיר וזול יחסית לערך שהיא מגנה עליו — ולכן מקובל לרשום אותה סמוך ככל האפשר לחתימה.",
  "en": "A cautionary note (he'arat azhara) is an entry in the land registry announcing to the world: this property carries a commitment. It does not transfer ownership — it blocks. Once registered, a conflicting transaction will not be recorded, and anyone checking the extract sees the property is \"taken.\" In a purchase, it is the buyer's main protection between signing and registration of title: it prevents the seller from selling twice or mortgaging the property in the meantime. Registering it is fast and cheap relative to the value it protects — which is why it is standard to register it as close to signing as possible.",
  "ru": "Предупредительная запись («хеарат азхара») — это отметка в земельном реестре, сообщающая миру: на этом объекте лежит обязательство. Она не передаёт собственность — она блокирует. С момента регистрации противоречащая сделка не будет записана, и каждый, кто проверяет выписку, видит, что объект «занят». При покупке это главная защита покупателя между подписанием и регистрацией права: она не даёт продавцу продать дважды или заложить объект. Её регистрация быстра и дёшева по сравнению с ценностью, которую она защищает, — поэтому принято регистрировать её как можно ближе к подписанию.",
  "fr": "La mention d'avertissement (he'arat azhara) est une inscription au registre foncier qui annonce au monde : ce bien porte un engagement. Elle ne transfère pas la propriété — elle bloque. Une fois inscrite, une transaction contraire ne sera pas enregistrée, et quiconque consulte l'extrait voit que le bien est « pris ». Dans un achat, c'est la protection principale de l'acquéreur entre la signature et l'inscription du titre : elle empêche le vendeur de vendre deux fois ou d'hypothéquer le bien entre-temps. Son inscription est rapide et peu coûteuse au regard de la valeur protégée — d'où l'usage de l'inscrire au plus près de la signature."
 },
 "gzTag": {"he": "מקרקעין", "en": "Real Estate", "ru": "Недвижимость", "fr": "Immobilier"},
 "gzTitle": {
  "he": "הערת אזהרה: לא מעבירה בעלות — חוסמת",
  "en": "Cautionary note: doesn't transfer ownership — it blocks",
  "ru": "Предупредительная запись: не передаёт — блокирует",
  "fr": "Mention d'avertissement : ne transfère pas — elle bloque"
 }
},
{
 "date": "27.08.2026", "slug": "qa-cancel-signed-contract",
 "format": "qa",
 "tag": {"he": "שאלות ששואלים", "en": "Questions We Get", "ru": "Вопросы, которые задают", "fr": "Questions fréquentes"},
 "title": {
  "he": "שואלים אותנו: \"חתמתי — אפשר עוד להתחרט?\"",
  "en": "We get asked: \"I've signed — can I still back out?\"",
  "ru": "Нас спрашивают: «Я подписал — можно ещё передумать?»",
  "fr": "On nous demande : « J'ai signé — puis-je encore me rétracter ? »"
 },
 "body": {
  "he": "זו כנראה השאלה הנפוצה ביותר אחרי חתימה נמהרת. נקודת המוצא: חוזה חתום מחייב, ו\"התחרטתי\" אינה עילת ביטול. אבל יש חריגים אמיתיים: הטעיה או הסתרת מידע מהותי, כפייה ועושק, הפרה של הצד השני — ובעסקאות צרכניות מסוימות, כמו רכישה מרחוק או ברוכלות, גם זכות ביטול קצובה שקבועה בדין. ההבדל בין \"אין מה לעשות\" ל\"יש פתח\" טמון בפרטים: מה נאמר לפני החתימה, מה הוסתר, ומה כתוב בסעיפי הביטול של החוזה עצמו. לכן התשובה הכנה היא: תלוי — ושווה בדיקה לפני שמרימים ידיים.",
  "en": "This is probably the most common question after a hasty signature. The starting point: a signed contract binds, and \"I changed my mind\" is not a ground for cancellation. But real exceptions exist: misrepresentation or concealment of material information, duress and exploitation, breach by the other side — and in certain consumer transactions, such as distance or door-to-door sales, a statutory cooling-off right as well. The difference between \"nothing to be done\" and \"there is an opening\" lies in the details: what was said before signing, what was concealed, and what the contract's own cancellation clauses provide. So the honest answer is: it depends — and it is worth checking before giving up.",
  "ru": "Это, пожалуй, самый частый вопрос после поспешной подписи. Исходная точка: подписанный договор обязывает, и «я передумал» — не основание для расторжения. Но есть настоящие исключения: введение в заблуждение или сокрытие существенной информации, принуждение и кабальность, нарушение другой стороной — а в некоторых потребительских сделках, например при дистанционной продаже, ещё и установленное законом право на отказ в определённый срок. Разница между «ничего не поделать» и «есть зацепка» — в деталях: что говорилось до подписания, что скрывалось и что написано в пунктах о расторжении самого договора. Поэтому честный ответ: зависит — и стоит проверить, прежде чем опускать руки.",
  "fr": "C'est probablement la question la plus fréquente après une signature hâtive. Point de départ : un contrat signé engage, et « j'ai changé d'avis » n'est pas un motif d'annulation. Mais de vraies exceptions existent : tromperie ou dissimulation d'une information essentielle, contrainte et abus de faiblesse, manquement de l'autre partie — et dans certaines transactions de consommation, comme la vente à distance, un droit de rétractation légal limité dans le temps. La différence entre « rien à faire » et « il y a une ouverture » tient aux détails : ce qui a été dit avant la signature, ce qui a été caché, et ce que prévoient les clauses d'annulation du contrat lui-même. La réponse honnête est donc : cela dépend — et cela vaut une vérification avant de baisser les bras."
 },
 "gzTag": {"he": "חוזים", "en": "Contracts", "ru": "Договоры", "fr": "Contrats"},
 "gzTitle": {
  "he": "\"התחרטתי\" אינה עילה — אבל יש חריגים אמיתיים",
  "en": "\"I changed my mind\" is no ground — but real exceptions exist",
  "ru": "«Передумал» — не основание, но исключения есть",
  "fr": "« J'ai changé d'avis » n'est pas un motif — mais il y a des exceptions"
 }
},
]

FULL_BODIES = {
"qa-cancel-signed-contract": """<p>השאלה מגיעה כמעט תמיד באותו ניסוח, ותמיד אחרי מעשה: "חתמתי אתמול. אפשר עוד לצאת מזה?"</p>
<h2>נקודת המוצא</h2>
<p>חוזה חתום מחייב. זו כל מהותו — ודאות. "התחרטתי", "לחצו עליי בנימוס", "לא קראתי עד הסוף" — אף אחת מאלה אינה עילת ביטול. מי שחותם מוחזק כמי שקרא והבין, גם אם בפועל דפדף.</p>
<h2>החריגים האמיתיים</h2>
<ul>
<li><strong>הטעיה.</strong> הוצג מצג שווא, או הוסתר מידע מהותי שהיה משנה את ההחלטה. ההסתרה חייבת להיות של עובדה מהותית — לא של פרט שולי.</li>
<li><strong>כפייה ועושק.</strong> חתימה תחת לחץ פסול או ניצול מצוקה, חולשה או חוסר ניסיון בתנאים גרועים במיוחד. רף גבוה — לחץ מסחרי רגיל אינו כפייה.</li>
<li><strong>הפרה של הצד השני.</strong> אם הוא אינו מקיים את חלקו, נפתחות זכויות — לרבות ביטול, בתנאים ובהודעות שהדין קובע.</li>
<li><strong>עסקאות צרכניות מסוימות.</strong> ברכישה מרחוק, ברוכלות ובעסקאות מסוימות נוספות קיימת זכות ביטול קצובה בזמן מכוח דין. היא חלה על צרכנים ובתנאים מוגדרים — לא על כל חוזה.</li>
</ul>
<h2>ומה עושים בפועל</h2>
<p>קודם כל קוראים את סעיפי הביטול של החוזה עצמו — לפעמים הפתח נמצא שם, בדמות תקופת יציאה או תנאי מתלה. אחר כך משחזרים את מה שקדם לחתימה: מה נאמר, מה הובטח, מה הוצג בכתב. ורק אז מחליטים אם יש בסיס לפנייה — רצוי מנוסחת היטב, כי מכתב הביטול הראשון מגדיר את העמדה לכל ההמשך.</p>
<p>השורה התחתונה: רוב החוזים החתומים נשארים חתומים. אבל "רוב" אינו "כל" — ומי שמוותר בלי בדיקה לא יידע לאיזו קבוצה הוא שייך.</p>""",

"term-heart-azhara": """<p>מכל המושגים בעסקת נדל"ן, הערת אזהרה היא אולי בעלת היחס הטוב ביותר בין עלות להגנה — ועדיין רבים חותמים בלי להבין מה היא עושה.</p>
<h2>מה היא</h2>
<p>רישום במרשם המקרקעין שמצהיר: קיימת התחייבות לעשות עסקה בנכס הזה, או להימנע מעסקה בו. היא אינה מעבירה בעלות ואינה יוצרת זכות קניינית מלאה — היא <strong>חוסמת</strong>: עסקה סותרת לא תירשם כל עוד ההערה בתוקף.</p>
<h2>למה היא קריטית לקונה</h2>
<p>בין חתימת חוזה המכר לרישום הבעלות עוברים שבועות ולעיתים חודשים — משכנתא, אישורי מיסים, מסמכים. בתקופה הזו הקונה כבר שילם חלק מהתמורה אך עדיין אינו הבעלים הרשום. הערת האזהרה היא שסוגרת את החלון הזה: היא מונעת מהמוכר למכור שוב, לשעבד או לרשום זכות סותרת, ומזהירה כל צד שלישי שבודק את הנסח.</p>
<h2>שלוש נקודות מעשיות</h2>
<ul>
<li>מקובל לרשום את ההערה סמוך ככל האפשר לחתימה — ולעיתים מתנים את התשלום הראשון ברישומה.</li>
<li>הערה לטובתכם אינה תחליף לבדיקת הערות קיימות לטובת אחרים — נסח מלא לפני חתימה חושף שעבודים, עיקולים והערות קודמות.</li>
<li>גם בעסקאות בתוך המשפחה ובמתנות — הערת אזהרה שומרת על הסדר כשהנסיבות משתנות.</li>
</ul>
<p>מנעול זול, דלת יקרה. זה כל הסיפור.</p>""",

"didyouknow-oral-contract-binding": """<p>אחת ההפתעות הגדולות של לקוחות: הם בטוחים שבלי חתימה אין חוזה. הדין הישראלי חושב אחרת.</p>
<h2>הכלל</h2>
<p>חוזה נכרת בהצעה וקיבול — ואלה יכולים להיעשות בכתב, בעל־פה ואפילו בהתנהגות. ספק ששלח הצעת מחיר, לקוח שאישר בטלפון "סגור, תתחילו" — לרוב נכרת חוזה, על כל המשתמע.</p>
<h2>החריג המרכזי</h2>
<p>סוגי עסקאות מסוימים דורשים כתב כתנאי מהותי, ובראשם התחייבות לעסקה במקרקעין. שם, בלי מסמך — אין עסקה. אבל זה החריג, לא הכלל.</p>
<h2>אז למה כולם חותמים?</h2>
<p>כי הבעיה האמיתית אינה התוקף אלא <strong>ההוכחה</strong>. כשאין כתב, כל צד זוכר גרסה אחרת: על המחיר, על הלוח, על מה שהובטח. חוזה בעל־פה מחייב — אבל את תוכנו קובע בדיעבד מי שהצליח להוכיח.</p>
<h2>ההרגל ששווה זהב</h2>
<p>אחרי כל סיכום בעל־פה — מייל של שלוש שורות: "כפי שסיכמנו בשיחה: היקף X, מחיר Y, מועד Z. אם משהו לא מדויק — תקנו אותי." מי שלא מתקן, אישר. שתי דקות שהופכות זיכרון לראיה, ולא פעם חוסכות את הסכסוך כולו — כי אי־הבנות מתגלות כשהן עוד קטנות.</p>""",

"bureaucracy-opening-osek-murshe": """<p>הרתיעה מפתיחת עוסק גדולה בדרך כלל מהתהליך עצמו. הנה הוא, מפורק לשלוש תחנות.</p>
<h2>תחנה 1: מע"מ</h2>
<p>פתיחת תיק עוסק וקבלת מספר — זה הרישום שהופך אתכם רשמית לעסק. כאן גם נקבעת ההבחנה החשובה: עוסק מורשה (גובה מע"מ, מקזז תשומות, מגיש דוחות תקופתיים) מול עוסק פטור (עד תקרת מחזור שנתית, בלי גביית מע"מ, עם דיווח שנתי מצומצם). הבחירה תלויה בצפי ההכנסות ובזהות הלקוחות — עסקים מעדיפים לעבוד מול מורשה.</p>
<h2>תחנה 2: מס הכנסה</h2>
<p>פתיחת תיק, סיווג הפעילות וקביעת מקדמות — תשלומים תקופתיים על חשבון המס השנתי. מקדמות שנקבעו גבוה מדי אפשר לבקש להקטין; נמוך מדי — צפו להפרש בדוח השנתי.</p>
<h2>תחנה 3: ביטוח לאומי</h2>
<p>סיווג כעצמאי ותשלום דמי ביטוח לפי ההכנסה. שימו לב להגדרות הסף של "עצמאי" לעניין זכויות — הן משפיעות על גמלאות כמו דמי פגיעה ולידה.</p>
<h2>מה באמת לוקח זמן</h2>
<p>לא הטפסים — ההחלטות: מורשה או פטור, איזה סיווג, והאם בכלל חברה עדיפה (אחריות מוגבלת מול עלויות ניהול). ושתי החלטות תפעוליות ששוות לקבל ביום הראשון: חשבון בנק נפרד לעסק, ותיעוד שיטתי של כל הוצאה. הדוח השנתי הראשון יגיד לכם תודה.</p>""",

"fear-demand-letter-first-hour": """<p>המעטפה נפתחת, הכותרת צועקת "התראה בטרם נקיטת הליכים", והדופק עולה. בדיוק לזה המכתב נועד. עכשיו — לנשום, ולקרוא את זה.</p>
<h2>מה המכתב הזה — ומה הוא לא</h2>
<p>מכתב התראה הוא מסמך שכותב עורך דין של הצד השני. הוא אינו פסק דין, אינו עיקול, ואינו קביעה של אף גורם מוסמך. ברוב המקרים הוא פתיחת משא ומתן: הצד השני מציג עמדה, לרוב בגרסה המקסימלית שלה, ומזמין תגובה. חלק ניכר מהמחלוקות נגמר במכתבים — בלי בית משפט.</p>
<h2>השעה הראשונה</h2>
<ul>
<li><strong>לקרוא פעמיים, בשקט.</strong> מה בדיוק נטען, על סמך מה, ומה נדרש.</li>
<li><strong>לאתר את המועד.</strong> "בתוך X ימים" — לרשום ביומן. מועדים הם הדבר הכי חשוב במסמך.</li>
<li><strong>לאסוף הכל.</strong> החוזה, ההתכתבויות, החשבוניות, ההודעות. לא למחוק שום דבר — גם לא מה שנראה רע. מחיקה תמיד נראית גרוע יותר.</li>
<li><strong>לכתוב לעצמכם את הגרסה.</strong> בעודה טרייה: מה קרה, מתי, מי אמר מה.</li>
</ul>
<h2>שלוש טעויות שעולות ביוקר</h2>
<ul>
<li><strong>להתקשר לצד השני בסערת רגשות.</strong> כל מילה עלולה להפוך לראיה — ושיחה כזו אף פעם לא משפרת עמדה.</li>
<li><strong>לענות מיד בכתב.</strong> תגובה נמהרת מקבעת עמדות, מודה בעובדות בלי כוונה, ומוותרת על טענות.</li>
<li><strong>להתעלם.</strong> הטעות היקרה מכולן. שתיקה מתפרשת כחוסר עניין או כהודאה, ומזמינה את הצעד הבא — שכבר יקר בהרבה.</li>
</ul>
<h2>ואז</h2>
<p>תגובה עניינית ושקולה, ברוב המקרים בליווי מקצועי, משנה את התמונה: היא מציגה את הצד שלכם, מתקנת עובדות, ולא פעם פותחת דלת לפתרון. מכתב התראה הוא תחילת שיחה — ומי שנכנס אליה מוכן, מדבר מעמדה אחרת לגמרי.</p>""",

"history-of-the-tabu": """<p>מעטות המילים שכל ישראלי מכיר ואיש כמעט אינו יודע מאיפה הגיעו. "טאבו" היא אחת מהן.</p>
<h2>האימפריה העות'מאנית</h2>
<p>במאה ה-19 ערכה האימפריה רפורמות קרקעות מקיפות, וביקשה לרשום מי מחזיק במה — בעיקר כדי לגבות מס ולגייס לצבא. לשכת הרישום נקראה בטורקית עות'מאנית בשם שממנו נגזר "טאבו", והשם דבק במוסד עד היום, גם כשהאימפריה עצמה נעלמה.</p>
<h2>המנדט הבריטי</h2>
<p>הבריטים ירשו רישום חלקי ולא אחיד, והשיקו את מפעל הסדר הזכויות: מדידה שיטתית, חלוקה לגושים וחלקות, ובירור תביעות בעלות חלקה-חלקה. המבנה הזה — גוש, חלקה, תת-חלקה — הוא שפת הנדל"ן הישראלית עד עצם היום.</p>
<h2>מדינת ישראל</h2>
<p>המדינה המשיכה את ההסדר, עיגנה את המרשם בחקיקה מודרנית, וקבעה עיקרון רב-עוצמה: רישום במרשם המוסדר הוא ראיה חותכת לתוכנו. לימים מוחשב המרשם כולו — ומה שדרש פעם נסיעה ללשכה ותור ארוך, מונפק היום אונליין בתוך דקות.</p>
<h2>למה זה מעניין מישהו שקונה דירה ב-2026</h2>
<p>כי ההיסטוריה הזו מסבירה את ההווה: למה יש נכסים "לא מוסדרים" שדורשים זהירות כפולה, למה חלק מהזכויות רשומות ברשות מקרקעי ישראל או בחברות משכנות ולא בטאבו, ולמה עורך דין מתעקש לראות נסח עדכני לפני כל חתימה. שלוש אימפריות בנו את המסמך הזה — שווה לקרוא אותו לפני שחותמים.</p>"""
}

def main():
    if not os.path.isfile(AJ):
        sys.exit("לא נמצא content/articles.json — להריץ משורש הריפו.")
    arts = json.load(open(AJ, encoding="utf-8"))
    dates = {a.get("date") for a in arts}
    slugs = {a.get("slug") for a in arts}
    added = [a for a in ARTICLES if a["date"] not in dates and a["slug"] not in slugs]
    for a in ARTICLES:
        if a not in added:
            print("דילוג — קיים:", a["date"], a["slug"])
    if not added:
        print("אין מה להוסיף."); return
    merged = added + arts
    merged.sort(key=lambda a: datetime.strptime(a["date"], "%d.%m.%Y"), reverse=True)
    os.makedirs(FULL, exist_ok=True)
    n = 0
    for a in added:
        p = os.path.join(FULL, a["slug"] + ".html")
        if not os.path.exists(p):
            open(p, "w", encoding="utf-8").write(FULL_BODIES[a["slug"]].strip() + "\n")
            n += 1
    json.dump(merged, open(AJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(AJ, "a", encoding="utf-8").write("\n")
    print(f"✓ נוספו {len(added)} כתבות פורמט ({added[-1]['date']} → {added[0]['date']})")
    print(f"✓ {n} עמודים מלאים · סה\"כ בקובץ: {len(merged)}")
    print("\nהבא: node scripts/build-articles.js && node scripts/build-practice.js && git add -A && git commit -m 'format week pilot' && git push")

if __name__ == "__main__":
    main()
