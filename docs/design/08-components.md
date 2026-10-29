# Komponentlar Spetsifikatsiyasi va Inventari (docs/design/08-components.md)

Ushbu hujjat **DiamondsByUK** standartidagi zargarlik brendi uchun ishlab chiqilgan komponentlar tizimini, ularning 10 ta holatini (default, hover, active, focus, disabled, loading, error, success, empty, selected) va kod darajasidagi Tailwind / CSS qoidalarini belgilaydi.

---

## 1. Asosiy Tugmalar (Buttons)

### 1.1 Variantlar
1. **Primary Luxury Button (`.btn-luxury-primary`):**
   - Fon: `#1B1E28` (Noble Charcoal) -> Hover: `#835E21` (Warm Honey Gold)
   - Matn: `#FFFFFF`, `font-sans font-medium text-[13px] tracking-[0.16em] uppercase`
   - Balandlik: `min-h-[50px]`, `px-8`, `rounded-full` (yoki DiamondsByUK kabi `rounded-none / rounded-[2px]`)
   - O'lcham: Minimal teginish maydoni (touch target) `min-h-[48px]`, `min-w-[48px]`.

2. **Secondary Outline Button (`.btn-luxury-outline`):**
   - Fon: `transparent` -> Hover: `#FBF8F5`
   - Chegara: `1.5px solid #1B1E28` -> Hover: `1.5px solid #835E21`
   - Matn: `#1B1E28` -> Hover: `#835E21`

3. **Gold Accent CTA (`.btn-luxury-gold`):**
   - Fon: `#835E21` -> Hover: `#68481D`
   - Matn: `#FFFFFF`

### 1.2 Tugma Holatlari (States)
| Holat | Vizual Ko'rinish | CSS / Tailwind Sinflari |
|---|---|---|
| **Default** | To'q kulrang fon, oq matn | `bg-[#1B1E28] text-white` |
| **Hover** | Oltin ohangga o'tish | `hover:bg-[#835E21] transition duration-300` |
| **Active / Pressed** | Engil qisqarish va to'q rang | `active:scale-[0.98] active:bg-[#68481D]` |
| **Focus-Visible** | 2px oltin kontur, 2px bo'shliq | `focus-visible:outline-2 focus-visible:outline-[#835E21] focus-visible:outline-offset-2` |
| **Disabled** | Ochiq kulrang, bosilmaydi | `disabled:opacity-40 disabled:cursor-not-allowed disabled:pointer-events-none` |
| **Loading** | Spinner paydo bo'ladi, matn yashirinadi | `.btn-loading` (ichida aylanuvchi oltin/oq spinner, `aria-busy="true"`) |

---

## 2. Formalar va Kiritish Maydonlari (Input Fields)

### 2.1 Variantlar
1. **Standart Matn/Telefon Maydoni (`.input-luxury`):**
   - Fon: `#FFFFFF`
   - Chegara: `1px solid #D6CEBE` -> Focus: `1.5px solid #835E21`
   - Balandlik: `h-[48px]`, `px-4`, `rounded-[4px]`
   - Matn: `#1B1E28`, `text-[14px] font-sans`
   - Placeholder: `#8A8780` (WCAG AA 4.5:1 kontrast qoidasiga mos)

2. **Xato Holati (Error State):**
   - Chegara: `1.5px solid #C43826`
   - Yordamchi xabar: `text-[12px] text-[#A62717] mt-1`

3. **Muvaffaqiyat Holati (Success State):**
   - Chegara: `1.5px solid #2D7A4F`
   - Belgisi: Yashil tasdiq belgisi

---

## 3. Mahsulot Kartasi (Product Card)

### 3.1 Anatomiyasi
- **Rasm bloki (Aspect 1:1 yoki 4:5):**
  - Fon: `#FAF8F5` (neytral issiq fon)
  - Badge (agar mavjud bo'lsa): `-30% OFF` yoki `POPULAR` — chap yuqori burchak, `text-[11px] font-mono tracking-wider bg-white/95 text-[#1B1E28] px-2.5 py-1 border border-[#E9E4DC]`
  - Wishlist (Sevimlilar) yurakchasi: O'ng yuqori burchak, **minimal 44x44px** hit area (`p-2.5 rounded-full hover:bg-white/90`)
- **Tavsif bloki:**
  - Kategoriya/Metal: `text-[11px] uppercase tracking-[0.16em] text-[#68481D] font-medium`
  - Mahsulot nomi: `text-[15px] font-serif font-normal text-[#1B1E28] hover:text-[#835E21] transition line-clamp-1`
  - Narx bloki:
    - Asosiy narx: `text-[16px] font-sans font-semibold text-[#1B1E28]`
    - Taqqoslash narxi: `text-[13px] font-sans line-through text-[#8A8780]`
  - Tezkor ko'rish / Tafsilotlar: `h-[40px] border border-[#1B1E28] hover:bg-[#1B1E28] hover:text-white text-[12px] uppercase tracking-wider`

### 3.2 Holatlar
- **Default:** `border border-[#EBE6DF] bg-white rounded-[6px] overflow-hidden transition-all duration-300`
- **Hover (Desktop):** `shadow-[0_12px_32px_rgba(27,30,40,0.08)] -translate-y-1`
- **Active (Mobile):** `scale-[0.99]`

---

## 4. O'lcham va Metall Tanlash Tugmalari (Selector Pills)

### 4.1 Metall Ranglari (Metal Swatches)
- **18K Yellow Gold:** `#E5C378`
- **18K White Gold:** `#E5E7EB`
- **18K Rose Gold:** `#E8B4A6`
- **Platinum:** `#D1D5DB`
- **Tanlangan (Selected):** Tashqi 2px oltin doira bilan o'ralgan (`ring-2 ring-offset-2 ring-[#835E21]`)

### 4.2 Uzuk O'lchamlari (Ring Sizes)
- **O'lchamlari:** Minimal `44x44px` teginish maydoni.
- **Default:** `border border-[#D6CEBE] bg-white text-[#1B1E28] rounded-[4px] text-[13px] font-medium`
- **Hover:** `border-[#835E21] text-[#835E21]`
- **Selected:** `border-[#1B1E28] bg-[#1B1E28] text-white font-semibold`

---

## 5. Modal va Fullscreen Sahifa (Product Detail Modal)

### 5.1 Xususiyatlari
- **Rol va A11y:** `role="dialog" aria-modal="true" aria-labelledby="product-modal-title"`
- **Navigatsiya (Popstate):** Sahifa ochilganda `history.pushState({ modal: 'product', id: ... })` chaqiriladi. Telefonning orqaga tugmasi (Back gesture) yoki `ESC` bosilganda sahifa silliq yopiladi.
- **Yopish tugmasi:** Minimal `48x48px` hit area, yuqori o'ng burchakda qulay o'rnashgan.

---

## 6. Bo'sh Holatlar (Empty States)

### 6.1 Sevimlilar (Wishlist Empty State)
- Rasm/Icon: Yupqa oltin chiziqli yurak ikonasi (`w-16 h-16 text-[#D6CEBE]`)
- Sarlavha: `Sizning sevimlilar ro'yxatingiz bo'sh` (`font-serif text-[22px] text-[#1B1E28]`)
- Matn: `O'zingizga ma'qul kelgan tilla va brilliant zargarlik buyumlarini yurakcha tugmasi orqali saqlab qo'ying.` (`text-[#605C55] text-[14px] max-w-md`)
- Asosiy CTA: `Katalogga o'tish` (`.btn-luxury-primary`, `min-h-[48px] px-8`)
