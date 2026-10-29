# Audit Hisoboti: Etap 1 — Auth va Secret Management
**Loyihaning turi:** Statik E-tijorat Veb-ilovasi (Single Page Application / GitHub Pages)  
**Sana:** 2026-10-29  
**Auditor:** Auth & Secret Management Auditor  
**Holat:** DIQQAT TALAB ETILADI (Critical zaifliklar mavjud)

---

## 1. Kontekst Tahlili

* **Autentifikatsiya mexanizmi:** Saytda an'anaviy parolli akkaunt, JWT, OAuth yoki cookie sessiyalari **mavjud emas**. Barcha tashrif buyuruvchilar **anonim mijoz (guest)** maqomida ishlaydi.
* **Sessiya va holat saqlash:** Mijoz holati faqat brauzerning `localStorage` xotirasida (`olmos_gold_cart_v2`, `olmos_gold_wishlist_v2`, `olmos_gold_currency`) saqlanadi.
* **Maxfiy kalitlar:** Kod ichida haqiqiy **Telegram Bot API Token** va **Admin Chat ID** to'g'ridan-to'g'ri ochiq yozilgan holda topildi.
* **Foydalanuvchi rollari:** 
  * `Anonim xaridor` (barcha katalog, filtrlar, savat, sevimlilarni ko'radi);
  * `Do'kon konsyerji / Admin` (Telegram orqali buyurtmalarni qabul qiladi).

---

## 2. Aniqlangan Zaifliklar Ro'yxati

### CRITICAL (Zudlik bilan bartaraf etilishi shart)

#### [CRIT-01] Ochiq manbada Telegram Bot API Token mavjudligi
* **Fayl va qator:** `index.html:2418` — Telegram Bot API Token topildi.
* **Muammo:** Telegram botining maxfiy tokeni (`TG_BOT_TOKEN`) mijoz brauzeriga yuklanadigan ochiq HTML/JS faylida ochiq matn (plain text) holatida saqlanmoqda.
* **Hujum stsenariysi:** Istalgan foydalanuvchi sahifa kodini ko'rib (`Ctrl+U` yoki `F12`), bot tokenini nusxalab oladi va `https://api.telegram.org/bot<TOKEN>/...` orqali bot boshqaruvini to'liq qo'lga oladi, bot nomidan firibgarlik xabarlarini tarqatadi yoki adminni bloklaydi.
* **Aniq Fix Kodi:**
```javascript
// O'CHIRILISHI KERAK (index.html:2418):
// const TG_BOT_TOKEN = "...";

// TO'G'RI YECHIM:
// Bot tokenini frontenddan butunlay olib tashlash. Buyurtmalarni token talab qilmaydigan
// xavfsiz Telegram Deep Link orqali mijozning o'z Telegram ilovasiga uzatish:
function openTelegramDirectOrder(orderSummary) {
  const message = encodeURIComponent(orderSummary);
  window.open(`https://t.me/OLMOS_GOLD?text=${message}`, '_blank', 'noopener,noreferrer');
}
```

#### [CRIT-02] Telegram Admin Chat ID ochiq manbada oshkor qilingan
* **Fayl va qator:** `index.html:2419` — Telegram Admin Chat ID topildi.
* **Muammo:** Do'kon rahbarining shaxsiy Telegram Chat ID raqami (`TG_ADMIN_CHAT_ID`) ochiq yozilgan.
* **Hujum stsenariysi:** Hujumchi admin ID sini bilib olib, unga maqsadli fishing (spear phishing), bot orqali cheksiz spam yoki Telegram API orqali soxta tranzaksiya bildirishnomalarini yuboradi.
* **Aniq Fix Kodi:**
```javascript
// O'CHIRILISHI KERAK (index.html:2419):
// const TG_ADMIN_CHAT_ID = "...";

