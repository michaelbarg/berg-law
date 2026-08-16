#!/usr/bin/env node
/* בונה: (1) עמוד HTML אינדקסבילי לכל מאמר, (2) ארכיון /articles/ עם חיפוש וסינון, (3) sitemap.xml.
   מאמר עם תאריך עתידי לא נכנס — כדי לא לחשוף את התור לגוגל מוקדם מדי. */
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, "..");
const SITE = "https://berg-law.co.il";

const articles = JSON.parse(fs.readFileSync(path.join(ROOT, "content/articles.json"), "utf8"));
const today = new Date(); today.setHours(23, 59, 59, 999);
const parse = d => { const p = d.split("."); return new Date(p[2], p[1] - 1, p[0]); };
const iso = d => { const p = d.split("."); return p[2] + "-" + p[1] + "-" + p[0]; };
const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const desc = s => { s = String(s); if (s.length <= 155) return s; const cut = s.lastIndexOf(" ", 152); return s.slice(0, cut > 80 ? cut : 152).replace(/[,:;·—-]$/, "") + "…"; };

/* ---------- shared design tokens: Silver Salon ---------- */
const TOKENS = `--graphite:#0F2A21;--graphite-950:#081512;--graphite-800:#1C4737;
  --pearl:#F5F2EA;--pearl-2:#FCFAF4;--ink:#1B211E;--slate:#525A56;
  --silver:#CDD4CE;--silver-bright:#EDF1EC;--silver-deep:#5B6863;
  --verde:#20604A;--verde-bright:#88CDA9;--blush:#EDBFB8;--blush-deep:#8C4A4E;
  --mist:#D9E1DB;--mute-d:#ABB8B0;--line:rgba(27,33,30,.15);--line-strong:rgba(27,33,30,.38);
  --display:'Frank Ruhl Libre',Georgia,serif;--sans:'Assistant','Segoe UI',system-ui,sans-serif;
  --mark:'Cormorant Garamond',Georgia,serif`;

const FONTS = `<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@300..700&family=Assistant:wght@200..700&family=Cormorant+Garamond:wght@300;400&display=swap" rel="stylesheet">`;

const FAVICON = `<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,` +
  Buffer.from('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">' +
    '<circle cx="32" cy="32" r="32" fill="#0F2A21"/>' +
    '<circle cx="32" cy="32" r="29" fill="none" stroke="#CDD4CE" stroke-width="1.5"/>' +
    '<circle cx="32" cy="32" r="26.2" fill="none" stroke="#CDD4CE" stroke-width="0.7" opacity="0.4"/>' +
    '<g fill="#EDF1EC" font-family="Georgia,Times New Roman,serif" font-size="26" text-anchor="middle">' +
    '<text x="21" y="41">M</text><text x="44" y="41">B</text></g>' +
    '<rect x="31.6" y="24" width="1" height="16" fill="#CDD4CE" opacity="0.85"/></svg>').toString("base64") + `">`;

