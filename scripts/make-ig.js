#!/usr/bin/env node
/* מייצר קרוסלות אינסטגרם 1080x1350 מתוך content/instagram-posts.json,
   במיתוג של המשרד (לכה אמרלד, כסף, ורד עתיק, פרנק רוהל + אסיסטנט, מונוגרמת M|B).
   הרצה:  node scripts/make-ig.js [slug]   →  ig/<slug>/01.png ... */
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, "..");
const POSTS = JSON.parse(fs.readFileSync(path.join(ROOT, "content/instagram-posts.json"), "utf8"));
const only = process.argv[2];
const W = 1080, H = 1350;
const esc = s => String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const nl = s => esc(s).replace(/\n/g, "<br>");

const CSS = `
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${W}px;height:${H}px;overflow:hidden}
body{direction:rtl;font-family:'Assistant',sans-serif;position:relative;color:#D9E1DB;
  background:radial-gradient(58% 42% at 80% -8%,rgba(255,232,214,.17) 0%,rgba(255,232,214,0) 56%),
   radial-gradient(74% 50% at 70% -12%,rgba(237,191,184,.20) 0%,rgba(237,191,184,0) 58%),
   linear-gradient(172deg,#1F5643 0%,#164033 20%,#102A21 52%,#0A1A15 78%,#081512 100%)}
body.light{color:#1B211E;background:#F5F2EA}
.plate{position:absolute;top:52%;left:50%;transform:translate(-50%,-50%);width:118%;aspect-ratio:9/6.4;
  opacity:.13;background-position:center;background-size:contain;background-repeat:no-repeat;
  -webkit-mask-image:radial-gradient(circle at 50% 50%,#000 44%,transparent 80%)}
body.light .plate{opacity:.09;filter:invert(1) brightness(.4)}
.grain{position:absolute;inset:0;opacity:.06;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.82' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)'/%3E%3C/svg%3E")}
.livery{position:absolute;top:0;left:0;right:0;height:9px;
  background:linear-gradient(to bottom,#CDD4CE 0 2px,transparent 2px 4px,#88CDA9 4px 6px,transparent 6px 7px,#EDBFB8 7px 9px)}
.frame{position:absolute;inset:46px;border:1px solid rgba(205,212,206,.3)}
body.light .frame{border-color:rgba(27,33,30,.22)}
.frame::before{content:"";position:absolute;inset:7px;border:1px solid rgba(205,212,206,.13)}
body.light .frame::before{border-color:rgba(27,33,30,.1)}
.pad{position:absolute;inset:0;padding:120px 96px 150px;display:flex;flex-direction:column;justify-content:center;z-index:3}
.kick{font-size:26px;font-weight:600;letter-spacing:.05em;color:#EDBFB8;margin-bottom:26px;display:flex;align-items:center;gap:18px}
.kick::before{content:"";width:52px;height:1px;background:#EDBFB8;flex-shrink:0}
body.light .kick{color:#8C4A4E}body.light .kick::before{background:#8C4A4E}
h1{font-family:'Frank Ruhl Libre',serif;font-weight:600;font-size:74px;line-height:1.28;color:#F6F9F4;letter-spacing:0}
body.light h1{color:#1B211E}
.txt{font-family:'Frank Ruhl Libre',serif;font-weight:400;font-size:56px;line-height:1.5;color:#EDF1EC}
body.light .txt{color:#1B211E}
.txt.sm{font-size:46px;line-height:1.62}
.foot{position:absolute;left:96px;right:96px;bottom:74px;display:flex;align-items:center;
  justify-content:space-between;gap:20px;z-index:3}
.mono{display:flex;align-items:center;gap:16px}
.mb{width:62px;height:62px;flex:0 0 62px;display:flex;align-items:center;justify-content:center;position:relative;
  border:1px solid #CDD4CE;border-radius:50%;color:#EDF1EC;direction:ltr;
  font-family:'Cormorant Garamond',serif;font-weight:300;font-size:25px;line-height:1}
body.light .mb{border-color:#5B6863;color:#1B211E}
.mb::after{content:"";position:absolute;inset:3px;border-radius:50%;border:1px solid rgba(205,212,206,.4)}
body.light .mb::after{border-color:rgba(91,104,99,.35)}
.mb i{display:block;width:1px;height:16px;background:#CDD4CE;opacity:.85;margin:0 5px}
body.light .mb i{background:#5B6863}
.name{font-family:'Frank Ruhl Libre',serif;font-size:27px;color:#EDF1EC;line-height:1.35}
.name span{display:block;font-family:'Assistant',sans-serif;font-size:17px;color:#ABB8B0;letter-spacing:.03em}
body.light .name{color:#1B211E}body.light .name span{color:#525A56}
.url{direction:ltr;font-size:22px;color:#CDD4CE;letter-spacing:.05em}
body.light .url{color:#5B6863}
.pg{position:absolute;top:74px;left:96px;font-size:20px;color:#ABB8B0;direction:ltr;letter-spacing:.1em;z-index:3}
body.light .pg{color:#525A56}
.swipe{position:absolute;bottom:74px;left:50%;transform:translateX(-50%);font-size:23px;color:#EDBFB8;
  display:flex;align-items:center;gap:12px;z-index:3}
.cta{font-family:'Frank Ruhl Libre',serif;font-size:50px;line-height:1.45;color:#F6F9F4}
.cta b{color:#EDBFB8;font-weight:600}
`;

