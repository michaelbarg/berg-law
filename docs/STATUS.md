# STATUS - עדכון אחרון: 2026-08-06

## מצב נוכחי
האתר חי ב-https://berg-law.netlify.app. דומיין berg-law.co.il חובר ב-Netlify, ממתין לעדכון NS ב-DomainTheNet.

## בוצע בסשן האחרון
- חילוץ index.html מ-v7 (~305KB עם תמונה מוטמעת)
- יצירת מבנה תיקיות: content/articles, assets, docs
- netlify.toml עם headers אבטחה (X-Frame-Options, X-Content-Type-Options)
- README.md עם תיעוד נקודות תצורה וחוקים קדושים
- ריפו פרטי github.com/michaelbarg/berg-law — נדחף
- סייט Netlify berg-law — נוצר ונפרס
- דומיין berg-law.co.il חובר + DNS zone נוצר
- NS: dns1-4.p04.nsone.net

## בעיות פתוחות
- ממתין להחלפת NS ב-DomainTheNet (עד 48 שעות propagation)
- TLS certificate ייווצר אוטומטית אחרי שה-NS יתעדכנו

## שאלות לארכיטקט
- אין שאלות פתוחות כרגע

## הוראות אחרונות מהארכיטקט
- (טרם התקבלו)
