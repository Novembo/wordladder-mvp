---
name: mobile-ux-guidelines
description: "Apply iOS HIG and Material guidelines: touch targets, safe areas, navigation, states, keyboard, dark mode, accessibility, and low-bandwidth design. Use when designing or reviewing mobile screens and flows."
---

# Mobile UX Guidelines

## Layout and interaction
- Touch targets at least ~44pt (iOS) / 48dp (Android) with adequate spacing; support one-handed reach for primary actions.
- Respect safe areas, notches, and system bars; handle keyboard avoidance and keep inputs visible while typing.
- Follow platform conventions for navigation (tab bar/bottom navigation, back behavior, gestures); avoid hidden critical actions behind gestures only.

## States and feedback
- Design every screen's loading (skeletons), empty, error (with recovery action), and offline states.
- Give immediate feedback for taps and submissions; prevent double-submits; confirm destructive actions and allow undo where possible.
- Use clear, short copy; label forms properly with correct keyboard types, autofill hints, and inline validation.

## Accessibility
Provide accessibility labels/roles/hints, logical focus order, Dynamic Type/font scaling support, sufficient contrast, and non-color cues. Test with VoiceOver and TalkBack. Respect reduced-motion settings.

## Theming and devices
Support light and dark mode with tokens; test small phones, large phones, tablets/foldables, and landscape where relevant.

## Low-bandwidth and low-end devices
Minimize payload sizes, compress and lazy-load images, cache aggressively, and let users retry; avoid blocking the UI on large downloads; keep app size reasonable.

## Verify
Walk key flows on real devices with throttled networks and large text sizes; fix issues before store submission.
