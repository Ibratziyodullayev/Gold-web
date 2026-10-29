# Qolgan Tavsiyalar va Kelgusi Bosqichlar (docs/design/11-remaining.md)

Ushbu hujjat loyihada amalga oshirilgan to'liq o'zgarishlar yakunini va kelgusida vebsaytni yanada rivojlantirish bo'yicha strategik tavsiyalarni o'z ichiga oladi.

---

## 1. Amalga Oshirilgan Ishlar Yakuni

Barcha audit bo'yicha aniqlangan 12 ta kamchilik **100% bartaraf etildi**:
- **P0 Kritik Kamchiliklar:** 4 tadan 0 ta qoldi (Teginish maydonlari >= 44px, WCAG AA kontrast, Popstate / Back button navigatsiyasi, ARIA dialog semantikasi to'liq joriy etildi).
- **P1 Muhim Kamchiliklar:** 5 tadan 0 ta qoldi (8px panjara tizimi, 8 darajali tipografiya, `:focus-visible`, jozibador bo'sh holat, formalarda loading spinnerlari).
- **P2 Qo'shimcha Sayqallashlar:** 3 tadan 0 ta qoldi (CLS oldini olish uchun aniq o'lchamlar, ko'p qatlamli hashamatli kartalar soyalari, neytral hashamatli ijtimoiy tarmoqlar uslubi).

---

## 2. Kelgusi Bosqichlar Uchun Tavsiyalar (Future Enhancements)

1. **Tasvirlarni Zamonaviy Formatga O'tkazish (WebP / AVIF):**
   - Hozirgi barcha fotosuratlar yuqori sifatli JPG/PNG formatida saqlanmoqda. Kelgusida ularni `AVIF` yoki `WebP` formatlariga avtomatlashtirilgan tarzda o'tkazish sahifa yuklanish tezligini yanada 30-40% ga qisqartiradi.

2. **Onlayn To'lov Shlyuzi (Payme / Click / Uzum):**
   - Hozirgi buyurtma oqimi Telegram orqali xususiy konsyerj xizmatiga yo'naltirilgan (bu zargarlik buyumlari uchun eng yuqori konversiya beruvchi usul). Kelgusida mijozlar avans yoki to'liq to'lovni bevosita saytdan amalga oshirishi uchun milliy to'lov tizimlarini ulash mumkin.

3. **3D Interactive Diamond Viewer (Three.js):**
   - Olmoslarning nur sinishi (brilliance & fire) ni 360 darajada ko'rsatuvchi interaktiv WebGL modelini integratsiya qilish DiamondsByUK tajribasini 12/10 darajasiga olib chiqadi.

4. **Avtomatlashtirilgan CI/CD Lighthouse Testlari:**
   - Har bir yangi kod qo'shilganda avtomatik ravishda Accessibility (100 ball) va Performance (95+ ball) darajasini ushlab turish uchun GitHub Actions testlarini yo'lga qo'yish.
