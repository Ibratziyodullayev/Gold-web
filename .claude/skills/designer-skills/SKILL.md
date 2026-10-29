---
name: designer-skills
description: Interaction flows, state management (empty, loading, error, success), microcopy craftsmanship, and developer-to-designer handoff specifications.
---

# Designer Skills

## Purpose
Design complete user flows, map edge cases (first-time visitor, offline, network failure, empty states), refine UX microcopy, and document tokenized design handoff specs.

## Checklist
- [ ] **State Coverage (10-State Rule):** Default, Hover, Active, Focus, Disabled, Loading, Error, Empty, Selected, Read-only.
- [ ] **Empty States:** Provide reassuring messages, clear next steps, and a direct action trigger (e.g. "Sevimlilar bo'sh" -> "Katalogga o'tish").
- [ ] **Loading States:** Skeletons or branded spinners preventing layout jump.
- [ ] **Microcopy Quality:** Human, polite, actionable, and culturally tuned (Uzbek / Russian luxury etiquette).
- [ ] **Confirmation & Reversal:** Allow cancellation before committing critical actions.

## Anti-Patterns
- Blank empty screens showing no guidance when lists are empty.
- Generic error messages like "Xatolik yuz berdi" with no recovery path.
- Clashing tonal voices between luxury branding and robotic technical copy.
- Unhandled network failures leaving spinners spinning forever.

## Fix Recipes
1. **Empty State Component:** Center illustration/icon + headline + concise explanation + CTA button.
2. **Action Feedback:** Immediate toast notifications with clear dismiss options.
3. **Microcopy Polish:** Replace command language ("Katalogni yukla") with value-driven wording ("VIP Katalogni Telegramda Olish").
