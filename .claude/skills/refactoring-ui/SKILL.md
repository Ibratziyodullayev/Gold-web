---
name: refactoring-ui
description: Professional visual design audit and systematic UI refinement based on Refactoring UI principles (visual hierarchy, spacing scale, elevation, color systems).
---

# Refactoring UI Skill

## Purpose
Systematic visual audit and interface refactoring to eliminate arbitrary values, improve typographic hierarchy, align spacing to strict 4px/8px scales, and refine borders, shadows, and color ramps.

## Checklist
- [ ] **Visual Hierarchy:** Is font size, weight, and contrast clearly communicating importance (primary, secondary, tertiary)?
- [ ] **Spacing Consistency:** Are all margins and paddings mapped strictly to a unified 4px/8px scale (e.g. 4, 8, 12, 16, 24, 32, 48, 64px)?
- [ ] **Depth & Elevation:** Are shadows subtle, tinted, and multi-layered instead of harsh black drop-shadows?
- [ ] **Color Contrast & Luminance:** Are grays, brand accents, and borders using intentional HSL shades rather than generic hex codes?
- [ ] **Layout Density & Alignment:** Is whitespace used actively to group related elements (Gestalt Law of Proximity)?
- [ ] **Borders vs. Backgrounds:** Are dividers used only where necessary, preferring background separation and whitespace where cleaner?

## Anti-Patterns
- Using random arbitrary pixel values (`p-[13px]`, `mt-[7px]`).
- Over-relying on gray borders when subtle background tone differences work better.
- Heavy pure black shadows (`box-shadow: 0 4px 6px #000000`).
- Equal visual weight on primary and secondary action buttons.
- Low-contrast light gray text on white backgrounds failing legibility.

## Fix Recipes
1. **Button Hierarchy:** Primary action = high-contrast solid filled button; Secondary = ghost/subtle border; Tertiary = text-only link.
2. **Layered Shadows:** Combine a tight ambient shadow with a soft diffused directional shadow (`box-shadow: 0 2px 4px rgba(0,0,0,0.04), 0 10px 24px rgba(0,0,0,0.08)`).
3. **Form Elements:** Match input heights, padding, and focus states across the system (`ring-2 ring-gold-500/50 outline-none`).
