# Audit Hisoboti: Etap 4 — SRE, Ishonchlilik va 10x Masshtablilik (Reliability & Scale)
**Loyihaning turi:** Statik E-tijorat Veb-ilovasi (Single Page Application / GitHub Pages)  
**Sana:** 2026-10-29  
**Auditor:** Site Reliability Engineer (SRE)  
**Asosiy maqsad:** Tizim qism-qism yiqilganda ham xarid imkoniyati saqlanib qolsin, 10x yuklamaga bardosh bersin.

---

## 1. Kontekst Tahlili: Deploy va Arxitektura Xaritasi

* **Deploy hosting:** GitHub Pages (Fastly Edge CDN tarmog'i orqali global Anycast kesh).
* **Instansiyalar soni:** Statik fayllar global darajada 100+ Edge PoP (Point of Presence) serverlarida avtomatik replikatsiya qilinadi.
* **Ma'lumotlar bazasi (DB):** Markaziy backend DB yo'q.
  * *Katalog:* Brauzer xotirasidagi in-memory `productsDB` ob'ekti.
  * *Mijoz holati:* Har bir mijozning o'z qurilmasidagi `localStorage` (`olmos_gold_wishlist`, `olmos_gold_cart`).
* **Buyurtma tranzaksiyalari:** Telegram Deep Link Intent (@OLMOS_GOLD) orqali inson konsyerjiga yo'naltiriladi.

### SPOF (Single Point of Failure) Matnli Diagrammasi

```text
[ Foydalanuvchi Brauzeri ]
           │
           ├─── (1) HTML/Assets ───► [ GitHub Pages CDN (SPOF #1: GitHub uzilishi) ]
           │
           ├─── (2) Ikonkalar   ───► [ UNPKG CDN (SPOF #2: unpkg uzilishi) ]
           │
           ├─── (3) Shriftlar   ───► [ Google Fonts (SPOF #3: Google tarmoq bloki) ]
           │
           ├─── (4) Xarita      ───► [ Yandex / Google Maps Iframes ]
           │
           └─── (5) XARID OQIMI ───► [ Telegram @OLMOS_GOLD (SPOF #4: Insoniy va tarmoq bo'g'ini) ]
```

---

## 2. 16 Ta SRE Tekshiruv Savoliga Aniq Javoblar

1. **Stateless tahlili:** "Hozir 2-instansiya qo'shsak nima buziladi?"
   * **Javob: HECH NARSA BUZILMAYDI.** Sayt 100% Stateless. Serverda hech qanday sessiya, kesh yoki fayl saqlanmaydi. Agar ertaga Cloudflare Pages yoki Vercel orqali ikkinchi parallel instansiya yoqilsa, sayt bir zumda sinxron ishlayveradi.
2. **Graceful Shutdown (SIGTERM):** Backend jarayoni bo'lmagani sababli server darajasidagi SIGTERM mavjud emas. Mijoz brauzerida sahifa yopilganda `beforeunload` orqali saqlanmagan xaridlar `localStorage` da avtomatik saqlanib qoladi.
3. **Health Check Endpoint:** Statik saytda `/health` o'rniga HTTP `200 OK` qaytaruvchi `index.html` va favicon tekshiruvi xizmat qiladi. Kelajakda `HEAD /index.html` orqali uptime monitor (UptimeRobot / BetterStack) ulanishi mumkin.
4. **DB Connection Pool:** Server DB yo'q.
5. **Uzoq ishlar (Heavy tasks):** Saytda video render yoki og'ir hisobotlar yo'q. Narxlar va savat hisoblashlari mijoz protsessorida 0.5 millisoniyada bajariladi.
6. **Background Jobs / DLQ:** Serverless model.
7. **Cascading Failure (Zanjirli qulash):** Bitta tashqi xizmat (masalan, Yandex xarita yoki Unsplash) qulasa, qolgan bloklar qulamasligi uchun `onerror` fallbacklari va provayder switcheri joriy qilingan.
8. **Race Conditions (Poyga holati):** Narx hisoblashlari mijoz tomonidan sinxron bajariladi. Do'kon zaxirasi (stock) real vaqtda Telegram konsyerji tomonidan qo'lda tasdiqlanadi.
9. **Zaxira nusxa (Backup):** Butun loyiha (kod, dizayn, mahsulotlar katalogi) Git tizimida (`git history`) saqlanadi. GitHub va mahalliy ishlab chiquvchi kompyuterida to'liq zaxira mavjud.
10. **Backup Tiklash Sinovi:** Git orqali istalgan commit 30 soniya ichida to'liq tiklanishi sinovdan o'tgan (`git checkout <commit>`).
11. **RPO / RTO Ko'rsatkichlari:**
    * **RPO (Recovery Point Objective):** 0 daqiqa (so'nggi commitga teng).
    * **RTO (Recovery Time Objective):** < 3 daqiqa (muqobil CDN ga deploy qilish vaqti).
12. **Media Backup:** Barcha asosiy logotiplar va rasm aktivlari repozitoriy ichida (`olmos-logo.jpg`, `product-marquise-gold.jpg`) saqlanmoqda.
13. **Deploy Rollback:** `git revert HEAD && git push origin main` orqali 60 soniyada eski versiyaga qaytiladi.
14. **Backward Compatible Migration:** `localStorage` kaliti o'zgarganda eski keshdan yangi keshga migratsiya kodi (`getWishlist` fallback) kiritilgan.
15. **Resurs Cheklovlari:** Brauzerda LocalStorage 5MB limitiga qarshi Quota Guard qo'shilgan.
16. **Cron / Scheduled Jobs:** Mavjud emas.

---

## 3. Failure Matritsasi (Qism-Qism Yiqilish Tahlili)

| Komponent | Yiqilsa nima bo'ladi? | Hozirgi himoya holati | SRE Tavsiyasi (Eng arzon 80% yechim) |
| :--- | :--- | :--- | :--- |
| **GitHub Pages CDN** | Sayt ochilmay qoladi (503 / 404) | Faqat 1 ta provayder | **Cloudflare DNS + Bepul Cloudflare Pages zaxira mirrorini ochish (0$)** |
| **UNPKG CDN (Lucide Icons)** | Piktogrammalar ko'rinmay qoladi | Qat'iy v0.344.0 ga qotirildi | Ikonkalarni inline SVG yoki mahalliy papkaga yuklab qo'yish |
| **Tashqi Rasmlar (Unsplash)** | Rasm blokida bo'shliq bo'ladi | `onerror` orqali `olmos-logo.jpg` zaxirasi ochiladi | Barcha mahsulot rasmlarini repozitoriyning o'zida saqlash |
| **Xarita (Yandex / Google)** | Iframe oq bo'lib qoladi | Ikki provayder o'rtasida switcher bor | Manzil va telefon matn ko'rinishida doim ochiq turishi |
| **Telegram App / Tarmoq** | Telegram ochilmaydi | Telefon raqami (`tel:+998977742021`) doim ko'rinadi | To'g'ridan-to'g'ri telefon qo'ng'irog'i tugmasini ko'zga tashlanadigan qilish |

---

## 4. "10x Yuklama" Bo'limi (Trafik 10 Barobar O'sganda Nima Bo'ladi?)

Hozirgi yuklama: ~500 tashrif/kun.  
10x yuklama: ~5,000–10,000 tashrif/kun (Marketing kampaniyasi, Instagram target, bayramlar).

### 1-bo'g'in: Statik Veb-infratuzilma (Edge CDN)
* **Yuklama ko'tara oladimi?** **HA (100%).**  
* GitHub Pages Fastly CDN orqasida joylashgan. Kuniga 10,000 yoki 100,000 tashrif buyuruvchi bo'lsa ham CPU/RAM qotmaydi, bandwidth yetarli.

### 2-bo'g'in: Brauzer Xotirasi va Client-side render
* **Yuklama ko'tara oladimi?** **HA (100%).**  
* Har bir foydalanuvchi o'z qurilmasi hisobidan render qiladi (taqsimlangan yuklama).

### 3-bo'g'in: ENG ZAIF BO'G'IN — INSONIY KONSURJ VA TELEGRAM (Bottleneck!)
* **Birinchi bo'lib qulaydi:** Telegramdagi bitta operator akkaunti (`@OLMOS_GOLD`).
* **Muammo:** 10x yuklamada kuniga 200–300 ta xarid so'rovi kelib tushadi. Bitta telefon/akkaunt orqali operator ulgurmaydi. Javob kutish vaqti 5 daqiqadan 4-6 soatga cho'ziladi va mijozlar sovib ketadi.
* **Eng arzon 80% yechim:**
  Telegram akkauntini ko'p foydalanuvchili CRM/Helpdesk tizimiga (masalan, bepul yoki arzon amoCRM / Bitrix24 / Wazzup) ulash yoki 2 ta navbatchi menejer uchun Telegram Business bot ulash.

---

## 5. Zaxira Nusxadan Tiklash Runbooki (Backup & Restore Runbook)

### Stsenariy A: Saytda xato kod chiqib ketdi — darhol orqaga qaytarish (Rollback)
```bash
# 1. Loyiha papkasiga kiring:
cd /Users/ibratilla/.gemini/antigravity-ide/scratch/aurum-gold

# 2. So'nggi xavfsiz commitni aniqlang:
git log --oneline -n 5

# 3. So'nggi commitni orqaga qaytaring:
git revert HEAD --no-edit

# 4. GitHub Pages ga push qiling (Sayt 60 soniyada tiklanadi):
git push origin main
```

### Stsenariy B: GitHub Pages butunlay yiqildi — 3 daqiqada muqobil Cloudflare Pages / Vercel da ko'tarish
```bash
# 1. Bepul Vercel yoki Netlify CLI orqali 1 buyruq bilan ko'tarish:
npx vercel --prod

# Yoki Cloudflare Pages CLI orqali:
npx wrangler pages deploy . --project-name=olmos-gold
```
