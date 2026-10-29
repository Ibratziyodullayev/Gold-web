---
name: ux-ui-mastery
description: Cognitive psychology heuristics, Nielsen 10 usability principles, Gestalt laws, cognitive load optimization, and accessibility compliance.
---

# UX/UI Mastery Skill

## Purpose
Comprehensive evaluation of user experience heuristics, mental models, cognitive friction, flow clarity, and accessibility standards (WCAG 2.2 AA).

## Checklist
- [ ] **Nielsen Heuristics:**
  - Visibility of system status (spinners, immediate response).
  - Match between system and real world (natural luxury terminology).
  - User control & freedom (undo, close modals, clear back buttons).
  - Consistency & standards (standard icons, predictable placement).
  - Error prevention (validation, clear phone masks).
  - Recognition rather than recall (pre-filled messages, clear previews).
  - Flexibility & efficiency of use (shortcuts, quick inquiry).
  - Aesthetic & minimalist design (clean focus, no clutter).
  - Help users recognize & recover from errors (inline friendly feedback).
  - Help & documentation (concierge hotlines, size guide).
- [ ] **Cognitive Load:** Minimize working memory strain (Miller's Law, Hicks Law).
- [ ] **Fitts's Law:** Interactive touch targets >= 44x44px on mobile devices.
- [ ] **WCAG 2.2 AA Contrast:** Normal text >= 4.5:1, large text/UI components >= 3:1.

## Anti-Patterns
- Trapping users in modals without ESC key or visible close buttons.
- Using color alone to signify state or feedback.
- Tiny touch targets on mobile (e.g. 24px buttons causing missed taps).
- Missing error messages or obscure technical error alerts.
- Sudden layout shifts during interaction (CLS).

## Fix Recipes
1. **Modal Containment:** Implement `role="dialog"`, `aria-modal="true"`, ESC key listener, and focus trapping.
2. **Accessible Form Inputs:** Ensure explicit `<label>` tags with matching `for` / `id` pairs and `aria-describedby` for helper text.
3. **Touch Targets:** Add `min-h-[44px] min-w-[44px]` for all interactive mobile targets.