// TO'G'RI YECHIM: Client-side kodda hech qanday shaxsiy Chat ID bo'lmasligi kerak.
// Aloqa faqat rasmiy username (@OLMOS_GOLD) orqali amalga oshiriladi.
```

#### [CRIT-03] Git Commit tarixida Telegram Bot Token abadiy saqlanib qolgan
* **Fayl va commit:** `Git commit: 25a9079 (index.html:1968)` — Telegram Bot API Token topildi.
* **Muammo:** Bot token `25a9079` commitida GitHub omboriga qo'shilgan. Fayldan o'chirilgan taqdirda ham, u git tarixida (`git log` yoki GitHub commit history) hammaga ochiq qoladi.
* **Hujum stsenariysi:** Avtomatlashtirilgan GitHub skaner botlari (masalan, GitGuardian, TruffleHog) 60 soniya ichida tokenni topadi va o'g'irlaydi.
* **Aniq Fix Kodi (Rotation rejasi quyida keltirilgan):**
```bash
# Git tarixini tozalash uchun (token yangilangandan so'ng):
# 1. BFG Repo-Cleaner yordamida:
bfg --replace-text banned-secrets.txt
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push origin --force --all
```

---

### HIGH (Jiddiy xavflar)

#### [HIGH-01] Telegram Bot API'ga to'g'ridan-to'g'ri so'rovlarda Rate-limiting va CAPTCHA yo'qligi
* **Fayl va qator:** `index.html:2429-2450` (`sendTelegramLeadNotification`)
* **Muammo:** Istalgan tashrif buyuruvchi yoki skript brauzer konsolidan `sendTelegramLeadNotification()` funksiyasini sekundiga 100 martalab cheklovlarsiz chaqira oladi.
* **Hujum stsenariysi:** Raqobatchi botnet orqali soxta buyurtmalar yuborib, do'kon adminini spamga ko'mib tashlaydi va Telegram API tomonidan bot vaqtincha yoki butunlay `429 Too Many Requests` bilan bloklanadi.
* **Aniq Fix Kodi:**
```javascript
// Xavfsiz debounce / throttle va client-side limit:
let lastOrderTime = 0;
const ORDER_COOLDOWN_MS = 15000; // 15 soniya cooldown

function canSubmitLead() {
  const now = Date.now();
  if (now - lastOrderTime < ORDER_COOLDOWN_MS) {
    alert("Iltimos, keyingi so'rovdan oldin bir oz kuting.");
    return false;
  }
  lastOrderTime = now;
  return true;
}
```

#### [HIGH-02] Uchinchi tomon xizmatlariga (api.telegram.org) ruxsatsiz CORS so'rovlari
* **Fayl va qator:** `index.html:2431`
* **Muammo:** Statik frontend to'g'ridan-to'g'ri Telegram serveriga `fetch()` orqali murojaat qilmoqda. Telegram ba'zi hududlarda yoki provayderlarda bloklangan bo'lsa, xarid so'rovi yo'qoladi va dasturchi bu haqda xabar topmaydi.
* **Hujum stsenariysi:** Tarmoq xatosi yoki Telegram bloklanishi sababli qimmatbaho zargarlik buyurtmalari adminga yetib bormaydi, konversiya 0 ga tushadi.
* **Aniq Fix Kodi:**
```javascript
// Buyurtmani Telegram Direct Havola orqali kafolatli ochish:
function dispatchOrderSecurely(leadText) {
  // 1. Zaxira: mijoz ilovasida to'g'ridan-to'g'ri chat ochish
  const tgUrl = `https://t.me/OLMOS_GOLD?text=${encodeURIComponent(leadText)}`;
  window.open(tgUrl, '_blank', 'noopener,noreferrer');
}
```

---

### MEDIUM (O'rta darajali xavflar)

#### [MED-01] .gitignore faylida .env va kalitlar ro'yxatdan qolib ketgan
* **Fayl va qator:** `.gitignore:1-4`
* **Muammo:** `.gitignore` faqat `.DS_Store`, `Thumbs.db`, `*.log`, `*.zip` fayllarini cheklaydi. Unda `.env`, `.env.local`, `*.pem`, `*.key`, `secrets.*` qoidalari yo'q.
* **Hujum stsenariysi:** Kelgusida ishlab chiquvchi lokal sinov yoki yangi integratsiya uchun `.env` fayl ochsa, u avtomatik tarzda ochiq omborga (public repo) commit bo'lib ketadi.
* **Aniq Fix Kodi:**
```gitignore
# .gitignore ga qo'shilishi shart:
.env
.env.*
*.pem
*.key
*.cert
secrets.*
credentials.*
```

#### [MED-02] LocalStorage ma'lumotlarida tamg'alash (tampering) va Schema validatsiyasi yo'qligi
* **Fayl va qator:** `index.html:2372, 2381`
* **Muammo:** `localStorage.getItem('olmos_gold_wishlist_v2')` va cart ob'ektlari tekshirilmasdan o'qiladi.
* **Hujum stsenariysi:** Foydalanuvchi konsol orqali savatidagi narxlarni `price: 1` qilib o'zgartirishi va bu soxta narx adminga Telegram buyurtmasi sifatida yetib borishi mumkin.
* **Aniq Fix Kodi:**
```javascript
function getVerifiedCart() {
  const raw = localStorage.getItem('olmos_gold_cart_v2');
  if (!raw) return [];
  try {
    const items = JSON.parse(raw);
    // Narxlarni do'konning haqiqiy katalogi (products massivi) bilan solishtirib tekshirish:
    return items.map(item => {
      const realProduct = products.find(p => p.id === item.id);
      return realProduct ? { ...item, price: realProduct.price } : null;
    }).filter(Boolean);
  } catch (e) {
    return [];
  }
}
```

---

### LOW (Kichik kamchiliklar)

#### [LOW-01] Doimiy autentifikatsiyalangan mijoz sessiyasi yo'qligi
* **Fayl va qator:** `index.html` (Umumiy arxitektura)
* **Muammo:** Mijoz brauzerini almashtirganda yoki keshini tozalaganda uning barcha tanlagan zargarlik buyumlari (wishlist/cart) o'chib ketadi.
* **Hujum stsenariysi:** Xavfsizlik xuruji emas, biroq xarid tajribasiga va konversiyaga salbiy ta'sir ko'rsatadi.
* **Aniq Fix Kodi:** Kelajakda yengil Telegram WebApp / Login Widget yoki havola orqali savatni tiklash (Share Cart Link `?cart=id1,id2`) imkoniyatini yaratish.

---

## 3. Secret Rotation Rejasi (Telegram Bot Token uchun)

> **DIQQAT:** Qoidaga ko'ra, token avtomatik almashtirilmadi. Quyidagi qadamlar do'kon egasi tomonidan Telegram orqali qo'lda amalga oshirilishi kerak:

1. **Telegramda @BotFather ga kiring:**
   * `/mybots` buyrug'ini yuboring.
   * Mavjud botni tanlang.
   * `API Token` bo'limiga kiring.
   * **`Revoke current token`** tugmasini bosing (eski fosh bo'lgan token darhol bekor qilinadi).
2. **Yangi tokenni saqlash:**
   * Yangi tokenni hech qachon `index.html` yoki frontend fayllariga qo'ymang!
   * Agar avtomatik bot xabarlari kerak bo'lsa, xavfsiz bepul serverless proxy (masalan, Cloudflare Workers yoki Netlify Functions) ochib, tokenni o'sha joyda Environment Variable sifatida saqlang.
   * Hozirgi bosqichda eng xavfsiz va tezkor yechim: Buyurtmalarni **Telegram Direct Link** (`https://t.me/OLMOS_GOLD?text=...`) orqali yuborish (bu usulda hech qanday token talab qilinmaydi va 100% xavfsiz).

