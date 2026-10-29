# FRONTEND PERFORMANCE & CORE WEB VITALS AUDIT
**Hujjat kodi:** `DOC-DSGN-04` | **Fayl:** `docs/design/04-frontend-perf.md`

---

## 1. Cumulative Layout Shift (CLS) Tekshiruvi
- **Topilma P1 (index.html:1158, 1465, 210):** Logotip `olmos-logo.jpg` teglari uchun `width` va `height` atributlari berilmagan, faqat CSS klasslari (`w-8 h-8`) mavjud. Brauzer birinchi renderda o'lchamni hisoblamasdan o'tishi sababli matnlar sakraydi (CLS > 0.05).
  - *Fix:* Barcha rasm teglariga `width="32" height="32"` yoki mos o'lchamlarini qat'iy kiritish.
- **Topilma P2 (index.html:1208-1214):** Mahsulot to'liq ekranidagi asosiy rasm (`#fs-main-image`) yuklanayotganda bo'sh turadi va rasm ochilganda to'satdan paydo bo'ladi.
  - *Fix:* Rasm konteyneriga nozik oltin tusli skeleton loader qo'yish va `opacity-0 transition-opacity duration-300 onload="this.classList.remove('opacity-0')"` qo'llash.

## 2. Largest Contentful Paint (LCP) & Assetlar
- **Topilma P3 (index.html:360-440):** Hero bo'limidagi eng katta element — markaziy marjon surati oddiy `loading="lazy"` bilan turishi mumkin, bu esa LCP vaqtini 1.8 soniyadan 2.6 soniyaga kechiktiradi.
  - *Fix:* Hero suratiga `fetchpriority="high"` va `loading="eager"` berish.
- **Topilma P4 (index.html:2550, 2565):** Har bir renderda `lucide.createIcons()` butun DOM bo'ylab qayta qidiruv o'tkazadi (CPU tsikllarini sarflaydi).
  - *Fix:* Yangilangan konteyner ichidagina `lucide.createIcons({ root: container })` qilib ishlash.
