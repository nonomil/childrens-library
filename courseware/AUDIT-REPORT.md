# Courseware Code Audit Report

## 1. Template Categories and File Counts

### A. Fredoka One Nursery Rhymes (27 files)
abc-song, baa-baa-black-sheep, bingo, cat-and-fiddle, five-little-monkeys, head-shoulders, hickory-dickory, humpty-dumpty, hush-little-baby, if-youre-happy, itsy-bitsy-spider, jack-and-jill, jack-be-nimble, london-bridge, mary-lamb, mulberry-bush, old-macdonald, pat-a-cake, rain-go-away, ring-around-rosy, row-your-boat, silent-night, skidamarink, three-blind-mice, twinkle-twinkle, wheels-on-bus, yankee-doodle

**Pattern:** Fredoka One font, `.book` container, rounded book-like card with double border/shadow, `.controls` bottom bar with nav-btn prev/next, top-nav-btn home link + next button, `.page-dots` + `.page-counter`, SVG-based illustrations, playSong/showMusicNotes functions.

### B. Chinese Pinyin Series — Nintendo/Retro Style (9 files)
chinese-04-nature through chinese-12-yunmu

**Pattern:** Nunito body + Press Start 2P decorative font, `#1a1a2e` dark background, `.app` flex-column container, red `.top-bar` with home/sound buttons + lesson title, `.bottom-nav` with prev/next + page-dots, separate `.read-btn`, game-like celebration screens with starfield.

### C. Chinese Standalone Lessons (12 files)
chinese-01-characters, chinese-02-strokes, chinese-03-heaven-earth, chinese-13-body through chinese-18-animals, chinese-19-compound, chinese-20-reading, chinese-21-antonyms, chinese-22-qa, chinese-23-poems, chinese-24-adventure, chinese-magic-characters

**Pattern:** All use Nunito, but each has a unique/custom layout — no shared template. chinese-01 has `.book-card`, chinese-02 has scroll layout, chinese-13-18 have various full-screen designs, chinese-19+ use GSAP 3.12.5 with newer patterns.

### D. Converted English Lessons — Unified Nav Pattern (12 files)
english-06-family, english-07-animals, english-08-body, english-09-food, english-10-toys, english-11-weather, english-12-clothes, english-13-actions, english-14-places, english-15-feelings, english-16-time, english-17-transport

**Pattern:** Nunito font, bottom `.nav-bar` with prev/next + page-dots, `navGoTo/navPrev/navNext` functions, touch swipe support, read-btn with "读给我听", speak script with MP3→flat→TTS fallback.

### E. Early English Book Style — JS-Rendered Pages (5 files)
english-01-hello, english-02-abc, english-03-abc-nz, english-04-colors, english-05-numbers

**Pattern:** Nunito, `.book` container, pages rendered by JS into `#pages-container`, `.nav` with prev/next/dots/speak, `goToPage/nextPage/prevPage` naming, keyboard listener, confetti via GSAP.

### F. Math — .book Full-Screen Gradient (6 files)
math-13-numbers100, math-14-addsub2digit, math-15-money, math-16-clock, math-17-shapes, math-18-sorting

**Pattern:** Nunito, `.book` full-screen with gradient (blue), absolute `.top-bar` with home+speak, absolute-positioned `.slide` elements, `navGoTo` pattern, GSAP 3.12.2.

### G. Math — Confetti Canvas Enhanced (2 files)
math-11-measurement, math-12-review

**Pattern:** Nunito, canvas-confetti CDN, `.bottom-nav` with `navGoTo`, celebration slides with confetti bursts.

### H. Math — Various/Slider (5 files)
math-01-counting, math-02-counting-11to20, math-03-compare, math-04-addition, math-05-addition10

**Pattern:** Varied. math-03 uses horizontal `.slider` + `.slide` flex. math-04 uses custom CSS variables. math-05 uses `100dvh` slider.

### I. Math — Newer GSAP 3.12.5 (4 files)
math-19-statistics, math-20-direction, math-21-multiplication, math-22-fractions

