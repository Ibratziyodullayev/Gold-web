# Audit Hisoboti: Etap 2 — Tashqi API Integratsiyalari, Webhook va Idempotentlik
**Loyihaning turi:** Statik E-tijorat Veb-ilovasi (Single Page Application / GitHub Pages)  
**Sana:** 2026-10-29  
**Auditor:** External API & Webhook Hardening Specialist  
**Fokus:** Tashqi chaqiruvlar, buyurtma oqimlari, chidamlilik va idempotentlik

---

## 1. Kontekst Tahlili: Tashqi Integratsiyalar Xaritasi

Loyiha serverless statik muhitda bo'lgani sababli barcha tashqi integratsiyalar **mijoz brauzeri (Client-side)** orqali amalga oshiriladi:

| Integratsiya | Turi | Maqsadi | Oqim | Sinxron / Queue |
| :--- | :--- | :--- | :--- | :--- |
| **Telegram Direct Intent** (`t.me`) | Deep Link Intent | Buyurtma va konsyerj so'rovlari | **PUL / BUYURTMA** | Sinxron (OS Intent) |
| **Secure Lead Webhook** (`fetch`) | HTTP POST JSON | Buyurtma telemetriyasini uzatish | **HOLAT O'ZGARIShI** | Sinxron (Client Fetch) |
| **Google Maps Embed** | iframe | Butik lokatsiyasini ko'rsatish | Informatsion | Asinxron (Iframe) |
| **Yandex Maps Embed** | iframe | Butik lokatsiyasini ko'rsatish | Informatsion | Asinxron (Iframe) |
| **CDN Scripts & Fonts** | HTTP GET | Stil, shrift va piktogrammalar | Resurs yuklash | Asinxron (Static CDN) |

> **MUHIM:** Saytda **kiruvchi webhook qabul qiluvchi endpointlar mavjud emas**, chunki GitHub Pages faqat statik fayllarga xizmat ko'rsatadi. To'lov tizimlari (Payme, Click, Stripe) webhooklarini qabul qilish uchun kelajakda serverless backend (Cloudflare Workers / AWS Lambda) talab etiladi.

---

## 2. Pul va Buyurtma Bilan Bog'liq Oqimlar Tahlili

Saytda 3 ta asosiy buyurtma oqimi mavjud:
1. **Marquise 18K Diamond Ring PDP Customizer:** Metall turi, karat va uzuk o'lchami tanlanib, to'g'ridan-to'g'ri Telegram konsyerjiga uzatiladi ($673+).
2. **Wishlist / Sevimlilar Savati:** Bir nechta qimmatbaho buyumlar yig'ilib, jami hisoblangan summa bilan adminga yuboriladi.
3. **VIP Lookbook & Fitting Request:** Butikda kiyib ko'rish yoki yangi katalog so'rovi.

### Ushbu oqimlardagi asosiy zaifliklar:
* **Idempotentlik yo'qligi:** Foydalanuvchi "Buyurtma berish" tugmasini tez-tez 2 marta bossa, ikkita alohida Telegram chati ochiladi va adminga ikkita bir xil so'rov boradi.
* **Client-side Timeout yo'qligi:** `fetch(SECURE_WEBHOOK_URL)` chaqiruvida `AbortController` o'rnatilmagan. Agar server sekin javob bersa yoki javob bermasa, ulanish uzoq vaqt osilib turadi.

---

## 3. Integratsiyalar Chidamlilik Jadvali

| Integratsiya | Timeout | Retry | Idempotent | Circuit Breaker | Dedup | Baho |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Telegram Intent (`t.me`)** | N/A (OS) | Yo'q | Yo'q (Double-click xavfi) | Graceful Fallback | Yo'q | **B+** |
| **Lead Webhook (`fetch`)** | ❌ Yo'q (Cheksiz) | ❌ Yo'q | ❌ Yo'q (Idempotency-Key yo'q) | ⚠️ Qisman (try/catch) | ❌ Yo'q | **C** |
| **Google Maps Embed** | ❌ Brauzer def | ❌ Yo'q | N/A (Read-only) | ✅ Provider Switcher | N/A | **A-** |
| **Yandex Maps Embed** | ❌ Brauzer def | ❌ Yo'q | N/A (Read-only) | ✅ Provider Switcher | N/A | **A-** |
| **CDN (Lucide, Fonts)** | ❌ Brauzer def | ❌ Yo'q | N/A (Read-only) | ⚠️ Xatolikda fallback yo'q | N/A | **B** |

---

## 4. "Nima Bo'lsa Nima Bo'ladi" Matritsasi

