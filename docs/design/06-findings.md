# YAGONA TOPILMALAR VA MUAMMOLAR RO'YXATI (Findings Register)
**Hujjat kodi:** `DOC-DSGN-06` | **Fayl:** `docs/design/06-findings.md`

Ushbu ro'yxat barcha audit skillari (`refactoring-ui`, `ux-ui-mastery`, `accesslint`, `vercel-agent-skills`, `designer-skills`) natijalarini birlashtiradi va dublikatlardan tozalangan yagona ustuvorliklar jadvalini taqdim etadi.

---

### Yagona Audit Jadvali:

| # | Muammo | Qaysi Ekran | Qaysi Skill Topdi | Og'irlik | Foydalanuvchiga Ta'siri | Effort |
| :- | :--- | :--- | :--- | :-: | :--- | :-: |
| **01** | **Kichik Touch Targetlar (<44px):** Mobil qurilmalarda yurakcha, yopish va o'lcham tugmalari 24–32px bo'lib, Fitts qonunini buzadi. | Butun sayt & Mahsulot ekrani | `ux-ui-mastery` | **P0** | Barmoq tegmaydi, noto'g'ri joy bosiladi, xaridor asabiylashadi. | **S** |
| **02** | **Oltin Matnning Oq Fondagi Past Kontrasti (<4.5:1):** Kichik oltin yozuvlar WCAG 1.4.3 AA talabiga yetmaydi. | Hero, Badglar, Karta detallari | `accesslint` | **P0** | Quyoshda yoki yorug' ekranda o'qib bo'lmaydi. | **S** |
| **03** | **Mahsulot Ekrani "Tuzog'i" (No Popstate / ESC):** Mahsulot ochilganda telefonning "Back" tugmasi bosilsa, butun sayt yopilib ketadi. | `#product-fullscreen-view` | `ux-ui-mastery` | **P0** | Xaridor saytni tark etadi, konversiya uziladi. | **M** |
| **04** | **Modal va Dialoglarda ARIA Yetishmasligi:** `role="dialog"`, `aria-modal="true"` va `aria-label`lar to'liq emas. | Modallar & Fullscreen view | `accesslint` | **P0** | Screen reader foydalanuvchilari uchun sayt chalkash bo'lib qoladi. | **S** |
| **05** | **96 xil Tarqoq Spacing va Oraliqlar:** Saytda yagona 8px panjarasi (grid) yo'q, hamma joyda ixtiyoriy piksellar. | Barcha bo'limlar | `refactoring-ui` | **P1** | Sayt "arzon kiyim do'koni"dek notekis va havaskor ko'rinadi. | **M** |
| **06** | **20 xil Font O'lchami va O'qilmas `text-[7px]`:** Kichik badgelar va tavsiflar mikroskopik bo'lib qolgan. | Mahsulot kartalari, Header | `refactoring-ui` | **P1** | Vizual ierarxiya buzilgan, nima muhimligi sezilmaydi. | **M** |
| **07** | **Forma Yuborishda Loading & Anti-Double-Click Yo'qligi:** Tugma bosilganda darhol holat o'zgarmaydi. | VIP zal formasi & Modallar | `designer-skills` | **P1** | Xaridor yuborildimi-yo'qmi bilmay, bir necha bor bosadi. | **S** |
| **08** | **Bo'sh Holat (Empty State) Passivligi:** Sevimlilar ro'yxati bo'sh bo'lsa, xaridorni ilhomlantiruvchi hech narsa yo'q. | `#wishlist-fullscreen-view` | `designer-skills` | **P1** | Xaridor bu ekrandan darhol chiqib ketadi. | **S** |
| **09** | **Logotip va Rasmlar CLS Sakrashi:** Explicit `width`/`height` bo'lmagani uchun ochilishda matn siljiydi. | Header & Galereya | `vercel-agent-skills` | **P1** | Sahifa yuklanayotganda sakrab, noqulaylik tug'diradi. | **S** |
| **10** | **Kartalar Sakrashi (translateY(-3px)) va Sariq Soya:** Hover effekti ortiqcha chaqqon bo'lib, elita luks sokinligiga to'g'ri kelmaydi. | Katalog kartalari | `refactoring-ui` | **P2** | Arzon o'yinchoq effekti beradi. | **S** |
| **11** | **Xom Rangli Ijtimoiy Havolalar (`#2AABEE`):** Telegram va Instagram ranglari saytning oq-oltin monoxrom estetikasini buzadi. | Mobil menyu & Aloqa | `refactoring-ui` | **P2** | Monoxrom qimmatbaho estetikaga mos emas. | **S** |
| **12** | **Klaviatura Fokus Halqalari (Focus Visible):** Tab tugmasi bosilganda fokus halqasi ko'rinmaydi. | Tugmalar & Kartalar | `accesslint` | **P2** | Klaviaturada harakatlanish noqulay. | **S** |

---
**Belgilar:**
- **P0:** Foydalanuvchi vazifani bajara olmaydi yoki qat'iy a11y buzilishi (4 ta muammo).
- **P1:** Sezilarli qiyinchilik, tushunarsizlik yoki izchillik buzilishi (5 ta muammo).
- **P2:** Vizual jilo va nozik tozalash (3 ta muammo).
- **Effort:** S (Kichik: <1 soat), M (O'rtacha: 1-2 soat), L (Katta: >2 soat).
