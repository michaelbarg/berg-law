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
const desc = s => { s = String(s); if (s.length <= 155) return s; const cut = s.lastIndexOf(" ", 152); return s.slice(0, cut > 80 ? cut : 152).replace(/[,:;·—-]$/, "") + "…"; };

const tpl = (a, slug, bodyHtml) => `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(a.title.he)} | ברג ושות׳ — משרד עורכי דין</title>
<meta name="description" content="${esc(desc(a.body.he))}">
<link rel="canonical" href="${SITE}/articles/${slug}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="${esc(a.title.he)}">
<meta property="og:description" content="${esc(desc(a.body.he))}">
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
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&family=Inter+Tight:wght@400;500;600&family=Frank+Ruhl+Libre:wght@400;700&family=Heebo:wght@400;600&family=Playfair+Display:wght@400&display=swap" rel="stylesheet">
<style>
:root{--night:#0F1E2E;--night-950:#0A1520;--brass:#C8A45C;--brass-bright:#E3C88F;--brass-deep:#8A6420;
  --oxblood:#59202A;--ivory:#F2EDDF;--ivory-2:#FAF7EC;--ink:#25231C;--sepia:#57503F;
  --parch:#D8CDB2;--mute-d:#A89E88;--line:rgba(37,35,28,.16);--line-strong:rgba(37,35,28,.4);
  --dark:var(--night);--gold:var(--brass);--paper:var(--ivory);--gray:var(--sepia)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter Tight','Heebo','Assistant',sans-serif;background:var(--ivory);color:var(--ink);line-height:1.9;position:relative}
body::before{content:"";position:fixed;top:0;right:0;left:0;height:5px;z-index:10;pointer-events:none;
  background:linear-gradient(to bottom,var(--brass) 0 1px,transparent 1px 4px,var(--brass-deep) 4px 5px)}
header{background:var(--night);padding:20px 24px;border-bottom:1px solid rgba(200,164,92,.25)}
header a{color:var(--ivory);text-decoration:none;font-family:'Lora','Frank Ruhl Libre',serif;font-size:19px;
  display:inline-flex;align-items:center;gap:13px}
header a span{color:var(--brass)}
/* מונוגרמת MB — זהה לדף הבית ולפרופיל גוגל */
.mb{width:40px;height:40px;flex:0 0 40px;display:flex;align-items:center;justify-content:center;
  border:1px solid var(--brass);border-radius:50%;color:var(--brass);direction:ltr;position:relative;
  font-family:'Playfair Display',serif;font-weight:400;font-size:15px;line-height:1}
.mb::after{content:"";position:absolute;inset:2px;border-radius:50%;border:1px solid rgba(200,164,92,.35)}
.mb i{display:block;width:1px;height:10px;background:var(--brass);opacity:.75;margin:0 3px}
main{max-width:740px;margin:0 auto;padding:56px 22px 80px}
.crumb{font-size:13px;color:var(--sepia);margin-bottom:26px;letter-spacing:.02em}
.crumb a{color:var(--sepia);text-decoration:none}
.crumb a:hover{color:var(--brass-deep)}
.meta{display:flex;gap:14px;align-items:baseline;font-size:12.5px;color:var(--sepia);margin-bottom:18px;flex-wrap:wrap;letter-spacing:.06em}
.tag{border:1px solid var(--brass-deep);color:var(--brass-deep);padding:5px 14px;font-size:12px;font-weight:600;letter-spacing:.08em}
h1{font-family:'Lora','Frank Ruhl Libre',serif;font-size:36px;font-weight:500;line-height:1.35;margin-bottom:22px}
.lead{font-family:'Lora','Frank Ruhl Libre',serif;font-size:19px;color:var(--sepia);line-height:1.85;
  border-inline-start:2px solid var(--brass);padding-inline-start:18px;margin-bottom:14px}
.lead-rule{border:none;width:72px;border-top:1px solid var(--brass-deep);position:relative;margin:30px 0 34px}
.lead-rule::after{content:"";position:absolute;top:3px;inset-inline-start:0;width:100%;border-top:1px solid rgba(138,100,32,.45)}
article h2{font-family:'Lora','Frank Ruhl Libre',serif;font-size:23px;font-weight:600;margin:36px 0 14px}
article p{margin-bottom:17px}
article ul{margin:0 0 20px 0;padding-inline-start:24px}
article li{margin-bottom:10px}
article a{color:var(--brass-deep)}
.cta{background:var(--ivory-2);border:1px solid var(--line-strong);padding:26px 28px;margin-top:44px;position:relative}
.cta::before{content:"";position:absolute;inset:5px;border:1px solid var(--line);pointer-events:none}
.cta a{color:var(--oxblood);font-weight:600;text-decoration:none;border-bottom:1px solid var(--brass);position:relative}
.disc{font-size:12.5px;color:var(--sepia);margin-top:30px;border-top:1px solid var(--line);padding-top:18px}
footer{background:var(--night-950);color:var(--mute-d);padding:30px 24px;font-size:13px;text-align:center;border-top:1px solid rgba(200,164,92,.3)}
footer a{color:var(--brass);text-decoration:none}
footer a:hover{color:var(--brass-bright)}
</style>
</head>
<body>
<header><a href="/"><span class="mb">M<i></i>B</span><span style="color:#F2EDDF">ברג ושות׳ <span>· משרד עורכי דין</span></span></a></header>
<main>
<div class="crumb"><a href="/">דף הבית</a> › <a href="/#articles">עדכונים משפטיים</a> › ${esc(a.tag.he)}</div>
<div class="meta"><span class="tag">${esc(a.tag.he)}</span><span>${esc(a.date)}</span><span>עו״ד מייקל ברג</span></div>
<h1>${esc(a.title.he)}</h1>
<p class="lead">${esc(a.body.he)}</p>
<hr class="lead-rule">
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
