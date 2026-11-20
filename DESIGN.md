# Business Letter Polisher design system

## Purpose
A focused desktop letter editor. Apple-inspired restraint, with Windows UI conventions: Segoe UI, clear blue actions, action then Cancel in confirmation footers, Escape and keyboard focus. Preserve toolbar order: history, theme, language, settings.

## Palette and typography
Light canvas #F3F4F6, white work surfaces, ink #202329, secondary #565D68 and blue #0067C0. Dark canvas #17191D, surfaces #22252B and #282B32, secondary text #B0B5BF. Use Segoe UI Variable Text / Segoe UI / Microsoft JhengHei. Body 13–14px, dialog heading 18px semibold. Use solid surfaces, subtle borders, minimal shadow; no decorative gradients or glowing controls.

## Layout and components
Use 14px dialog corners, 10px group corners and 7–8px controls. Keep labels above inputs, errors immediately below the triggering control. Preserve name → API format → URL → key → model → temperature. Model input, toggle and reload remain separate. Provider presets populate a draft; Save commits and Cancel restores it.

## Dialogs and keyboard
Confirmation, detail, guide and update dialogs sit at the viewport center, with 24px exterior clearance (16px on narrow windows), bounded height and internal scroll. Confirmation messages use textContent. Queue concurrent confirmations. Initial confirmation focus is Cancel; trap Tab, make the background inert and restore focus on close. Active update progress cannot be dismissed with Escape; errors can. Custom select portals remain operable above their parent panel. Close the top layer before underlying panels.

## Responsive and motion
Wrap the toolbar below 640px without changing order. Stack model reload under the input below 480px. No horizontal overflow. Keep stable panel scrollbars and 36–38px targets. State transitions are short and respect reduced motion.

## Output boundary
All three transports share request deadlines, captured configuration, text extraction, and a result validator. Require a JSON object with exactly polished and suggestions (2–5 single-line strings). The polished field cannot contain known preambles, explanation headings, analysis tags or code fences. Retry once with the original letter and a corrective contract. A failed or stale response never replaces displayed results or adds history. Structure is enforceable; arbitrary model semantics, fact accuracy and every language convention are not fully machine-verifiable.

## Localization
UI labels, notices, accessible names and examples follow zh-TW / zh-CN / en interface locale. Letter language and region independently control source conventions and suggestion language; result language and region control polished content. Preserve generated results on interface language changes.

## References
- https://developer.apple.com/design/human-interface-guidelines/alerts
- https://learn.microsoft.com/en-us/windows/apps/design/controls/dialogs-and-flyouts/dialogs
- https://fluent2.microsoft.design/accessibility
