#!/usr/bin/env node
/* בונה עמוד נחיתה לכל תחום עיסוק: /practice/<slug>.html + /practice/ (אינדקס).
   כל עמוד: לוח חרוט משלו, תוכן, שאלות ותשובות (FAQ schema), כתבות רלוונטיות מאותו תחום,
   וטופס יצירת קשר בתחתית. הרצה: node scripts/build-practice.js */
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, ".."), SITE = "https://berg-law.co.il";
const AREAS = JSON.parse(fs.readFileSync(path.join(ROOT, "content/practice-areas.json"), "utf8"));
const ARTICLES = JSON.parse(fs.readFileSync(path.join(ROOT, "content/articles.json"), "utf8"));
const today = new Date(); today.setHours(23, 59, 59, 999);
const parse = d => { const p = d.split("."); return new Date(p[2], p[1] - 1, p[0]); };
const iso = d => { const p = d.split("."); return p[2] + "-" + p[1] + "-" + p[0]; };
const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const desc = s => { s = String(s).replace(/\s+/g, " "); if (s.length <= 155) return s; const c = s.lastIndexOf(" ", 152); return s.slice(0, c > 80 ? c : 152) + "…"; };
const WA = "972546665615";

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
    '<circle cx="32" cy="32" r="32" fill="#0F2A21"/><circle cx="32" cy="32" r="29" fill="none" stroke="#CDD4CE" stroke-width="1.5"/>' +
    '<circle cx="32" cy="32" r="26.2" fill="none" stroke="#CDD4CE" stroke-width="0.7" opacity="0.4"/>' +
    '<g fill="#EDF1EC" font-family="Georgia,Times New Roman,serif" font-size="26" text-anchor="middle">' +
    '<text x="21" y="41">M</text><text x="44" y="41">B</text></g>' +
    '<rect x="31.6" y="24" width="1" height="16" fill="#CDD4CE" opacity="0.85"/></svg>').toString("base64") + `">`;

