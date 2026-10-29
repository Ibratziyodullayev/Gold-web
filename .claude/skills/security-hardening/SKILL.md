---
name: security-hardening
description: Statik frontend va brauzer e-tijoratida DOM XSS, Content Security Policy (CSP), tabnabbing va xavfsiz headerlarni ta'minlashda ishlatiladi. Triggerlar: xss, csp, security, innerHTML, noopener, sanitize, injection.
---

# Security Hardening (Static Frontend & DOM Stack)

## Qachon ishlatiladi
Foydalanuvchi kiritgan ma'lumotlar (qidiruv maydoni, aloqa formasi, savatga qo'shish), URL hash/search parametrlari va tashqi havolalar orqali DOM-based XSS, clickjacking yoki reverse tabnabbing xurujlari sodir bo'lishining oldini olishda ishlatiladi.

## Checklist
1. **DOM XSS tekshiruvi:** `element.innerHTML`, `outerHTML` yoki `document.write` ga tekshirilmagan qidiruv matnlari yoki foydalanuvchi qiymatlari to'g'ridan-to'g'ri berilmasligi (`textContent` yoki sanitize qilingan qiymatlar ishlatilishi).
2. **Reverse Tabnabbing himoyasi:** Barcha `target="_blank"` bo'lgan tashqi havolalarda (`t.me`, xarita, ijtimoiy tarmoqlar) `rel="noopener noreferrer"` mavjudligi.
3. **Content Security Policy (CSP):** `index.html` boshida `<meta http-equiv="Content-Security-Policy" content="...">` o'rnatilganligi.
4. **X-Frame-Options / Clickjacking:** Sayt boshqa firibgar saytlar ichida `<iframe>` orqali ochilmasligi uchun CSP `frame-ancestors 'none'` yoki framebuster skripti borligi.
5. **Form Input Sanitization:** Telefon raqami va buyurtmachi ismi kiritiladigan inputlarda regex tekshiruvi (`pattern="^\+?[0-9\s\-]{9,15}$"`).
6. **URL Injection himoyasi:** `window.location.hash` yoki `URLSearchParams` orqali sahifa modalini ochishda faqat ruxsat berilgan ID'lar ro'yxatidan (whitelist) foydalanish.
7. **Referrer Policy:** `<meta name="referrer" content="strict-origin-when-cross-origin">` mavjudligi.

## Anti-patterns
- **Qidiruv natijalarini innerHTML ga qo'shish:** `resultsDiv.innerHTML = "Topildi: " + searchInput.value;` — bu yerda `<img src=x onerror=alert(1)>` kiritilsa XSS yuz beradi.
- **Tashqi havolada `rel="noopener"` qolib ketishi:** o'tgan sahifa `window.opener.location` orqali fishing sahifasiga yo'naltirishi mumkin.
- **Javascript protocol injection:** `<a href="javascript:...">` ko'rinishidagi URL'larga filtrsiz yo'l qo'yish.

## Fix recipes

### 1. Xavfsiz matn kiritish (DOM XSS dan himoya)
```javascript
// Xavfli:
// document.getElementById('search-query-display').innerHTML = userQuery;

// Xavfsiz (DOM textContent):
function setSafeText(elementId, text) {
  const el = document.getElementById(elementId);
  if (el) el.textContent = text;
}

// Yoki HTML entity encoder:
function escapeHTML(str) {
  return str.replace(/[&<>'"]/g, 
    tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
  );
}
```

### 2. CSP Meta Tag (GitHub Pages uchun)
```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://unpkg.com https://cdnjs.cloudflare.com;
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com https://cdnjs.cloudflare.com;
  font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com data:;
  img-src 'self' data: https://images.unsplash.com https://res.cloudinary.com https://*.tile.openstreetmap.org https://i.ibb.co;
  connect-src 'self';
  frame-ancestors 'none';
">
```

## Tekshirish buyruqlari
```bash
# 1. innerHTML ishlatilgan barcha qatorlarni topish va audit qilish
grep -n "innerHTML" index.html

# 2. target="_blank" bo'lib rel atributida noopener bo'lmagan havolalarni qidirish
grep -n "target=\"_blank\"" index.html | grep -v "noopener" || echo "Hammasida noopener mavjud!"

# 3. eval yoki inline event handlerlarni (onclick="...") tekshirish
grep -n "onclick=" index.html | wc -l
```
