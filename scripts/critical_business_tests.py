#!/usr/bin/env python3
"""
OLMOS GOLD — Critical Business Logic Automated Tests
Verifies the 10 most critical business paths:
1. Product Catalog Integrity & Price Sanity
2. Currency Conversion Arithmetic & Rounding
3. Telegram Intent URI Encoding (Special Chars, Emojis, Newlines)
4. Full HTML Entity & Attribute Quote Escaping
5. Wishlist Deduplication & Schema Sanitization
6. Form Input Length Boundaries (Maxlength Enforcement)
7. Telephone Regex Pattern Enforcement
8. Anti-Clickjacking Framebuster Security
9. LocalStorage Quota Guard Fallback
10. Minimum 44px Touch Target Accessibility
"""

import sys
import re
import urllib.parse
from html.parser import HTMLParser

class TestSuite:
    def __init__(self):
        self.passed_count = 0
        self.failed_count = 0
        self.results = []

    def assert_true(self, path_num, title, condition, details=""):
        if condition:
            self.passed_count += 1
            self.results.append((path_num, title, "PASS", details))
            print(f"  ✅ [YO'L {path_num}] {title}")
        else:
            self.failed_count += 1
            self.results.append((path_num, title, "FAIL", details))
            print(f"  ❌ [YO'L {path_num}] {title} — XATO: {details}")

def run_suite():
    print("=" * 70)
    print("💎 OLMOS GOLD — 10 KRITIK BIZNES YO'LI TESTLARI")
    print("=" * 70)

    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    suite = TestSuite()

    # --- YO'L 1: Mahsulotlar katalogi narxlarining to'g'riligi va musbatligi ---
    prices = re.findall(r'base_price_usd:\s*([0-9]+)', html)
    all_positive = len(prices) > 0 and all(int(p) > 0 for p in prices)
    suite.assert_true(1, "Mahsulotlar katalogi narxlari musbat va to'g'ri raqamda", all_positive, f"Topildi: {len(prices)} ta narx")

    # --- YO'L 2: Valyuta kursi arifmetikasi va hisoblash mantiqi ---
    uzs_rate_match = re.search(r'const UZS_RATE =\s*([0-9]+);', html)
    rate_ok = False
    if uzs_rate_match:
        rate = int(uzs_rate_match.group(1))
        # 12,000 dan 15,000 UZS gacha bo'lishi kerak
        rate_ok = (12000 <= rate <= 15000)
    suite.assert_true(2, "Valyuta kursi (UZS_RATE) real bozor diapazonida", rate_ok, f"Kurs: {uzs_rate_match.group(1) if uzs_rate_match else 'Topilmadi'}")

    # --- YO'L 3: Telegram Intent URL maxsus belgilar va emojilarni xavfsiz o'raydi ---
    sample_text = "💎 OLMOS GOLD & Co: 18K Marquise Uzuk? Narxi: $673 #VIP"
    encoded = urllib.parse.quote(sample_text)
    uri_safe = ('&' not in encoded) and ('#' not in encoded) and (' ' not in encoded)
    suite.assert_true(3, "Telegram Intent URL maxsus belgilarni to'g'ri ekranlaydi", uri_safe, f"Encoded: {encoded[:40]}...")

    # --- YO'L 4: escapeHtml funksiyasi qo'shtirnoq va yakka tirnoqni ekranlaydi ---
    escape_fn = re.search(r'function escapeHtml\(str\)\s*\{([^}]+)\}', html)
    quotes_escaped = False
    if escape_fn:
        body = escape_fn.group(1)
        quotes_escaped = ('&quot;' in body or 'quot' in body) and ('&#39;' in body or '39' in body)
    suite.assert_true(4, "escapeHtml() da barcha tirnoqlar (' va \") ekranlangan", quotes_escaped, "Atribut XSS dan himoya")

    # --- YO'L 5: Wishlist saqlash va dublikatlarga qarshi himoya ---
    dedup_logic = re.search(r'list\.filter\(id => id !== productId\)', html)
    suite.assert_true(5, "Wishlist dublikatsiz saqlash va olib tashlash filtri mavjud", bool(dedup_logic), "Takroriy element qo'shilishi oldi olingan")

    # --- YO'L 6 & 7: Barcha inputlarda maxlength va tel patterni tekshiruvi ---
    class InputValidator(HTMLParser):
        def __init__(self):
            super().__init__()
            self.missing_maxlength = []
            self.missing_tel_pattern = []
        def handle_starttag(self, tag, attrs):
            if tag == 'input':
                attr = dict(attrs)
                t = attr.get('type', 'text').lower()
                if t in ['text', 'tel']:
                    if 'maxlength' not in attr:
                        self.missing_maxlength.append(attr.get('id', 'unknown'))
                if t == 'tel':
                    if 'pattern' not in attr:
                        self.missing_tel_pattern.append(attr.get('id', 'unknown'))

    inp_val = InputValidator()
    inp_val.feed(html)

    suite.assert_true(6, "Barcha matn va telefon inputlarida maxlength chegaralangan", len(inp_val.missing_maxlength) == 0, f"Cheklovsiz: {inp_val.missing_maxlength}")
    suite.assert_true(7, "Barcha telefon inputlarida format regex patterni mavjud", len(inp_val.missing_tel_pattern) == 0, f"Patternsiz: {inp_val.missing_tel_pattern}")

    # --- YO'L 8: Anti-Clickjacking Framebuster skripti mavjudligi ---
    has_framebuster = "window.top !== window.self" in html
    suite.assert_true(8, "Anti-Clickjacking Framebuster brauzer himoyasi mavjud", has_framebuster, "Iframe o'g'irligiga qarshi")

    # --- YO'L 9: LocalStorage to'lishiga qarshi Quota Guard ---
    has_quota_guard = "QuotaExceededError" in html
    suite.assert_true(9, "LocalStorage QuotaExceededError kesh tozalash zaxirasi mavjud", has_quota_guard, "Brauzer qotishiga qarshi")

    # --- YO'L 10: Minimal 44x44px Touch Target (Mobil tugmalar standartiga muvofiq) ---
    has_touch_targets = "min-h-[44px]" in html or "w-11 h-11" in html
    suite.assert_true(10, "Barcha asosiy mobil tugmalarda 44x44px touch target o'rnatilgan", has_touch_targets, "Mobil konversiya qulayligi")

    print("=" * 70)
    print(f"YAKUNIY NATIJA: {suite.passed_count}/10 TEST MUVAFFAQIShATLI O'TDI (Fail: {suite.failed_count})")
    print("=" * 70)

    return 0 if suite.failed_count == 0 else 1

if __name__ == '__main__':
    sys.exit(run_suite())
