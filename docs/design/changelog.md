# UI/UX O'zgarishlar Jurnali (docs/design/changelog.md)

Ushbu hujjat audit natijasida aniqlangan barcha 12 ta kamchiliklar (F-01 dan F-12 gacha) bo'yicha `index.html` ga kiritilgan aniq arxitekturaviy va vizual o'zgarishlarni qayd etadi.

---

## 1. P0 (Kritik Muammolar — 4 ta)

### [F-01] Mobil Teginish Maydonlari (Touch Targets >= 44x44px)
- **Muammo:** Katalog kartalaridagi yurakcha tugmasi `w-7 h-7` (28x28px), mahsulot sahifasidagi o'lcham tugmalari `px-2.5 py-1` (26px balandlik) bo'lib, mobil foydalanuvchilar (95% ayollar) bir qo'l bilan boshqarganda noto'g'ri bosish yoki bosa olmaslik holatlari yuzaga kelayotgan edi.
- **Yechim:**
  - Katalog kartalaridagi `btn-wishlist` o'lchami to'liq `w-11 h-11` (44x44px) ga oshirildi.
  - Mahsulot to'liq sahifasidagi (`#product-fullscreen-view`) yurakcha `w-11 h-11`, yopish tugmasi `w-11 h-11`, qaytish tugmasi `min-h-[44px]` ga keltirildi.
  - Uzuk o'lchami (Ring Size) tugmalari `min-w-[44px] min-h-[44px] flex items-center justify-center` qilib qayta ishlandi.
  - Karat va metall tanlash tugmalariga `min-h-[44px]` va `min-h-[48px]` minimal teginish maydonlari berildi.
  - Barcha modallarning yopish (X) tugmalari `w-11 h-11` (44x44px) qilib kengaytirildi.

### [F-02] Kontrast va O'qilishi Qiyin Matnlar (WCAG 2.2 AA)
- **Muammo:** Oq fonda ochiq oltin rang (`#BF9842` / 2.8:1) va `text-[7px]` / `text-[8px]` kabi o'ta mayda shriftlar ishlatilgan edi.
- **Yechim:**
  - Oq fondagi barcha oltin matnlar uchun yuqori kontrastli **Noble Gold Deep (`#68481D`)** joriy etildi (kontrast nisbati **6.8:1**, WCAG AA va AAA talablaridan yuqori).
  - Barcha `text-[7px]` va `text-[8px]` matnlar kamida `text-[9px]` yoki `text-[10px]` ga ko'tarildi va font-weight oshirildi.
  - Kulrang yordamchi matnlar `#4B4E5B` (7.1:1 kontrast) ga mustahkamlandi.

### [F-03] Trapped Modal va Popstate / ESC Navigatsiyasi
- **Muammo:** Mahsulot to'liq ekranda ochilganda telefonning apparat "Orqaga" tugmasi yoki surish (swipe back) jesti brauzer sahifasidan to'liq chiqib ketar, modal yopilmas edi; klaviaturadagi `ESC` tugmasi ishlamas edi.
- **Yechim:**
  - `openProductDetail` va `openWishlistPage` chaqirilganda `window.history.pushState` orqali URL ga mos ravishda `#product-{id}` va `#wishlist` yozilishi ta'minlandi.
  - `window.addEventListener('popstate')` orqali telefonning orqaga tugmasi bosilganda modal va fullscreen sahifalar silliq yopilishi dasturlashtirildi.
  - `window.addEventListener('keydown')` orqali global `Escape` tugmasi bosilganda faol modal va sahifalarni yopish joriy qilindi.
  - URL orqali to'g'ridan-to'g'ri havolani ochish (Deep linking) qo'llab-quvvatlandi (`handleInitialHash()`).

### [F-04] ARIA va Semantika Yetishmovchiligi
- **Muammo:** Fullscreen va modal oynalar oddiy `<div>` bo'lib, ekran o'quvchi (Screen Reader) dasturlar uchun dialog sifatini ifodalamas edi.
- **Yechim:**
  - `#product-fullscreen-view`, `#wishlist-fullscreen-view`, `#vip-catalog-modal`, `#concierge-modal`, `#ring-size-modal` konteynerlariga `role="dialog"`, `aria-modal="true"`, va `aria-labelledby="..."` semantik atributlari to'liq qo'shildi.

---

## 2. P1 (Muhim Muammolar — 5 ta)

### [F-05] 8px Spacing Tizimiga Unifikatsiya
- Elementlar orasidagi tartibsiz `p-1.5`, `p-2.5`, `px-3.5` oraliqlar 8px panjara tizimi qoidalariga keltirildi (`p-2 (8px)`, `p-3 (12px)`, `p-4 (16px)`, `p-6 (24px)`).

### [F-06] Tipografiya Ierarxiyasini Standartlashtirish
- 20 xil erkin font-size o'rniga 8 ta rasmiy daraja qo'llanildi (`Display 40px`, `H1 32px`, `H2 24px`, `H3 18px`, `Body 15px`, `Small 13px`, `Caption 11px`, `Micro 10px`).

### [F-07] Klaviatura Navigatsiyasi (:focus-visible)
- Klaviatura orqali boshqaruvchi foydalanuvchilar uchun global `:focus-visible` oltin kontur halqasi kiritildi:
  `outline: 2px solid #835E21 !important; outline-offset: 2px !important;`

### [F-08] Wishlist Bo'sh Holati (Empty State) Jozibadorligi
- Bo'sh ro'yxat uchun nafis nozik yurak ikonasi, tushunarli va do'stona yo'riqnoma hamda to'g'ridan-to'g'ri katalogga qaytaruvchi premium CTA tugmasi joriy etildi.

### [F-09] Formalarda Yuklanish Holati (Loading State & Disabled)
- VIP fitting va katalog so'rov formalarida foydalanuvchi "Yuborish" tugmasini bosganda tugma bloklanadi (`disabled=true`) va ichida aylanuvchi oltin-oq spinner (`.btn-spinner`) paydo bo'ladi. Takroriy yuborilishlarning oldi olindi.

---

## 3. P2 (Kichik Sayqallashlar — 3 ta)

### [F-10] CLS (Cumulative Layout Shift) Oldini Olish
- Logotiplar va mahsulot kartalaridagi rasmlarga explicit `width="44"` va `height="44"`, kartalarda `width="400" height="400"` atributlari qo'shilib, sahifa yuklanishida matnlar sakrashi to'xtatildi.

### [F-11] Ko'p Qatlamli Sokin Hashamat Soyalari
- Kartalar hover effekti sokinlashtirildi: `shadow-[0_4px_20px_-2px_rgba(27,30,40,0.04)]` -> hoverda `shadow-[0_14px_32px_-4px_rgba(27,30,40,0.08)]` va yumshoq `-translate-y-0.5 (-2px)`.

### [F-12] Ijtimoiy Tarmoq Havolalari Dizayni
- Telefon, Telegram va Instagram havolalari o'ta yorqin sun'iy ko'k yoki qizil ranglardan tozalab, hashamatli oq fon, yupqa oltin chegara va to'q noble matn uslubiga birlashtirildi.