---

## 4. Rollback (Orqaga Qaytish) Rejasi

Agar Telegram bot tokeni olib tashlangandan so'ng xabarlashuvda uzilish sezilsa:
1. `index.html` dagi barcha buyurtma tugmalari standart `window.open("https://t.me/OLMOS_GOLD?text=...", "_blank")` funksiyasiga ulanganligini tekshirish.
2. Git orqali zaxira versiyaga qaytish:
   ```bash
   git revert HEAD
   ```

---

## 5. Agar Hech Narsa Tuzatilmasa, Eng Ehtimolli 3 Ta Buzilish Stsenariysi

1. **Botning to'liq egallab olinishi va o'chirilishi (Bot Takeover & Account Ban):**
   Ochiq qolgan `TG_BOT_TOKEN` tufayli tajovuzkor Telegram API orqali botni o'z boshqaruviga oladi, spam/noqonuniy xabarlar jo'natadi va natijada Telegram ma'muriyati botni butunlay bloklaydi. Do'kon barcha mijoz buyurtmalaridan uzilib qoladi.
2. **Admin hisobiga fishing va spam hujumi (Denial of Service & Phishing):**
   `TG_ADMIN_CHAT_ID` va ochiq `sendTelegramLeadNotification()` orqali skriptlar yordamida har daqiqada minglab soxta buyurtmalar yuboriladi. Do'kon menejeri haqiqiy mijozlarni soxta xabarlardan ajrata olmay qoladi.
3. **Kesh va narx manipulyatsiyasi (Price & Order Tampering):**
   Mijoz tomonidan kiritiladigan buyurtma narxi katalog bilan tekshirilmagani sababli, xaridor $673 lik 18K Marquise uzukni $1 qilib yuborishi va operatorni adashtirib nizoli vaziyat keltirib chiqarishi mumkin.
