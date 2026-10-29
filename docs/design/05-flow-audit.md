# USER FLOW, STATES & MICROCOPY AUDIT (Designer Skills)
**Hujjat kodi:** `DOC-DSGN-05` | **Fayl:** `docs/design/05-flow-audit.md`

---

## 1. 10 ta Holat (States) Qamrovi

- **Topilma F1 — Bo'sh Holat (Empty State) Ilhomlantiruvchi Bo'lishi:**
  - *Muammo (index.html:2248-2254):* Sevimlilar bo'sh bo'lganda oddiy xira xabar chiqadi. Xaridorni ilhomlantiruvchi taklif yo'q.
  - *Fix:* Bo'sh holatda nafis oltin zargarlik illyustratsiyasi, *"Hozircha saqlangan buyumlar yo'q. Olmos Gold eksklyuziv kolleksiyasidan o'zingizga yoqqan uzuk yoki marjonni tanlang"* degan iliq matn va to'g'ridan-to'g'ri `#collections` ga olib boruvchi tugma qo'yish.

- **Topilma F2 — Formalarda Loading va Duplicate Submit Himoyasi:**
  - *Muammo (index.html:1370, 1744):* Formani yuborish (Submit) tugmasi bosilganda tugma darhol `disabled` bo'lmaydi va ichida spinner chiqmaydi. Foydalanuvchi bir necha marta qayta-qayta bosishi mumkin.
  - *Fix:* Tugmaga `loading` holatini kiritish: tugma matni *"Yuborilmoqda..."* ga aylanadi, spinner aylanadi va qayta bosish bloklanadi.

## 2. Mikromatnlar (Microcopy Quality)

- **Topilma F3 — "Arzon E-commerce" Mikromatnlaridan Qutulish:**
  - *Muammo:* "Katalogni Olish", "Yuborish", "Band qilish" kabi so'zlar DiamondsByUK va Cartier kabi elita butiklar tiliga mos kelmaydi.
  - *Fix:*
    - "Katalogni Olish" → *"2026 VIP Lookbookni Qabul Qilish"*
    - "Band qilish" → *"Butikda Ko'rish & Tanlash"*
    - "Yuborish" → *"Konsyerj bilan Bog'lanish"*
