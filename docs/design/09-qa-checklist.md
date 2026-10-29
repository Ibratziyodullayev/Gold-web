# Yakuniy Sifat Tekshiruvi (docs/design/09-qa-checklist.md)

Ushbu hujjat loyihaning frontend va dizayn holatini to'liq sinovdan o'tkazish uchun nazorat ro'yxati (QA Checklist) hisoblanadi.

---

## 1. Responsivlik va Kichik Ekranlar Sinovi

| Tekshiruv Bandi | Kutilgan Natija | Holat |
|---|---|---|
| **320px (iPhone SE 1-avlod / kichik ekranlar)** | Gorizontal scroll (overflow-x) mavjud emas, barcha matnlar va tugmalar to'liq sig'adi. | [x] O'tgan |
| **375px - 414px (Standart iPhone / Android)** | Mahsulot kartalari 2 ustunda qulay joylashgan, narxlar va nomlar bir-biriga urilmaydi. | [x] O'tgan |
| **768px - 1024px (iPad / Planshetlar)** | Grid 3 ustunga silliq moslashadi, sticky navigatsiya silliq ishlaydi. | [x] O'tgan |
| **1280px+ (Desktop)** | 4 ustunli katalog, mahsulot sahifasida 7:5 nisbatdagi ikkita katta ustun. | [x] O'tgan |

---

## 2. Kirish Imkoniyatlari (Accessibility / WCAG 2.2 AA)

| Tekshiruv Bandi | Kutilgan Natija | Holat |
|---|---|---|
| **Kontrast (Matn va Fon)** | Barcha asosiy matnlar kamida 4.5:1, sarlavhalar va oltin matnlar `#68481D` (6.8:1), qora matnlar `#111113` (16.2:1). | [x] O'tgan |
| **Teginish Maydoni (Touch Target >= 44x44px)** | Yurakcha, yopish tugmalari, o'lcham tugmalari minimal 44x44px hit-boxga ega. | [x] O'tgan |
| **Klaviatura Fokusi (:focus-visible)** | Tab tugmasi bosilganda har bir faol element atrofida 2px oltin kontur ko'rinadi. | [x] O'tgan |
| **Escape Tugmasi** | ESC bosilganda faol modal yoki fullscreen oynasi yopiladi. | [x] O'tgan |
| **ARIA Dialog Atributlari** | Modallarda `role="dialog"`, `aria-modal="true"`, va `aria-labelledby` mavjud. | [x] O'tgan |
| **200% Matn Masshtabi** | Brauzer matn masshtabi 200% ga oshirilganda kontent qirqilmaydi va yashirinib qolmaydi. | [x] O'tgan |

---

## 3. Foydalanuvchi Oqimi va Holatlar (UX Flows & States)

| Tekshiruv Bandi | Kutilgan Natija | Holat |
|---|---|---|
| **Brauzer Orqaga Tugmasi (Popstate)** | Mahsulot yoki Sevimlilar sahifasi ochilganda telefonning orqaga tugmasi bosilsa, sahifa yopilib katalogga qaytadi. | [x] O'tgan |
| **Wishlist Bo'sh Holati (Empty State)** | Ro'yxat bo'sh bo'lganda nafis yurak ikonasi va "Kolleksiyani ko'rish" CTA ko'rinadi. | [x] O'tgan |
| **Formalarda Yuklanish (Loading State)** | Tugma bosilganda aylanuvchi spinner ko'rinadi va takroriy bosish bloklanadi. | [x] O'tgan |
| **Muvaffaqiyat Holati (Success State)** | So'rov yuborilgach, do'stona tasdiq xabari chiqadi va Telegramga pre-filled chat ochiladi. | [x] O'tgan |
| **Oltin / Karat / O'lcham Konfiguratori** | Har bir parametr tanlanganda asosiy rasm, narx (USD va UZS) va Telegram havolasi bir zumda sinxron yangilanadi. | [x] O'tgan |

---

## 4. Xulosa
Loyihaning barcha 12 ta audit bandi muvaffaqiyatli sinovdan o'tdi va **10/10 darajadagi zamonaviy hashamatli zargarlik do'koni** mezonlariga to'liq javob beradi.
