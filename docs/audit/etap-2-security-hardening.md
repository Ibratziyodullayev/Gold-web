# Audit Hisoboti: Etap 2 — Security Hardening
**Loyihaning turi:** Statik E-tijorat Veb-ilovasi (Single Page Application / GitHub Pages)  
**Sana:** 2026-10-29  
**Auditor:** Security Hardening Auditor  
**Holat:** TUZATILMOQDA (O'rta va past darajadagi xavflar aniqlandi va himoyalandi)

---

## 1. Kontekst Tahlili
* **Platforma:** GitHub Pages orqali statik hosting qilingan mijoz ilovasi.
* **Hujum yuzalari (Attack Surfaces):**
  * Tashqi havolalar orqali **Reverse Tabnabbing** (foydalanuvchini soxta sahifaga yo'naltirish);
  * Brauzer xavfsizlik sarlavhalari (Content Security Policy, Referrer Policy) yo'qligi sababli uchinchi tomon skriptlarining nazoratsizligi;
  * Qidiruv va mahsulot kartalari renderida **DOM XSS** xavfi;
  * Tashqi iframelar orqali saytni soxtalashtirish (Clickjacking).

---

## 2. Aniqlangan Zaifliklar Ro'yxati

### HIGH (Jiddiy xavflar)

#### [SEC-01] Content Security Policy (CSP) sarlavhasi yo'qligi
* **Fayl va qator:** `index.html:1-12` (`<head>` bo'limi)
* **Muammo:** Sahifada CSP meta tegi yo'q. Agar CDN kutubxonalaridan biri (Tailwind, Lucide, Leaflet) buzilsa, hujumchi saytga ixtiyoriy zararli skript yuklashi mumkin.
* **Hujum stsenariysi:** Zararlangan CDN orqali butun sayt foydalanuvchilarining ma'lumotlari yoki kartalari fishing sahifasiga yuboriladi.
* **Aniq Fix Kodi:**
```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self'; 
  script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://unpkg.com https://cdnjs.cloudflare.com; 
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com https://cdnjs.cloudflare.com; 
  font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com data:; 
  img-src 'self' data: https:; 
  frame-src 'self' https://maps.google.com https://yandex.uz; 
  connect-src 'self';
">
<meta name="referrer" content="strict-origin-when-cross-origin">
```

---

### MEDIUM (O'rta darajali xavflar)

#### [SEC-02] Tashqi havolalarda Reverse Tabnabbing zaifligi
* **Fayl va qatorlar:** 
  * `index.html:850`
  * `index.html:1183`
  * `index.html:1193`
  * `index.html:1820`
  * `index.html:1997`
* **Muammo:** Ushbu havolalarda `target="_blank"` ishlatilgan, ammo `rel="noopener noreferrer"` qo'yilmagan.
* **Hujum stsenariysi:** Yangi ochilgan oyna (Telegram yoki boshqa havola) `window.opener.location` orqali foydalanuvchi qoldirgan Olmos Gold sahifasini firibgarlik (phishing) saytiga almashtirib qo'yishi mumkin.
* **Aniq Fix Kodi:**
```html
<!-- Barcha target="_blank" havolalariga rel qo'shish -->
<a href="https://t.me/OLMOS_GOLD" target="_blank" rel="noopener noreferrer" ...>
```

#### [SEC-03] JavaScript `window.open()` da `noopener` yo'qligi
* **Fayl va qatorlar:** `index.html:2805, 3302, 3742, 3773`
* **Muammo:** `window.open(tgUrl, '_blank')` chaqiruvlarida uchinchi parametr sifatida `'noopener,noreferrer'` ko'rsatilmagan.
* **Hujum stsenariysi:** Eski brauzerlarda `window.opener` ochiq qoladi va ochilgan yangi oyna asosiy sahifani manipulyatsiya qilishi mumkin.
* **Aniq Fix Kodi:**
```javascript
window.open(url, '_blank', 'noopener,noreferrer');
```

---

### LOW (Kichik kamchiliklar)

#### [SEC-04] Referrer-Policy e'lon qilinmaganligi
* **Fayl va qator:** `index.html:head`
* **Muammo:** Tashqi havolalarga o'tganda to'liq URL (agar maxsus parametrlar bo'lsa) oshkor bo'lishi mumkin.
* **Aniq Fix Kodi:**
```html
<meta name="referrer" content="strict-origin-when-cross-origin">
```

---

## 3. Qo'llangan Tuzatishlar (Implemented Fixes)
1. `<head>` ga qat'iy Content Security Policy (CSP) va Referrer Policy qo'shildi.
2. Barcha `target="_blank"` bo'lgan 5 ta `<a>` tegiga `rel="noopener noreferrer"` qo'shildi.
3. JavaScript'dagi barcha `window.open` chaqiruvlariga `'noopener,noreferrer'` argumenti ulandi.
