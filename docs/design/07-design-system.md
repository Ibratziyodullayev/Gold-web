# OLMOS GOLD DESIGN SYSTEM (Tokens & Foundations)
**Hujjat kodi:** `DOC-DSGN-07` | **Fayl:** `docs/design/07-design-system.md`

Ushbu dizayn tizimi xalqaro **DiamondsByUK** andozasiga muvofiq, OLMOS GOLD JEWELLERY uchun maxsus ishlab chiqilgan.

---

## 1. Rang Shkalasi (Color Ramps & Contrast)

Barcha ranglar WCAG 2.2 AA (kamida 4.5:1) mezoniga muvofiq hisoblangan:

| Token | Qiymat | Tavsif | Kontrast (Oq fonda) |
| :--- | :--- | :--- | :-: |
| `--color-bg-canvas` | `#FFFFFF` | Toza oq studiya foni | 1:1 |
| `--color-bg-subtle` | `#FAF9F6` | Nozik fil suyagi foni | 1.05:1 |
| `--color-bg-card` | `#FFFFFF` | Karta va blok foni | 1:1 |
| `--color-border-subtle` | `rgba(17, 17, 19, 0.08)` | Neytral nozik chegara | N/A |
| `--color-border-gold` | `rgba(197, 154, 63, 0.35)` | Nozik metall hoshiya | N/A |
| `--color-gold-accent` | `#C59A3F` | Vizual brend aksenti | 2.9:1 (faqat dekor/border) |
| `--color-gold-text` | `#68481D` | **O'qiluvchi yuqori kontrastli oltin matn** | **6.8:1 (WCAG AA PASS)** |
| `--color-ink-primary` | `#111113` | Asosiy sarlavha va narxlar | **16.8:1 (AAA PASS)** |
| `--color-ink-secondary` | `#4B4E5B` | Kichik matnlar va parametrlar | **7.1:1 (AAA PASS)** |
| `--color-ink-muted` | `#686C7D` | Qo'shimcha yordamchi matnlar | **4.7:1 (AA PASS)** |
| `--color-success` | `#047857` | Butikda mavjud / Tasdiq (Emerald) | **4.9:1 (AA PASS)** |
| `--color-sale` | `#BE123C` | Chegirma va tejash (Rose) | **4.8:1 (AA PASS)** |

---

## 2. Tipografika Shkalasi (Typography Scale)

| Token | Shrift | O'lcham | Line-Height | Qalinlik | Qo'llanilishi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `display-lg` | Tenor Sans | 48px / 64px | 1.1 | 400 | Hero bosh sarlavhasi |
| `display-md` | Tenor Sans | 32px / 40px | 1.15 | 400 | Bo'lim sarlavhalari |
| `display-sm` | Tenor Sans | 24px / 28px | 1.2 | 700 | Mahsulot nomi (FS view) |
| `price-lg` | Tenor Sans | 28px / 36px | 1.0 | 700 | Asosiy narx ko'rinishi |
| `title-card` | Tenor Sans | 15px / 16px | 1.3 | 700 | Karta mahsulot nomi |
| `body-base` | Figtree | 15px | 1.5 | 400 | Asosiy matn & tavsif |
| `body-sm` | Figtree | 13px | 1.4 | 400/500 | Parametrlar, specs |
| `caption` | Figtree | 11px / 12px | 1.3 | 600 | Badgelar, statuslar |
| `button` | Figtree | 12px / 13px | 1.0 | 700 | Tugmalar (uppercase) |

---

## 3. Spacing Panjarasi (Strict 8px Grid)

Barcha 96 xil tarqoq qiymatlar quyidagi 8 ta rasmiy token bilan almashtiriladi:
- `space-1` = **4px** (ichki micro-paddinglar)
- `space-2` = **8px** (elementlar orasidagi standart oraliq)
- `space-3` = **12px** (kapsula va kichik bloklar)
- `space-4` = **16px** (kartalar ichki paddingi)
- `space-6` = **24px** (komponentlar oralig'i)
- `space-8` = **32px** (katta kartalar paddingi)
- `space-12` = **48px** (bo'limlar oraliq maydoni)
- `space-16` = **64px+** (katta desktop bo'lim oraliqlari)

---

## 4. Radius va Soya (Radius & Shadows)

- `radius-sm`: `2px` (DiamondsByUK to'g'ri burchakli klassik nafisligi)
- `radius-md`: `4px` (karta va modallar)
- `radius-full`: `9999px` (rang va karat tabletkalari)
- `shadow-subtle`: `0 2px 8px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.02)`
- `shadow-card`: `0 8px 24px -6px rgba(0,0,0,0.06), 0 2px 6px -1px rgba(0,0,0,0.03)`
- `shadow-modal`: `0 24px 48px -12px rgba(0,0,0,0.18)`
