# UX AUDIT (UX/UI Mastery & Evristikalar Bo'yicha)
**Hujjat kodi:** `DOC-DSGN-02` | **Fayl:** `docs/design/02-ux-audit.md`

---

## 1. Nielsen Usability Heuristics Tekshiruvi

- **Topilma U1 — User Control & Freedom (Nielsen #3):**
  - *Muammo (index.html:1145):* `#product-fullscreen-view` ochilganda brauzerning "Orqaga" (Back) tugmasi bosilsa, butun sayt yopilib ketadi yoki oldingi domeniga qaytib ketadi (URL hash o'zgarmaydi). ESC tugmasi ham mahsulotni yopmaydi.
  - *Buzilish:* Foydalanuvchi to'liq ekranda "tuzoqqa" tushgandek his qiladi.
  - *Fix:* `openProductDetail` chaqirilganda `history.pushState({view: 'product', id: productId}, '', '#product-' + productId)` qo'yish va `window.onpopstate` orqali orqaga qaytishni boshqarish; shuningdek `keyup` voqeasida `ESC` tugmasi bilan yopish.

- **Topilma U2 — Consistency and Standards (Nielsen #4):**
  - *Muammo (index.html:2448-2458):* Bosh katalogdagi karta bosilganda mahsulot sahifasi ochiladi, biroq qidiruv/katalogdagi ayrim tugmalar ilgari boshqa modallarni chaqirgan.
  - *Fix:* Barcha mahsulot kartalari va "Tanlash / Ko'rish" tugmalari qat'iy yagona harakatga — to'liq interaktiv DiamondsByUK uslubidagi mahsulot sahifasiga yo'naltiriladi.

- **Topilma U3 — Error Prevention & Status Visibility (Nielsen #1, #5):**
  - *Muammo (index.html:1385-1393):* VIP zalga yozilish formasi (`#fit-phone`) oddiy `type="tel"` bo'lib, xato kiritilganda darhol inline ko'rinmaydi.
  - *Fix:* O'zbekiston raqamlari uchun `(90) 123-45-67` formatidagi avtomatik kiritish maskasi va submit qilinganda tugmada 1 soniyalik mikro-animatsiya (loading) qo'yish.

## 2. Laws of UX va Kognitiv Yuklama (Cognitive Load)

- **Topilma U4 — Fitts's Law (Touch Target Size):**
  - *Muammo (index.html:2490-2497, 1185, 1730):* Sevimlilar yurakcha tugmasi `w-7 h-7 sm:w-8 sm:h-8` (28px - 32px), modallardagi "X" tugmalari esa `p-1` (24px). Apple HIG va Google Material Design bo'yicha barmoq tegish maydoni kamida **44x44px** bo'lishi shart.
  - *Buzilish:* 95% mobil foydalanuvchilar kichik tugmani bosolmay adashadi, mahsulotga tasodifan kirib ketadi.
  - *Fix:* Barcha interaktiv mobil tugmalarga `min-w-[44px] min-h-[44px]` sensor maydoni berish.

- **Topilma U5 — Gestalt Law of Proximity (Guruhlash):**
  - *Muammo (index.html:1280-1320):* Mahsulot sahifasidagi narx, chegirma va variantlar (metall, karat, o'lcham) orasidagi bo'shliqlar juda bir xil bo'lib, qaysi parametr narxga ta'sir qilishi darhol anglashilmaydi.
  - *Fix:* Metall va Karat selektorlarini bitta vizual guruh ("Konfiguratsiya") sifatida ajratib, narx o'zgarishini ko'rsatuvchi yorqinroq vizual aloqa (feedback) berish.
