---
name: reliability-and-scale
description: Brauzer xotirasi (memory leaks), LocalStorage kvotalari, statik yuklamalar va mobil qurilmalarda barqaror ishlashni ta'minlashda ishlatiladi. Triggerlar: reliability, scale, memory, leak, quota, localStorage, performance_crash.
---

# Reliability and Scale (Client-Side & Static Architecture)

## Qachon ishlatiladi
Foydalanuvchilar soni ko'payganda, zaif smartfonlarda xotira to'lib ketishi (RAM leak), `localStorage` 5MB limitidan oshib ketishi, qayta-qayta ochilgan modal va animatsiyalar sababli brauzer qotib qolishini bartaraf etishda qo'llaniladi.

## Checklist
1. **LocalStorage Quota Guard:** `localStorage.setItem()` doimo `try...catch (e)` bloki bilan o'ralgan bo'lishi (`QuotaExceededError` holatida eski keshni tozalash).
2. **Event Listener Memory Leaks:** Qayta render bo'ladigan komponentlarda (filtrlar, mahsulot kartalari) eski event listenerlar olib tashlanishi yoki hodisalar delegatsiyasi (Event Delegation) ishlatilishi.
3. **Timer va Interval tozaligi:** Modallar yoki avtomatik slaydlar yopilganda `clearInterval()` va `clearTimeout()` chaqirilishi.
4. **Statik Fayl Keshi va Versiyalash:** CSS va JS yangilanishlari foydalanuvchilarga darhol yetib borishi uchun versiya kesh busteri (`?v=3.1`) bo'lishi.
5. **Katta DOM masshtabliligi:** 100+ zargarlik mahsulotlari qo'shilganda DOM renderini bloklamaslik uchun sahifalash (pagination) yoki "Ko'proq yuklash" (infinite scroll/lazy rendering) bo'lishi.
6. **Brauzer orqaga/oldinga navigatsiyasi:** `popstate` va `hashchange` hodisalari orqali modal ochiq holatda brauzer orqaga tugmasi bosilganda to'g'ri ishlashi.
7. **Mobil Viewport va Scroll Barqarorligi:** Mobil Safari va Android Chrome'da `100vh` muammosini hal qilish uchun `100dvh` ishlatilganligi.

## Anti-patterns
- **Har bir mahsulot kartasiga alohida `addEventListener` qo'shish:** 50 ta mahsulot 10 marta filtrlanganda minglab eskirgan hodisalar xotirani to'ldiradi.
- **`localStorage.setItem()` ni tekshiruvsiz chaqirish:** Safari private browsing rejimida yoki xotira to'lganda butun JS ijrosi to'xtab qoladi.
- **Rasm preloadingni me'yordan oshirish:** Bir vaqtning o'zida 40 ta yuqori sifatli rasmni parallel yuklab mobil internet va xotirani quritish.

## Fix recipes

### 1. Xavfsiz LocalStorage Quota Guard
```javascript
function safeSetStorage(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (err) {
    if (err.name === 'QuotaExceededError' || err.code === 22) {
      console.warn('LocalStorage to‘ldi! Eski keraksiz kesh tozalanmoqda...');
      // Muhim bo'lmagan keshni tozalash
      localStorage.removeItem('temp_search_cache');
      try {
        localStorage.setItem(key, JSON.stringify(value));
      } catch (retryErr) {
        console.error('Qayta saqlash muvaffaqiyatsiz bo‘ldi', retryErr);
      }
    }
  }
}
```

### 2. Hodisalar delegatsiyasi (Event Delegation)
```javascript
// Har bir kartaga alohida listener ulamang:
// BAD: items.forEach(el => el.addEventListener('click', ...))

// GOOD: Bitta ota konteynerga listener ulang
const gridContainer = document.getElementById('products-grid');
if (gridContainer) {
  gridContainer.addEventListener('click', (e) => {
    const buyBtn = e.target.closest('[data-action="quick-buy"]');
    if (buyBtn) {
      const productId = buyBtn.dataset.productId;
      handleQuickBuy(productId);
      return;
    }
    const card = e.target.closest('[data-product-card]');
    if (card) {
      openProductDetails(card.dataset.productId);
    }
  });
}
```

## Tekshirish buyruqlari
```bash
# 1. To'g'ridan-to'g'ri try-catch siz chaqirilgan setItem larni topish
grep -n "localStorage.setItem" index.html

# 2. addEventListener chaqiruvlari sonini hisoblash
grep -n "addEventListener" index.html | wc -l

# 3. Kesh buster versiyalarini tekshirish
grep -E "\.(css|js|jpg|png)\?v=" index.html
```
