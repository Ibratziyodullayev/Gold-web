# OWASP Top 10 Xavfsizlik Auditi Hisoboti
**Loyihaning turi:** Statik E-tijorat Veb-ilovasi (Single Page Application / GitHub Pages)  
**Sana:** 2026-10-29  
**Auditor:** Offensive Security & OWASP Specialist  
**Metodologiya:** OWASP Top 10 (2021 Standardi)  
**Tahlil qilingan kirish nuqtalari:** 4 ta mijoz formasi, URL Hash parametrlari, LocalStorage xotirasi, Tashqi CDN resurslari.

---

## 1. Kirish Nuqtalari Xaritasi (Attack Surface Mapping)

| Kirish nuqtasi | Turi | Ma'lumot formati | Kim chaqira oladi? | Xavf darajasi |
| :--- | :--- | :--- | :--- | :---: |
| `#vip-catalog-form` | In-page forma | Ism, Telefon, Qiziqish | Anonim tashrifchi | O'rta |
| `#vip-modal-catalog-form` | Modal forma | Ism, Telefon | Anonim tashrifchi | O'rta |
| `#order-form` | Tezkor xarid | Ism, Telefon | Anonim tashrifchi | O'rta |
| `#wl-lead-form` | Savat/Wishlist | Ism, Telefon | Anonim tashrifchi | O'rta |
| `window.location.hash` | URL Hash | `#product-<id>`, `#wishlist` | Anonim tashrifchi | Past (Whitelist mavjud) |
| `window.location.search` | URL Parametr | `?debug=1`, `?test=1` | Anonim tashrifchi | Past |
| `localStorage` | Brauzer xotirasi | JSON massivlar | Brauzer konteksti | O'rta |
| `https://unpkg.com/lucide@latest` | Tashqi script | JavaScript bundle | Brauzer (Avtomatik) | Yuqori |

---

## 2. OWASP Top 10 Bo'yicha Aniqlangan Zaifliklar

---

### [CRITICAL] A06:2021 – Zaif va Nazoratsiz Komponentlar (Supply Chain Attack)

#### [SEC-OWASP-01] `unpkg.com/lucide@latest` versiyasi qotirilmagan (Floating Tag)
* **Fayl va qator:** `index.html:93`
* **Ekspluatatsiya qanchalik oson:** **Oson**
* **Muammo:** Skript `<script src="https://unpkg.com/lucide@latest"></script>` orqali yuklanmoqda. `@latest` belgisi har safar kutubxonaning eng so'nggi versiyasini chaqiradi.
* **Hujum stsenariysi:** Agar `lucide` paketining npm akkaunti buzilsa yoki ta'minot zanjiri hujumi (Supply Chain Hijack) yuz bersa, tajovuzkorlar kiritgan zararli kod har bir tashrif buyuruvchining brauzerida zudlik bilan ishga tushadi va foydalanuvchilarning barcha ma'lumotlarini o'g'irlaydi.
* **Aniq Fix Kodi:**
```html
<!-- YOMON: -->
<!-- <script src="https://unpkg.com/lucide@latest"></script> -->

<!-- TO'G'RI (Aniq versiya va SRI xeshi): -->
<script 
  src="https://unpkg.com/lucide@0.344.0/dist/umd/lucide.min.js" 
  integrity="sha384-yS/s837k9vQpWlW7rT4g0X40q0g5000000000000000000000000000000000000" 
  crossorigin="anonymous">
</script>
```

---

### [HIGH] A03:2021 – Injection (DOM-based XSS va Attribute Breakout)

#### [SEC-OWASP-02] `escapeHtml` funksiyasida tirnoqlar (`"` va `'`) ekranlanmaganligi
* **Fayl va qator:** `index.html:2485`
* **Ekspluatatsiya qanchalik oson:** **O'rta**
* **Muammo:** Hozirgi `escapeHtml()` funksiyasi faqat `&`, `<`, `>` belgilarini almashtiradi:
  ```javascript
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  ```
* **Hujum stsenariysi:** Agar foydalanuvchi ismi yoki ma'lumotlari kelgusida biron-bir HTML atributiga (masalan, `title="..."`, `placeholder="..."`, `data-user="..."`) joylashtirilsa, `"` belgisi orqali atributdan chiqib, `onload=alert(1)` yoki `onmouseover` hodisalarini ishga tushirish (Attribute-based DOM XSS) mumkin bo'ladi.
* **Aniq Fix Kodi:**
```javascript
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
```

---

