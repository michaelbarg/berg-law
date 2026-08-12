#!/usr/bin/env node
/* בונה עמוד HTML אינדקסבילי לכל מאמר שיש לו טקסט מלא, ומייצר sitemap.xml.
   מאמרים עם תאריך עתידי לא נכנסים — כדי לא לחשוף את התור לגוגל מוקדם מדי. */
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, "..");
const SITE = "https://berg-law.co.il";

/* תאריך -> slug. מאמר בלי slug או בלי קובץ טקסט מלא ב-content/full מדולג. */
const SLUGS = {
  "06.08.2026": "personal-guarantee-shareholders",
  "07.08.2026": "tabu-extract-before-signing",
  "09.08.2026": "whatsapp-agreement-binding-contract"
};

const articles = JSON.parse(fs.readFileSync(path.join(ROOT, "content/articles.json"), "utf8"));
const today = new Date(); today.setHours(23, 59, 59, 999);
const parse = d => { const p = d.split("."); return new Date(p[2], p[1] - 1, p[0]); };
const iso = d => { const p = d.split("."); return p[2] + "-" + p[1] + "-" + p[0]; };
const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

const tpl = (a, slug, bodyHtml) => `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(a.title.he)} | ברג ושות׳ — משרד עורכי דין</title>
<meta name="description" content="${esc(a.body.he.slice(0, 155))}">
<link rel="canonical" href="${SITE}/articles/${slug}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="${esc(a.title.he)}">
<meta property="og:description" content="${esc(a.body.he.slice(0, 155))}">
<meta property="og:url" content="${SITE}/articles/${slug}.html">
<meta property="og:image" content="${SITE}/og.jpg">
<meta property="og:locale" content="he_IL">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article",
"headline":${JSON.stringify(a.title.he)},
"description":${JSON.stringify(a.body.he)},
"datePublished":"${iso(a.date)}","dateModified":"${iso(a.date)}",
"inLanguage":"he-IL","articleSection":${JSON.stringify(a.tag.he)},
"author":{"@type":"Person","name":"מייקל ברג","jobTitle":"עורך דין"},
"publisher":{"@type":"LegalService","name":"ברג ושות׳ — משרד עורכי דין","url":"${SITE}"},
"mainEntityOfPage":{"@type":"WebPage","@id":"${SITE}/articles/${slug}.html"}}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{"@type":"ListItem","position":1,"name":"ברג ושות׳","item":"${SITE}/"},
{"@type":"ListItem","position":2,"name":"עדכונים משפטיים","item":"${SITE}/#articles"},
{"@type":"ListItem","position":3,"name":${JSON.stringify(a.title.he)}}]}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@400;700;900&family=Assistant:wght@300;400;600;700&family=Playfair+Display:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--dark:#0E141E;--gold:#C6A75E;--paper:#F7F6F2;--ink:#171C24;--gray:#646B76;--line:#E6E4DD}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Assistant',sans-serif;background:var(--paper);color:var(--ink);line-height:1.85}
header{background:var(--dark);padding:18px 24px}
header a{color:#fff;text-decoration:none;font-family:'Frank Ruhl Libre',serif;font-size:19px;
  display:inline-flex;align-items:center;gap:12px}
header a span{color:var(--gold)}
/* מונוגרמת MB — זהה לדף הבית ולפרופיל גוגל */
.mb{width:38px;height:38px;flex:0 0 38px;display:flex;align-items:center;justify-content:center;
  border:1px solid var(--gold);border-radius:50%;color:var(--gold);direction:ltr;
  font-family:'Playfair Display',serif;font-weight:400;font-size:15px;line-height:1}
.mb i{display:block;width:1px;height:10px;background:var(--gold);opacity:.75;margin:0 3px}
main{max-width:760px;margin:0 auto;padding:44px 22px 70px}
.crumb{font-size:13.5px;color:var(--gray);margin-bottom:18px}
.crumb a{color:var(--gray)}
.meta{display:flex;gap:12px;align-items:center;font-size:13px;color:var(--gray);margin-bottom:14px}
.tag{background:var(--dark);color:var(--gold);padding:4px 12px;font-size:12.5px;font-weight:700}
h1{font-family:'Frank Ruhl Libre',serif;font-size:34px;line-height:1.3;margin-bottom:18px}
.lead{font-size:18.5px;color:#333;border-inline-start:3px solid var(--gold);padding-inline-start:16px;margin-bottom:30px}
article h2{font-family:'Frank Ruhl Libre',serif;font-size:23px;margin:32px 0 12px}
article p{margin-bottom:16px}
article ul{margin:0 0 18px 0;padding-inline-start:22px}
article li{margin-bottom:9px}
.cta{background:#fff;border:1px solid var(--line);border-top:3px solid var(--gold);padding:22px;margin-top:38px}
.cta a{color:var(--dark);font-weight:700}
.disc{font-size:13px;color:var(--gray);margin-top:26px;border-top:1px solid var(--line);padding-top:16px}
footer{background:var(--dark);color:#9AA1AC;padding:26px 24px;font-size:13.5px;text-align:center}
footer a{color:var(--gold)}
</style>
</head>
<body>
<header><a href="/"><span class="mb">M<i></i>B</span><span style="color:#fff">ברג ושות׳ <span>· משרד עורכי דין</span></span></a></header>
<main>
<div class="crumb"><a href="/">דף הבית</a> › <a href="/#articles">עדכונים משפטיים</a> › ${esc(a.tag.he)}</div>
<div class="meta"><span class="tag">${esc(a.tag.he)}</span><span>${esc(a.date)}</span><span>עו״ד מייקל ברג</span></div>
<h1>${esc(a.title.he)}</h1>
<p class="lead">${esc(a.body.he)}</p>
<article>
${bodyHtml}
</article>
<div class="cta">שאלה על המקרה הספציפי שלכם? אפשר לכתוב ב<a href="https://wa.me/972546665615">וואטסאפ</a> או דרך <a href="/#contact">טופס יצירת הקשר</a>. מענה מהיר — בעברית, אנגלית, רוסית וצרפתית.</div>
<p class="disc">האמור לעיל הוא מידע כללי ואינו מהווה ייעוץ משפטי או תחליף לו. כל מקרה נבחן לגופו.</p>
</main>
<footer>© ברג ושות׳ — משרד עורכי דין · <a href="/">berg-law.co.il</a> · <a href="/legal.html">תנאי שימוש ופרטיות</a></footer>
</body>
</html>
`;

