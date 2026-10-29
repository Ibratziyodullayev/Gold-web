---
name: data-modeling
description: Zargarlik mahsulotlari sxemasi, Schema.org JSON-LD semantikasi, savat modeli va LocalStorage ma'lumotlar migratsiyasini standartlashtirishda ishlatiladi. Triggerlar: data_model, schema, json_ld, product_schema, cart_model, migration.
---

# Data Modeling (E-commerce Entities & Schema.org)

## Qachon ishlatiladi
Zargarlik buyumlari katalogi strukturasini standartlashtirish, har xil metallar va olmos xususiyatlarini aniq tavsiflash, Google qidiruv tizimi uchun boy natijalar (Rich Snippets / Schema.org) yaratish va LocalStorage dagi ma'lumotlar strukturasi o'zgarganda xatoliklarsiz migratsiya qilishda ishlatiladi.

## Checklist
1. **To'liq Zargarlik Mahsulot Sxemasi:** Har bir mahsulotda `id`, `sku`, `name_uz`, `name_ru`, `price_usd`, `metal_type` (18k_yellow/rose/white), `gemstone` (olmos, zumrad), `carat`, `images[]` mavjudligi.
2. **Schema.org JSON-LD (Product & Offer):** Google qidiruvida narx, valyuta, mavjudlik holati (`InStock`) chiqishi uchun to'g'ri JSON-LD skripti bo'lishi.
3. **LocalBusiness Schema:** Do'kon nomi (`OLMOS GOLD`), manzili (`Bunyodkor 15/1`), telefon raqami va ish vaqti Googlega tushunarli formatda berilishi.
4. **Savat Elementi Modeli (Cart Item):** Mahsulot varianti (tanlangan metall va uzuk o'lchami) alohida noyob kalit bilan saqlanishi (masalan, `prod_1_18k_yellow_size_17`).
5. **Storage Migratsiyasi (Versioning):** Agar ma'lumot formati o'zgarsa (v1 -> v2), foydalanuvchining eski savati buzilmasdan yangi formatga o'tkazilishi.
6. **Narxlar aniqligi:** Narxlar doimo sof raqamda saqlanishi (`price: 673`), string yoki belgi bilan aralashmasligi (`price: "$673"` anti-pattern).
7. **Ikkilamchi til modellari:** Barcha mahsulot tavsiflari va xarakteristikalari o'zbek va rus tillari uchun alohida maydonlarda saqlanishi.

## Anti-patterns
- **Raqamli narx o'rniga formatlangan matn saqlash:** `price: "673 $"` yoki `"8 600 000 so'm"` — keyinchalik filtrlash, saralash va valyuta o'zgartirishni butunlay ishdan chiqaradi.
- **Variantlarni hisobga olmaslik:** 16-o'lchamdagi uzuk va 18-o'lchamdagi uzuk savatda bir xil element deb hisoblanishi.
- **Eski kesh migratsiyasiz qolishi:** Kalit o'zgarganda eski foydalanuvchilarda oq sahifa (TypeError) yuz berishi.

## Fix recipes

### 1. Zargarlik Mahsulotining Standart Ob'ekti (Clean Data Contract)
```javascript
const ProductModel = {
  id: "og-marquise-01",
  sku: "RNG-MQ-18KY-01",
  title: {
    uz: "18K Sariq Oltin Marquise Brilliant Uzuk",
    ru: "Кольцо с бриллиантом огранки Маркиз 18К"
  },
  price_usd: 673,
  specs: {
    metal: "18K Sariq Oltin (750 probali)",
    diamond_carat: 0.50,
    diamond_cut: "Excellent",
    diamond_clarity: "VS1",
    weight_grams: 3.2
  },
  available_sizes: [16, 16.5, 17, 17.5, 18, 18.5, 19],
  images: [
    "product-marquise-gold.jpg"
  ],
  in_stock: true
};
```

### 2. Schema.org JSON-LD Standarti
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "18K Marquise Brilliant Uzuk",
  "image": "https://ibratziyodullayev.github.io/Gold-web/product-marquise-gold.jpg",
  "description": "Tabiiy brilliant va 750 probali Italiya oltinidan tayyorlangan eksklyuziv uzuk.",
  "sku": "RNG-MQ-18KY-01",
  "brand": {
    "@type": "Brand",
    "name": "OLMOS GOLD"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://ibratziyodullayev.github.io/Gold-web/",
    "priceCurrency": "USD",
    "price": "673",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "JewelryStore",
      "name": "OLMOS GOLD JEWELLERY",
      "address": "Toshkent, Bunyodkor ko'chasi 15/1"
    }
  }
}
</script>
```

## Tekshirish buyruqlari
```bash
# 1. Mahsulotlar massividagi barcha kalitlarni tahlil qilish
grep -n "price:" index.html | head -n 10

# 2. Schema.org JSON-LD mavjudligini tekshirish
grep -n "application/ld+json" index.html

# 3. LocalStorage kalit versiyalarini tekshirish
grep -n "_STORAGE_KEY" index.html
```
