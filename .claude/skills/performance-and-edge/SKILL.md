---
name: performance-and-edge
description: Core Web Vitals (LCP, CLS, INP), rasmlar optimizatsiyasi, fontlar yuklanishi va statik Edge keshini optimallashtirishda ishlatiladi. Triggerlar: performance, lcp, cls, inp, lighthouse, lazy_load, webp, edge.
---

# Performance and Edge (Core Web Vitals & Static Delivery)

## Qachon ishlatiladi
Sayt yuklanish tezligini oshirish, Google Lighthouse ballini 95+ ga yetkazish, mobil qurilmalarda LCP (Largest Contentful Paint) ni 1.8s dan kamaytirish va CLS (Cumulative Layout Shift) ni 0 ga tushirishda ishlatiladi.

## Checklist
1. **LCP Hero Image Optimization:** Birinchi ko'rinadigan mahsulot rasmi (Hero Marquise Ring) `fetchpriority="high"`, `loading="eager"` bilan yuklanishi, `loading="lazy"` berilmasligi.
2. **Katalog Rasmlari (Lazy Loading):** Ekranning pastki qismidagi barcha mahsulot rasmlarida `loading="lazy"` va `decoding="async"` mavjudligi.
3. **Layout Shift (CLS = 0):** Barcha `<img>` teglarida aniq `width`, `height` yoki CSS `aspect-ratio` bo'lishi (rasm yuklanguncha joy sakramaydi).
4. **Font Preconnect & Display Swap:** Google Fonts havolalarida `rel="preconnect"` va har bir shriftda `&display=swap` o'rnatilganligi.
5. **Tailwind CDN o'rniga ishlab chiqarish CSS:** Ishlab chiqarishda brauzerda 300KB Tailwind JIT runtime kompilyatorini ishlatmaslik, faqat ishlatilgan CSS sinflarini yuklash.
6. **Edge Caching Headers:** GitHub Pages va brauzer uchun statik assetlar (rasmlar, shriftlar) uzoq muddatli keshlanishi.
7. **DOM hajmi va murakkabligi:** Jami DOM elementlari soni 1500 tadan oshmasligi.

## Anti-patterns
- **Birinchi ekrandagi rasmga `loading="lazy"` berish:** LCP 2-3 barobar kechikadi.
- **Rasm o'lchamlarini ko'rsatmaslik:** rasm yuklanganda butun sahifa pastga sakraydi (katta CLS jarimasi).
- **Katta og'irlikdagi rasm formatlari:** 2-3 megabaytli siqilmagan PNG/JPG rasmlarni to'g'ridan-to'g'ri ko'rsatish (WebP/AVIF o'rniga).

## Fix recipes

### 1. LCP va CLS ni 0 ga tushirish uchun rasm tegi
```html
<!-- Hero / LCP Asosiy Rasm -->
<img 
  src="product-marquise-gold.jpg" 
  alt="18K Marquise Brilliant Uzuk" 
  width="600" 
  height="600" 
  fetchpriority="high"
  decoding="async"
  class="w-full h-auto aspect-square object-cover rounded-md shadow-sm"
/>

<!-- Katalogdagi pastki rasmlar -->
<img 
  src="${product.image}" 
  alt="${product.name}" 
  width="400" 
  height="400" 
  loading="lazy"
  decoding="async"
  class="w-full h-auto aspect-square object-cover"
/>
```

### 2. Shriftlarni kechiktirmasdan yuklash (Preconnect)
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700&family=Tenor+Sans&display=swap" rel="stylesheet">
```

## Tekshirish buyruqlari
```bash
# 1. Rasmlarda width/height yoki aspect-ratio mavjudligini tekshirish
grep -n "<img" index.html | head -n 10

# 2. Hero rasmda fetchpriority="high" mavjudligini tekshirish
grep -n "fetchpriority" index.html

# 3. Fayl hajmini tekshirish
ls -lh index.html *.jpg *.png 2>/dev/null
```