const BASE_CSS = `
:root{${TOKENS}}
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;scroll-behavior:smooth}
html,body{font-synthesis-weight:none}
body{font-family:var(--sans);background:var(--pearl);color:var(--ink);line-height:1.85;font-size:17px;position:relative}
/* פס הביטנה: כסף · ורדיגריס · ורד עתיק */
body::before{content:"";position:fixed;top:0;right:0;left:0;height:6px;z-index:20;pointer-events:none;
  background:linear-gradient(to bottom,#CDD4CE 0 1px,transparent 1px 3px,#88CDA9 3px 4px,transparent 4px 5px,#EDBFB8 5px 6px)}
::selection{background:var(--verde);color:var(--pearl-2)}
a{color:inherit}
h1,h2,h3,h4{font-family:var(--display);font-weight:500;letter-spacing:0;text-wrap:balance}
p{text-wrap:pretty}
.stamp,time,.date{font-variant-numeric:lining-nums tabular-nums}
:focus-visible{outline:2px solid var(--verde-bright);outline-offset:3px}
header.site{background:var(--graphite);padding:18px 24px;border-bottom:1px solid rgba(205,212,206,.22);
  display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap}
header.site .brand{color:var(--pearl);text-decoration:none;font-family:var(--display);font-size:19px;
  display:inline-flex;align-items:center;gap:13px}
header.site .brand em{color:var(--silver);font-style:normal;font-size:15px}
header.site nav{display:flex;gap:22px;font-size:14px}
header.site nav a{color:var(--mist);text-decoration:none;transition:color .25s}
header.site nav a:hover{color:var(--silver-bright)}
.mb{width:42px;height:42px;flex:0 0 42px;display:flex;align-items:center;justify-content:center;
  border:1px solid var(--silver);border-radius:50%;color:var(--silver);direction:ltr;position:relative;
  font-family:var(--mark);font-weight:400;font-size:17px;line-height:1}
.mb::after{content:"";position:absolute;inset:2px;border-radius:50%;border:1px solid rgba(205,212,206,.35)}
.mb i{display:block;width:1px;height:11px;background:var(--silver);opacity:.8;margin:0 3px}
.crumb{font-size:13px;color:var(--slate);margin-bottom:26px}
.crumb a{color:var(--slate);text-decoration:none}
.crumb a:hover{color:var(--blush-deep)}
.chip{border:1px solid var(--silver-deep);color:var(--silver-deep);padding:5px 14px;font-size:12.5px;font-weight:600}
footer.site{background:var(--graphite-950);color:var(--mute-d);padding:34px 24px;font-size:13.5px;
  text-align:center;border-top:1px solid rgba(205,212,206,.28)}
footer.site a{color:var(--silver);text-decoration:none}
footer.site a:hover{color:var(--silver-bright)}
footer.site .soc{display:flex;justify-content:center;gap:16px;margin:0 0 16px}
footer.site .soc a{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;
  border:1px solid rgba(205,212,206,.34);border-radius:50%;color:var(--silver);transition:.25s}
footer.site .soc a:hover{color:var(--graphite-950);background:var(--silver-bright);border-color:var(--silver-bright)}
footer.site .soc svg{width:17px;height:17px}
@media(max-width:640px){header.site nav{gap:16px;font-size:13px}}
`;

const HEADER = `<header class="site">
<a class="brand" href="/"><span class="mb">M<i></i>B</span><span>ברג ושות׳ <em>· משרד עורכי דין</em></span></a>
<nav><a href="/articles/">כל הכתבות</a><a href="/#services">תחומי עיסוק</a><a href="/#contact">יצירת קשר</a></nav>
</header>`;

const FOOTER = `<footer class="site"><div class="soc"><a href="https://www.instagram.com/berg_law.co.il/" target="_blank" rel="noopener" aria-label="Instagram" title="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg></a><a href="https://www.linkedin.com/in/michael-barg-passparto/" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-.95 1.83-1.95 3.77-1.95 4.03 0 4.78 2.55 4.78 5.87V21h-4v-5.5c0-1.31-.02-3-1.9-3-1.9 0-2.2 1.43-2.2 2.9V21H9z"/></svg></a><a href="https://g.page/r/CY5RIVB2bPH9EBM" target="_blank" rel="noopener" aria-label="Google" title="Google Business Profile"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21s-6.5-5.6-6.5-10.1A6.5 6.5 0 0 1 12 4.4a6.5 6.5 0 0 1 6.5 6.5C18.5 15.4 12 21 12 21z"/><circle cx="12" cy="10.7" r="2.4"/></svg></a></div>© ברג ושות׳ — משרד עורכי דין · <a href="/">berg-law.co.il</a> · <a href="/articles/">ארכיון הכתבות</a> · <a href="/legal.html">תנאי שימוש ופרטיות</a></footer>`;

