## Direction: Extract shared JS library from duplicated inline scripts

### What
Create a lightweight, zero-dependency shared JS library (`docs/courseware/shared/courseware.js`) that extracts the four most-duplicated code blocks — speak-page (MP3→TTS), unified navigation (`navGoTo`/`navPrev`/`navNext`), touch swipe, and confetti — and reference it from each HTML file via a single `<script>` tag. Each file drops ~150 lines of duplicate code and gains centralized bug fixing.

### Why this over others
This is the root cause of most other issues:

- **Navigation inconsistency** exists because there's no shared nav — fix it once in the library, all files get the fix.
- **4000+ lines of duplicated speak code** is the single largest maintenance debt. One bug in the speak logic (e.g., the audio fallback chain) has to be fixed in 80+ places today.
- **GSAP version fragmentation and inline event handlers** are symptoms of the same problem: no shared code means every file is its own island, making any cross-cutting change expensive.
- The audit's #1 recommendation was this. It's also the most **feasible** change for standalone HTML files — no build system, no bundler, just a `<script src="...">` tag added to each `<head>`. Every other option (unify nav, standardize GSAP, refactor event handlers) either depends on shared code or becomes dramatically cheaper once shared code exists.

### Implementation approach
1. Create `docs/courseware/shared/courseware.js` containing the four extracted modules, each wrapped in a self-contained IIFE or plain object, gated by feature detection so they don't throw if markup is absent.
2. One `<link rel="stylesheet">` to `docs/courseware/shared/courseware.css` for the shared animation keyframes (`speakPulse`, `fadeIn`, confetti styles).
3. In each HTML file, replace the duplicated inline blocks with a single `<script src="../shared/courseware.js"></script>` and the CSS link.
4. Keep each file's lesson-specific code (page content, illustration SVGs, per-lesson styles) in place — the shared library only owns **infrastructure** (nav, speak, swipe, confetti).
5. Add a minimal migration guide comment at the top of courseware.js explaining the pattern for future authors.

### Estimated effort
- **~80 HTML files** to modify (add script tag + remove inline blocks)
- Each file takes ~2 minutes of mechanical editing = ~3 hours
- Shared JS file: ~200 lines
- Shared CSS file: ~30 lines
- Unknown: some files use diverged naming (`goToPage` vs `navGoTo`, custom `speak()` vs `navSpeakCurrentPage()`) — these need per-file shims or a config object

### What it unlocks
- **Centralized bug fixes**: fix audio fallback, add `addEventListener`, or add keyboard nav once.
- **Consistent UX**: all files automatically get the same nav behavior, home button placement, swipe sensitivity.
- **One GSAP version**: the shared library can load GSAP 3.12.5 and expose it to the page, so individual files no longer need their own GSAP `<script>` tag.
- **Future features**: dark mode, progress tracking, or analytics — add to the library, all 80 files get it.
- **Reduced new-file friction**: a new lesson template becomes `<script src="../shared/courseware.js"></script>` + page-specific content, instead of copy-pasting 150 lines of boilerplate.

### First concrete step
Extract the "Speak Page" IIFE (the most-duplicated block, ~80 lines including the CSS keyframes) into `docs/courseware/shared/courseware.js`, add the shared CSS file, then pick one lesson (e.g., `english-06-family`) and migrate it to use the shared library. Verify TTS, MP3 fallback, and the speak button pulse animation all work identically. Then note any per-file config (course name, language) that needs to be parameterized before the bulk migration.
