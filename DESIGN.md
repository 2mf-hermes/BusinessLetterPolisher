# Business Letter Polisher design system

## Purpose and atmosphere
A focused desktop writing workspace with balanced density. Settings follow the task sequence: provider name, API format, URL, key, model, temperature. Preserve the toolbar order: history, theme, language, settings.

## Color and typography
Use the existing dark canvas (#0C1117), light canvas (#F2F2F7), and a single functional blue accent. Secondary text in light mode is #5C6069, tertiary text #737985. Avoid decorative gradients and glowing actions. Use the installed sans-serif UI font stack with Chinese fallbacks; use monospace only for URLs and API values. Settings group titles are 13px, with hierarchy conveyed by weight. Labels have 1.5 line height; hints have 1.7 line height.

## Components and spacing
Place labels above inputs and errors below the control that triggered them. Use 16px field spacing, 22px section spacing, and at least 38px settings control height. Presets are native buttons. Maintain a visible 2px focus outline with 3px offset. Keep model input, list toggle and reload action separate. API keys stay masked by default.

## Responsive behavior
At 640px and below, wrap the toolbar without changing action order. At 480px and below, move the model reload button below the input. Settings content scrolls vertically and reserves a stable scrollbar gutter. Avoid horizontal overflow.

## Interaction and motion
Provider presets populate a draft. Save commits it; Cancel restores the previous provider and model list. Preserve generated results across interface language changes. Use short CSS state transitions and honor prefers-reduced-motion. This utility needs no hero imagery or perpetual animation.

## Localization and content
All labels, hints, placeholders, accessible names, language names and regional names follow the interface locale (zh-TW, zh-CN, en). Samples follow that locale independently of the selected source-letter language. Model IDs and user-entered provider names remain literal. Guide formatting escapes text before permitting only bold emphasis.

## References
- https://fluent2.microsoft.design/accessibility
- https://fluent2.microsoft.design/