/* ---------- single article page ---------- */
const tpl = (a, slug, bodyHtml, prev, next, related, future) => `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(a.title.he)} | ברג ושות׳ — משרד עורכי דין</title>
<meta name="description" content="${esc(desc(a.body.he))}">
<meta name="theme-color" content="#0F2A21">
<link rel="canonical" href="${SITE}/articles/${slug}.html">
${future ? '<meta name="robots" content="noindex,follow">\n' : ""}${FAVICON}
<meta property="og:type" content="article">
<meta property="og:title" content="${esc(a.title.he)}">
<meta property="og:description" content="${esc(desc(a.body.he))}">
<meta property="og:url" content="${SITE}/articles/${slug}.html">
<meta property="og:image" content="${SITE}/og.jpg">
<meta property="og:locale" content="he_IL">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article",
"headline":${JSON.stringify(a.title.he)},
"description":${JSON.stringify(a.body.he)},
"datePublished":"${iso(a.date)}","dateModified":"${iso(a.date)}",
"inLanguage":"he-IL","articleSection":${JSON.stringify(a.tag.he)},
"image":"${SITE}/og.jpg",
"author":{"@type":"Person","name":"מייקל ברג","jobTitle":"עורך דין","url":"${SITE}/#about"},
"publisher":{"@type":"LegalService","name":"ברג ושות׳ — משרד עורכי דין","url":"${SITE}"},
"isPartOf":{"@type":"Blog","name":"עדכונים משפטיים","@id":"${SITE}/articles/"},
"mainEntityOfPage":{"@type":"WebPage","@id":"${SITE}/articles/${slug}.html"}}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{"@type":"ListItem","position":1,"name":"ברג ושות׳","item":"${SITE}/"},
{"@type":"ListItem","position":2,"name":"עדכונים משפטיים","item":"${SITE}/articles/"},
{"@type":"ListItem","position":3,"name":${JSON.stringify(a.title.he)}}]}
</script>
${FONTS}
<style>${BASE_CSS}
main{max-width:730px;margin:0 auto;padding:54px 22px 24px}
.meta{display:flex;gap:14px;align-items:baseline;font-size:13px;color:var(--slate);margin-bottom:18px;flex-wrap:wrap}
h1{font-size:clamp(28px,4.2vw,39px);line-height:1.36;margin-bottom:22px}
.lead{font-family:var(--display);font-size:19.5px;color:var(--slate);line-height:1.8;
  border-inline-start:2px solid var(--blush-deep);padding-inline-start:19px;margin-bottom:8px}
.lead-rule{border:none;width:74px;border-top:1px solid var(--silver-deep);position:relative;margin:30px 0 34px}
.lead-rule::after{content:"";position:absolute;top:3px;inset-inline-start:0;width:100%;border-top:1px solid rgba(140,74,78,.45)}
article h2{font-size:23px;font-weight:600;margin:38px 0 14px;color:var(--verde)}
article p{margin-bottom:17px}
article ul{margin:0 0 20px;padding-inline-start:22px}
article li{margin-bottom:11px}
article li::marker{color:var(--blush-deep)}
article b{font-weight:600;color:var(--ink)}
.cta{background:var(--pearl-2);border:1px solid var(--line-strong);padding:26px 28px;margin-top:46px;position:relative}
.cta::before{content:"";position:absolute;inset:5px;border:1px solid var(--line);pointer-events:none}
.cta a{color:var(--verde);font-weight:600;text-decoration:none;border-bottom:1px solid var(--blush-deep)}
.disc{font-size:12.5px;color:var(--slate);margin-top:28px;border-top:1px solid var(--line);padding-top:18px}
.pager{display:grid;grid-template-columns:1fr 1fr;gap:0;margin-top:46px;border-top:1px solid var(--line-strong)}
.pager a{padding:24px 22px;text-decoration:none;display:block;transition:background .3s}
.pager a:hover{background:var(--pearl-2)}
.pager a+a{border-inline-start:1px solid var(--line)}
.pager span{display:block;font-size:11.5px;letter-spacing:.06em;color:var(--blush-deep);font-weight:600;margin-bottom:8px}
.pager b{font-family:var(--display);font-size:16.5px;font-weight:500;line-height:1.5;color:var(--ink)}
.pager .nx{text-align:start}
.rel{margin-top:52px;border-top:1px solid var(--line-strong);padding-top:30px}
.rel h2{font-size:17px;letter-spacing:.04em;color:var(--slate);margin-bottom:20px;font-family:var(--sans);font-weight:600}
.rel ul{list-style:none;padding:0}
.rel li{border-bottom:1px solid var(--line);padding:14px 0}
.rel li:last-child{border-bottom:none}
.rel a{text-decoration:none;display:flex;gap:14px;align-items:baseline;flex-wrap:wrap}
.rel .d{font-size:12.5px;color:var(--slate);font-variant-numeric:tabular-nums;flex:0 0 auto}
.rel .t{font-family:var(--display);font-size:16.5px;line-height:1.5;transition:color .25s}
.rel a:hover .t{color:var(--blush-deep)}
.allbtn{display:inline-block;margin-top:30px;border:1px solid var(--silver-deep);color:var(--silver-deep);
  padding:13px 26px;text-decoration:none;font-weight:600;font-size:14px;transition:all .3s}
.allbtn:hover{background:var(--graphite);border-color:var(--graphite);color:var(--silver-bright)}
@media(max-width:620px){.pager{grid-template-columns:1fr}.pager a+a{border-inline-start:none;border-top:1px solid var(--line)}}
</style>
</head>
<body>
${HEADER}
<main>
<div class="crumb"><a href="/">דף הבית</a> › <a href="/articles/">עדכונים משפטיים</a> › ${esc(a.tag.he)}</div>
<div class="meta"><span class="chip">${esc(a.tag.he)}</span><span>${esc(a.date)}</span><span>עו״ד מייקל ברג</span></div>
<h1>${esc(a.title.he)}</h1>
<p class="lead">${esc(a.body.he)}</p>
<hr class="lead-rule">
<article>
${bodyHtml}
</article>
<div class="cta">שאלה על המקרה הספציפי שלכם? אפשר לכתוב ב<a href="https://wa.me/972546665615">וואטסאפ</a> או דרך <a href="/#contact">טופס יצירת הקשר</a>. מענה מהיר — בעברית, אנגלית, רוסית וצרפתית.</div>
<nav class="pager">${
  next ? `<a class="nx" href="/articles/${next.slug}.html"><span>הכתבה הבאה →</span><b>${esc(next.title.he)}</b></a>` : ""
}${
  prev ? `<a href="/articles/${prev.slug}.html"><span>← הכתבה הקודמת</span><b>${esc(prev.title.he)}</b></a>` : ""
}</nav>
${related.length ? `<section class="rel"><h2>עוד בנושא ${esc(a.tag.he)}</h2><ul>${
  related.map(r => `<li><a href="/articles/${r.slug}.html"><span class="d">${esc(r.date)}</span><span class="t">${esc(r.title.he)}</span></a></li>`).join("")
}</ul><a class="allbtn" href="/articles/">לארכיון כל הכתבות</a></section>` : `<a class="allbtn" href="/articles/">לארכיון כל הכתבות</a>`}
<p class="disc">האמור לעיל הוא מידע כללי ואינו מהווה ייעוץ משפטי או תחליף לו. כל מקרה נבחן לגופו.</p>
</main>
${FOOTER}
</body>
</html>
`;

