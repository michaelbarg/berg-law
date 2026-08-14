#!/usr/bin/env python3
"""
לוחות אווירה מקוריים לאתר — נוצרים מתמטית, לא נלקחים מבנק תמונות.
1. גיליוש — שפת התחריט של שטרות ותעודות מניה. הסימן של מסמך רשמי.
2. חזית העיר הלבנה — קו הבניין הבאוהאוסי של תל אביב.
3. קשתות — קצב עמודים, בלי הפטיש והמאזניים.
הרצה:  python3 scripts/make-plates.py   →  assets/plate-*.svg
"""
import math, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(OUT, exist_ok=True)
S = '#CDD4CE'


def guilloche(w=1000, h=1000, stroke=S):
    cx, cy = w / 2, h / 2
    fam = [(250, 47, 128, 1.00, .55, .85), (250, 47, 128, 0.85, .38, .75),
           (250, 47, 128, 0.70, .28, .7), (210, 31, 150, 0.58, .32, .7),
           (210, 31, 150, 0.46, .22, .6), (170, 23, 110, 0.32, .28, .6)]
    out = []
    for R, r, d, sc, op, lw in fam:
        k = (R + r) / r
        span = 2 * math.pi * (r / math.gcd(int(R), int(r)))
        pts = []
        for i in range(1501):
            t = span * i / 1500
            x = ((R + r) * math.cos(t) - d * math.cos(k * t)) * sc * .78
            y = ((R + r) * math.sin(t) - d * math.sin(k * t)) * sc * .78
            pts.append(f'{cx + x:.0f},{cy + y:.0f}')
        out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{stroke}" '
                   f'stroke-width="{lw}" opacity="{op}" stroke-linejoin="round"/>')
    for rad, op in ((372, .5), (363, .26), (250, .2)):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="{stroke}" '
                   f'stroke-width="1" opacity="{op}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">' + ''.join(out) + '</svg>'


def facade(w=1800, h=760, stroke=S):
    e = []
    ground = h - 46
    def ln(x1, y1, x2, y2, op=.4, lw=1):
        e.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                 f'stroke="{stroke}" stroke-width="{lw}" opacity="{op:.2f}"/>')
    def grid(x, y, ww, hh, cols, rows, op=.22):
        for i in range(1, rows): ln(x, y + hh * i / rows, x + ww, y + hh * i / rows, op)
        for j in range(1, cols): ln(x + ww * j / cols, y, x + ww * j / cols, y + hh, op * .8)
    def windows(x, y, ww, hh, cols, rows, op=.3):
        pw, ph = ww / cols * .56, hh / rows * .5
        for r in range(rows):
            for c in range(cols):
                wx = x + ww * (c + .5) / cols - pw / 2
                wy = y + hh * (r + .55) / rows - ph / 2
                e.append(f'<rect x="{wx:.0f}" y="{wy:.0f}" width="{pw:.0f}" height="{ph:.0f}" '
                         f'fill="none" stroke="{stroke}" stroke-width=".9" opacity="{op:.2f}"/>')
    x, bw, top = 70, 430, 250
    e.append(f'<path d="M{x} {ground} L{x} {top+64} Q{x} {top} {x+64} {top} L{x+bw} {top} '
             f'L{x+bw} {ground}" fill="none" stroke="{stroke}" stroke-width="1.5" opacity=".6"/>')
    fl = (ground - top) / 5
    for i in range(1, 5):
        y = top + fl * i
        ln(x, y, x + bw, y, .26)
        ln(x - 24, y - 12, x + bw * .58, y - 12, .5, 1.3)
        ln(x - 24, y - 12, x - 24, y - 1, .3)
        for j in range(11):
            bx = x - 19 + j * (bw * .58 + 5) / 11
            ln(bx, y - 12, bx, y - 30, .14)
    sx = x + bw * .70
    e.append(f'<rect x="{sx:.0f}" y="{top+22:.0f}" width="54" height="{ground-top-52:.0f}" rx="5" '
             f'fill="none" stroke="{stroke}" stroke-width="1.1" opacity=".45"/>')
    for i in range(1, 11):
        yy = top + 22 + (ground - top - 52) * i / 11
        ln(sx, yy, sx + 54, yy, .17)
    x2 = x + bw + 34
    e.append(f'<rect x="{x2}" y="150" width="176" height="{ground-150}" fill="none" '
             f'stroke="{stroke}" stroke-width="1.3" opacity=".5"/>')
    grid(x2, 150, 176, ground - 150, 3, 8, .16); windows(x2, 150, 176, ground - 150, 3, 8, .3)
    x3 = x2 + 210; bw3, t3 = 400, 196
    e.append(f'<rect x="{x3}" y="{t3}" width="{bw3}" height="{ground-t3-52}" fill="none" '
             f'stroke="{stroke}" stroke-width="1.3" opacity=".52"/>')
    grid(x3, t3, bw3, ground - t3 - 52, 6, 6, .15); windows(x3, t3, bw3, ground - t3 - 52, 6, 6, .28)
    ln(x3, ground - 52, x3 + bw3, ground - 52, .5, 1.3)
    for j in range(7): ln(x3 + 22 + j * (bw3 - 44) / 6, ground - 52, x3 + 22 + j * (bw3 - 44) / 6, ground, .42)
    x4 = x3 + bw3 + 30; t4 = ground - 232
    e.append(f'<rect x="{x4}" y="{t4}" width="300" height="232" fill="none" '
             f'stroke="{stroke}" stroke-width="1.2" opacity=".45"/>')
    for i in range(1, 4):
        y = t4 + 232 * i / 4
        ln(x4, y, x4 + 300, y, .2); ln(x4 - 16, y - 9, x4 + 172, y - 9, .32, 1.2)
    for j in range(1, 14): ln(x4 + 190 + 110 * j / 14, t4 + 14, x4 + 190 + 110 * j / 14, ground - 16, .13)
    x5 = x4 + 330
    e.append(f'<rect x="{x5}" y="96" width="126" height="{ground-96}" fill="none" '
             f'stroke="{stroke}" stroke-width="1" opacity=".28"/>')
    grid(x5, 96, 126, ground - 96, 2, 13, .1)
    ln(30, ground, w - 30, ground, .55, 1.5); ln(30, ground + 8, w - 30, ground + 8, .18)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">' + ''.join(e) + '</svg>'