const CSS = `
:root{${TOKENS}}
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;scroll-behavior:smooth}
html,body{font-synthesis-weight:none}
body{font-family:var(--sans);background:var(--pearl);color:var(--ink);line-height:1.85;font-size:17px}
::selection{background:var(--verde);color:var(--pearl-2)}
a{color:inherit}
h1,h2,h3{font-family:var(--display);font-weight:500;letter-spacing:0;text-wrap:balance}
p{text-wrap:pretty}
:focus-visible{outline:2px solid var(--verde-bright);outline-offset:3px}
.livery{position:fixed;top:0;right:0;left:0;height:6px;z-index:30;pointer-events:none;
  background:linear-gradient(to bottom,var(--silver) 0 1px,transparent 1px 3px,var(--verde-bright) 3px 4px,transparent 4px 5px,var(--blush) 5px 6px)}
header.site{background:var(--graphite-950);padding:18px 24px;display:flex;align-items:center;
  justify-content:space-between;gap:20px;flex-wrap:wrap;position:relative;z-index:5}
header.site .brand{color:var(--pearl);text-decoration:none;font-family:var(--display);font-size:19px;display:inline-flex;align-items:center;gap:13px}
header.site .brand em{color:var(--silver);font-style:normal;font-size:15px}
header.site nav{display:flex;gap:22px;font-size:14px}
header.site nav a{color:var(--mist);text-decoration:none;transition:color .25s}
header.site nav a:hover{color:var(--silver-bright)}
.mb{width:42px;height:42px;flex:0 0 42px;display:flex;align-items:center;justify-content:center;
  border:1px solid var(--silver);border-radius:50%;color:var(--silver);direction:ltr;position:relative;
  font-family:var(--mark);font-weight:400;font-size:17px;line-height:1}
.mb::after{content:"";position:absolute;inset:2px;border-radius:50%;border:1px solid rgba(205,212,206,.35)}
.mb i{display:block;width:1px;height:11px;background:var(--silver);opacity:.8;margin:0 3px}
/* ---- hero ---- */
.ph{position:relative;overflow:hidden;color:var(--mist);isolation:isolate;
  background:radial-gradient(58% 46% at 80% -10%,rgba(255,232,214,.16) 0%,rgba(255,232,214,0) 56%),
    radial-gradient(74% 54% at 70% -14%,rgba(237,191,184,.19) 0%,rgba(237,191,184,0) 58%),
    linear-gradient(172deg,#1F5643 0%,#164033 22%,#102A21 56%,#0A1A15 82%,#081512 100%)}
.ph::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:1;opacity:.055;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.82' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)'/%3E%3C/svg%3E");background-size:180px 180px}
.ph .plate{position:absolute;top:50%;inset-inline-end:-4%;transform:translateY(-50%);
  width:min(560px,48vw);aspect-ratio:9/6.4;z-index:0;opacity:.16;pointer-events:none;
  background-position:center;background-size:contain;background-repeat:no-repeat;
  -webkit-mask-image:radial-gradient(circle at 50% 50%,#000 46%,transparent 82%);mask-image:radial-gradient(circle at 50% 50%,#000 46%,transparent 82%)}
.ph .inner{position:relative;z-index:2;max-width:1080px;margin:0 auto;padding:86px 26px 82px}
.crumb{font-size:13px;color:var(--mute-d);margin-bottom:26px}
.crumb a{color:var(--mute-d);text-decoration:none}
.crumb a:hover{color:var(--blush)}
.eyebrow{display:inline-flex;align-items:center;gap:14px;font-size:13px;font-weight:600;letter-spacing:.06em;color:var(--blush);margin-bottom:18px}
.eyebrow::before{content:"";width:34px;height:1px;background:var(--blush);flex-shrink:0}
.ph h1{font-size:clamp(29px,4.4vw,46px);line-height:1.32;color:#F6F9F4;max-width:17em}
.ph .lede{margin-top:22px;font-size:18.5px;font-weight:300;line-height:1.85;max-width:40em;color:var(--mist)}
/* ---- body ---- */
main{max-width:1080px;margin:0 auto;padding:0 26px}
.wrap{display:grid;grid-template-columns:1fr 320px;gap:64px;padding:62px 0 20px;align-items:start}
article h2{font-size:23.5px;font-weight:600;margin:38px 0 14px;color:var(--verde)}
article h2:first-child{margin-top:0}
article p{margin-bottom:16px}
article ul{margin:0 0 20px;padding-inline-start:22px}
article li{margin-bottom:11px}
article li::marker{color:var(--blush-deep)}
aside .box{border:1px solid var(--line-strong);background:var(--pearl-2);padding:24px 22px;margin-bottom:22px;position:relative}
aside .box::before{content:"";position:absolute;inset:5px;border:1px solid var(--line);pointer-events:none}
aside h3{font-family:var(--sans);font-size:12.5px;font-weight:700;letter-spacing:.05em;color:var(--slate);margin-bottom:16px;position:relative}
aside .rel a{display:block;text-decoration:none;padding:11px 0;border-top:1px solid var(--line);position:relative}
aside .rel a:first-of-type{border-top:none;padding-top:0}
aside .rel .d{font-size:12px;color:var(--silver-deep);font-variant-numeric:tabular-nums}
aside .rel .t{display:block;font-family:var(--display);font-size:15.5px;line-height:1.5;margin-top:3px;transition:color .25s}
aside .rel a:hover .t{color:var(--blush-deep)}
aside .others a{display:block;padding:9px 0;font-size:14.5px;text-decoration:none;color:var(--slate);border-top:1px solid var(--line);position:relative;transition:color .25s}
aside .others a:first-of-type{border-top:none}
aside .others a:hover{color:var(--verde)}
/* ---- faq ---- */
.faq{border-top:2px solid var(--ink);margin-top:52px;padding-top:2px;position:relative}
.faq::before{content:"";position:absolute;top:3px;right:0;left:0;border-top:1px solid var(--line-strong)}
.faq h2{font-size:20px;margin:26px 0 6px;font-family:var(--sans);font-weight:700;letter-spacing:.03em;color:var(--slate)}
.faq details{border-bottom:1px solid var(--line);padding:4px 0}
.faq summary{cursor:pointer;padding:16px 0;font-family:var(--display);font-size:18px;font-weight:600;list-style:none;display:flex;justify-content:space-between;gap:16px;align-items:baseline}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--blush-deep);font-family:var(--sans);font-size:20px;flex-shrink:0}
.faq details[open] summary::after{content:"–"}
.faq details p{padding:0 0 18px;color:var(--slate);margin:0}
/* ---- contact ---- */
.pc{background:var(--graphite);color:var(--mist);margin-top:70px;position:relative;overflow:hidden;isolation:isolate}
.pc::after{content:"";position:absolute;inset:0;pointer-events:none;opacity:.05;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.82' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)'/%3E%3C/svg%3E")}
.pc .in{position:relative;z-index:2;max-width:1080px;margin:0 auto;padding:64px 26px 68px;
  display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start}
.pc h2{font-size:30px;color:var(--silver-bright);margin-bottom:14px}
.pc p{font-weight:300;max-width:34em}
.pc .lines{margin-top:28px;font-size:15.5px}
.pc .lines a,.pc .lines span{display:block;padding:12px 0;border-bottom:1px solid rgba(205,212,206,.16);text-decoration:none;color:var(--mist);transition:color .25s}
.pc .lines a:hover{color:var(--blush)}
.pc .phone{display:inline-block;direction:ltr;font-variant-numeric:lining-nums tabular-nums;text-align:start}
form .f{margin-bottom:20px}
form label{display:block;font-size:12.5px;letter-spacing:.04em;color:var(--mute-d);margin-bottom:7px}
form input,form textarea{width:100%;background:transparent;border:none;border-bottom:1px solid rgba(205,212,206,.3);
  color:var(--silver-bright);font-family:var(--sans);font-size:16px;padding:9px 0;transition:border-color .25s}
form input:focus,form textarea:focus{outline:none;border-bottom-color:var(--blush)}
form input::placeholder,form textarea::placeholder{color:rgba(171,184,176,.6)}
.btns{display:flex;gap:14px;flex-wrap:wrap;margin-top:26px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:15px 30px;font-weight:600;
  font-size:15px;cursor:pointer;border:1px solid transparent;font-family:var(--sans);text-decoration:none;transition:all .3s}
.btn-s{background:var(--silver);border-color:var(--silver);color:var(--graphite)}
.btn-s:hover{background:var(--silver-bright);border-color:var(--silver-bright)}
.btn-o{border-color:rgba(237,191,184,.55);color:var(--blush)}
.btn-o:hover{background:rgba(237,191,184,.1);border-color:var(--blush)}
.err{display:none;color:var(--blush);font-size:13.5px;margin-top:10px}
.err.on{display:block}
.disc{font-size:12.5px;color:var(--slate);border-top:1px solid var(--line);padding-top:16px;margin:44px 0 0}
footer.site{background:var(--graphite-950);color:var(--mute-d);padding:34px 24px;font-size:13.5px;text-align:center;border-top:1px solid rgba(205,212,206,.28)}
footer.site a{color:var(--silver);text-decoration:none}
footer.site a:hover{color:var(--silver-bright)}
footer.site .soc{display:flex;justify-content:center;gap:16px;margin:0 0 16px}
footer.site .soc a{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;
  border:1px solid rgba(205,212,206,.34);border-radius:50%;color:var(--silver);transition:.25s}
footer.site .soc a:hover{color:var(--graphite-950);background:var(--silver-bright);border-color:var(--silver-bright)}
footer.site .soc svg{width:17px;height:17px}
@media(max-width:900px){.wrap{grid-template-columns:1fr;gap:44px}.pc .in{grid-template-columns:1fr;gap:38px}
  .ph .plate{opacity:.1;width:70vw}.ph .inner{padding:62px 22px 58px}}
`;