/* ---------- blog index: /articles/index.html ---------- */
const indexTpl = (list) => {
  const tags = [...new Set(list.map(a => a.tag.he))];
  return `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>עדכונים משפטיים — כל הכתבות | ברג ושות׳ משרד עורכי דין</title>
<meta name="description" content="ארכיון העדכונים המשפטיים של משרד ברג ושות׳: פסיקה, חקיקה ותקנות בשפה פשוטה, עם השורה התחתונה לעסק. חיפוש וסינון לפי תחום.">
<meta name="theme-color" content="#0F2A21">
<link rel="canonical" href="${SITE}/articles/">
${FAVICON}
<meta property="og:type" content="website">
<meta property="og:title" content="עדכונים משפטיים — ארכיון הכתבות | ברג ושות׳">
<meta property="og:description" content="פסיקה, חקיקה ותקנות בשפה פשוטה, עם השורה התחתונה לעסק שלך.">
<meta property="og:url" content="${SITE}/articles/">
<meta property="og:image" content="${SITE}/og.jpg">
<meta property="og:locale" content="he_IL">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Blog","@id":"${SITE}/articles/",
"name":"עדכונים משפטיים — ברג ושות׳","inLanguage":"he-IL","url":"${SITE}/articles/",
"description":"פסיקה, חקיקה ותקנות בשפה פשוטה, עם השורה התחתונה לעסק.",
"publisher":{"@type":"LegalService","name":"ברג ושות׳ — משרד עורכי דין","url":"${SITE}"},
"blogPost":[${list.map(a => `{"@type":"BlogPosting","headline":${JSON.stringify(a.title.he)},"url":"${SITE}/articles/${a.slug}.html","datePublished":"${iso(a.date)}","articleSection":${JSON.stringify(a.tag.he)},"author":{"@type":"Person","name":"מייקל ברג"}}`).join(",")}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{"@type":"ListItem","position":1,"name":"ברג ושות׳","item":"${SITE}/"},
{"@type":"ListItem","position":2,"name":"עדכונים משפטיים","item":"${SITE}/articles/"}]}
</script>
${FONTS}
<style>${BASE_CSS}
main{max-width:920px;margin:0 auto;padding:56px 22px 30px}
.head h1{font-size:clamp(30px,4.4vw,44px);line-height:1.3;margin-bottom:16px}
.head p{color:var(--slate);font-size:17.5px;font-weight:300;max-width:44em}
.rule{border:none;width:76px;border-top:1px solid var(--silver-deep);position:relative;margin:26px 0 34px}
.rule::after{content:"";position:absolute;top:3px;inset-inline-start:0;width:100%;border-top:1px solid rgba(140,74,78,.45)}
.tools{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:22px}
.searchbox{flex:1 1 280px;position:relative;display:flex;align-items:center}
.searchbox svg{position:absolute;inset-inline-start:14px;width:17px;height:17px;color:var(--slate);pointer-events:none}
.searchbox input{width:100%;font-family:var(--sans);font-size:16px;color:var(--ink);background:var(--pearl-2);
  border:1px solid var(--line-strong);padding:14px 44px;transition:border-color .25s}
.searchbox input:focus{outline:none;border-color:var(--verde)}
.searchbox input::placeholder{color:var(--slate);opacity:.75}
.chips{display:flex;gap:8px;flex-wrap:wrap}
.chips button{font-family:var(--sans);font-size:13.5px;font-weight:600;cursor:pointer;padding:9px 16px;
  background:transparent;border:1px solid var(--line-strong);color:var(--slate);transition:all .25s}
.chips button:hover{border-color:var(--verde);color:var(--verde)}
.chips button.on{background:var(--verde);border-color:var(--verde);color:var(--pearl-2)}
.count{font-size:13px;color:var(--slate);margin-bottom:6px}
.list{list-style:none;border-top:2px solid var(--ink);position:relative;padding:0}
.list::before{content:"";position:absolute;top:3px;right:0;left:0;border-top:1px solid var(--line-strong)}
.list li{border-bottom:1px solid var(--line)}
.list a{display:grid;grid-template-columns:130px 1fr;gap:26px;padding:26px 6px;text-decoration:none;
  transition:background .3s;align-items:start}
.list a:hover{background:var(--pearl-2)}
.list .side{font-size:12.5px;color:var(--slate);line-height:1.9}
.list .side .t{display:block;color:var(--silver-deep);font-weight:600;margin-top:2px}
.list h2{font-size:21px;line-height:1.5;font-weight:600;margin-bottom:9px;transition:color .25s}
.list a:hover h2{color:var(--blush-deep)}
.list p{font-size:15px;color:var(--slate);font-weight:300;line-height:1.8;margin:0}
.list .more{display:inline-block;margin-top:12px;font-size:13.5px;font-weight:600;color:var(--verde)}
.empty{padding:52px 6px;color:var(--slate);text-align:center;display:none}
.backhome{display:inline-block;margin-top:34px;border:1px solid var(--silver-deep);color:var(--silver-deep);
  padding:13px 26px;text-decoration:none;font-weight:600;font-size:14px;transition:all .3s}
.backhome:hover{background:var(--graphite);border-color:var(--graphite);color:var(--silver-bright)}
mark{background:rgba(237,191,184,.4);color:inherit;padding:0 2px}
@media(max-width:660px){.list a{grid-template-columns:1fr;gap:9px}.list .side{display:flex;gap:12px}.list .side .t{margin:0}}
</style>
</head>
<body>
${HEADER}
<main>
<div class="head">
  <div class="crumb"><a href="/">דף הבית</a> › עדכונים משפטיים</div>
  <h1>עדכונים משפטיים</h1>
  <p>פסיקה, חקיקה ותקנות — מוסברים בשפה פשוטה, עם השורה התחתונה לעסק שלך. כתבה חדשה מתפרסמת מדי יום.</p>
  <hr class="rule">
</div>
<div class="tools">
  <label class="searchbox">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.6-3.6"/></svg>
    <input id="q" type="search" placeholder="חיפוש בכל הכתבות — נושא, חוק, מילה" aria-label="חיפוש בכתבות" autocomplete="off">
  </label>
</div>
<div class="chips" id="chips">
  <button class="on" data-tag="">הכול</button>
  ${tags.map(t => `<button data-tag="${esc(t)}">${esc(t)}</button>`).join("")}
</div>
<p class="count" id="count">${list.length} כתבות</p>
<ul class="list" id="list">
${list.map(a => `  <li data-tag="${esc(a.tag.he)}" data-s="${esc((a.title.he + " " + a.body.he + " " + a.tag.he).toLowerCase())}">
    <a href="/articles/${a.slug}.html">
      <span class="side">${esc(a.date)}<span class="t">${esc(a.tag.he)}</span></span>
      <span><h2>${esc(a.title.he)}</h2><p>${esc(a.body.he)}</p><span class="more">לקריאת הכתבה ←</span></span>
    </a>
  </li>`).join("\n")}
</ul>
<p class="empty" id="empty">לא נמצאה כתבה שמתאימה לחיפוש. אפשר לנסות מילה אחרת, או <a href="/#contact" style="color:var(--verde);font-weight:600">לשאול אותנו ישירות</a>.</p>
<a class="backhome" href="/">חזרה לדף הבית</a>
</main>
${FOOTER}
<script>
(function(){
  var q=document.getElementById("q"),list=document.getElementById("list"),
      items=[].slice.call(list.children),count=document.getElementById("count"),
      empty=document.getElementById("empty"),tag="";
  function norm(s){return (s||"").toLowerCase().replace(/[\u0591-\u05C7]/g,"").replace(/["'׳״’“”]/g,"").replace(/\s+/g," ").trim();}
  /* גיזום קל לעברית — "חוזה" מוצא גם "חוזים" */
  function stems(w){var v=[w];if(w.length>=5)v.push(w.slice(0,-2));if(w.length>=4)v.push(w.slice(0,-1));return v;}
  function run(){
    var t=norm(q.value),n=0;
    items.forEach(function(li){
      var okTag=!tag||li.dataset.tag===tag;
      var hay=norm(li.dataset.s);
      var okTxt=!t||t.split(" ").every(function(w){return stems(w).some(function(v){return hay.indexOf(v)>-1;});});
      var show=okTag&&okTxt; li.style.display=show?"":"none"; if(show)n++;
    });
    count.textContent=n+(n===1?" כתבה":" כתבות");
    empty.style.display=n?"none":"block";
  }
  q.addEventListener("input",run);
  document.getElementById("chips").addEventListener("click",function(e){
    var b=e.target.closest("button"); if(!b)return;
    tag=b.dataset.tag;
    [].forEach.call(this.children,function(x){x.classList.toggle("on",x===b);});
    run();
  });
  var pre=new URLSearchParams(location.search).get("q");
  if(pre){q.value=pre;run();}
})();
</script>
</body>
</html>
`;
};

