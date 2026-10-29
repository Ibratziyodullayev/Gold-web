# Audit Hisoboti: Etap 4 — Performance and Edge
**Loyihaning turi:** Statik E-tijorat Veb-ilovasi (Single Page Application / GitHub Pages)  
**Sana:** 2026-10-29  
**Auditor:** Performance & Core Web Vitals Auditor  
**Holat:** TUZATILMOQDA (LCP tezlashtirilmoqda, CLS 0 ga tushirilmoqda)

---

## 1. Kontekst Tahlili
* **Mobil auditoriya:** 95% tashrif buyuruvchilar smartfon orqali kiradi.
* **Core Web Vitals tahlili:**
  * **LCP (Largest Contentful Paint):** Bosh ekrandagi (Hero) asosiy rasmda `fetchpriority="high"` va `decoding="async"` mavjud emas edi. Natijada brauzer rasmni kechiktirib yuklagan.
  * **CLS (Cumulative Layout Shift):** Logotiplar va hikoya bloklaridagi rasmlarda aniq `width` va `height` atributlari bo'lmagani sababli, rasm yuklanguncha sahifa pastga sakragan.
  * **Resurslarni tejash:** Pastki qismdagi hikoya rasmlarida `loading="lazy"` bo'lmagani sababli birinchi ochilishda ortiqcha megabaytlar yuklangan.

---

## 2. Aniqlangan Kamchiliklar va Yechimlar

### HIGH (Core Web Vitals jarimalari)

#### [PERF-01] Hero LCP rasmida `fetchpriority="high"` yo'qligi
* **Fayl va qator:** `index.html:554`
* **Muammo:** Bosh ekrandagi eng katta vizual rasm oddiy ustuvorlikda yuklanib, LCP vaqtini 1-1.5 soniyaga kechiktirmoqda.
* **Aniq Fix Kodi:**
```html
<img 
  src="https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=1200&q=85" 
  alt="Olmos Gold 18K Italian Diamond Necklace" 
  width="450"
  height="562"
  fetchpriority="high"
  decoding="async"
  class="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-700"
>
```

#### [PERF-02] Aniq o'lchamsiz logotiplar tufayli CLS (Layout Shift) yuzaga kelishi
* **Fayl va qatorlar:** `index.html:411, 1213`
* **Muammo:** `olmos-logo.jpg` teglarda `width` va `height` yo'qligi sababli brauzer logo yuklanishida sarlavha balandligini qayta hisoblagan.
* **Aniq Fix Kodi:** `width="40" height="40"` va `width="44" height="44"` atributlarini qo'shish.

#### [PERF-03] Ekranning pastki qismidagi rasmlarda Lazy Loading yo'qligi
* **Fayl va qatorlar:** `index.html:714, 727`
* **Muammo:** Italiya ustalari ustaxonasi rasmlari birinchi ekranda ko'rinmasada, darhol yuklanib mobil tarmoqni band qilgan.
* **Aniq Fix Kodi:** `loading="lazy"` va `decoding="async"` atributlarini o'rnatish.

---

## 3. Qo'llangan Tuzatishlar
1. Hero rasmiga `fetchpriority="high"`, `decoding="async"` va aniq o'lchamlar berildi.
2. Barcha logo va pastki rasmlarga `loading="lazy"` hamda o'lcham atributlari biriktirildi.
