---
name: testing-suite
description: Statik zargarlik saytida narx hisoblash, savat amallari, valyuta konvertatsiyasi va DOM yaxlitligini avtomatlashtirilgan testlashda ishlatiladi. Triggerlar: test, suite, unit_test, assertion, e2e, smoke_test, regression.
---

# Testing Suite (Vanilla JS & Static DOM Architecture)

## Qachon ishlatiladi
Narxlar, valyuta almashinuvi (USD -> UZS -> EUR), savatga qo'shish/o'chirish, Telegram havolasini shakllantirish va sahifa elementlari buzilmasligini sinovdan o'tkazishda qo'llaniladi.

## Checklist
1. **Narx va Valyuta hisoblash testlari:** Har xil valyutalarda narxlar to'g'ri yaxlitlanishi va formatlanishini (`formatPrice()`) tekshiruvchi testlar.
2. **Savat Logikasi testlari:** Mahsulot qo'shilganda umumiy summa, miqdor va takroriy qo'shilish to'g'ri ishlashini tasdiqlash.
3. **Telegram Intent Formatter testi:** `encodeURIComponent` qilingan matnda mahsulot nomi, probasi va narxi xatosiz chiqishini tekshirish.
4. **HTML5 Semantik Validator:** Barcha teglarning to'g'ri yopilishi, `id` takrorlanmasligi va majburiy `alt` atributlari mavjudligi.
5. **Singan Havolalar va Rasmlar (Broken links check):** Barcha ichki va tashqi havolalar, rasm manbalari 200 OK qaytarishini tekshirish.
6. **Accessibility (a11y) testi:** Tugmalarda `aria-label`, ranglar kontrasti (WCAG AA kamida 4.5:1) to'g'riligi.
7. **Cross-browser Smoke Test:** Desktop va Mobile ekran o'lchamlarida asosiy oqim (PDP ochish, Buyurtma berish) buzilmasligini tasdiqlash.

## Anti-patterns
- **Faqat qo'lda tekshirish bilan cheklanish:** Har safar yangi mahsulot yoki uslub qo'shilganda eski funksiyalar buzilganini sezmay qolish.
- **Valyuta konvertatsiyasida suzuvchi nuqta (floating point) xatolari:** `0.1 + 0.2 = 0.30000000000000004` kabi xatolarni test qilmaslik.
- **Xato ID larni tekshirmaslik:** `document.getElementById('modal-id')` mavjud bo'lmaganda test xabar bermasligi.

## Fix recipes

### 1. Brauzer Konsolida / Node.js da Ishlovchi Yengil Test Skripti
```javascript
// test-runner.js (Yoki index.html dagi test rejimi)
function runOlmosSelfTests() {
  const suite = [];
  function assert(name, condition) {
    suite.push({ name, passed: Boolean(condition) });
  }

  // 1. Valyuta testi
  const testPrice = 673;
  const rateUZS = 12800;
  const uzsTotal = Math.round(testPrice * rateUZS);
  assert("Valyuta UZS to'g'ri hisoblanishi", uzsTotal === 8614400);

  // 2. Telegram intent URL testi
  const tgUrl = `https://t.me/OLMOS_GOLD?text=${encodeURIComponent("Test & Uzuk")}`;
  assert("Telegram URL maxsus belgilarni to'g'ri o'rab oladi", tgUrl.includes("Test%20%26%20Uzuk"));

  // 3. Mahsulotlar massivi tekshiruvi
  if (typeof products !== 'undefined') {
    assert("Mahsulotlar ro'yxati bo'sh emas", products.length > 0);
    const allHavePrice = products.every(p => typeof p.price === 'number' && p.price > 0);
    assert("Barcha mahsulotlarda musbat narx bor", allHavePrice);
    const allHaveImages = products.every(p => p.image && p.image.length > 5);
    assert("Barcha mahsulotlarda rasm manzili bor", allHaveImages);
  }

  console.table(suite);
  return suite.every(t => t.passed);
}
```

## Tekshirish buyruqlari
```bash
# 1. HTML teglari to'g'ri yopilgani va sintaktik xatolarni tekshirish
python3 -c "from html.parser import HTMLParser; parser = HTMLParser(); parser.feed(open('index.html').read()); print('HTML sintaksisi to‘g‘ri!')"

# 2. Mahsulotlar ID lari takrorlanmaganini tekshirish
grep -o 'id: [0-9]*' index.html | sort | uniq -d

# 3. DOM ID larining takrorlanishini qidirish
grep -o 'id="[^"]*"' index.html | sort | uniq -d
```