/* ---------- build ---------- */
fs.mkdirSync(path.join(ROOT, "articles"), { recursive: true });
/* כל מאמר שיש לו טקסט מלא מקבל עמוד — גם עתידי. אחרת, ביום שהכרטיס מופיע בדף הבית
   הקישור מוביל ל-404 עד שמישהו יריץ build. מאמר עתידי מסומן noindex ואינו בסייטמאפ
   ואינו בארכיון, כך שגוגל לא רואה אותו לפני הזמן. */
const renderable = articles
  .filter(a => a.slug && fs.existsSync(path.join(ROOT, "content/full", a.slug + ".html")))
  .sort((x, y) => parse(y.date) - parse(x.date));   // newest first
const published = renderable.filter(a => parse(a.date) <= today);
const queued = renderable.filter(a => parse(a.date) > today);

const skipped = articles.filter(a => !renderable.includes(a))
  .map(a => a.date + (!a.slug ? " (אין slug)" : " (אין טקסט מלא)"));

renderable.forEach(a => {
  const future = parse(a.date) > today;
  const pool = future ? renderable : published;
  const i = pool.indexOf(a);
  const next = pool[i - 1] || null;   // newer
  const prev = pool[i + 1] || null;   // older
  const related = published.filter(r => r.tag.he === a.tag.he && r.slug !== a.slug).slice(0, 3);
  const bodyHtml = fs.readFileSync(path.join(ROOT, "content/full", a.slug + ".html"), "utf8").trim();
  fs.writeFileSync(path.join(ROOT, "articles", a.slug + ".html"), tpl(a, a.slug, bodyHtml, prev, next, related, future));
});
fs.writeFileSync(path.join(ROOT, "articles", "index.html"), indexTpl(published));

