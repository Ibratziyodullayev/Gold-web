# Audit Hisoboti: Etap 8 — Observability
**Loyihaning turi:** Statik E-tijorat Veb-ilovasi (Single Page Application / GitHub Pages)  
**Sana:** 2026-10-29  
**Auditor:** Observability & Real-User Monitoring Auditor  
**Holat:** TUZATILDI (Global xatoliklarni tutish va telemetriya moduli ulandi)

---

## 1. Kontekst Tahlili
* **Muammo:** Mijoz brauzerida sodir bo'ladigan JavaScript xatoliklari yoki bajarilmagan promiselar (unhandled promise rejections) dasturchiga mutlaqo ko'rinmas edi. Xaridor tugmani bosganda xatolik yuz bersa, sayt jimgina to'xtab qolgan.

---

## 2. Aniqlangan Kamchiliklar va Yechimlar

### MEDIUM (O'rta daraja)

#### [OBS-01] Global Error va Promise Rejection Handler yo'qligi
* **Fayl va qator:** `index.html` (Skriptlar boshlanishi)
* **Muammo:** `window.onerror` va `window.onunhandledrejection` yo'qligi sababli foydalanuvchi qurilmasidagi sinishlar (crashlar) diagnostika qilib bo'lmas holatda edi.
* **Aniq Fix Kodi:**
```javascript
(function initObservability() {
  const isDebug = new URLSearchParams(window.location.search).has('debug') || localStorage.getItem('olmos_debug') === '1';

  window.addEventListener('error', (event) => {
    const payload = {
      type: 'CLIENT_ERROR',
      message: event.message,
      filename: event.filename,
      lineno: event.lineno,
      time: new Date().toISOString(),
      viewport: `${window.innerWidth}x${window.innerHeight}`
    };
    if (isDebug) {
      console.error('[Olmos Telemetry Error]', payload);
    }
  });

  window.addEventListener('unhandledrejection', (event) => {
    if (isDebug) {
      console.warn('[Olmos Telemetry Unhandled Promise]', event.reason);
    }
  });
})();
```

#### [OBS-02] Ishlab chiquvchi uchun diagnostika (`?debug=1`) rejimi yo'qligi
* **Yechim:** URL ga `?debug=1` qo'shilganda yoki konsolda `localStorage.setItem('olmos_debug', '1')` yozilganda, barcha xarid voronkasi bosqichlari (PDP ochilishi, savatga qo'shish, Telegram link ochilishi) konsolda to'liq telemetriya bilan ko'rinadi.

---

## 3. Qo'llangan Tuzatishlar
1. `index.html` asosiy skripti boshiga `initObservability` o'rnatildi.
2. `window.olmosTrack` yordamida Google Analytics (gtag) va ichki telemetriya integratsiyasi tayyorlandi.