**Pattern:** GSAP 3.12.5. math-19: simple scroll. math-20/21: fixed top-bar + scroll-container. math-22: fixed-size #app (1024x600).

### J. Math — Standalone (2 files)
math-23-word-problems (no GSAP, Segoe UI), math-24-carnival (Baloo 2 + Noto Sans SC, no GSAP)

### K. English — GSAP 3.12.5 Newer Lessons (6 files)
english-18-review, english-19-lost-cat, english-20-storm, english-21-birthday, english-22-farm, english-23-treasure, english-24-review

**Pattern:** GSAP 3.12.5, custom per-file layouts, english-21/23 use ScrollTrigger. english-22-farm is completely standalone (page IDs, goToPage, custom navigation).

### L. Storybook Style — .book Container (7 files)
gears-transmission, elephant-piggie-surprise, phonics-fat-cat, sight-word-tales-can-we-get-a-pet, sight-word-tales-come-to-the-party, rainforest-adventure, nature-lesson-4, english-colors, math-numbers-1-10

**Pattern:** Nunito, `.book` container, similar CSS reset, varying nav implementations.

---

## 2. Feature Matrix (5 Target Files)

| Feature | english-01-hello | chinese-04-nature | math-09-subtraction20 | english-22-farm | twinkle-twinkle |
|---------|-----------------|-------------------|----------------------|-----------------|-----------------|
| GSAP version | 3.12.2 | 3.12.2 | 3.12.2 (defer) | 3.12.5 | 3.12.2 |
| Nav functions | goToPage/next/prev | navGoTo/navPrev/navNext | navGoTo/navPrev/navNext | goToPage (by id) | prevPage/nextPage |
| Bottom nav bar | .nav (prev/dots/speak/next) | .nav-bar (prev/dots/next) + .read-btn | .nav-bar (prev/dots/next) + .read-btn | None (top bar only) | .controls (prev/music/read/sing/next) |
| Home button | No (no nav link) | .btn-home in top-bar | .home-btn in top-bar | Top bar only | .top-nav-btn.home (link) |
| Speak button | .speak-btn in nav bar | .btn-sound in top-bar + .read-btn | .speak-btn in top-bar + .read-btn | No speak button | .read-btn (separate) |
| Page dots | .dots | .page-dots | .page-dots | None | .page-dots + .page-counter |
| Touch/swipe | Yes (touchstart/move/end) | Yes | Yes | No (no touch handlers) | Yes |
| Confetti | Yes (GSAP-based DOM confetti) | No | No | No | CSS keyframe confetti |
| Font | Nunito (system stack) | Nunito + Press Start 2P | Nunito + PingFang SC | Nunito | Fredoka One |
| Keyboard nav | Yes (ArrowLeft/Right/Home) | No | No | Yes (ArrowRight/Left/Home) | No |
| Top bar | No | Yes (red) | Yes (blue, fixed) | Yes (green, fixed) | No (.top-nav-btn only) |
| Page transitions | CSS animation (fadeSlide) | CSS animation (fadeIn) | CSS animation (fadeIn) | GSAP tween (opacity) | CSS animation (fadeIn) |

**Key Navigation Differences:**
- **english-01-hello:** Bottom-only nav, no home button, nav in `.nav` div inline with speak btn
- **chinese-04-nature:** Dual nav (top bar + bottom nav-bar), has home+speak in top bar, separate read-btn below
- **math-09-subtraction20:** Dual nav (fixed top bar + bottom nav-bar), has home+speak in top bar, separate read-btn
- **english-22-farm:** Top bar only, no bottom nav, no page dots, GSAP-based page transitions, no speak button
- **twinkle-twinkle:** Top-nav-btn (home link + next button) + bottom .controls with music/speak buttons, page counter

---

## 3. Issues and Inconsistencies

