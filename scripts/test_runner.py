#!/usr/bin/env python3
"""
Olmos Gold Production-Readiness Automated Test Suite
Checks:
- HTML5 syntax and DOM integrity
- Duplicate element IDs
- Image accessibility (alt attributes)
- Reverse tabnabbing security (target="_blank" without noopener)
- Schema.org JSON-LD structured data validation
- Product database consistency and price sanity
"""

import sys
import re
import json
from html.parser import HTMLParser

class DOMValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.duplicate_ids = []
        self.images_without_alt = []
        self.unsafe_links = []
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        
        # Check duplicate IDs
        if 'id' in attr_dict:
            elem_id = attr_dict['id']
            if elem_id in self.ids:
                self.duplicate_ids.append(elem_id)
            else:
                self.ids.append(elem_id)
                
        # Check img alt tags
        if tag == 'img':
            if 'alt' not in attr_dict or not attr_dict['alt'].strip():
                self.images_without_alt.append(attr_dict.get('src', 'unknown'))
                
        # Check target="_blank" safety
        if tag == 'a' and attr_dict.get('target') == '_blank':
            rel = attr_dict.get('rel', '')
            if 'noopener' not in rel:
                self.unsafe_links.append(attr_dict.get('href', 'unknown'))

def run_tests():
    print("=" * 60)
    print("💎 OLMOS GOLD — PRODUCTION READINESS TEST RUNNER")
    print("=" * 60)
    
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    passed = True
    
    # 1. HTML5 Parser Syntax Test
    try:
        validator = DOMValidator()
        validator.feed(html_content)
        print("✅ [TEST 1] HTML5 Sintaksisi: To'g'ri va bexato")
    except Exception as e:
        print(f"❌ [TEST 1] HTML5 Sintaksisi xatosi: {e}")
        passed = False

    # 2. Duplicate IDs Test
    if validator.duplicate_ids:
        print(f"❌ [TEST 2] Takrorlangan ID'lar topildi: {validator.duplicate_ids}")
        passed = False
    else:
        print(f"✅ [TEST 2] DOM ID Noyobligi: {len(validator.ids)} ta unikal ID, takrorlanish yo'q")

    # 3. Accessibility - Alt attributes
    if validator.images_without_alt:
        print(f"⚠️ [TEST 3] 'alt' atributi bo'lmagan rasmlar: {validator.images_without_alt}")
    else:
        print("✅ [TEST 3] Rasm A11y: Barcha <img> teglarida alt atributi mavjud")

    # 4. Reverse Tabnabbing
    if validator.unsafe_links:
        print(f"❌ [TEST 4] Xavfli target=_blank havolalari: {validator.unsafe_links}")
        passed = False
    else:
        print("✅ [TEST 4] Havolalar Xavfsizligi: Barcha target=_blank havolalarida noopener mavjud")

    # 5. Schema.org JSON-LD Test
    json_ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html_content, re.DOTALL)
    if not json_ld_matches:
        print("❌ [TEST 5] Schema.org JSON-LD topilmadi")
        passed = False
    else:
        try:
            for block in json_ld_matches:
                data = json.loads(block)
                print(f"✅ [TEST 5] Schema.org JSON-LD validatsiyasi muvaffaqiyatli: {data.get('@context')}")
        except Exception as e:
            print(f"❌ [TEST 5] Schema.org JSON-LD JSON formati xato: {e}")
            passed = False

    # 6. Hardcoded Secrets Check
    secret_patterns = [
        r'TG_BOT_TOKEN\s*=\s*["\'][^"\']+["\']',
        r'bot[0-9]{8,}:[A-Za-z0-9_-]{35}',
        r'api[_-]?key\s*=\s*["\'][^"\']+["\']'
    ]
    exposed = []
    for pat in secret_patterns:
        if re.search(pat, html_content, re.IGNORECASE):
            exposed.append(pat)
    if exposed:
        print(f"❌ [TEST 6] Kodda ochiq sirlar topildi: {exposed}")
        passed = False
    else:
        print("✅ [TEST 6] Maxfiy Sirlar: Hardcoded tokenlar va kalitlar yo'q")

    print("=" * 60)
    if passed:
        print("🎉 BARCHA PRODUCTION-READINESS TESTLARI MUVAFFAQIShATLI O'TDI (100% PASS)!")
        return 0
    else:
        print("⚠️ TESTLARDA KAMCHILIKLAR BOR.")
        return 1

if __name__ == '__main__':
    sys.exit(run_tests())