const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@300..700&family=Assistant:wght@200..700&family=Cormorant+Garamond:wght@300;400&display=swap" rel="stylesheet">`;

const chrome = (p, n, motif, light) => `
<div class="plate" style="background-image:url('file://${ROOT}/assets/motif-${motif}.svg')"></div>
<div class="grain"></div><div class="livery"></div><div class="frame"></div>
${n ? `<div class="pg">${p} / ${n}</div>` : ""}
<div class="foot">
  <div class="mono"><span class="mb">M<i></i>B</span>
    <span class="name">ברג ושות׳<span>משרד עורכי דין</span></span></div>
  <span class="url">berg-law.co.il</span>
</div>`;

const slideHtml = (post, i, total) => {
  const light = i > 0 && i % 3 === 2;           // כל שלישית על נייר — קצב ויזואלי
  const isCover = i === 0;
  const isLast = i === total - 1;
  const body = isCover
    ? `<div class="kick">${esc(post.pillar)} · יום ${esc(post.day)}</div><h1>${nl(post.slides[0].split("\n").slice(1).join("\n") || post.title)}</h1>`
    : isLast
      ? `<div class="cta">רוצים לדבר על זה<br>לגבי <b>העסק שלכם</b>?<br><br>קישור בביו · הודעה בדיירקט</div>`
      : `<div class="txt${post.slides[i].length > 90 ? " sm" : ""}">${nl(post.slides[i])}</div>`;
  return `<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="UTF-8">${FONTS}<style>${CSS}</style></head>
<body class="${light ? "light" : ""}">${chrome(i + 1, total, post.motif, light)}
<div class="pad">${body}</div>
${isCover ? `<div class="swipe">החליקו ←</div>` : ""}
</body></html>`;
};

(async () => {
  const list = only ? POSTS.filter(p => p.slug === only) : POSTS;
  if (!list.length) { console.log("no post matched", only); return; }
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  for (const post of list) {
    const dir = path.join(ROOT, "ig", post.slug);
    fs.mkdirSync(dir, { recursive: true });
    const total = post.slides.length + 1;                  // + שקופית סיום
    for (let i = 0; i < total; i++) {
      const page = await ctx.newPage();
      await page.setContent(slideHtml(post, i, total), { waitUntil: "networkidle" });
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(450);
      await page.screenshot({ path: path.join(dir, String(i + 1).padStart(2, "0") + ".png") });
      await page.close();
    }
    fs.writeFileSync(path.join(dir, "caption.txt"),
      post.caption + "\n\n" + post.tags + "\n\n" +
      "האמור אינו ייעוץ משפטי ואינו תחליף לו. כל מקרה נבחן לגופו.");
    console.log(`${post.slug}  ${total} slides  (${post.day} · ${post.pillar})`);
  }
  await browser.close();
})();
