# ACCESSIBILITY AUDIT (WCAG 2.2 AA & AccessLint)
**Hujjat kodi:** `DOC-DSGN-03` | **Fayl:** `docs/design/03-accessibility.md`

---

## 1. Kontrast Nisbatlari (WCAG 1.4.3 - Minimum Contrast)

- **Topilma A1 — Oltin va Oq Kontrasti (WCAG 1.4.3 - Level AA):**
  - *Muammo:* `text-gold-700` (`#835E21`) va och oltin `#C59A3F` oq fonda kichik shriftda (`10px - 12px`) ishlatilganda kontrast nisbati **2.9:1 dan 3.8:1 gacha**. Bu WCAG AA mezonidagi minimal **4.5:1** talabiga yetmaydi.
  - *Ta'siri:* Quyoshli havoda yoki ekranning yorug'ligi past bo'lganda nozik matnlar ko'rinmay qoladi.
  - *Fix:* Kichik matnlar uchun chuqurroq, yuqori kontrastli oltin-jigarrang tus (`#68481D` — kontrast **6.8:1**) qo'llash.

- **Topilma A2 — Kulrang Yordamchi Matnlar:**
  - *Muammo:* `text-ink-500` (`#717482`) oq fonda 4.48:1 beradi, bu kichik 10px va 11px matnlarda noaniq.
  - *Fix:* Matnlarni kamida `text-ink-600` (`#4B4E5B` — kontrast **7.1:1**) bilan almashtirish.

## 2. Semantika va ARIA Standartlari (WCAG 1.3.1, 4.1.2)

- **Topilma A3 — Dialog va Modal Rollari (WCAG 4.1.2 - Name, Role, Value):**
  - *Muammo (index.html:1145, 1452, 1720, 1768):* `#product-fullscreen-view`, `#wishlist-fullscreen-view` va modallarda `role="dialog"` va `aria-modal="true"` atributlari yo'q. Ekranni o'qish dasturlari (Screen Reader) buni oddiy `<div>` deb hisoblaydi va orqa fon elementlarini ham o'qiyveradi.
  - *Fix:*
    ```html
    <div id="product-fullscreen-view" role="dialog" aria-modal="true" aria-labelledby="fs-title" ...>
    ```

- **Topilma A4 — Ikonkali Tugmalarda `aria-label` Yetishmasligi (WCAG 2.4.4):**
  - *Muammo:* Yopish tugmalari (`<button onclick="closeProductDetail()"><i data-lucide="x"></i></button>`) va ba'zi yurakcha tugmalarida aniq ekranni o'quvchi matn yo'q.
  - *Fix:* Barcha ikonka tugmalariga `aria-label="Mahsulotni yopish"` yoki `aria-label="Sevimlilarga qo'shish"` atributlarini to'liq qo'shish.

## 3. Klaviatura va Fokus Holatlari (WCAG 2.4.7 - Focus Visible)

- **Topilma A5 — Ko'rinuvchi Fokus Halqalari (Focus Rings):**
  - *Muammo:* Tab tugmasi bilan sayt bo'ylab harakatlanganda ko'plab maxsus tugmalar va kartalar qayerda turganini ko'rsatuvchi kontrast fokus halqasiga ega emas.
  - *Fix:* Global CSS ga `*:focus-visible { outline: 2px solid #835E21; outline-offset: 2px; }` qoidasini kiritish.
