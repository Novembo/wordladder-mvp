---
name: frontend-performance
description: "Measure and optimize web loading, rendering, runtime responsiveness, and bundle size. Use for slow page loads, Core Web Vitals, bundle size, rendering jank, or lazy loading."
---

# Frontend Performance

## Workflow
1. Measure baseline on representative devices/network profiles.
2. Inspect Core Web Vitals and relevant user-centric metrics: LCP, INP, CLS.
3. Analyze bundles, route chunks, images, fonts, scripts, and third-party code.
4. Fix the largest measured bottleneck first.
5. Optimize image formats/sizes, responsive delivery, caching, and critical rendering.
6. Reduce unnecessary JS, expensive re-renders, layout shifts, and long tasks.
7. Re-measure and document before/after conditions.

## Rules
- Do not optimize from intuition alone.
- Avoid lazy-loading above-the-fold critical images.
- Reserve image/media dimensions to reduce layout shift.
- Use code splitting where it reduces initial cost without harming navigation.
- Avoid excessive third-party scripts.
- Consider low-end mobile devices and slow networks.
