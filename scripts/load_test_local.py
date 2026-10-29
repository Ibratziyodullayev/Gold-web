#!/usr/bin/env python3
"""
OLMOS GOLD — Local / Staging Concurrent Benchmark Tool
Zero-dependency Python concurrent benchmark for staging testing.
Usage:
  python3 scripts/load_test_local.py [TARGET_URL] [CONCURRENCY] [TOTAL_REQUESTS]
Example:
  python3 scripts/load_test_local.py http://localhost:8080 20 200
"""

import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

def fetch_url(url):
    start = time.time()
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Olmos-LoadTest-Runner/1.0'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            code = response.getcode()
            content_len = len(response.read())
            duration = (time.time() - start) * 1000
            return (True, code, duration, content_len)
    except Exception as e:
        duration = (time.time() - start) * 1000
        return (False, str(e), duration, 0)

def run_benchmark(target_url, concurrency=20, total_requests=200):
    print("=" * 65)
    print(f"🚀 OLMOS GOLD — CONCURRENT STAGING BENCHMARK")
    print(f"Target URL:    {target_url}")
    print(f"Concurrency:   {concurrency} parallel virtual clients")
    print(f"Total So'rov:  {total_requests} ta so'rov")
    print("=" * 65)

    endpoints = [
        target_url,
        f"{target_url}/product-marquise-gold.jpg",
        f"{target_url}/olmos-logo.jpg",
    ]

    urls = [endpoints[i % len(endpoints)] for i in range(total_requests)]

    start_all = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        results = list(executor.map(fetch_url, urls))

    total_time = time.time() - start_all
    successes = [r for r in results if r[0]]
    failures = [r for r in results if not r[0]]
    durations = sorted([r[2] for r in successes])

    rps = len(results) / total_time
    p50 = durations[int(len(durations) * 0.50)] if durations else 0
    p95 = durations[int(len(durations) * 0.95)] if durations else 0

    print("\n📊 NATIJALAR:")
    print(f"  • Umumiy vaqt:        {total_time:.2f} soniya")
    print(f"  • Muvaffaqiyatli:     {len(successes)}/{total_requests} ({len(successes)/total_requests*100:.1f}%)")
    print(f"  • Xatoliklar soni:    {len(failures)}")
    print(f"  • O'tkazuvchanlik:    {rps:.1f} so'rov/soniya (RPS)")
    print(f"  • Median (p50):       {p50:.1f} ms")
    print(f"  • 95-persentil (p95): {p95:.1f} ms")
    print("=" * 65)

    if failures:
        print(f"⚠️ Xatolik namunasi: {failures[0][1]}")
        return 1
    else:
        print("🎉 STAGING YUKLAMA SINOVI MUVAFFAQIShATLI YAKUNLANDI!")
        return 0

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080'
    conc = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    reqs = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    sys.exit(run_benchmark(target, conc, reqs))