const HEADER = `<div class="livery" aria-hidden="true"></div><header class="site">
<a class="brand" href="/"><span class="mb">M<i></i>B</span><span>ברג ושות׳ <em>· משרד עורכי דין</em></span></a>
<nav><a href="/practice/">תחומי עיסוק</a><a href="/articles/">כל הכתבות</a><a href="/#pricing">מסלולי ליווי</a><a href="/#contact">יצירת קשר</a></nav>
</header>`;
const FOOTER = `<footer class="site"><div class="soc"><a href="https://www.instagram.com/berg_law.co.il/" target="_blank" rel="noopener" aria-label="Instagram" title="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg></a><a href="https://www.linkedin.com/in/michael-barg-passparto/" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-.95 1.83-1.95 3.77-1.95 4.03 0 4.78 2.55 4.78 5.87V21h-4v-5.5c0-1.31-.02-3-1.9-3-1.9 0-2.2 1.43-2.2 2.9V21H9z"/></svg></a><a href="https://g.page/r/CY5RIVB2bPH9EBM" target="_blank" rel="noopener" aria-label="Google" title="Google Business Profile"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21s-6.5-5.6-6.5-10.1A6.5 6.5 0 0 1 12 4.4a6.5 6.5 0 0 1 6.5 6.5C18.5 15.4 12 21 12 21z"/><circle cx="12" cy="10.7" r="2.4"/></svg></a></div>© ברג ושות׳ — משרד עורכי דין · <a href="/">berg-law.co.il</a> · <a href="/practice/">תחומי עיסוק</a> · <a href="/articles/">ארכיון הכתבות</a> · <a href="/legal.html">תנאי שימוש ופרטיות</a></footer>`;