| Hodisa | Telegram Intent (`t.me`) | Lead Webhook (`fetch`) | Xarita (Google / Yandex) | Tizimning Yakuniy Holati |
| :--- | :--- | :--- | :--- | :--- |
| **API Sekin (High Latency)** | Ta'sir qilmaydi (Brauzer darhol Telegram ilovasiga uzatadi) | So'rov 30-60 soniya osilib qoladi, xotirani band qiladi | Xarita bloki oq bo'lib turadi | Sayt ishlaydi, ammo webhook sekinligi fon resurslarini ushlab turadi |
| **API 500 (Server Error)** | Telegram 500 bermaydi (Mijoz app ochiladi) | `try/catch` xatoni ushlaydi, ammo operatorga buyurtma yetmaydi | Iframe xato beradi; foydalanuvchi "Google / Yandex" almashtirish tugmasini bosishi mumkin | Foydalanuvchi Telegram chatiga o'tib buyurtmani qo'lda tasdiqlay oladi |
| **API Butunlay O'lgan (DNS / Offline)** | Saytda "Internet uzildi" toasti chiqadi | So'rov rad etiladi (`TypeError: Failed to fetch`), `catch` ga tushadi | Xarita o'rniga matnli manzil va telefon ko'rsatiladi | Xarid jarayoni to'xtamaydi (Telefon va Telegram zaxirasi bor) |
| **Dublikat So'rov (Double-Click)** | 2 ta Telegram chati va 2 ta xabar ochiladi | Ikkita dublikat lead yuboriladi | Ta'sir qilmaydi | Operator ikkita bir xil so'rov oladi, adashish xavfi bor |

---

## 5. Aniq Kamchiliklar va Tavsiya Etiladigan Fix Retseptlari

### [API-01] Lead Webhook chaqiruvida Timeout (AbortController) va Idempotency-Key yo'qligi
* **Fayl va qator:** `index.html:2573` (`sendTelegramLeadNotification`)
* **Muammo:** `await fetch(SECURE_WEBHOOK_URL, ...)` so'rovi hech qanday timeoutsiz ishga tushadi. Agar server qotib qolsa, funksiya tugamaydi. Shuningdek, `Idempotency-Key` yuborilmaydi.
* **Aniq Fix Kodi:**
```javascript
async function sendTelegramLeadNotification(messageHtml) {
  if (SECURE_WEBHOOK_URL) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000); // 8 soniya qat'iy timeout
    const idempotencyKey = 'lead_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);

    try {
      await fetch(SECURE_WEBHOOK_URL, {
        method: "POST",
        signal: controller.signal,
        headers: { 
          "Content-Type": "application/json",
          "Idempotency-Key": idempotencyKey
        },
        body: JSON.stringify({ 
          text: messageHtml,
          idempotency_key: idempotencyKey,
          timestamp: new Date().toISOString()
        })
      });
    } catch (err) {
      if (err.name === 'AbortError') {
        console.warn("[Lead Dispatch] So'rov vaqti tugadi (Timeout: 8s)");
      } else {
        console.debug("[Lead Dispatch] Webhook xatosi:", err);
      }
    } finally {
      clearTimeout(timeoutId);
    }
  }
  console.info("[Olmos Gold] Buyurtma konsyerjga yo'naltirildi.");
  return true;
}
```

### [API-02] Forma tugmalarida Double-Submission (Dublikat buyurtma) himoyasi
* **Fayl va qatorlar:** Barcha forma yuborish funksiyalari (`handleVipFormSubmit`, `handleModalCatalogSubmit`, `handleWishlistLeadSubmit`)
* **Muammo:** Tugma bosilganda darhol bloklanmasa (debounce), foydalanuvchi bir necha bor bosishi natijasida bir nechta so'rov generatsiya bo'ladi.
* **Aniq Fix Kodi:**
```javascript
let isSubmitting = false;

function safeSubmitHandler(formSubmitFn) {
  return async function(e) {
    e.preventDefault();
    if (isSubmitting) return;
    isSubmitting = true;
    try {
      await formSubmitFn(e);
    } finally {
      setTimeout(() => { isSubmitting = false; }, 3000); // 3 soniyalik blokirovka
    }
  };
}
```

---

## 6. Kelajakdagi To'lov Tizimlari Uchun Tavsiyalar (Payme / Click / Stripe)

Agar saytga kelgusida to'lov tizimlari ulanishi rejalashtirilsa:
1. **Serverless Backend (Cloudflare Worker / AWS Lambda):** GitHub Pages orqali webhook qabul qilib bo'lmaydi. Webhooklar alohida serverless endpointga yo'naltirilishi kerak.
2. **HMAC Signature tekshiruvi:** Har bir kiruvchi to'lov xabarida `X-Signature` sarlavhasi do'kon maxfiy kaliti orqali tekshirilishi shart.
3. **Idempotency va Dedup Table:** DB da `transaction_id` bo'yicha unikal indeks bo'lishi va bir xil tranzaksiya qayta ishlashga tushmasligi kerak.