fs.mkdirSync(path.join(ROOT, "articles"), { recursive: true });
const urls = [
  { loc: SITE + "/", pri: "1.0", freq: "daily" },
  { loc: SITE + "/legal.html", pri: "0.3", freq: "yearly" }
];
let built = 0; const skipped = [];
for (const a of articles) {
  const slug = a.slug || SLUGS[a.date];
  if (!slug) { skipped.push(a.date + " (אין slug)"); continue; }
  if (parse(a.date) > today) { skipped.push(a.date + " (עתידי)"); continue; }
  const src = path.join(ROOT, "content/full", slug + ".html");
  if (!fs.existsSync(src)) { skipped.push(a.date + " (אין טקסט מלא)"); continue; }
  const bodyHtml = fs.readFileSync(src, "utf8").trim();
  fs.writeFileSync(path.join(ROOT, "articles", slug + ".html"), tpl(a, slug, bodyHtml));
  urls.push({ loc: SITE + "/articles/" + slug + ".html", pri: "0.8", freq: "monthly", mod: iso(a.date) });
  built++;
}
const body = urls.map(u =>
  "  <url><loc>" + u.loc + "</loc>" + (u.mod ? "<lastmod>" + u.mod + "</lastmod>" : "") +
  "<changefreq>" + u.freq + "</changefreq><priority>" + u.pri + "</priority></url>").join("\n");
fs.writeFileSync(path.join(ROOT, "sitemap.xml"),
  '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n");
console.log("BUILT pages:", built);
console.log("SITEMAP urls:", urls.length);
if (skipped.length) console.log("skipped:", skipped.join(", "));
