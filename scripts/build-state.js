#!/usr/bin/env node
/* build-state.js — כותב ops/state.json לקריאת הארכיטקט.
   רץ אחרי build-articles + build-practice, בכל בילד.
   לא קורא ל-Buffer API — אין .env ב-CI. */

const fs = require("fs"), path = require("path"), { execSync } = require("child_process");
const ROOT = path.join(__dirname, "..");
const LANGS = ["he", "en", "ru", "fr"];
const I18N_FIELDS = ["tag", "title", "body", "gzTag", "gzTitle"];

function safe(fn) { try { return fn(); } catch { return null; } }
function readJSON(rel) { return safe(() => JSON.parse(fs.readFileSync(path.join(ROOT, rel), "utf8"))); }
function parseDate(d) { const p = d.split("."); return new Date(p[2], p[1] - 1, p[0]); }

/* --- git --- */
const sha = process.env.COMMIT_REF || safe(() => execSync("git rev-parse HEAD", { cwd: ROOT }).toString().trim());
const branch = process.env.BRANCH || safe(() => execSync("git rev-parse --abbrev-ref HEAD", { cwd: ROOT }).toString().trim());
const committedAt = safe(() => execSync("git log -1 --format=%aI", { cwd: ROOT }).toString().trim());

/* --- articles --- */
const articles = readJSON("content/articles.json") || [];
const today = new Date(); today.setHours(23, 59, 59, 999);
const futureArticles = articles.filter(a => parseDate(a.date) > today);

const missingSlug = articles.filter(a => !a.slug).map(a => a.date);
const missingFullPage = articles
  .filter(a => a.slug && !fs.existsSync(path.join(ROOT, "content/full", a.slug + ".html")))
  .map(a => a.date + " " + a.slug);

const incompleteTranslations = [];
articles.forEach(a => {
  const missing = [];
  I18N_FIELDS.forEach(field => {
    if (!a[field]) return;
    LANGS.forEach(lang => {
      if (!a[field][lang]) missing.push(field + "." + lang);
    });
  });
  if (missing.length) incompleteTranslations.push({ date: a.date, slug: a.slug || null, missing });
});

const sorted = articles.slice().sort((a, b) => parseDate(b.date) - parseDate(a.date));
const newest = sorted.length ? sorted[0].date : null;
const lastScheduled = futureArticles.length
  ? futureArticles.sort((a, b) => parseDate(b.date) - parseDate(a.date))[0].date
  : null;

/* --- pages --- */
const fullBodies = safe(() => fs.readdirSync(path.join(ROOT, "content/full")).filter(f => f.endsWith(".html")).length) || 0;
const practicePages = safe(() => fs.readdirSync(path.join(ROOT, "practice")).filter(f => f.endsWith(".html") && f !== "index.html").length) || 0;
const articlePages = safe(() => fs.readdirSync(path.join(ROOT, "articles")).filter(f => f.endsWith(".html") && f !== "index.html").length) || 0;

/* --- external files --- */
const buffer = readJSON("ops/buffer.json");
const tasks = readJSON("ops/tasks.json");

/* --- output --- */
const state = {
  generatedAt: new Date().toISOString(),
  git: { sha, committedAt, branch },
  articles: {
    total: articles.length,
    newest,
    lastScheduled,
    runwayDays: futureArticles.length,
    missingSlug,
    missingFullPage,
    incompleteTranslations
  },
  pages: { fullBodies, practice: practicePages, articles: articlePages },
  buffer,
  tasks
};

fs.mkdirSync(path.join(ROOT, "ops"), { recursive: true });
fs.writeFileSync(path.join(ROOT, "ops/state.json"), JSON.stringify(state, null, 2) + "\n");

/* --- warnings --- */
if (state.articles.runwayDays <= 3)
  console.warn("⚠  RUNWAY WARNING: only " + state.articles.runwayDays + " future articles remaining");
if (missingSlug.length)
  console.warn("⚠  MISSING SLUG:", missingSlug.join(", "));
if (missingFullPage.length)
  console.warn("⚠  MISSING FULL PAGE:", missingFullPage.join(", "));
if (incompleteTranslations.length)
  console.warn("⚠  INCOMPLETE TRANSLATIONS: " + incompleteTranslations.length + " articles");

console.log("BUILT ops/state.json — " + articles.length + " articles, runway " + futureArticles.length + " days");
