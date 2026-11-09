# Human Interface 04 | Design systems, responsive interfaces and accessibility

[← Case studies](03_UX_CASE_STUDIES.md) · [Volume VI](../OMNIMASTER_HUMAN_INTERFACE.md) · [Next: Measuring usability →](05_MEASURE_USABILITY.md)

A design system is not a gallery of pretty buttons. It is a shared set of decisions that helps people build predictable interfaces without re-solving every interaction.

My cross-stack experience makes this important: I have worked with reporting interfaces, React applications, native-mobile ambitions and administrative tools. Every inconsistent control adds a small cognitive cost, and those costs accumulate.

## Start with principles

- **Meaning:** text, icons and colour should communicate the same state.
- **Consistency:** one action should look and behave similarly across related screens.
- **Feedback:** loading, success, partial success, warning and failure should be distinct.
- **Access:** keyboard, touch, zoom, assistive technology and different devices matter.
- **Restraint:** visual effects should support hierarchy rather than distract from work.
- **Truth:** never style a draft state so it resembles a completed transaction.

## Tokens that carry meaning

~~~css
:root {
  --surface: #101f2b;
  --surface-raised: #1a3443;
  --text-primary: #f3f7f8;
  --text-muted: #c6d6dc;
  --accent: #75e8d4;
  --warning: #f1ce84;
  --danger: #ffb6aa;
  --focus-ring: 3px solid var(--warning);
  --radius-control: 0.65rem;
}
~~~

These are **illustrative OmniMaster design tokens**, not a claim that all my production applications share a formal component library. A real system would validate contrast for every foreground/background combination and interaction state.

## Design a component around behaviour

Consider a **Submit & Sync** button.

| State | Visible behaviour | Underlying requirement |
|---|---|---|
| Ready | Clear label and action | User authorised, input valid |
| Processing | “Syncing…” with progress or status | Prevent unintended duplicate submissions |
| Partial result | “37 imported, 3 need review” | Backend supports partial-result semantics |
| Complete | Confirmation plus useful next step | Transaction actually committed |
| Failed safely | Explanation and retry/recovery path | Server knows what changed and what did not |
| Not permitted | Disabled/hidden only for clarity | Server must independently deny the request |

A single spinner cannot represent the whole workflow.

## Accessibility is a development responsibility

Use semantic HTML and labels first; add ARIA when native semantics do not supply the needed information. Respect visible focus, correct tab order, zoom and reflow, reduced-motion preferences, meaningful alt text and feedback to assistive technology.

For data charts, provide understandable titles, units and a text/table alternative. Don't rely only on red/green to distinguish performance. For forms, show exactly which field needs correction and preserve previously entered valid information where safe.

**Standard to study:** WCAG 2.2 AA is a useful design and test target. A small unit-test suite or Lighthouse result does not certify complete compliance.

## Responsive, not merely smaller

~~~css
.dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr));
  gap: 1rem;
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { scroll-behavior: auto; animation-duration: 0.01ms; }
}
~~~

A layout that technically fits at 320 pixels may still be difficult to use. Check tap targets, column priority, sticky headers, long identifiers, error messages and the real task flow on representative devices.

## The test pyramid for interfaces

| Test | Helps detect | Does not guarantee |
|---|---|---|
| Component/unit | Wrong local state or error copy | User comprehends the flow |
| Responsive visual | Overflow, clipping, theme regression | Touch/keyboard accessibility |
| Accessibility automation | Many semantic, contrast and label issues | Every WCAG requirement |
| Keyboard/manual | Focus order, traps, usable controls | Every screen-reader interaction |
| Assistive technology | Announcements and interaction behaviour | Population-wide task success |
| Moderated usability study | Confusion, hesitation, wrong turns | Universal needs from a tiny sample |
| Operational telemetry | Error rates and workflow drop-off | The reason for a failure without further research |

## A mini design system exercise

Implement one **upload status card** with four statuses: idle, uploading, validated and failed. Define its tokens and component props. Use a status heading and text, not colour alone. Include a keyboard-visible Retry action.

Ask a colleague to explain each state without hearing your interpretation. If they cannot, revise the wording and hierarchy before adding animation.

## What I'd like to sharpen

I want to improve consistency across web and native experiences, documented design decisions, accessibility in interactive data visualisation, and validation with real users. The outcome I care about is a dependable experience, not an arbitrary design-tool score.

[← Case studies](03_UX_CASE_STUDIES.md) · [Next: Usability measurement →](05_MEASURE_USABILITY.md)
