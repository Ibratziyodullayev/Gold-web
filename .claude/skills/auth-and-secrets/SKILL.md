---
name: auth-and-secrets
description: Statik e-tijorat va mijoz brauzeri muhitida maxfiy kalitlar, Telegram bot tokenlari, auth sessiyalar va xavfsiz ma'lumotlarni boshqarishda ishlatiladi. Triggerlar: secrets, api_key, token, auth, session, telegram_bot_token.
---

# Auth and Secrets (Vanilla Static / GitHub Pages Stack)

## Qachon ishlatiladi
Ushbu skill loyihada API kalitlar (Telegram Bot token, xarita provayderi kalitlari, to'lov shlyuzlari), mijoz tomonidagi sessiyalar (localStorage, cookie), shaxsiy ma'lumotlar (mijoz telefon raqamlari, buyurtma tafsilotlari) va GitHub omborida maxfiy ma'lumotlar oshkor bo'lishining oldini olish uchun ishlatiladi.

## Checklist
1. **GitHub Pages ochiq manba tekshiruvi:** `index.html` yoki JS skriptlarda hech qanday maxfiy token (masalan, Telegram Bot Token `bot<token>/sendMessage`) ochiq yozilmaganligini tasdiqlash.
2. **Telegram Concierge xavfsiz modeli:** Telegram bot tokenini brauzerga qo'ymasdan, xavfsiz URL intent (`https://t.me/OLMOS_GOLD?text=...`) orqali to'g'ridan-to'g'ri mijoz appiga uzatish.
3. **LocalStorage ma'lumotlar gigiyenasi:** `localStorage` da foydalanuvchining shaxsiy to'lov kartalari, parollar yoki maxfiy identifikatorlar saqlanmasligi.
4. **Git tarixini tozalash:** `.git` tarixida o'tmishda qoldirilgan `.env`, API kalitlar yoki tokenlar yo'qligini tekshirish.
5. **Uchinchi tomon API kalitlari cheklovi:** Agar Mapbox/Google Maps ishlatilsa, kalit faqat `https://ibratziyodullayev.github.io/Gold-web/*` domeni uchun HTTP Referrer chekloviga ega bo'lishi.
6. **Admin kirish huquqlari:** Statik saytda soxta mijoz admin panel bo'lmasligi yoki admin funksiyalar server tomoni himoyasisiz JS ichida qoldirilmasligi.
7. **XSS orqali sessiya o'g'irlanishi:** `localStorage.getItem('olmos_gold_cart_v2')` va `wishlist` ma'lumotlarini manipulatsiya qilish orqali foydalanuvchi hisobiga zarar yetkazilmasligi.

## Anti-patterns
- **Telegram Bot API tokenini brauzerda saqlash:** `fetch("https://api.telegram.org/bot123456:ABC-DEF/sendMessage")` ni bevosita `index.html` ga yozish. Oqibat: bot token 5 soniyada o'g'irlanadi va bot spam/hujum uchun ishlatiladi.
- **Maxfiy narx chegirmalari va promo-kodlarni ochiq JS ob'ektida saqlash:** mijoz kodni o'qib ixtiyoriy 99% chegirma yasashi.
- **Shaxsiy telefon raqamlarni LocalStorage ga shifrlanmasdan uzoq muddatga saqlash.**

## Fix recipes

### 1. Telegram xavfsiz Concierge URL Intent (Token talab qilmaydi)
```javascript
// YOMON (Token ochiladi):
// fetch(`https://api.telegram.org/bot${BOT_SECRET}/sendMessage?chat_id=${CHAT_ID}&text=${msg}`);

// TO'G'RI (Client-side xavfsiz intent):
function sendToTelegramConcierge(orderData) {
  const safeText = encodeURIComponent(
    `✨ OLMOS GOLD — Yangi Buyurtma\n` +
    `Mahsulot: ${orderData.name}\n` +
    `Metall: ${orderData.metal}\n` +
    `Narxi: $${orderData.price}\n` +
    `Aloqa: ${orderData.phone || 'Telegram orqali'}`
  );
  window.open(`https://t.me/OLMOS_GOLD?text=${safeText}`, '_blank', 'noopener,noreferrer');
}
```

### 2. LocalStorage tozalash va xavfsiz tekshiruv
```javascript
// Xavfsiz o'qish (malformed JSON yoki zararli payloadga qarshi)
function getSafeStorage(key, defaultValue = []) {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return defaultValue;
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : defaultValue;
  } catch (e) {
    console.warn(`[Storage] Xato kalit: ${key}, tozalandi.`, e);
    localStorage.removeItem(key);
    return defaultValue;
  }
}
```

## Tekshirish buyruqlari
```bash
# 1. Kod ichida ehtimoliy API tokenlar, kalitlar va bot parollarini qidirish
grep -Ei "(bot[0-9]{8,}:|api[_-]?key|secret|password|bearer|auth[_-]?token)" index.html

# 2. Git commit tarixida maxfiy ma'lumotlar borligini tekshirish
git log -S "bot" -p -n 5
git log -S "token" -p -n 5

# 3. .gitignore faylida maxfiy fayllar kiritilganini tekshirish
cat .gitignore
```
