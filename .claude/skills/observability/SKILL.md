---
name: observability
description: Mijoz brauzeridagi xatoliklarni kuzatish (window.onerror), konversiya va foydalanuvchi harakatlarini loglash hamda telemetriyani tahlil qilishda ishlatiladi. Triggerlar: observability, telemetry, error_tracking, analytics, logging, monitor.
---

# Observability (Client-Side & Real User Monitoring)

## Qachon ishlatiladi
Foydalanuvchi qurilmasida yuz beradigan ko'rinmas JS xatoliklari, sindiruvchi istisnolar (unhandled promise rejections), 404 rasm xatolari va zargarlik xarid voronkasidagi (PDP -> Savat -> Telegram) konversiyalarni aniqlashda ishlatiladi.

## Checklist
1. **Global Xatoliklarni tutish (Global Error Catcher):** `window.addEventListener('error', ...)` va `window.addEventListener('unhandledrejection', ...)` orqali barcha JS xatolarining ro'yxatga olinishi.
2. **Buzilgan resurslar telemetriyasi:** Yuklanmay qolgan rasmlar, fontlar yoki skriptlar haqida konsolga va tahlil tizimiga xabar jo'natish.
3. **Konversiya hodisalari:** Muhim tugmalar bosilganda (`Telegram Konsyerj`, `Savatga qo'shish`, `Valyuta o'zgarishi`) maxsus telemetriya loglari (`console.info` yoki analitika piksellari) yozilishi.
4. **Debug rejimi:** Ishlab chiquvchi yoki admin uchun URL da `?debug=1` bo'lganda batafsil diagnostika paneli ko'rinishi.
5. **Core Web Vitals monitoringi:** `PerformanceObserver` orqali real foydalanuvchi LCP va CLS ko'rsatkichlarini kuzatish.
6. **Mijoz qurilmasi konteksti:** Xato yuz berganda brauzer turi, ekran o'lchami va internet tezligi ma'lumotlarini qayd etish.
7. **Shaxsiy ma'lumotlar xavfsizligi:** Loglarda mijozning maxfiy telefon raqamlari yoki manzillari ochiq saqlanmasligi (maskalash).

## Anti-patterns
- **Xatoliklarni jimgina yutib yuborish:** `catch (e) {}` (bo'sh catch bloki) tufayli tugma bosilganda hech narsa bo'lmasligi va sababi noma'lum qolishi.
- **Konsolni yuzlab `console.log` bilan to'ldirish:** Ishlab chiqarishda oddiy foydalanuvchiga keraksiz axlat chiqarish.
- **Cheksiz xato tsikli (Error loop):** Xato yuz berganda xato jo'natuvchi funksiyaning o'zi yangi xato chiqarishi.

## Fix recipes

### 1. Ishonchli Global Telemetriya va Xatolik Kuzatuvchisi
```javascript
(function initObservability() {
  const isDebug = new URLSearchParams(window.location.search).has('debug') || localStorage.getItem('olmos_debug') === '1';

  window.addEventListener('error', function(event) {
    const errorPayload = {
      type: 'JS_ERROR',
      message: event.message,
      filename: event.filename,
      lineno: event.lineno,
      time: new Date().toISOString(),
      viewport: `${window.innerWidth}x${window.innerHeight}`
    };
    if (isDebug) {
      console.error('[Olmos Telemetry Error]', errorPayload);
    }
  });

  window.addEventListener('unhandledrejection', function(event) {
    if (isDebug) {
      console.warn('[Olmos Telemetry Unhandled Promise]', event.reason);
    }
  });
})();
```

### 2. Xarid Voronkasi Hodisalarini Loglash
```javascript
function trackEvent(eventName, eventData = {}) {
  const payload = {
    event: eventName,
    data: eventData,
    timestamp: Date.now()
  };
  // Agar Google Analytics (gtag) yoki Meta Pixel mavjud bo'lsa uzatadi
  if (typeof window.gtag === 'function') {
    window.gtag('event', eventName, eventData);
  }
  // Maxsus ichki log
  console.debug(`[Event: ${eventName}]`, payload);
}
```

## Tekshirish buyruqlari
```bash
# 1. Kodda console.log, warn, error qayerlarda ishlatilganini ko'rish
grep -n "console\." index.html | wc -l

# 2. Global error handler mavjudligini tekshirish
grep -n "window.onerror" index.html
grep -n "unhandledrejection" index.html
```