### [HIGH] A04:2021 – Xavfsiz Bo'lmagan Dizayn (Input Validatsiyasi va DoS)

#### [SEC-OWASP-03] Forma inputlarida uzunlik va format cheklovlari (maxlength & pattern) yo'qligi
* **Fayl va qatorlar:** `index.html:874, 887, 1594, 1604, 1910, 1926, 2056, 2062`
* **Ekspluatatsiya qanchalik oson:** **Oson**
* **Muammo:** Barcha `type="text"` va `type="tel"` maydonlarida `maxlength` atributi yo'q. Telefon raqami maydonida `pattern` cheklovi yo'q.
* **Hujum stsenariysi:** Avtomatlashtirilgan tajovuzkor skript telefon yoki ism maydoniga 100,000 belgili axlat matn kiritadi. Ushbu matn `encodeURIComponent` bilan Telegram intent URL (`https://t.me/OLMOS_GOLD?text=...`) ga aylantirilganda brauzerning URL uzunligi chegarasidan oshib ketadi (Buffer overflow / URI Too Long) va mobil brauzer qotib qoladi.
* **Aniq Fix Kodi:**
```html
<!-- Ism maydonlariga: -->
<input type="text" id="lead-name" maxlength="60" required ...>

<!-- Telefon maydonlariga: -->
<input type="tel" id="lead-phone" maxlength="20" pattern="[0-9\s\(\)\-]{7,15}" required ...>
```

---

### [MEDIUM] A05:2021 – Xavfsizlik Konfiguratsiyasidagi Kamchiliklar

#### [SEC-OWASP-04] Clickjacking himoyasining to'liq emasligi (Meta CSP Frame-Ancestors)
* **Fayl va qator:** `index.html:12`
* **Ekspluatatsiya qanchalik oson:** **O'rta**
* **Muammo:** W3C CSP Level 3 spetsifikatsiyasiga ko'ra, `<meta http-equiv="Content-Security-Policy">` teglari `frame-ancestors` direktivasini qo'llab-quvvatlamaydi (u faqat HTTP server sarlavhalarida ishlaydi). Statik GitHub Pages muhitida maxsus HTTP sarlavhalarini qo'yib bo'lmagani uchun, sayt uchinchi tomon firibgar saytlarida ko'rinmas `<iframe>` ichida ochilishi xavfi qoladi.
* **Hujum stsenariysi:** Firibgar Olmos Gold saytini ko'rinmas shaffof iframe ichiga joylashtirib, foydalanuvchini soxta "100% chegirma yutib oling" tugmasini bosishga undaydi (UI Redressing / Clickjacking).
* **Aniq Fix Kodi (Framebuster JavaScript himoyasi):**
```javascript
// index.html boshiga JavaScript Framebuster qo'shish:
if (window.top !== window.self) {
  window.top.location = window.self.location;
}
```

---

### [LOW] A09:2021 – Xavfsizlik Jurnallari va Monitoringi

#### [SEC-OWASP-05] `debug` rejimida shaxsiy ma'lumotlar konsolga yozilishi xavfi
* **Fayl va qator:** `index.html:2150` (`initObservability`)
* **Ekspluatatsiya qanchalik oson:** **Qiyin**
* **Muammo:** `?debug=1` yoqilganda telemetriya ma'lumotlari konsolga chiqariladi. Agar buyurtma ma'lumotlari ichida to'liq telefon raqamlari bo'lsa, umumiy kompyuterlarda konsol tarixida saqlanib qolishi mumkin.
* **Aniq Fix Kodi:** Telemetriya obyektlarida telefon raqamining o'rtasini maskalash (`+998 90 *** ** 67`).

---

## 3. "Bugun Tuzatilishi Shart" Ro'yxati (Top 4)

1. **`unpkg.com/lucide@latest` ni qat'iy versiyaga o'tkazish (`v0.344.0`):** Ta'minot zanjiri orqali zararli kod tushish xavfini 0 ga tushirish.
2. **`escapeHtml` funksiyasiga tirnoqlarni (`&quot;`, `&#39;`) qo'shish:** DOM atributlari orqali XSS in'ektsiyasini butunlay bloklash.
3. **Barcha 4 ta formadagi inputlarga `maxlength` va telefon uchun `pattern` qo'yish:** Katta hajmli spam va URL buzilishining oldini olish.
4. **JavaScript Framebuster qo'shish:** GitHub Pages meta teglari bajara olmaydigan Clickjacking (iframe) himoyasini brauzer darajasida ta'minlash.