def arcade(w=1600, h=420, stroke=S):
    e = []; n, pad = 10, 60
    span = (w - pad * 2) / n; base, cap = h - 34, 132
    for i in range(n + 1):
        x = pad + i * span; fade = 1 - abs(i - n / 2) / (n / 2) * .6
        e.append(f'<line x1="{x:.0f}" y1="{cap}" x2="{x:.0f}" y2="{base}" stroke="{stroke}" stroke-width="1.3" opacity="{.5*fade:.2f}"/>')
        e.append(f'<line x1="{x-8:.0f}" y1="{cap}" x2="{x+8:.0f}" y2="{cap}" stroke="{stroke}" stroke-width="1.6" opacity="{.55*fade:.2f}"/>')
        e.append(f'<line x1="{x-10:.0f}" y1="{base}" x2="{x+10:.0f}" y2="{base}" stroke="{stroke}" stroke-width="1.6" opacity="{.5*fade:.2f}"/>')
    for i in range(n):
        x = pad + i * span; r = span / 2; fade = 1 - abs(i + .5 - n / 2) / (n / 2) * .6
        e.append(f'<path d="M{x:.0f} {cap} A{r:.0f} {r:.0f} 0 0 1 {x+span:.0f} {cap}" fill="none" stroke="{stroke}" stroke-width="1.3" opacity="{.45*fade:.2f}"/>')
        e.append(f'<path d="M{x+6:.0f} {cap} A{r-6:.0f} {r-6:.0f} 0 0 1 {x+span-6:.0f} {cap}" fill="none" stroke="{stroke}" stroke-width="1" opacity="{.2*fade:.2f}"/>')
    e.append(f'<line x1="{pad-20}" y1="{cap-24}" x2="{w-pad+20}" y2="{cap-24}" stroke="{stroke}" stroke-width="1.4" opacity=".4"/>')
    e.append(f'<line x1="{pad-20}" y1="{cap-18}" x2="{w-pad+20}" y2="{cap-18}" stroke="{stroke}" stroke-width="1" opacity=".2"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">' + ''.join(e) + '</svg>'


for name, svg in (('plate-guilloche', guilloche()), ('plate-facade', facade()), ('plate-arcade', arcade())):
    open(os.path.join(OUT, name + '.svg'), 'w').write(svg)
    print(f'{name:18s} {len(svg)/1024:6.1f} KB')