/* ---------- contact block (same on every practice page) ---------- */
const contact = a => `<section class="pc" id="contact">
  <div class="in">
    <div>
      <h2>נדבר על ${esc(a.title)}?</h2>
      <p>שיחה ראשונה ללא התחייבות. אפשר להשאיר פרטים כאן, או לכתוב ישירות בוואטסאפ. מענה בעברית, אנגלית, רוסית וצרפתית.</p>
      <div class="lines">
        <a href="tel:+${WA}"><span class="phone">054-666-5615</span></a>
        <a href="https://wa.me/${WA}?text=${encodeURIComponent("שלום, אשמח לדבר בנושא " + a.title)}" target="_blank" rel="noopener">וואטסאפ — מענה מהיר</a>
        <a href="mailto:michael@passparto.com">michael@passparto.com</a>
        <span>תל אביב · פגישות בתיאום מראש</span>
      </div>
    </div>
    <form onsubmit="return sendPractice(event)" novalidate>
      <div class="f"><label for="pn">שם מלא</label><input id="pn" type="text" placeholder="ישראל ישראלי" required></div>
      <div class="f"><label for="pp">טלפון</label><input id="pp" type="tel" placeholder="050-0000000" required></div>
      <div class="f"><label for="pm">בכמה מילים על מה מדובר</label><textarea id="pm" rows="3" placeholder="ספרו בקצרה על העסק ועל הצורך"></textarea></div>
      <span class="err" id="pe">נא למלא שם וטלפון</span>
      <div class="btns">
        <button class="btn btn-s" type="submit">שליחת פנייה</button>
        <a class="btn btn-o" href="https://wa.me/${WA}?text=${encodeURIComponent("שלום, אשמח לדבר בנושא " + a.title)}" target="_blank" rel="noopener">וואטסאפ</a>
      </div>
    </form>
  </div>
  <script>
  function sendPractice(ev){
    ev.preventDefault();
    var n=document.getElementById("pn").value.trim(), p=document.getElementById("pp").value.trim(),
        m=document.getElementById("pm").value, e=document.getElementById("pe");
    if(!n||!p){ e.classList.add("on"); return false; }
    e.classList.remove("on");
    location.href="mailto:michael@passparto.com?subject="+encodeURIComponent("פנייה מהאתר — ${a.title.replace(/"/g, "")}")+
      "&body="+encodeURIComponent("שם: "+n+"\\nטלפון: "+p+"\\nתחום: ${a.title.replace(/"/g, "")}\\n\\n"+m);
    return false;
  }
  <\/script>
</section>`;

