---
name: tty-design
description: Design and refine terminal TTY/TUI command flows for CLIs, especially pickers, menus, status screens, and interactive prompts. Use when work involves raw terminal mode, ANSI styling, session or symbol selectors, keyboard-driven CLI menus, or making terminal UX more scannable and reliable across terminal emulators.
metadata:
  short-description: Build reliable, scannable terminal pickers and TTY flows
---

# TTY Design

Use this skill when a CLI flow needs an interactive terminal surface rather than plain prompts.

## Goal

Produce TTY flows that are:

- consistent across commands
- readable at a glance
- safe in raw terminal mode
- compatible with common ANSI terminals, tmux panes, and narrow widths

## Core Rules

1. Separate terminal mechanics from workflow semantics.
   Put raw-mode input, alternate-screen lifecycle, redraw behavior, scrolling, and width handling in a shared shell. Keep command-specific logic limited to option eligibility, row formatting, filters, and post-selection execution.
2. Keep layouts strictly left-aligned.
   Do not place independent bits of information across the screen. Use vertical grouping: title, status, controls, examples, body, footer.
3. In raw mode, render lines with `\r\n`, not bare `\n`.
   Bare linefeeds can drift horizontally in raw-mode redraws.
4. Make ANSI styling width-safe.
   Trim, indent, and wrap based on visible width, not raw string length. ANSI escape sequences must not affect width math.
5. Scope the screen explicitly.
   Always show the current symbol, entity, or target in the title or status line. Do not assume the user remembers upstream context.

## Selection Semantics

### Single-select

- `enter` may accept the highlighted row
- preselecting the first option is acceptable

### Multi-select

- start with nothing selected
- `space` should feel additive
- `enter` must require at least one marked option
- provide `a` for select all visible and `u` for clear

Do not silently switch between single-select and multi-select semantics without changing the flow or making the scope obvious.

## Eligibility Rules

Never show options that cannot actually be acted on.

- symbol pickers should only show symbols with eligible downstream sessions
- session pickers should respect the current minimum-duration or other filter
- when only one eligible upstream entity exists, skip that selection step
- when skipping an upstream step, make the downstream picker clearly state the scope

## Header Design

Headers should be grouped into short lines:

- title
- status line
- blank spacer
- controls
- examples or filter syntax

Prefer short labeled lines over dense inline tables.

Good:

- `Select BTC sessions`
- `BTC  6 visible  2 selected  filter none`
- `Move j/k  Mark space`
- `Confirm enter`
- `Bulk a all, u clear`
- `Filter f duration`
- `Quit q`

Avoid:

- one-line control dumps
- right-aligned fragments
- explanatory paragraphs inside the picker

## Styling

Use ANSI styling sparingly:

- bold title
- emphasized active cursor marker
- clear selected state
- dim secondary metadata
- limited accent color for scope or active state

Do not rely on color alone to communicate state.

## Prompt Design

If the user must type freeform input inside a TTY flow:

- show examples on their own line
- avoid long wrapped instruction sentences
- include the current value when useful
- keep the actual input line visually distinct, for example with `> `

Example:

```text
Minimum duration for visible sessions
Examples: 300, 15m, 1h, 1h30m  |  blank clears  |  current none
>
```

## Fallback Contract

Every TTY flow should still have a non-interactive fallback:

- numbered plain-text listing
- explicit input prompt
- same eligibility rules as the TTY path

Do not let the fallback path drift into different semantics from the TTY path.

## Recommended Implementation Pattern

1. Resolve eligible entities first.
2. If more than one eligible upstream entity exists, pick one.
3. Open the shared picker for downstream selection.
4. Return typed selections to the command code.
5. Keep output-writing and execution outside the TTY module.

## Verification

When changing a TTY flow, verify:

- raw-mode redraw stays left-aligned
- ANSI styling does not break trimming
- narrow widths still keep key information visible
- multi-select preserves multiple marks
- single-select and multi-select `enter` semantics differ correctly
- omitted upstream arguments still produce the intended flow
