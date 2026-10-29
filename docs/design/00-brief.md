# DIZAYN BRIFI — OLMOS GOLD JEWELLERY
**Hujjat kodi:** `DOC-DSGN-00` | **Sana:** 2026-10-29 | **Status:** Tasdiqlangan

---

## 1. Loyiha Missiyasi va Asosiy Maqsad
OLMOS GOLD JEWELLERY vebsaytining UI/UX arxitekturasini "oddiy va chalkash e-commerce sayti" darajasidan xalqaro andoza — **DiamondsByUK** darajasidagi nufuzli, sof, ishonchli va yuqori daromadli **Zamonaviy Elita Zargarlik Atelesi (Modern Clean Luxury)** darajasiga olib chiqish.

## 2. Auditoriya va Foydalanish Konteksti
- **Asosiy auditoriya:** Tabiiy olmoslar va 18K qotishma tilla buyumlarni qadrlovchi nozik didli ayollar (shuningdek to'y va qimmatbaho sovg'a xaridorlari).
- **Qurilmalar nisbati:** **95% Mobil** (iOS Safari va zamonaviy Android). Sayt birinchi navbatda bosh barmoq ergonomikasiga (Touch Target >= 44px) to'liq moslashgan bo'lishi shart.
- **Seans davomiyligi:** 4–5 daqiqa. Foydalanuvchi vaqtining **80% qismini alohida ochiladigan Mahsulot Ekrani (Product Detail View)** ichida o'tkazadi.

## 3. Asosiy Muammolar (Mavjud Holat Tanqidi)
1. **Vizual chalkashlik:** Ortiqcha yaltiroq elementlar, 96 xil tarqoq spacing va 20 xil font o'lchami elita brend hissini yo'qotib, arzon kiyim do'koni taassurotini bermoqda.
2. **Ierarxiya zaifligi:** Sarlavhalar, narxlar, tavsiflar va ishonch elementlari o'rtasida aniq kontrast va havodorlik (whitespace) yetishmaydi.
3. **Muvofiqlik yo'qligi:** Ranglar, burchaklar va tugmalar yagona dizayn tokenlariga to'liq bo'ysunmagan.

## 4. Benchmark va Vizual Taste
- **Asosiy mezon:** `https://diamondsbyuk.co.uk`
- **Vizual uslub:** Toza oq fon (Pure White `#FFFFFF`), och fil suyagi (`#FAF9F6`), nozik oltin aksentlar va qat'iy o'qiluvchi to'q grafit tipografika.
- **Fazoviy tartib:** Erkin va havodor (Spacious, 8px grid).
- **Tipografika:** Sarlavhalar uchun `Tenor Sans`, matn va narxlar uchun `Figtree`.
- **Animatsiyalar:** O'rtacha, silliq va sokin (micro-interactions, zero layout shifts).

## 5. Texnik va Biznes Cheklovlari
- **Stack:** Pure HTML5, Tailwind CSS, Modular ES6+ JavaScript. Hech qanday og'ir qo'shimcha framework yuklanmaydi.
- **Integratsiya:** Telegram bot (`@OLMOS_GOLD`), telefon (+998 97 774 20 21) va butik manzili (Bunyodkor 15/1) oqimi 100% uzluksiz ishlashi shart.
- **Katalog:** 10 ta boyitilgan elita mahsulot bazasi to'liq saqlanadi.

## 6. Muvaffaqiyat Mezoni
- Sayt foydalanuvchida ilk 3 soniyada 100% qimmatbaho, xavfsiz va sertifikatlangan Toshkent butiki ishonchini uyg'otishi (10/10 baho).
- Mahsulot ochilganda hech qanday chalkashliksiz, bir qarashda tushunarli konstruktor va to'g'ridan-to'g'ri xarid oqimi mavjudligi.
