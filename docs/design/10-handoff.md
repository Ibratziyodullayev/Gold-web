# Dizayn Topshirish Hujjati (docs/design/10-handoff.md)

Ushbu spetsifikatsiya frontend dasturchilar va mahsulot jamoasi uchun OLMOS GOLD JEWELLERY vebsaytining dizayn tizimi, komponentlar qoidalari va arxitekturaviy talablarini belgilaydi.

---

## 1. Asosiy Dizayn Tokenlari (Design Tokens)

### 1.1 Ranglar Palitrasi (Color Palette)
- **Fon:** `#FAF9F6` (Issiq Oq Fil Suyagi fon), `#FFFFFF` (Kartalar va modallar foni)
- **Noble Gold Deep (Matn va Urg'ular):** `#68481D` (Kontrast 6.8:1 oq fonda — WCAG AA va AAA)
- **Noble Gold Accent (Tugmalar va Chegaralar):** `#835E21`
- **Asosiy Matn:** `#111113` (Chuqur Qora — Kontrast 16.2:1)
- **Yordamchi Matn:** `#4B4E5B` (Sokin Kulrang — Kontrast 7.1:1)
- **Muvaffaqiyat (Success):** `#2D7A4F`
- **Xatolik / Sevimlilar (Rose/Error):** `#C43826` / `#E11D48`

### 1.2 Shriftlar (Typography - DiamondsByUK Benchmark)
- **Sarlavhalar va Brend:** `Tenor Sans, sans-serif`
  - Display: `36px - 40px`, `leading-tight`
  - H1: `28px - 32px`
  - H2: `22px - 24px`
  - H3: `18px - 20px`
- **Matn va Narxlar:** `Figtree, sans-serif`
  - Body: `14px - 15px`, `leading-relaxed`
  - Small / UI: `12px - 13px`
  - Caption: `10px - 11px`, `tracking-wider uppercase`
  - Price: `Tenor Sans + Figtree`, `font-bold tabular-nums`

### 1.3 Spacing (8px Grid)
- `2 (8px)`, `3 (12px)`, `4 (16px)`, `6 (24px)`, `8 (32px)`, `12 (48px)`, `16 (64px)`

### 1.4 Soyalar va Burchaklar
- `border-radius`: `rounded-sm (2px)` yoki `rounded-[4px]` (Qat'iy hashamatli burchaklar)
- `box-shadow`:
  - Card Default: `0 4px 20px -2px rgba(27, 30, 40, 0.04), 0 2px 6px -1px rgba(0, 0, 0, 0.02)`
  - Card Hover: `0 14px 32px -4px rgba(27, 30, 40, 0.08), 0 4px 12px -2px rgba(0, 0, 0, 0.03)`

---

## 2. Komponentlar Arxitekturasi

### 2.1 Tugmalar (Buttons)
- **Minimal teginish maydoni:** Barcha mobil tugmalar kamida `44x44px` bo'lishi shart (`.touch-target-44` yoki `min-h-[44px]`).
- **Focus visible:** Har bir interaktiv tugmada klaviatura orqali boshqaruv uchun `:focus-visible` oltin konturi (`outline: 2px solid #835E21; outline-offset: 2px`) mavjud.
- **Loading holati:** Formani yuborishda tugma ichida `.btn-spinner` ko'rsatiladi va tugma `disabled` qilinadi.

### 2.2 Modallar va Dialoglar (A11y & Popstate)
- Barcha modallarda:
  - `role="dialog"`
  - `aria-modal="true"`
  - `aria-labelledby="{id}"`
- Modal ochilganda:
  - `history.pushState({ modal: '...', id: '...' }, '', '#...')` chaqiriladi.
  - Orqaga tugmasi (Popstate) yoki `ESC` bosilganda modal silliq yopiladi.

---

## 3. Kodni Saqlash Qoidalari
1. To'g'ridan-to'g'ri yangi ranglarni ad-hoc kiritmaslik — faqat tokenizatsiyalangan ranglardan foydalanish.
2. Matn o'lchamlarini `text-[7px]` yoki `text-[8px]` kabi o'qilmaydigan darajaga tushirmaslik.
3. Yangi tugma yoki belgi qo'shilganda uning minimal teginish maydoni 44px dan kichik bo'lmasligini ta'minlash.