### Navigation Pattern Inconsistencies
1. **3 different navigation paradigms**: (a) bottom-only nav, (b) top bar + bottom nav, (c) top-only nav
2. **2 function naming conventions**: `goToPage`/`nextPage`/`prevPage` vs `navGoTo`/`navPrev`/`navNext`
3. **Inconsistent home button placement**: Some have home in top bar, some as a link, some have none
4. **english-22-farm has no bottom nav at all** — completely different UX

### GSAP Version Fragmentation
- **3.12.2** used in ~95 files
- **3.12.5** used in 13 files (english-18-review, english-19-lost-cat, english-20-storm, english-21-birthday, english-22-farm, english-23-treasure, english-24-review, math-19-statistics, math-20-direction, math-21-multiplication, math-22-fractions, chinese-19-compound, chinese-20-reading)
- math-23 and math-24 have **no GSAP at all**

### Duplicated Code
2. **Speak page script** duplicated identically across ~80+ files (~50 lines each = ~4000+ lines total)
3. **Touch swipe handler** duplicated identically across ~80+ files
4. **Nav script** (navGoTo pattern) duplicated identically across ~60+ files
5. **CSS reset/boilerplate** duplicated across every file
6. **Confetti code** has at least 5 different implementations (GSAP DOM, canvas-confetti library, custom canvas draw, CSS animations, inline SVG)

### Code Quality Issues
1. **Inline event handlers** (`onclick`, `onerror`, `oncanplaythrough`) used pervasively instead of addEventListener
2. **No shared CSS/JS files** — zero code reuse between files
3. **No consistent build system** — all files are standalone HTML
4. **Mixed var/let/const** usage (var dominates older files, newer files mix)
5. **english-22-farm** loads GSAP at line 507 (mid-body), not in `<head>`
6. **english-01-hello** has no `lang="en"` despite being an English lesson (`lang="zh-CN"`)
7. **Some GSAP loads use `defer`** (math-09, math-10), most don't

### Broken/Missing Features
1. **english-22-farm** missing keyboard navigation for swipe (has keyboard but no touch)
2. **No font loading strategy** — no `font-display: swap` or preload for Google Fonts
3. **Confetti implementations are inconsistent** — some use GSAP, some canvas, some CSS
4. **Page counter** only in nursery rhyme template (twinkle-twinkle), not in lesson templates

---

## 4. Top 5 Recommended Improvements (Ranked by Impact)

1. **Create shared JS library** — Extract nav, speak, swipe, and confetti into a single shared JS file. Saves ~100+ lines per file, fixes inconsistency, enables centralized updates. **Impact: High** (reduces duplication, fixes nav inconsistency)

2. **Unify navigation template** — Choose one nav paradigm (recommend: top-bar with home+speak + bottom nav-bar with prev/dots/next). Convert all files to use same `navGoTo/navPrev/navNext` function names. **Impact: High** (consistent UX across all lessons)

3. **Standardize GSAP version to 3.12.5** — Update all files from 3.12.2 to 3.12.5. Add GSAP to math-23 and math-24. **Impact: Medium** (version consistency, bug fixes)

4. **Replace inline event handlers with addEventListener** — Refactor `onclick`, `onerror` etc. to use proper event listeners. Enables easier maintenance and debugging. **Impact: Medium** (code quality)

5. **Add proper font loading strategy** — Add `font-display: swap` to Google Fonts links, preload critical fonts, add fallback fonts consistently. **Impact: Low-Medium** (perceived performance)

---

## 5. Bugs and Broken Features

1. **english-01-hello has wrong `lang`** — Set to `zh-CN` but it's an English lesson
2. **english-22-farm lacks touch swipe** — Has keyboard nav but no touch handlers, making it unusable on tablets
3. **math-23 and math-24 have no GSAP** — If other parts of the app depend on GSAP being globally available, this could break shared functionality
4. **No 404/error handling for audio files** — MP3 loading silently fails, falling back to TTS without user feedback
5. **Confetti memory leak risk** — The GSAP-based DOM confetti (english-01-hello) creates 80+ DOM elements that are cleaned up with setTimeout after 2s, but if user navigates quickly, elements may accumulate
