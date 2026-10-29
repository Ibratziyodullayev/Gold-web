---
name: api-integration-hardening
description: Tashqi API'lar, CDN kutubxonalari, Leaflet xaritalari, Telegram linklari va rasm resurslari barqarorligini mustahkamlashda ishlatiladi. Triggerlar: api, cdn, fetch, network, leaflet, telegram_link, tile_server.
---

# API Integration Hardening (Static Web & CDN Stack)

## Qachon ishlatiladi
Tashqi CDN'lar (Tailwind, FontAwesome, Leaflet), OpenStreetMap tile serverlari, Telegram havolalari yoki tashqi rasm hostinglari (Cloudinary, Unsplash) ishlamay qolganda, tarmoq uzilganda yoki sekinlashganda sayt to'xtab qolmasligi va xatoliklarni xavfsiz boshqarish uchun qo'llaniladi.

## Checklist
1. **CDN Fallback mexanizmi:** Tailwind CDN, FontAwesome yoki Leaflet yuklanmay qolsa, sahifa qotib qolmasligi yoki konsolda xatolik berib to'xtab qolmasligi.
2. **Subresource Integrity (SRI):** Barcha uchinchi tomon script va CSS linklarida `integrity="sha384-..."` va `crossorigin="anonymous"` mavjudligi.
3. **Telegram Intent URL validation:** Foydalanuvchi ma'lumotlari (`name`, `phone`, `items`) `encodeURIComponent()` orqali to'liq ekranlanganligi, maxsus belgilar URL buzilishiga olib kelmasligi.
4. **Leaflet Tile Error Handling:** OpenStreetMap tile'lari 429 (Rate Limit) yoki 503 bersa, xarita o'rniga do'konning aniq manzili va static fallback ko'rsatilishi.
5. **Rasm yuklanish xatoliklari (Image error fallbacks):** Har bir `<img>` elementida `onerror` zaxira rasmi (`olmos-logo.jpg` yoki inline SVG placeholder) borligi.
6. **Tarmoq holati (Offline/Online detection):** Foydalanuvchi interneti uzilib qolganda Telegram yoki buyurtma tugmasi bosilsa, foydalanuvchiga aniq bildirishnoma ko'rsatish.
7. **Timeout va AbortController:** Kelajakdagi har qanday `fetch()` so'rovlari uchun qat'iy timeout (masalan, 8000ms) o'rnatilganligi.

## Anti-patterns
- **SRI hesiz tashqi skriptlarni yuklash:** `<script src="https://cdnjs.cloudflare.com/..."></script>` buzilsa, butun saytga zararli kod in'ektsiya qilinishi mumkin.
- **URL parametrlarini ekranlamaslik:** `https://t.me/OLMOS_GOLD?text=` ga to'g'ridan-to'g'ri `&` yoki `#` belgisi bor mahsulot nomini qo'shib yuborish.
- **Zaxirasiz tashqi rasm URL'lariga bog'lanish:** Unsplash yoki Cloudinary rasm o'chib ketsa, mahsulot kartasi singan ikonka ko'rsatib qolishi.

## Fix recipes

### 1. Rasm yuklanish xatoligini to'g'rilash (Image Fallback)
```javascript
// index.html dagi mahsulot renderlash funksiyasida:
function getSafeProductImage(url, fallback = 'olmos-logo.jpg') {
  return `
    <img 
      src="${url}" 
      alt="Olmos Gold Zargarlik Mahsuloti"
      loading="lazy"
      decoding="async"
      onerror="this.onerror=null; this.src='${fallback}'; this.classList.add('fallback-img');"
      class="w-full h-full object-cover transition duration-700"
    />
  `;
}
```

### 2. Leaflet Xarita xatoliklarini himoyalash
```javascript
function initSafeStoreMap() {
  const mapContainer = document.getElementById('store-map');
  if (!mapContainer || typeof L === 'undefined') {
    if (mapContainer) {
      mapContainer.innerHTML = `
        <div class="flex flex-col items-center justify-center h-full p-6 text-center bg-ivory-100 text-ink-700">
          <p class="font-bold">Manzilimiz: Toshkent sh., Bunyodkor ko'chasi 15/1</p>
          <a href="https://maps.google.com/?q=41.2858,69.2035" target="_blank" class="mt-2 text-gold-700 underline font-semibold">
            Google Xaritada Ko'rish &rarr;
          </a>
        </div>`;
    }
    return;
  }
  try {
    const map = L.map('store-map').setView([41.2858, 69.2035], 16);
    const tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap'
    });
    tileLayer.on('tileerror', function() {
      console.warn('Xarita qatlami yuklanmadi, tarmoqni tekshiring.');
    });
    tileLayer.addTo(map);
  } catch (err) {
    console.error('Xaritani yuklashda xatolik:', err);
  }
}
```

## Tekshirish buyruqlari
```bash
# 1. Barcha tashqi script va CSS resurslarini tekshirish
grep -E "(src=|href=)[\"']http" index.html

# 2. SRI (integrity) atributi mavjudligini sanash
grep -c "integrity=" index.html

# 3. onerror atributi qo'llangan rasmlar sonini aniqlash
grep -c "onerror=" index.html
```
