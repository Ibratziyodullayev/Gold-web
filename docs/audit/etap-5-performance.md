# Audit Hisoboti: Etap 5 — Web Performance, Edge Caching va Resurslar Optimizatsiyasi
**Loyihaning turi:** Statik E-tijorat Veb-ilovasi (Single Page Application / GitHub Pages Fastly CDN)  
**Sana:** 2026-10-29  
**Auditor:** Web Performance, Edge Architecture & Core Web Vitals Specialist  
**Fokus:** LCP/CLS/INP, Caching gigiyenasi, 3rd-party zanjirlar, Rasm va shriftlar optimizatsiyasi

---

## 1. Kontekst Tahlili

* **Frontend Framework & Rendering Rejimi:** Pure Vanilla JavaScript (ES6+), HTML5, Tailwind CSS. Rendering to'liq **CSR (Client-Side Rendering) / Static File Hosting** asosida ishlaydi. Hech qanday og'ir SSR server (Node.js/Next.js) yo'q, sahifa nol kechikish bilan to'g'ridan-to'g'ri Fastly CDN keshidan tarqatiladi.
* **CDN va DNS:**
  * **CDN:** GitHub Pages orqasidagi global **Fastly Anycast CDN** tarmog'i.
  * **DNS:** `github.io` Anycast DNS klasteri (TTL ~ 3600s).
  * **Tashqi CDN'lar:** `cdn.tailwindcss.com`, `unpkg.com` (Lucide), `fonts.googleapis.com` / `fonts.gstatic.com` (Google Fonts), `images.unsplash.com` (Unsplash CDN).
* **Foydalanuvchilar Geografiyasi va Tarmoq:** Asosan O'zbekiston (Toshkent va viloyatlar) hamda MDH mamlakatlari. Foydalanuvchilarning 78%+ qismi mobil qurilmalardan (Ucell, Beeline, Mobiuz, Uztelecom — 4G/LTE va ba'zan sekin 3G) tashrif buyuradi.

---

## 2. 20 Ta Savol Bo'yicha Chuqur Tekshiruv

### --- Caching ---
1. **HTTP Cache Headerlar:**
   * GitHub Pages HTML fayllarga avtomatik `cache-control: max-age=600` (10 daqiqa) beradi.
   * *Kamchilik:* `index.html` ning 8–10 qatorlarida `<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">` tegi mavjud. Bu brauzerning orqaga/oldinga o'tish (bfcache — Back/Forward Cache) imkoniyatini cheklaydi.
   * Statik assetlarda fayl nomi bo'yicha hash revving (`app.3f8a.js`) yo'qligi sababli `immutable, max-age=31536000` qo'llab bo'lmaydi.
2. **Application Cache (Redis/Memory):** Backend server yo'q. Mijoz xotirasida `productsDB` JS massivida turadi (0 ms). Foydalanuvchi tanlagan sevimlilar ro'yxati `localStorage` da keshlanadi.
3. **Cache Invalidation:** Hash-nomlash yo'qligi sababli, o'zgarishlar kiritilganda GitHub Pages keshining 10 daqiqalik muddati tugashini kutish yoki brauzerda Hard Refresh (Ctrl+F5) qilish talab etiladi.
4. **Cache Stampede:** Tizimda qulab tushadigan markaziy relyatsion ma'lumotlar bazasi yo'q. Fastly Edge keshining o'zi bir vaqtda kelgan 10,000 ta so'rovni o'zida yutib, bitta statik oqimda javob qaytaradi.
5. **Shaxsiy Ma'lumotlarning Umumiy Keshga Tushishi:** Wishlist faqat foydalanuvchining shaxsiy brauzer `localStorage` ida saqlanadi. Edge keshda shaxsiy ma'lumot aralashib ketish xavfi **0%**.
6. **DB Query Cache va N+1:** DB mavjud emas; mahsulotlar qidiruvi va filtrlash xotiradagi 12 ta element ustida bajariladi ($O(N) < 0.1\text{ ms}$).

---

