---
name: vercel-agent-skills
description: Web performance, Core Web Vitals, asset optimization, render cycle efficiency, Cumulative Layout Shift (CLS) prevention, and accessible semantic DOM trees.
---

# Vercel Agent Skills (Web Performance & Optimization)

## Purpose
Optimize DOM performance, eliminate unnecessary repaints, prevent Cumulative Layout Shift (CLS), optimize imagery and font loading, and streamline hydration and rendering cycles.

## Checklist
- [ ] **Image Optimization:** Explicit `width` and `height` or aspect-ratio boxes preventing layout reflow.
- [ ] **Lazy Loading:** `loading="lazy"` on below-the-fold media; `fetchpriority="high"` on Hero LCP elements.
- [ ] **Font Loading:** `font-display: swap`, preconnecting to font CDNs, zero FOIT (Flash of Invisible Text).
- [ ] **Asset Weight:** Minified SVGs, WebP/modern image formats, low payload footprints.
- [ ] **Scroll & Animation Performance:** Use GPU-accelerated CSS properties (`transform`, `opacity`), avoiding `top/left/height` transitions.
- [ ] **Interaction Responsiveness (INP):** Immediate visual feedback (<50ms) on clicks and taps.

## Anti-Patterns
- Loading massive 10MB uncompressed raw camera images directly into web image tags.
- Missing dimensions on images causing jumping text as images load (high CLS).
- Animating layout-triggering properties (`width`, `margin`, `padding`).
- Blocking render with un-deferred heavy scripts.

## Fix Recipes
1. **Aspect Ratio Containers:** Wrap images in `<div class="aspect-square relative overflow-hidden">` with `object-cover`.
2. **Smooth Transitions:** Use `transition-transform duration-300 ease-out active:scale-95`.
3. **Passive Event Listeners:** Attach scroll and touch listeners with `{ passive: true }` to keep 60fps frame rates.
