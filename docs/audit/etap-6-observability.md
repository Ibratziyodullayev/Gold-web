# Audit Hisoboti: Etap 6 — Monitoring, Telemetriya va Biznes Analitika
**Loyihaning turi:** Statik E-tijorat Veb-ilovasi (Single Page Application / GitHub Pages)  
**Sana:** 2026-10-29  
**Auditor:** Observability, Telemetry & SRE Specialist  
**Fokus:** Loglar gigiyenasi, Real User Monitoring (RUM), Konversiya voronkasi va ogohlantirishlar (Alerting)

---

## 1. Kontekst Tahlili

* **Mavjud Logging:** Kod ichida `window.addEventListener('error')` moduli mavjud, biroq u faqat `?debug=1` bo'lgandagina brauzer konsoliga chiqaradi. Ishlab chiqarishda (oddiy xaridorda) yuz beradigan nosozliklar serverga yetib bormaydi va tab yopilishi bilan yo'qoladi.
* **Monitoring va Alerting:** Tashqi uptime monitoring tizimi mavjud emas. Agar GitHub Pages CDN uzilsa, hech kimga avtomatik SMS/Telegram xabar bormaydi.
* **Biznes Analytics:** `window.olmosTrack()` funksiyasi e'lon qilingan, biroq asosiy tugmalarda (Savat, Customizer, Buyurtma) chaqirilmagan. Qaysi zargarlik buyumi eng ko'p ko'rilayotgani va xaridor qaysi bosqichda chiqib ketayotgani noma'lum.

---

## 2. 19 Ta Tekshiruv Savoliga Aniq Tahlil

### --- Logging ---
1. **Strukturalangan loglar:** JSON formatida (`type`, `message`, `filename`, `lineno`, `viewport`, `time`).
2. **Trace ID:** Har bir xarid so'roviga `Idempotency-Key` / Trace ID biriktirilgan.
3. **Log darajalari:** `console.error`, `console.warn`, `console.info` to'g'ri ajratilgan.
4. **Logda maxfiy ma'lumotlar:** Telefon raqamlari va shaxsiy ma'lumotlar ochiq loglanmaydi.
5. **Loglarni saqlash joyi:** **YO'Q (Kritik bo'shliq).** Mijoz konsolidagi loglar sessiya tugashi bilan o'chib ketadi.
6. **Log hajmi va rotatsiya:** Mijoz xotirasini to'ldirmasligi uchun faqat in-memory saqlanadi.

### --- Monitoring ---
7. **Error Tracking (Sentry va h.k.):** **YO'Q.** Brauzerdagi xatolar markaziy serverga yuborilmaydi.
8. **Uptime Monitoring:** **YO'Q.** Tashqi ping/health-check o'rnatilmagan.
9. **Asosiy Metrikalar:** GitHub Pages orqasida bo'lgani sababli CPU/RAM server darajasida ko'rinmaydi; RUM (Real User Monitoring) Core Web Vitals (LCP, CLS, FID) o'lchanmayapti.
10. **Alerting:** **YO'Q.** Do'kon egasiga nosozlik haqida tezkor xabar beruvchi bot yo'q.
11. **Alert shovqini:** Alertlar yo'qligi sababli shovqin ham yo'q.
12. **SLO / SLI:** Aniqlanmagan. "Sayt ishlayapti" — LCP < 2.0s, Uptime > 99.9%, Telegram xarid havolasi 100% ochilishi bo'lishi kerak.
13. **Tashqi API holati:** Telegram va xaritalar holati passiv kuzatiladi.
14. **Background joblar:** Yo'q.

### --- Analytics ---
15. **Biznes eventlari:** `olmosTrack` mavjud bo'lsada, tugmalarga ulanmagan.
16. **Funnel (Voronka):** Qidiruv -> PDP -> Customizer (Karat/Metall) -> Telegram o'tish bosqichlari ajratilmagan.
17. **Analytics performance ta'siri:** Hozircha og'ir uchinchi tomon skriptlari yo'q (yengil).
18. **Maxfiylik (Privacy):** Shaxsiy bank kartalari so'ralmaydi, faqat ixtiyoriy telefon raqami olinadi.
19. **Dashboard:** Analitika paneli yo'q.

---

## 3. "Ko'r Nuqtalar" (Blind Spots) Ro'yxati
> *"Nimani o'lchamasak, nima bo'layotganini bilmaymiz."*

