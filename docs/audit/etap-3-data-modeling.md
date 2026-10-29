# Audit Hisoboti: Etap 3 — Data Modeling
**Loyihaning turi:** Statik E-tijorat Veb-ilovasi (Single Page Application / GitHub Pages)  
**Sana:** 2026-10-29  
**Auditor:** Data Modeling & Schema Auditor  
**Holat:** TUZATILMOQDA (Schema.org JSON-LD semantikasi qo'shilmoqda, narx parsingi to'g'rilanmoqda)

---

## 1. Kontekst Tahlili
* **Entitetlar:** `productsDB` massivida 12 ta zargarlik buyumi ob'ekti saqlanadi.
* **Qidiruv tizimi semantikasi (SEO):** Sahifada Google va boshqa qidiruv tizimlari uchun hech qanday `Schema.org JSON-LD` kodi yo'q edi. Natijada Google qidiruvida zargarlik do'koni manzili, narxlar va olmos sertifikatlari Rich Snippet sifatida ko'rinmaydi.
* **Narxlar modellanishi:** Narx hisob-kitoblarida formatlangan stringlardan (`"$2,450"`) regex bilan raqam ajratib olish anti-patterni mavjud edi.

---

## 2. Aniqlangan Kamchiliklar va Yechimlar

### HIGH (Jiddiy daraja)

#### [DATA-01] Schema.org JSON-LD structured data yo'qligi
* **Fayl va qator:** `index.html:head`
* **Muammo:** Google qidiruv tizimi mahsulotlarni va do'konni oddiy matn deb biladi. Do'konning rasmiy joylashuvi (`Bunyodkor 15/1`), telefon raqami (`+998 97 774 20 21`) va asosiy 18K Marquise Diamond Ring narxi ($673, `InStock`) bo'yicha boy natijalar (Rich Snippets) chiqmaydi.
* **Aniq Fix Kodi:** `<head>` bo'limiga rasmiy `JewelryStore` va `Product` JSON-LD skriptini qo'shish.

---

### MEDIUM (O'rta daraja)

#### [DATA-02] Formatlangan narx satridan raqam ajratish anti-patterni
* **Fayl va qator:** `index.html:2785`
* **Muammo:** `parseInt(it.price_usd.replace(/\D/g, ''), 10)` orqali narx hisoblangan. Ob'ektda tayyor sonli qiymat (`base_price_usd`) bo'la turib, string parsing ishlatilgan.
* **Hujum / Xato stsenariysi:** Agar narx formati o'zgartirilsa (masalan, sentlar yoki proba raqamlari qo'shilsa), regex butun narx hisobini buzib yuboradi.
* **Aniq Fix Kodi:**
```javascript
// O'RNIGA to'g'ridan-to'g'ri sonli maydondan foydalanish:
const num = typeof it.base_price_usd === 'number' ? it.base_price_usd : (parseInt(it.price_usd.replace(/\D/g, ''), 10) || 0);
```

---

## 3. Qo'llangan Tuzatishlar
1. `index.html` ning `<head>` qismiga Google qidiruv standarti bo'yicha to'liq `JewelryStore` va `Product` Schema.org JSON-LD kiritildi.
2. Narx hisoblash joylarida `base_price_usd` sonli maydoniga o'tildi.