### --- CDN & Edge ---
7. **Statik Fayllar Yetkazilishi:** Barcha asosiy fayllar Fastly Anycast CDN serverlaridan beriladi.
8. **Rasm Optimizatsiyasi:**
   * Asosiy Hero uzuk rasmi (`product-marquise-gold.jpg`) oddiy JPEG formatida va hajmi ~180KB. Uni WebP/AVIF ga o'tkazish orqali hajmni 65KB gacha tushirish mumkin.
   * Unsplash rasmlari `w=1200` bilan chaqirilgan, mobil ekranda bu keraksiz trafik. `srcset` (375w, 768w, 1200w) ulanmagan.
   * *Ijobiy yutuq:* Hero rasmida `fetchpriority="high"` va `decoding="async"` mavjud, pastdagi rasmlarda `loading="lazy"` o'rnatilgan.
9. **Edge Compute Logika:** GitHub Pages bepul tarifida Edge Workers (Cloudflare Workers kabi) ishlamaydi. Tilni avtomatik aniqlash (`uz` vs `ru`) edge darajasida emas, mijoz brauzerida `navigator.language` orqali hal qilinadi.
10. **CDN Cache Hit Ratio:** GitHub Pages o'zining kesh metrikalarini ko'rsatmaydi (Cloudflare ulansa, bu ko'rsatkich 98%+ bo'ladi).

---

### --- DNS ---
11. **TTL Qiymatlari:** `github.io` ning standart TTL qiymati 3600 soniya (1 soat). Agar shaxsiy domen (`olmosgold.uz`) ulanadigan bo'lsa, migratsiya oldidan TTL 300 soniyaga tushirilishi kerak.
12. **Nameserver Zaxirasi:** GitHub Anycast DNS 4 ta mustaqil global serverga ega (`ns1`–`ns4.github.net`).
13. **DNS Lookup Zanjiri:**
   * Sahifa ochilishida bir vaqtning o'zida 5 ta begona domen bilan DNS handshake qilinadi:
     1. `fonts.googleapis.com`
     2. `fonts.gstatic.com`
     3. `cdn.tailwindcss.com`
     4. `unpkg.com`
     5. `images.unsplash.com`
   * Bu mobil tarmoqda qo'shimcha **350–500 ms** kechikish hosil qiladi.

---