1. **Safari/iOS Maxsus Brauzer Xatolari:** Agar eskiroq iPhone yoki Safari 15 da yangi CSS/JS xususiyati sababli "Buyurtma berish" tugmasi bosilmay qolsa — dasturchi buni bilmaydi, xaridor jim ketadi (Yo'qotilgan daromad: har bir uzuk uchun $673+).
2. **Telegram Bloklanishi / Deep Link nosozligi:** Agar foydalanuvchida Telegram o'rnatilmagan bo'lsa yoki provayder bloklasa — xaridor xatolik xabarisiz qoladi.
3. **Katalog Voronkasida Uzilish (Funnel Drop-off):** Nechta mijoz narxni ko'rib chiqib ketdi, nechta kishi uzuk o'lchamini bilolmay savatni tashlab ketdi — ko'rinmaydi.
4. **Rasmlar 404 Xatosi:** Unsplash yoki tashqi rasm o'chib ketsa, nechta foydalanuvchi singan rasmni ko'rgani noma'lum.
5. **CDN Uptime Uzilishi:** GitHub Pages tunda 15 daqiqa uzilsa, do'kon rahbariyati bundan bexabar qoladi.

---

## 4. Minimal Monitoring To'plami (Minimal Effort, Maximum Coverage)
*Eng kam mehnat bilan eng ko'p natija beradigan 4 qadam:*

1. **Tashqi Uptime Monitoring (0$):**
   * *SaaS:* **UptimeRobot** (5 daqiqalik bepul tekshiruv) yoki **BetterStack**.
   * *Self-hosted muqobil:* **Uptime Kuma** (bepul, o'z serverida yoki Docker'da).
   * Tekshiriladigan URL: `https://ibratziyodullayev.github.io/Gold-web/`
2. **Client-side Error Telemetry Beacon (0$):**
   * *SaaS:* **GlitchTip** (Sentry protokoliga mos, bepul/arzon) yoki **Sentry Free Tier** (oyiga 5,000 ta xato bepul).
   * *Yengil muqobil:* Xatolar yuz berganda `navigator.sendBeacon()` orqali xavfsiz Telegram Admin chatiga yoki Webhookka avtomatik yuborish.
3. **Google Analytics 4 / PostHog hodisalarini yoqish:**
   * Voronka hodisalari: `pdp_view`, `customizer_change`, `add_to_wishlist`, `telegram_checkout`.
   * *Self-hosted muqobil:* **Umami Analytics** yoki **PostHog Open Source** (to'liq maxfiy, cookie-free).
4. **Telegram Instant Alerting Bot:**
   * Sayt ishlamay qolganda yoki kritik xato yuz berganda do'kon administratorining Telegramiga xabar borishi.

---

## 5. Tavsiya Etilgan Alertlar Jadvali

| Metrika / Hodisa | Threshold (Chegara qiymat) | Xabar Kanali | Kim javobgar? |
| :--- | :--- | :--- | :--- |
| **Sayt Uptime (HTTP Status)** | != 200 yoki javob vaqti > 3.0s (3 marta ketma-ket) | Telegram Bot + SMS | DevOps / Sayt ma'muri |
| **Client JS Error Spike** | 10 daqiqa ichida > 15 ta JS xatosi | Telegram Guruh | Frontend dasturchi |
| **Telegram Checkout Click** | Konversiya hodisasi (Har bir bosilishda) | Ichki Analitika | Savdo menejeri |
| **Resurs Yuklanish Xatosi (404 rasm/skript)** | Kuniga > 5 ta singan rasm hodisasi | Email / Dashboard | Kontent menejer |
| **Core Web Vitals (LCP)** | p75 LCP > 2.5 soniya | Haftalik hisobot | Frontend arxitektor |

---

## 6. Voronka Hodisalarini Kod Darajasida Bog'lash Rejasi

`window.olmosTrack` funksiyasini quyidagi 4 ta kritik nuqtaga ulash:
```javascript
// 1. Mahsulot ochilganda:
olmosTrack('view_item', { id: product.id, price: product.base_price_usd });

// 2. Sevimlilarga qo'shilganda:
olmosTrack('add_to_wishlist', { id: product.id });

// 3. Telegram orqali xarid bosilganda:
olmosTrack('begin_checkout', { id: product.id, price: product.base_price_usd, metal: selectedMetal });

// 4. VIP Katalog yoki Forma to'ldirilganda:
olmosTrack('lead_generated', { form: 'vip_lookbook' });
```
