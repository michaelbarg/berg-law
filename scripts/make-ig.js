#!/usr/bin/env node
/* ברג ושות׳ — מחולל קרוסלות אינסטגרם 1080x1350.
   ספריית פורמטים: כל עמוד תוכן מקבל קומפוזיציה משלו, וקרקע מתחלפת
   כך שאין שתי משבצות סמוכות ברשת עם אותו רקע.
   הרצה:  node scripts/make-ig.js [slug]   →  ig/<slug>/01.jpg ...
   דורש רשת (Google Fonts) — להריץ דרך Desktop Commander, לא device_bash. */
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, "..");
const POSTS = JSON.parse(fs.readFileSync(path.join(ROOT, "content/instagram-posts.json"), "utf8"));
const only = process.argv[2];
const W = 1080, H = 1350;

const esc = s => String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const nl = s => esc(s).replace(/\n/g, "<br>");
const enc = svg => "data:image/svg+xml;utf8," + encodeURIComponent(svg).replace(/'/g, "%27");
const du = f => enc(fs.readFileSync(path.join(ROOT, "assets", f), "utf8"));
const dj = f => "data:image/jpeg;base64," + fs.readFileSync(path.join(ROOT, "assets", f)).toString("base64");
const hash = s => { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; };

/* ── קרקעות. הטווח הטונלי הרחב הוא מה שפתר את ה״אנמי״ ── */
const GROUNDS = {
  deep:  { bg: "linear-gradient(168deg,#143A2E 0%,#0F2A21 44%,#0A1A15 80%,#081512 100%)",
           fg: "#EDF1EC", dim: "#ABB8B0", acc: "#EDBFB8", rule: "rgba(205,212,206,.30)", hair: "rgba(205,212,206,.13)", ink: "#CDD4CE", bgFlat: "#0F2A21" },
  paper: { bg: "radial-gradient(120% 80% at 76% -14%,#FCFAF4 0%,rgba(252,250,244,0) 58%),#F5F2EA",
           fg: "#1B211E", dim: "#525A56", acc: "#8C4A4E", rule: "rgba(27,33,30,.22)", hair: "rgba(27,33,30,.10)", ink: "#5B6863", bgFlat: "#F5F2EA" },
  verde: { bg: "linear-gradient(168deg,#247056 0%,#20604A 46%,#1C4737 78%,#143528 100%)",
           fg: "#F5F2EA", dim: "#B9D6C7", acc: "#88CDA9", rule: "rgba(245,242,234,.30)", hair: "rgba(245,242,234,.13)", ink: "#D9E1DB", bgFlat: "#20604A" },
};
const ORDER = ["deep", "paper", "verde"];
/* (n + floor(n/3)) % 3 — ריבוע לטיני: אף שתי משבצות צמודות (אופקית או אנכית)
   לא חולקות רקע, בכל היסט של הרשת. n % 3 היה נותן שלושה פסים אנכיים. */
const groundFor = n => ORDER[(n + Math.floor(n / 3)) % 3];
const other = k => ORDER[(ORDER.indexOf(k) + 1) % 3];

/* ── גיאומטריה נוצרת: שדה סרטים (התאבכות) ── */
function ribbonField(seed, stroke, op) {
  let s = seed >>> 0; const rnd = () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296;
  const N = 46, A = 120 + rnd() * 90, k = 0.0042 + rnd() * 0.0026, drift = rnd() * 6.283, out = [];
  for (let i = 0; i < N; i++) {
    const base = 60 + i * (760 / N), ph = drift + i * (0.10 + rnd() * 0.02);
    const amp = A * (0.35 + 0.65 * Math.sin(Math.PI * i / N));
    let d = "";
    for (let x = 0; x <= 1200; x += 12)
      d += (x ? "L" : "M") + x + "," + (base + amp * Math.sin(k * x * 2.4 + ph) + 26 * Math.sin(k * x * 6.1 + ph * 2)).toFixed(1) + " ";
    out.push(`<path d="${d}" fill="none" stroke="${stroke}" stroke-width="${(0.9 + (i % 3) * 0.35).toFixed(2)}" opacity="${(op * (0.45 + 0.55 * Math.sin(Math.PI * i / N))).toFixed(3)}"/>`);
  }
  return enc((`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 880">${out.join("")}</svg>`));
}

/* ── גיאומטריה נוצרת: חותם. זרע מה-slug ⇒ לכל פוסט חותם משלו ── */
function sealRing(seed, stroke) {
  let s = seed >>> 0; const rnd = () => (s = (s * 1103515245 + 12345) >>> 0) / 2147483648 % 1;
  let g = "";
  for (let r = 120; r <= 300; r += 12) {
    const pts = [], lobes = 5 + Math.floor(rnd() * 4), amp = 4 + rnd() * 7;
    for (let a = 0; a <= 360; a += 2) {
      const rad = a * Math.PI / 180, rr = r + amp * Math.sin(lobes * rad + r * 0.05);
      pts.push((320 + rr * Math.cos(rad)).toFixed(1) + "," + (320 + rr * Math.sin(rad)).toFixed(1));
    }
    g += `<polyline points="${pts.join(" ")}" fill="none" stroke="${stroke}" stroke-width="1.0" opacity="${(0.34 + 0.24 * rnd()).toFixed(2)}"/>`;
  }
  return enc((`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640">${g}</svg>`));
}

/* ── דיאגרמת שלבים, RTL: צומת 1 מימין. הצומת האחרון דלוק ⇒ נקרא כמסקנה ── */
function schemaFlow(labels, stroke, acc, fg, lit) {
  const cx = [900, 570, 240], cy = 300, r = 128;
  const on = i => (lit === "all" || i === 2);
  let g = `<line x1="900" y1="${cy}" x2="240" y2="${cy}" stroke="${stroke}" stroke-width="1.4" opacity=".5"/>`;
  cx.forEach((x, i) => {
    const c = on(i) ? acc : stroke;
    g += `<circle cx="${x}" cy="${cy}" r="${r}" fill="none" stroke="${c}" stroke-width="${on(i) ? 2.4 : 1.4}" opacity="${on(i) ? 1 : .68}"/>`;
    g += `<circle cx="${x}" cy="${cy}" r="${r - 9}" fill="none" stroke="${c}" stroke-width=".9" opacity="${on(i) ? .55 : .3}"/>`;
    g += `<text x="${x}" y="${cy + 16}" text-anchor="middle" font-family="'Frank Ruhl Libre',serif" font-size="52" fill="${on(i) ? acc : fg}">${i + 1}</text>`;
    g += `<text x="${x}" y="${cy + r + 78}" text-anchor="middle" font-family="Assistant,sans-serif" font-weight="600" font-size="34" fill="${fg}" opacity=".82" direction="rtl">${esc(labels[i] || "")}</text>`;
    if (i < 2) g += `<path d="M${x - r - 26},${cy} l26,-13 v26 z" fill="${stroke}" opacity=".7"/>`;
  });
  return enc((`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1140 520">${g}</svg>`));
}

const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@300..700&family=Assistant:wght@200..700&family=Cormorant+Garamond:wght@300;400&display=block" rel="stylesheet">`;

const CSS = g => `
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${W}px;height:${H}px;overflow:hidden}
body{direction:rtl;font-family:Assistant,sans-serif;color:${g.fg};background:${g.bg};position:relative;
  font-synthesis:none;-webkit-font-smoothing:antialiased;letter-spacing:0}
.grain{position:absolute;inset:0;opacity:.055;mix-blend-mode:overlay;pointer-events:none;z-index:9;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.82' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)'/%3E%3C/svg%3E")}
.livery{position:absolute;top:0;left:0;right:0;height:9px;z-index:8;
  background:linear-gradient(to bottom,#CDD4CE 0 2px,transparent 2px 4px,#88CDA9 4px 6px,transparent 6px 7px,#EDBFB8 7px 9px)}
.frame{position:absolute;inset:46px;border:1px solid ${g.rule};z-index:2}
.frame::before{content:"";position:absolute;inset:7px;border:1px solid ${g.hair}}
.pg{position:absolute;top:74px;right:96px;font-size:20px;color:${g.dim};direction:ltr;letter-spacing:.1em;z-index:6;
  font-variant-numeric:lining-nums tabular-nums}
.foot{position:absolute;left:96px;right:96px;bottom:74px;display:flex;align-items:center;justify-content:space-between;z-index:6}
.mono{display:flex;align-items:center;gap:16px}
.mb{width:62px;height:62px;flex:0 0 62px;display:flex;align-items:center;justify-content:center;position:relative;
  border:1px solid ${g.ink};border-radius:50%;color:${g.fg};direction:ltr;font-family:'Cormorant Garamond',serif;font-weight:300;font-size:25px}
.mb::after{content:"";position:absolute;inset:3px;border-radius:50%;border:1px solid ${g.hair}}
.mb i{display:block;width:1px;height:16px;background:${g.ink};opacity:.85;margin:0 5px}
.name{font-family:'Frank Ruhl Libre',serif;font-size:27px;color:${g.fg};line-height:1.35}
.name span{display:block;font-family:Assistant,sans-serif;font-size:17px;color:${g.dim};letter-spacing:.03em}
.url{direction:ltr;font-size:22px;color:${g.ink};letter-spacing:.05em}
.upper{position:absolute;left:96px;right:96px;top:150px;height:590px;z-index:1}
.lower{position:absolute;left:96px;right:96px;bottom:246px;z-index:4}
.kick{font-size:26px;font-weight:600;letter-spacing:.05em;color:${g.acc};margin-bottom:28px;
  display:flex;align-items:center;gap:18px}
.kick::before{content:"";width:52px;height:1px;background:${g.acc};flex:0 0 52px}
h1{font-family:'Frank Ruhl Libre',serif;font-weight:600;font-size:104px;line-height:1.16;color:${g.fg};text-wrap:balance}
h1.m{font-size:84px;line-height:1.22}
h1.s{font-size:70px;line-height:1.26}
.sub{font-size:32px;font-weight:400;line-height:1.58;color:${g.dim};margin-top:26px}
.rule{height:1px;background:${g.rule}}
.lede{font-family:'Frank Ruhl Libre',serif;font-weight:400;font-size:62px;line-height:1.52;color:${g.fg};text-wrap:pretty}
.lede.sm{font-size:52px;line-height:1.6}
.lbl{font-size:24px;font-weight:600;letter-spacing:.1em;color:${g.dim};margin-bottom:26px}
`;

const chrome = (g, i, n) => `<div class="grain"></div><div class="livery"></div><div class="frame"></div>
<div class="pg">${String(i).padStart(2, "0")} / ${String(n).padStart(2, "0")}</div>
<div class="foot"><div class="mono"><span class="mb">M<i></i>B</span>
<span class="name">ברג ושות׳<span>משרד עורכי דין</span></span></div><span class="url">berg-law.co.il</span></div>`;

/* ══════════ קומפוזיציות שער ══════════ */
const COVER = {
  /* סעיף השבוע — עיקרון מצוטט על שורות פנקס, סרגל הדגשה בשוליים המובילים */
  clause: (t, g, seed) => `
   <div class="upper" style="top:150px;height:560px;background:url('${ribbonField(seed, g.ink, .55)}') center/125% no-repeat;
     -webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 22%,#000 62%,transparent 100%);opacity:.9"></div>
   <div style="position:absolute;left:96px;right:96px;top:372px;z-index:3">
     <div style="border-right:3px solid ${g.acc};padding-right:34px">
       <div style="font-family:'Frank Ruhl Libre',serif;font-size:58px;line-height:1.62;color:${g.fg};
         background:repeating-linear-gradient(to bottom,transparent 0 94px,${g.hair} 94px 95px)">${nl(t.line)}</div>
     </div></div>
   <div class="lower"><div class="kick">${esc(t.kick)}</div><h1 class="m">${nl(t.title)}</h1></div>`,

  /* טעות שעולה כסף — ספרה חלולה שגולשת מהמסגרת. האובייקט הכי בעל ניגוד בספרייה */
  numeral: (t, g) => `
   <div style="position:absolute;left:-72px;top:104px;z-index:1;font-family:'Frank Ruhl Libre',serif;font-weight:300;
     font-size:560px;line-height:.78;color:transparent;-webkit-text-stroke:2.5px ${g.acc};opacity:.85;direction:ltr">${esc(t.num)}</div>
   <div style="position:absolute;right:96px;top:222px;left:520px;z-index:4;text-align:right">
     <div class="kick">${esc(t.kick)}</div>
     <div style="font-size:32px;line-height:1.6;color:${g.dim}">${nl(t.line)}</div></div>
   <div class="lower"><div class="rule" style="margin-bottom:40px"></div><h1>${nl(t.title)}</h1></div>`,

  /* עיקרון בשורה אחת — אפיגרף בין שני קווים. הפורמט היחיד בלי הסבר בשער */
  maxim: (t, g, seed) => `
   <div style="position:absolute;left:0;right:0;top:135px;height:1080px;z-index:1;
     background:url('${sealRing(seed, g.ink)}') 112% 16%/860px no-repeat;opacity:.85"></div>
   <div style="position:absolute;left:96px;right:96px;top:392px;z-index:4">
     <div class="rule"></div>
     <div style="font-family:'Frank Ruhl Libre',serif;font-weight:500;font-size:88px;line-height:1.30;
       color:${g.fg};padding:52px 0;text-wrap:balance">${nl(t.line)}</div>
     <div class="rule"></div>
     <div class="kick" style="margin-top:40px">${esc(t.kick)}</div></div>`,

  /* מן הפסיקה — כרטיס תיק. המשבצת הכי שקטה ברשת: היא אמורה להיקרא כמסמך */
  docket: (t, g) => `
   <div style="position:absolute;right:96px;left:96px;top:200px;z-index:4">
     <div style="display:flex;justify-content:space-between;border-top:2px solid ${g.acc};
       border-bottom:1px solid ${g.rule};padding:20px 0;font-size:25px;font-weight:600;letter-spacing:.04em;color:${g.acc}">
       <span>${esc(t.court)}</span><span style="color:${g.dim};font-weight:400">${esc(t.field)}</span></div>
     <div style="font-size:22px;color:${g.dim};padding-top:16px;direction:ltr;text-align:right;
       letter-spacing:.14em;font-variant-numeric:lining-nums tabular-nums">${esc(t.docketNo)}</div></div>
   <div style="position:absolute;right:96px;top:200px;bottom:246px;width:2px;z-index:2;
     background:linear-gradient(to bottom,${g.acc} 0,${g.rule} 30%,transparent 100%)"></div>
   <div style="position:absolute;left:96px;right:150px;top:426px;z-index:4">
     <div class="lbl">מה נקבע</div>
     <div style="font-family:'Frank Ruhl Libre',serif;font-weight:500;font-size:82px;line-height:1.26;
       color:${g.fg};text-wrap:balance">${nl(t.line)}</div></div>
   <div class="lower"><div class="rule" style="margin-bottom:32px"></div>
     <div style="font-size:30px;line-height:1.55;color:${g.dim}">${nl(t.title)}</div></div>`,

  /* מה בודקים / מילון — דיאגרמה. המשבצת היחידה שנראית שימושית במבט אחד */
  schema: (t, g) => `
   <div style="position:absolute;left:70px;right:70px;top:214px;height:470px;z-index:3;
     background:url('${schemaFlow(t.nodes, g.ink, g.acc, g.fg)}') center/contain no-repeat"></div>
   <div class="lower"><div class="kick">${esc(t.kick)}</div><h1 class="m">${nl(t.title)}</h1></div>`,


  /* LEXICON — ערך מילוני. עמודת מילון: קו תוחם, המונח גדול, וההגדרה בהזחה תלויה. */
  lexicon: (t, g) => `
   <div style="position:absolute;right:96px;top:150px;bottom:246px;width:1px;background:${g.rule};z-index:2"></div>
   <div style="position:absolute;right:88px;bottom:640px;width:17px;height:17px;border-radius:50%;
     border:1px solid ${g.acc};background:${g.bgFlat};z-index:3"></div>
   <div style="position:absolute;left:0;top:210px;width:560px;height:560px;z-index:1;
     background:url('${sealRing(t.seed, g.ink)}') -22% 46%/620px no-repeat;opacity:.5"></div>
   <div style="position:absolute;right:150px;left:96px;bottom:246px;z-index:4">
     <div style="font-size:23px;font-weight:600;letter-spacing:.14em;color:${g.acc};margin-bottom:20px">${esc(t.kick)}</div>
     <div style="font-family:'Frank Ruhl Libre',serif;font-weight:600;font-size:112px;line-height:1.10;
       color:${g.fg};text-wrap:balance">${nl(t.title)}</div>
     <div style="width:100%;height:1px;background:${g.rule};margin:34px 0 30px"></div>
     <div style="font-size:33px;line-height:1.56;color:${g.dim};padding-right:34px;
       border-right:2px solid ${g.hair}">${nl(t.line)}</div></div>`,
  /* שאלה מהשטח — סימן שאלה חתוך בשוליים. הפורמט היחיד בקולו של הקורא */
  question: (t, g) => `
   <div style="position:absolute;left:-20px;top:128px;z-index:1;font-family:'Frank Ruhl Libre',serif;font-weight:300;
     font-size:520px;line-height:.8;color:transparent;-webkit-text-stroke:2px ${g.acc};opacity:.55;direction:ltr">?</div>
   <div style="position:absolute;right:96px;left:96px;top:338px;z-index:4">
     <div class="kick">${esc(t.kick)}</div>
     <div style="font-family:'Frank Ruhl Libre',serif;font-weight:500;font-size:84px;line-height:1.26;
       color:${g.fg};text-wrap:balance">${nl(t.title)}</div></div>
   <div class="lower"><div class="rule" style="margin-bottom:36px"></div>
     <div style="font-size:31px;line-height:1.55;color:${g.dim}">${nl(t.line)}</div></div>`,


  /* PORTRAIT — פורמט היכרות. הפנים נושאות את הקאדר, הטיפוגרפיה מלווה. */
  portrait: (t, g) => `
   <div style="position:absolute;left:96px;top:150px;width:452px;height:900px;z-index:3;
     background:url('${dj("mb-portrait-wide.jpg")}') center 12%/cover no-repeat;
     border:1px solid ${g.rule};box-shadow:0 0 0 7px ${g.bgFlat},0 0 0 8px ${g.hair}"></div>
   <div style="position:absolute;right:96px;left:600px;top:214px;z-index:4">
     <div class="kick">${esc(t.kick)}</div>
     <h1 class="m" style="margin-bottom:22px">${nl(t.title)}</h1>
     <div style="width:64px;height:1px;background:${g.acc};margin-bottom:22px"></div>
     <div style="font-size:31px;line-height:1.55;color:${g.dim}">${nl(t.line)}</div></div>`,
  /* לסוף השבוע — עיטור מלא. הפורמט היחיד שבו התמונה גוברת על הטיפוגרפיה */
  plate: (t, g) => `
   <div style="position:absolute;inset:0;z-index:1;background:url('${du("plate-guilloche.svg")}') 30% 24%/175% no-repeat;
     opacity:.58;-webkit-mask-image:linear-gradient(to bottom,#000 0,#000 54%,transparent 86%)"></div>
   <div class="lower"><div class="rule" style="margin-bottom:38px"></div>
     <div class="kick">${esc(t.kick)}</div><h1 class="m">${nl(t.title)}</h1></div>`,
};

/* ══════════ שקופיות פנים ══════════ */
const body = (head, rest, g, fmt, seed, idx) => {
  const long = rest.length > 88;
  const orn = fmt === "schema"
    ? `<div class="upper" style="top:168px;height:400px;background:url('${sealRing(seed + idx, g.ink)}') 96% 8%/520px no-repeat;opacity:.5"></div>`
    : `<div class="upper" style="top:168px;height:430px;background:url('${ribbonField(seed + idx * 7, g.ink, .42)}') center/135% no-repeat;
        -webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 26%,#000 66%,transparent 100%);opacity:.62"></div>`;
  return `${orn}
   <div class="lower">${head ? `<div class="lbl">${esc(head)}</div>` : ""}
     <div class="lede${long ? " sm" : ""}">${nl(rest)}</div></div>`;
};

/* כרטיס חתימה עם דיוקן — פעם בשבוע בלבד, בפוסט "שאלה מהשטח":
   הפורמט היחיד שכתוב בקולו של הקורא, ולכן החתימה של מי שעונה שייכת דווקא שם. */
const PORTRAIT_DAY = "שישי";

const closingPortrait = () => {
  const g = GROUNDS.paper;
  return `<div style="position:absolute;left:96px;top:150px;width:430px;height:780px;z-index:3;
      background:url('${dj("mb-portrait-duo.jpg")}') center/cover no-repeat;
      border:1px solid ${g.rule};box-shadow:0 0 0 7px ${g.bgFlat},0 0 0 8px ${g.hair}"></div>
    <div style="position:absolute;right:96px;left:580px;top:214px;z-index:4">
      <div class="kick">מייקל ברג · עורך דין</div>
      <div style="font-family:'Frank Ruhl Libre',serif;font-weight:500;font-size:62px;line-height:1.30;
        color:${g.fg};text-wrap:balance">רוצים לדבר<br>על זה לגבי<br><b style="color:${g.acc};font-weight:600">העסק שלכם</b>?</div>
    </div>
    <div class="lower"><div class="rule" style="margin-bottom:34px"></div>
      <div style="font-size:31px;line-height:1.6;color:${g.dim}">
        שיחת היכרות ומיפוי צרכים · קישור בביו · הודעה בדיירקט</div></div>`;
};

const closingPlain = g => `
  <div style="position:absolute;inset:0;z-index:1;background:url('${du("plate-arcade.svg")}') 40% 30%/260% no-repeat;
    opacity:.4;-webkit-mask-image:linear-gradient(to bottom,#000 0,#000 46%,transparent 82%)"></div>
  <div class="lower"><div class="rule" style="margin-bottom:38px"></div>
    <div style="font-family:'Frank Ruhl Libre',serif;font-size:62px;line-height:1.42;color:${g.fg}">
      רוצים לדבר על זה<br>לגבי <b style="color:${g.acc};font-weight:600">העסק שלכם</b>?</div>
    <div class="sub" style="margin-top:30px">קישור בביו · הודעה בדיירקט</div></div>`;

/* ══════════ גזירת נתוני שער מתוכן קיים — בלי להמציא ניסוח משפטי ══════════ */
const PILLAR_FMT = {
  "סעיף השבוע": "clause", "טעות שעולה כסף": "numeral", "עיקרון בשורה אחת": "maxim",
  "מה בודקים לפני ש…": "schema", "מילון": "lexicon", "שאלה מהשטח": "question",
  "לסוף השבוע": "plate", "מן הפסיקה": "docket", "היכרות": "portrait",
};
const firstLine = s => String(s || "").split("\n")[0].replace(/[:：]\s*$/, "").trim();
const capLead = p => String(p.caption || "").split("\n").filter(Boolean)[0] || "";

function coverData(p, seqInPillar) {
  const c = p.cover || {};
  const s0 = (p.slides[0] || "").split("\n");
  const shortTitle = s0.slice(1).join("\n").trim() || p.title;
  const fmt = c.format || p.format || PILLAR_FMT[p.pillar] || "clause";
  const base = { kick: c.kick || p.pillar, title: c.title || shortTitle, line: c.line || capLead(p) };
  if (fmt === "numeral") base.num = c.num || String(seqInPillar).padStart(2, "0");
  if (fmt === "maxim") { base.line = c.line || capLead(p) || shortTitle; base.title = shortTitle; }
  if (fmt === "question") { base.title = c.title || firstLine(p.slides[1] || "").replace(/^השאלה\s*/, "") || shortTitle; base.line = c.line || capLead(p); }
  if (fmt === "lexicon") base.seed = hash(p.slug);
  if (fmt === "schema") base.nodes = c.nodes || p.slides.slice(1, 4).map(s => firstLine(s).slice(0, 22));
  if (fmt === "docket") { base.court = c.court || ""; base.field = c.field || ""; base.docketNo = c.docketNo || ""; base.line = c.holding || ""; base.title = c.source || ""; }
  return { fmt, t: base };
}

/* שער מסוג docket אסור בלי מקור מאומת — שער בנייה, לא בדיקה ידנית */
function gate(p, fmt) {
  if (fmt !== "docket") return;
  const c = p.cover || {};
  const miss = ["court", "docketNo", "holding", "source_url", "verified_at"].filter(k => !c[k]);
  if (miss.length) throw new Error(`[${p.slug}] פוסט "מן הפסיקה" חסר שדות חובה: ${miss.join(", ")}`);
}

(async () => {
  const list = only ? POSTS.filter(p => p.slug === only) : POSTS;
  if (!list.length) { console.error("no post matched", only); process.exit(1); }
  const seqCount = {};
  POSTS.forEach(p => { seqCount[p.pillar] = (seqCount[p.pillar] || 0) + 1; p._seq = seqCount[p.pillar]; });

  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  for (const post of list) {
    const n = POSTS.indexOf(post);
    const seed = hash(post.slug);
    const { fmt, t } = coverData(post, post._seq);
    gate(post, fmt);
    const gk = fmt === "portrait" ? "paper" : groundFor(n), gAlt = other(gk);
    const withPortrait = post.day === PORTRAIT_DAY && fmt !== "portrait";   /* דיוקן פעם בשבוע, ולא פעמיים באותו פוסט */
    const dir = path.join(ROOT, "ig", post.slug);
    fs.mkdirSync(dir, { recursive: true });
    const total = post.slides.length + 1;

    for (let i = 0; i < total; i++) {
      /* קצב ABA בתוך הקרוסלה: הציר (3) והסיום מתהפכים — שקופית הסיום היא זו שמצלמים */
      const key = (i === total - 1 && withPortrait) ? "paper" : ((i === 2 || i === total - 1) ? gAlt : gk);
      const g = GROUNDS[key];
      let inner;
      if (i === 0) inner = COVER[fmt](t, g, seed);
      else if (i === total - 1) inner = withPortrait ? closingPortrait() : closingPlain(g);
      else {
        const parts = (post.slides[i] || "").split("\n");
        const head = parts.length > 1 && parts[0].trim().endsWith(":") ? parts[0].replace(/:$/, "") : "";
        inner = body(head, head ? parts.slice(1).join("\n") : parts.join("\n"), g, fmt, seed, i);
      }
      const html = `<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="UTF-8">${FONTS}
<style>${CSS(g)}</style></head><body>${chrome(g, i + 1, total)}${inner}</body></html>`;

      const page = await ctx.newPage();
      const failed = [];
      page.on("requestfailed", r => failed.push(r.url().slice(0, 90)));
      await page.setContent(html, { waitUntil: "networkidle" });
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(420);
      /* נכס שנפל = שקופית ריקה בלי שגיאה. נופלים ברעש, לא בשקט. */
      if (failed.length) throw new Error(`[${post.slug} #${i + 1}] נכסים שלא נטענו:\n  ` + failed.join("\n  "));
      await page.screenshot({ path: path.join(dir, String(i + 1).padStart(2, "0") + ".jpg"), type: "jpeg", quality: 92 });
      await page.close();
    }
    fs.writeFileSync(path.join(dir, "caption.txt"),
      post.caption + "\n\n" + post.tags + "\n\nהאמור אינו ייעוץ משפטי ואינו תחליף לו. כל מקרה נבחן לגופו.");
    console.log(`${String(n).padStart(2, "0")} ${post.slug.padEnd(26)} ${fmt.padEnd(9)} ${gk.padEnd(6)} ${total} slides${withPortrait ? "  +portrait" : ""}`);
  }
  await browser.close();
})().catch(e => { console.error("FATAL", e.message); process.exit(1); });