/* ---------- one practice page ---------- */
const page = (a, rel, others) => {
  const body = a.sections.map(s =>
    `<h2>${esc(s.h)}</h2>` +
    (s.p ? s.p.map(x => `<p>${esc(x)}</p>`).join("") : "") +
    (s.list ? `<ul>${s.list.map(x => `<li>${esc(x)}</li>`).join("")}</ul>` : "")).join("");
  const metaDesc = desc(a.lede);
  return `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(a.title)} | ברג ושות׳ — משרד עורכי דין תל אביב</title>
<meta name="description" content="${esc(metaDesc)}">
<meta name="theme-color" content="#0F2A21">
<link rel="canonical" href="${SITE}/practice/${a.slug}.html">
${FAVICON}
<meta property="og:type" content="website">
<meta property="og:title" content="${esc(a.title)} | ברג ושות׳">
<meta property="og:description" content="${esc(metaDesc)}">
<meta property="og:url" content="${SITE}/practice/${a.slug}.html">
<meta property="og:image" content="${SITE}/og.jpg">
<meta property="og:locale" content="he_IL">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service",
"name":${JSON.stringify(a.title)},"description":${JSON.stringify(metaDesc)},
"serviceType":${JSON.stringify(a.title)},"inLanguage":"he-IL",
"areaServed":{"@type":"Place","name":"תל אביב והמרכז"},
"availableLanguage":["he","en","ru","fr"],
"provider":{"@type":"LegalService","name":"ברג ושות׳ — משרד עורכי דין","url":"${SITE}",
"telephone":"+${WA}","address":{"@type":"PostalAddress","addressLocality":"Tel Aviv","addressCountry":"IL"}},
"url":"${SITE}/practice/${a.slug}.html"}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[${
  a.faq.map(([q, ans]) => `{"@type":"Question","name":${JSON.stringify(q)},"acceptedAnswer":{"@type":"Answer","text":${JSON.stringify(ans)}}}`).join(",")}]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{"@type":"ListItem","position":1,"name":"ברג ושות׳","item":"${SITE}/"},
{"@type":"ListItem","position":2,"name":"תחומי עיסוק","item":"${SITE}/practice/"},
{"@type":"ListItem","position":3,"name":${JSON.stringify(a.title)}}]}
</script>
${FONTS}
<style>${CSS}</style>
</head>
<body>
${HEADER}
<section class="ph">
  <div class="plate" style="background-image:url('/assets/motif-${a.motif}.svg')" aria-hidden="true"></div>
  <div class="inner">
    <div class="crumb"><a href="/">דף הבית</a> › <a href="/practice/">תחומי עיסוק</a> › ${esc(a.title)}</div>
    <span class="eyebrow">${esc(a.eyebrow)}</span>
    <h1>${esc(a.title)}</h1>
    <p class="lede">${esc(a.lede)}</p>
  </div>
</section>
<main>
  <div class="wrap">
    <article>${body}
      ${a.faq.length ? `<section class="faq"><h2>שאלות שחוזרות</h2>${
        a.faq.map(([q, ans]) => `<details><summary>${esc(q)}</summary><p>${esc(ans)}</p></details>`).join("")}</section>` : ""}
      <p class="disc">האמור בעמוד זה הוא מידע כללי ואינו מהווה ייעוץ משפטי או תחליף לו. כל מקרה נבחן לגופו.</p>
    </article>
    <aside>
      ${rel.length ? `<div class="box rel"><h3>כתבות בנושא</h3>${
        rel.map(r => `<a href="/articles/${r.slug}.html"><span class="d">${esc(r.date)}</span><span class="t">${esc(r.title.he)}</span></a>`).join("")
      }<a href="/articles/" style="border-top:1px solid var(--line);color:var(--verde);font-weight:600;font-size:14px">לכל הכתבות ›</a></div>` : ""}
      <div class="box others"><h3>תחומים נוספים</h3>${
        others.map(o => `<a href="/practice/${o.slug}.html">${esc(o.title)}</a>`).join("")
      }<a href="/practice/" style="color:var(--verde);font-weight:600">כל התחומים ›</a></div>
    </aside>
  </div>
</main>
${contact(a)}
${FOOTER}
</body>
</html>
`;
};

