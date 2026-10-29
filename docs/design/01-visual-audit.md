# VIZUAL AUDIT (Refactoring UI Bo'yicha)
**Hujjat kodi:** `DOC-DSGN-01` | **Fayl:** `docs/design/01-visual-audit.md`

---

## 1. Vizual Ierarxiya Muammolari
- **Topilma V1 (index.html:368-372):** Hero H1 sarlavhasida `gold-text-glow` (sariq matn soyasi) ishlatilgan. Oq fonda bu matn chetlarini yuvib yuboradi va o'qish qiyinlashadi.
  - *Fix:* `text-shadow` olib tashlanadi, qat'iy yuqori kontrastli `#111113` va toza oltin gradient ishlatiladi.
- **Topilma V2 (index.html:2480-2486):** Mahsulot kartalari tepasidagi proba va sertifikat badgelarida `text-[7px]` va `text-[8px]` font o'lchami berilgan. Zamonaviy smartfonlarda bu deyarli o'qilmaydi va arzon ko'rinish beradi.
  - *Fix:* Minimal shrift o'lchamini `text-[10px]` (kamida 11px) ga ko'tarish, paddingni `px-2 py-0.5` qilib standartlash.
- **Topilma V3 (index.html:2520-2530):** Mahsulot kartasi pastki narx bloki: Narx va UZS ekvivalenti bilan "Tanlash" tugmasi bir qatorda siqilib turibdi (`gap-1.5`).
  - *Fix:* Tugma va narx o'rtasida aniq vertikal yoki gorizontal 8px margin ajratish, narxni yirikroq va sof ko'rsatish.

## 2. Spacing Izchilligi (Spacing Inconsistency)
- **Topilma V4 (Butun loyiha bo'yicha):** Kodda 96 xil tarqoq padding/margin ishlatilgan (`p-[2.5px]`, `px-3.5`, `py-1.5`, `gap-1.5`, `mt-0.5`, `mb-2.5`).
  - *Fix:* Barcha oraliqlarni qat'iy **8px tizimiga** (4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px) mapping qilish.
- **Topilma V5 (index.html:1203-1206):** Mahsulot to'liq ekranida chap galereya va o'ng konstruktor bloki orasidagi bo'shliq `gap-10 lg:gap-14`. Desktopda havo yetarli, lekin planshet va mobil ekranda bo'limlar orasida havodorlik notekis.
  - *Fix:* Standartlashtirilgan container padding `px-4 sm:px-6 lg:px-12` va `gap-8 lg:gap-12` qo'llash.

## 3. Rang va Soya (Color & Elevation)
- **Topilma V6 (index.html:126-137):** `.luxury-white-card` kartasi 3 xil turlicha oltin soyaga ega (`rgba(197, 154, 63, 0.22)`). Hover holatida karta 3px tepaga sakraydi, bu esa sokin luks hissi o'rniga "sakrovchi o'yinchoq" effekti beradi.
  - *Fix:* Sakrashni `translateY(-1px)` ga yumshatish, soyani tabiiy neytral yumshoq ambient soyaga (`rgba(0,0,0,0.04) + rgba(197,154,63,0.08)`) almashtirish.
- **Topilma V7 (index.html:325-331):** Mobil menyu va havolalarda to'g'ridan-to'g'ri xom ranglar (`bg-[#2AABEE]/10`, `text-[#0088cc]`) ishlatilgan, bu DiamondsByUK ning monoxrom nafisligiga zid.
  - *Fix:* Barcha ijtimoiy va aloqa havolalarini yagona neytral qora/oltin luxury tokenlarga o'tkazish.