/* ---------- inject top-3 cards into index.html ---------- */
const INDEX_HTML = path.join(ROOT, "index.html");
try {
  const top3 = published.slice(0, 3);
  const cards = top3.map(a =>
    '      <article class="article"><div class="article-meta">' +
    '<span class="tag">' + esc(a.tag.he) + '</span>' +
    '<span class="stamp">' + a.date + '</span></div>' +
    '<h3>' + esc(a.title.he) + '</h3>' +
    '<p>' + esc(a.body.he) + '</p>' +
    '<a class="read-more" href="/articles/' + a.slug + '.html"><span>לקריאת העדכון המלא</span> <span class="arr">←</span></a></article>'
  ).join("\n");
  let idx = fs.readFileSync(INDEX_HTML, "utf8");
  idx = idx.replace(/<!-- BUILD:ARTICLES_GRID -->[\s\S]*?(?=<\/div>\s*<div class="articles-foot)/, cards + "\n");
  fs.writeFileSync(INDEX_HTML, idx);
  console.log("INJECTED top-3 article cards into index.html");
} catch (e) { console.log("  ! index.html card injection skipped:", e.message); }

/* ---------- sitemap ---------- */
const newest = published.length ? iso(published[0].date) : null;
const urls = [
  { loc: SITE + "/", pri: "1.0", freq: "daily" },
  { loc: SITE + "/articles/", pri: "0.9", freq: "daily", mod: newest },
  { loc: SITE + "/practice/", pri: "0.9", freq: "monthly" },
  { loc: SITE + "/legal.html", pri: "0.3", freq: "yearly" }
];
/* עמודי תחומי העיסוק — נבנים ב-build-practice.js, נכנסים לסייטמאפ כאן */
try {
  JSON.parse(fs.readFileSync(path.join(ROOT, "content/practice-areas.json"), "utf8"))
    .forEach(a => urls.push({ loc: SITE + "/practice/" + a.slug + ".html", pri: "0.85", freq: "monthly" }));
} catch (e) { console.log("  ! practice-areas.json not read:", e.message); }
published.forEach(a => urls.push({ loc: SITE + "/articles/" + a.slug + ".html", pri: "0.8", freq: "monthly", mod: iso(a.date) }));
const body = urls.map(u =>
  "  <url><loc>" + u.loc + "</loc>" + (u.mod ? "<lastmod>" + u.mod + "</lastmod>" : "") +
  "<changefreq>" + u.freq + "</changefreq><priority>" + u.pri + "</priority></url>").join("\n");
fs.writeFileSync(path.join(ROOT, "sitemap.xml"),
  '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n");

console.log("BUILT article pages:", renderable.length, "(" + published.length + " live, " + queued.length + " queued/noindex)");
console.log("BUILT blog index:   articles/index.html");
console.log("SITEMAP urls:", urls.length);
if (skipped.length) console.log("skipped:", skipped.join(", "));
