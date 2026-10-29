import http from 'k6/http';
import { check, sleep, group } from 'k6';

// k6 Load Test Configuration for Staging/Production Readiness
export const options = {
  stages: [
    { duration: '30s', target: 50 },   // 1. Ramp-up to 50 concurrent users
    { duration: '1m', target: 100 },   // 2. Sustained high traffic (100 users)
    { duration: '15s', target: 200 },  // 3. Spike test (200 concurrent users)
    { duration: '30s', target: 0 },    // 4. Cool-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<400'], // 95% of requests must complete within 400ms
    http_req_failed: ['rate<0.01'],   // Less than 1% errors
  },
};

const BASE_URL = __ENV.TARGET_URL || 'http://localhost:8080';

export default function () {
  // Scenario 1: Initial Page Visit & Assets Load
  group('01_Home_Page_Visit', function () {
    const res = http.get(`${BASE_URL}/`);
    check(res, {
      'status is 200': (r) => r.status === 200,
      'body contains OLMOS GOLD': (r) => r.body.includes('OLMOS GOLD'),
      'response time < 350ms': (r) => r.timings.duration < 350,
    });
  });

  sleep(1);

  // Scenario 2: Load Static Imagery Assets
  group('02_High_Res_Jewelry_Assets', function () {
    const res = http.get(`${BASE_URL}/product-marquise-gold.jpg`);
    check(res, {
      'asset status 200': (r) => r.status === 200,
      'asset size > 50KB': (r) => r.body.length > 50000,
    });
  });

  sleep(2);

  // Scenario 3: Product Customizer & Modal Interaction (Simulated)
  group('03_PDP_Customizer_View', function () {
    const res = http.get(`${BASE_URL}/#product-OLM-MRQ-01`);
    check(res, {
      'pdp view status 200': (r) => r.status === 200,
    });
  });

  sleep(1.5);
}
