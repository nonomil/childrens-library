# Battle Conclusion: Option 1 Wins

## The Verdict

**Option 1 — Lightweight OPT-IN shared library with NO forced navigation.**

## Why Option 1

The shared library should extract what is **truly universal**: `speakText` (or SpeakPage MP3/TTS), `playClick`, `confetti`, and swipe gesture handling. These functions are copy-pasted with near-identical code across 100+ files. That is the real duplication problem.

Navigation must stay file-local because **every file's navigation is fundamentally different**:

| File | Nav Style | Why it can't be standardized |
|---|---|---|
| english-07-animals | `goToPage(index, direction)` | GSAP transitions, confetti hook, custom dot management, per-page auto-speech |
| twinkle-twinkle | `prevPage/nextPage` → `renderPage(idx)` | Tracks `gameDone[]` state, quiz/cover/starfind page types, `.page-counter` |
| chinese-04-nature | `goToPage(n)` | GSAP opacity, 1-indexed pages, confetti at specific pages, custom `updateDots/updateButtons` |
| english-22-farm | `goToPage(id_string)` | GSAP timeline, **string-based page IDs** (`page-story-0`, `page-cover`), completely incompatible with index-based nav |

Even the "successful" english-06 migration is fragile — it only works because that file happened to already use `navGoTo` naming. english-07 and chinese-04 both have the unified nav wrapper appended, but their **inline scripts remain the real navigation authority**, creating two competing systems. Confetti hooks, GSAP animations, and per-page game state logic are all tangled into the inline `goToPage`. The wrapper can't replace it.

## Why the other options lose

**Option 2 (Modular with adapters) is over-engineering.** The "base" library (speak + confetti + swipe) is ~50 lines. The "adapters" for each type would each be 30-60 lines — almost as much as the original navigation code. We'd create a fragile abstraction layer with 4+ adapters, each needing maintenance when a file changes. And some files (english-22-farm with string IDs, GSAP) don't fit any existing type. Adapters for "one-off" files defeat the purpose.

**Option 3 (Only migrate compatible files) solves nothing.** Files like english-07 and chinese-04 look like they use `navGoTo` but their real navigation is the inline `goToPage` with GSAP and confetti — the unified nav wrapper is just a thin shell that doesn't actually control page transitions. The amount of truly compatible files (already using `navGoTo` with a simple `classList.toggle` page system) is tiny. We'd migrate 5 files and leave 95 untouched. The duplication problem remains.

## The Plan

1. Extract `shared/courseware.js` containing only: `speakText()`, `playClick()`, `fireConfetti()`, `initSwipe()` — with sensible defaults per language.
2. Each file imports the shared lib via `<script src="../shared/courseware.js"></script>` and removes its inline copy of these functions.
3. Navigation stays exactly as-is in each file. No adapter, no wrapper, no forced naming convention.
4. Files are migrated one at a time, file by file, with zero risk of breaking navigation.

This maximizes gain (eliminates the real duplication) with zero risk (no navigation changes). Anything more ambitious will break pages.