/* ---------- index ---------- */
const indexPage = () => `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>תחומי עיסוק | ברג ושות׳ — משרד עורכי דין תל אביב</title>
<meta name="description" content="תחומי העיסוק של משרד ברג ושות׳: חוזים ומסחר, מקרקעין, רישום חברות והסכמי מייסדים, קניין רוחני וסימני מסחר, דיני עבודה, גבייה, פרטיות ועוד.">
<meta name="theme-color" content="#0F2A21">
<link rel="canonical" href="${SITE}/practice/">
${FAVICON}
<meta property="og:type" content="website">
<meta property="og:title" content="תחומי עיסוק | ברג ושות׳">
<meta property="og:url" content="${SITE}/practice/">
<meta property="og:image" content="${SITE}/og.jpg">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ItemList","name":"תחומי עיסוק — ברג ושות׳","itemListElement":[${
  AREAS.map((a, i) => `{"@type":"ListItem","position":${i + 1},"name":${JSON.stringify(a.title)},"url":"${SITE}/practice/${a.slug}.html"}`).join(",")}]}
</script>
${FONTS}
<style>${CSS}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-top:2px solid var(--ink);position:relative;margin:44px 0 0}
.grid::before{content:"";position:absolute;top:3px;right:0;left:0;border-top:1px solid var(--line-strong)}
.card{position:relative;padding:34px 30px 30px;border-inline-start:1px solid var(--line);border-bottom:1px solid var(--line);
  text-decoration:none;display:flex;flex-direction:column;overflow:hidden;transition:background .3s}
.card:nth-child(3n+1){border-inline-start:none}
.card:hover{background:var(--pearl-2)}
.card .m{position:absolute;inset-inline-end:-14%;top:50%;transform:translateY(-50%);width:62%;aspect-ratio:9/6.4;
  opacity:.07;background-position:center;background-size:contain;background-repeat:no-repeat;pointer-events:none;transition:opacity .35s}
.card:hover .m{opacity:.13}
.card .e{font-size:12px;font-weight:600;color:var(--blush-deep);letter-spacing:.04em;margin-bottom:10px;position:relative}
.card h2{font-size:20px;font-weight:600;line-height:1.5;margin-bottom:10px;position:relative;transition:color .25s}
.card:hover h2{color:var(--blush-deep)}
.card p{font-size:14.5px;color:var(--slate);font-weight:300;line-height:1.8;position:relative;flex:1}
.card .go{margin-top:16px;font-size:13.5px;font-weight:600;color:var(--verde);position:relative}
@media(max-width:980px){.grid{grid-template-columns:repeat(2,1fr)}.card:nth-child(3n+1){border-inline-start:1px solid var(--line)}.card:nth-child(2n+1){border-inline-start:none}}
@media(max-width:620px){.grid{grid-template-columns:1fr}.card{border-inline-start:none!important}}
</style>
</head>
<body>
${HEADER}
<section class="ph">
  <div class="plate" style="background-image:url('/assets/motif-seal.svg')" aria-hidden="true"></div>
  <div class="inner">
    <div class="crumb"><a href="/">דף הבית</a> › תחומי עיסוק</div>
    <span class="eyebrow">מה המשרד עושה</span>
    <h1>תחומי עיסוק</h1>
    <p class="lede">${AREAS.length} תחומים, כל אחד עם עמוד משלו: מה נכלל, מה נבדק, ומה שווה לדעת לפני שמתחילים.</p>
  </div>
</section>
<main>
  <div class="grid">${AREAS.map(a => `
    <a class="card" href="/practice/${a.slug}.html">
      <span class="m" style="background-image:url('/assets/motif-${a.motif}.svg')" aria-hidden="true"></span>
      <span class="e">${esc(a.eyebrow)}</span>
      <h2>${esc(a.title)}</h2>
      <p>${esc(desc(a.lede))}</p>
      <span class="go">לעמוד התחום ←</span>
    </a>`).join("")}</div>
  <p class="disc">האמור באתר הוא מידע כללי ואינו מהווה ייעוץ משפטי או תחליף לו.</p>
</main>
${contact({ title: "העסק שלך", slug: "index" })}
${FOOTER}
</body>
</html>
`;

/* ---------- build ---------- */
fs.mkdirSync(path.join(ROOT, "practice"), { recursive: true });
const live = ARTICLES.filter(a => a.slug && parse(a.date) <= today).sort((x, y) => parse(y.date) - parse(x.date));
AREAS.forEach((a, i) => {
  const rel = live.filter(r => a.tags.includes(r.tag.he)).slice(0, 3);
  const others = [...AREAS.slice(i + 1), ...AREAS.slice(0, i)].slice(0, 5);
  fs.writeFileSync(path.join(ROOT, "practice", a.slug + ".html"), page(a, rel, others));
});
fs.writeFileSync(path.join(ROOT, "practice", "index.html"), indexPage());
console.log("BUILT practice pages:", AREAS.length, "+ index");
AREAS.forEach(a => {
  const n = live.filter(r => a.tags.includes(r.tag.he)).length;
  if (!n) console.log("  ! no related articles:", a.slug);
});