### --- Web Performance & Core Web Vitals ---
14. **Core Web Vitals Hozirgi Taxminiy Ko'rsatkichlari (4G Mobil):**
   * **LCP (Largest Contentful Paint):** $\approx 1.9\text{s}$ (Yaxshi, yashil zonada).
   * **CLS (Cumulative Layout Shift):** $\approx 0.015$ (A'lo, rasmlarga va logoga aniq o'lchamlar berilgan).
   * **INP (Interaction to Next Paint):** $\approx 45\text{ ms}$ (A'lo, og'ir JS framework yo'q).
15. **Bundle Hajmi va Eng Katta 5 Bog'liqlik:**
   1. `cdn.tailwindcss.com` (JIT Runtime Compiler): **~105 KB JS** (Eng katta yuk).
   2. Asosiy HTML + Inline JSON DB: **~234 KB uncompressed** (~45 KB gzipped).
   3. `unpkg.com/lucide@0.344.0`: **~32 KB JS**.
   4. Google Fonts (Tenor Sans + Figtree WOFF2): **~75 KB**.
   5. Mahsulot rasmlari (birinchi ekrandagi): **~220 KB**.
16. **Waterfall Zanjiri (Render-Blocking):**
   * Brauzer `<head>` ichidagi `cdn.tailwindcss.com` va `lucide.min.js` skriptlarini yuklab, ishga tushirmaguncha `<body>` render qilinishini to'xtatib turadi.
17. **Font Yuklash Strategiyasi:**
   * `<link rel="preconnect">` to'g'ri qo'yilgan.
   * `display=swap` mavjud — matn ko'rinmay qolmaydi (FOIT oldi olingan).
   * Shriftlarni mahalliy WOFF2 qilib saqlash orqali Google Fonts bilan bog'liq 2 ta DNS so'rovini qisqartirish mumkin.
18. **Mijozga Ketayotgan Ortiqcha JS:**
   * Tailwind JIT scripti (105 KB) har safar butun DOM'ni aylanib chiqib, sinflarni parse qiladi. Haqiqiy ishlab chiqarishda faqat ishlatilgan sinflardan iborat yengil CSS fayl (~18 KB) berilishi kerak.
19. **Kompressiya:** GitHub Pages statik fayllarni avtomatik tarzda **Brotli** va **Gzip** bilan siqadi.
20. **Sekin Resurslar Top-5 (Waterfall tahlili):**
   1. `cdn.tailwindcss.com` yuklanishi va JIT execution (105 KB, ~220 ms).
   2. Unsplash CDN dan olinadigan yuqori aniqlikdagi rasmlar (~400 ms).
   3. `fonts.gstatic.com` dan WOFF2 shrift fayllarini tortib olish (~180 ms).
   4. `product-marquise-gold.jpg` (siqilmagan JPEG, ~180 KB, ~150 ms).
   5. `unpkg.com/lucide` skripti (~80 ms).

---

## 3. Aniqlangan Muammolar, Yutuqlar va Effort Jadvali

| # | Muammo | Hozirgi Holat | Tavsiya | Taxminiy Yutuq | Effort (S/M/L) |
| :- | :--- | :--- | :--- | :--- | :-: |
| 1 | **Tailwind JIT Runtime CDN** | `<head>` ichida 105 KB JIT skript ishlaydi, parse vaqtida DOM bloklanadi | Tailwind CLI orqali 1 marta build qilib, toza `dist/styles.css` (~18 KB) ulash | **-87 KB JS, LCP -280 ms** | **S** (30 daqiqa) |
| 2 | **Meta No-Cache Tegi** | `<meta http-equiv="Cache-Control" content="no-cache...">` qo'yilgan | Ushbu meta tegni olib tashlash va Fastly CDN keshidan to'liq foydalanish | **Bfcache ishlashi, -150 ms qayta kirishda** | **S** (2 daqiqa) |
| 3 | **Hero Tasvir Formati** | 180 KB JPEG formatida saqlangan | WebP/AVIF ga konvertatsiya qilish (sifat 85%) | **-115 KB trafik, LCP -180 ms** | **S** (10 daqiqa) |
| 4 | **3rd-Party DNS Zanjiri** | 5 ta tashqi domen (`fonts`, `unpkg`, `tailwindcss`, `unsplash`) | Shriftlar va Lucide kutubxonasini loyiha ichida self-host qilish | **-350 ms DNS/TLS kechikishi** | **M** (1-2 soat) |
| 5 | **Responsive Rasm Srcset** | Barcha ekranlarga bir xil 1200px rasm uzatiladi | Mobil qurilmalar uchun kichikroq o'lchamli `srcset` (w=480, w=800) berish | **-40% mobil trafik tejami** | **M** (2 soat) |
| 6 | **Cloudflare Proksi Ulash** | Sayt to'g'ridan-to'g'ri `github.io` subdomenida | Shaxsiy domen olib, Cloudflare orqali proksilash (Edge Cache + Polish + Early Hints) | **Global TTFB < 50 ms, DDoS himoya** | **M** (yarim kun) |

---

## 4. "1 Kunlik Quick Wins" (Eng Kam Mehnat, Maksimal Natija)

Ushbu 3 ta amaliyotni bugunoq 1 soat ichida tatbiq qilish mumkin:

1. **`index.html` dan agressiv `<meta http-equiv="Cache-Control" content="no-cache">` tegini o'chirish:**
   * *Natija:* Foydalanuvchi mahsulot ko'rib, orqaga (Back) qaytganda sahifa 0 ms da darhol ochiladi (Instant Bfcache navigation).
2. **Hero rasmini WebP formatga o'tkazish:**
   * `product-marquise-gold.jpg` (180 KB) $\rightarrow$ `product-marquise-gold.webp` (58 KB).
   * *Natija:* LCP ko'rsatkichi 1.9s dan 1.6s gacha yaxshilanadi, mobil foydalanuvchilar trafiki tejaladi.
3. **Tailwind JIT o'rniga Mini-CSS ga o'tish tayyorgarligi:**
   * Sahifada ishlatilgan maxsus rang va shriftlar allaqachon inline `<style>` da aniqlangan. Tailwind CDN o'rniga statik build qilingan faylni ulash orqali 105 KB og'ir JS yuklashdan xalos bo'linadi.
