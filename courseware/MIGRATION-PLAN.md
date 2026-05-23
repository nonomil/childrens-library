# Courseware Migration Plan

Based on AUDIT-REPORT.md (12 template types) and first-20-lines analysis of all files.

**Excluded (already done):** english-06-family, nature-lesson-4

---

## Type A: Nursery Rhymes Fredoka — 27 files

Fredoka One font, `.book` container, rounded card with double border/shadow, `.controls` bottom bar, SVG illustrations, playSong/showMusicNotes, page-dots + page-counter.

Files: abc-song, baa-baa-black-sheep, bingo, cat-and-fiddle, five-little-monkeys, head-shoulders, hickory-dickory, humpty-dumpty, hush-little-baby, if-youre-happy, itsy-bitsy-spider, jack-and-jill, jack-be-nimble, london-bridge, mary-lamb, mulberry-bush, old-macdonald, pat-a-cake, rain-go-away, ring-around-rosy, row-your-boat, silent-night, skidamarink, three-blind-mice, twinkle-twinkle, wheels-on-bus, yankee-doodle

**Representative:** `twinkle-twinkle.html`

## Type B: Chinese Pinyin Retro — 8 files

Nunito + Press Start 2P, `#1a1a2e` dark background, `.app` flex-column, red `.top-bar` with home/sound + title, `.bottom-nav` with prev/dots/next, separate `.read-btn`.

Files: chinese-04-nature, chinese-05-family, chinese-06-school, chinese-07-pinyin, chinese-09-shengmu1, chinese-10-shengmu2, chinese-11-shengmu3, chinese-12-yunmu

**Representative:** `chinese-04-nature.html`

## Type C: Chinese Standalone Custom — 16 files

Nunito, each unique layout. chinese-01 has `.book-card`, chinese-02 scroll layout, chinese-13-18 full-screen designs, chinese-19+ use GSAP 3.12.5.

Files: chinese-01-characters, chinese-02-strokes, chinese-03-heaven-earth, chinese-13-body, chinese-14-colors, chinese-15-food, chinese-16-actions, chinese-17-direction-time, chinese-18-animals, chinese-19-compound, chinese-20-reading, chinese-21-antonyms, chinese-22-qa, chinese-23-poems, chinese-24-adventure, chinese-magic-characters

**Representative:** `chinese-01-characters.html`

## Type D: Converted English — Unified Nav — 11 files

Nunito, bottom `.nav-bar` (prev/dots/next), `navGoTo/navPrev/navNext`, touch swipe, speak btn, top bar with home.

Files: english-07-animals, english-08-body, english-09-food, english-10-toys, english-11-weather, english-12-clothes, english-13-actions, english-14-places, english-15-feelings, english-16-time, english-17-transport

**Representative:** `english-07-animals.html`

## Type E: Early English Book — JS-Rendered Pages — 5 files

Nunito, `.book` container, JS-rendered `#pages-container`, `.nav` with goToPage/nextPage/prevPage naming, keyboard listener, confetti via GSAP.

Files: english-01-hello, english-02-abc, english-03-abc-nz, english-04-colors, english-05-numbers

**Representative:** `english-01-hello.html`

## Type F: Math .book Full-Screen Gradient — 6 files

Nunito, `.book` full-screen blue gradient, absolute `.top-bar` with home+speak, absolute `.slide` elements, `navGoTo`.

Files: math-13-numbers100, math-14-addsub2digit, math-15-money, math-16-clock, math-17-shapes, math-18-sorting

**Representative:** `math-13-numbers100.html`

## Type G: Math Confetti Canvas — 2 files

Nunito, canvas-confetti CDN, `.bottom-nav` with `navGoTo`, celebration slides with confetti bursts.

Files: math-11-measurement, math-12-review

**Representative:** `math-11-measurement.html`

## Type H: Math Various/Slider — 5 files

All Nunito + GSAP 3.12.2 but different layouts. math-03 uses `.slider`+`.slide` flex. math-04 uses CSS variables. math-05 uses 100dvh slider.

Files: math-01-counting, math-02-counting-11to20, math-03-compare, math-04-addition, math-05-addition10

**Representative:** `math-03-compare.html`

## Type I: Math Converted Retrofit — 5 files

Nunito, GSAP 3.12.2. Originally had custom nav (`.bottom-nav` or `.nav-dots`), retrofitted with unified `.nav-bar` + `navGoTo`. Dual CSS patterns coexist.

Files: math-06-subtraction5, math-07-subtraction10, math-08-addition20, math-09-subtraction20, math-10-shapes

**Representative:** `math-09-subtraction20.html`

## Type J: Math Newer GSAP 3.12.5 — 4 files

GSAP 3.12.5, custom per-file layouts. math-19 simple scroll, math-20/21 fixed top-bar + scroll-container, math-22 fixed-size 1024x600 app.

Files: math-19-statistics, math-20-direction, math-21-multiplication, math-22-fractions

**Representative:** `math-19-statistics.html`

## Type K: Math Standalone — 2 files

math-23 no GSAP (Segoe UI), math-24 no GSAP (Baloo 2 + Noto Sans SC).

Files: math-23-word-problems, math-24-carnival

**Representative:** `math-23-word-problems.html`

## Type L: English GSAP 3.12.5 Newer — 7 files

GSAP 3.12.5, custom per-file layouts. english-21/23 use ScrollTrigger. english-22 is completely standalone (page IDs, goToPage by id, no bottom nav).

Files: english-18-review, english-19-lost-cat, english-20-storm, english-21-birthday, english-22-farm, english-23-treasure, english-24-review

**Representative:** `english-22-farm.html`

## Type M: Storybook Style — 9 files

Nunito, `.book` or `.book-card` container, warm gradient backgrounds, varying nav implementations, similar CSS reset.

Files: gears-transmission, elephant-piggie-surprise, phonics-fat-cat, sight-word-tales-can-we-get-a-pet, sight-word-tales-come-to-the-party, rainforest-adventure, english-colors, math-numbers-1-10, i-am-an-apple

**Representative:** `rainforest-adventure.html`

---

## Migration Difficulty

### EASIEST (most uniform, least custom code)

| Rank | Type | Reason |
|------|------|--------|
| 1 | **D — Converted English** | Already have navGoTo/.nav-bar, closest to english-06-family pattern |
| 2 | **A — Nursery Rhymes** | 27 nearly identical files, pure SVG content swap, simple nav |
| 3 | **B — Chinese Pinyin** | 8 consistent files, same template, no confetti |
| 4 | **G — Math Confetti Canvas** | Only 2 files, similar structure, canvas-confetti is standard CDN |
| 5 | **I — Math Converted Retrofit** | Already have navGoTo, just need to strip duplicate nav CSS |

### HARDEST (most custom code, unique layouts)

| Rank | Type | Reason |
|------|------|--------|
| 1 | **C — Chinese Standalone** | 16 files, each completely unique, no shared template at all |
| 2 | **L — English GSAP 3.12.5** | Custom per-file layouts, ScrollTrigger, english-22 has no bottom nav |
| 3 | **H — Math Various/Slider** | All have different layout mechanisms (slider flex, CSS vars, 100dvh) |
| 4 | **M — Storybook** | Varying nav implementations, unique content structure per file |
| 5 | **F — Math .book Gradient** | Absolute-positioned slides, dual nav (top bar + bottom) to untangle |

### Key Migration Notes

- **Confetti:** 5 different implementations across codebase (GSAP DOM, canvas-confetti library, custom canvas draw, CSS animations, inline SVG). Type A uses CSS keyframe confetti, Type E uses GSAP DOM confetti (memory leak risk), Type G uses canvas-confetti CDN.
- **Nav naming:** 3 naming conventions — `goToPage/nextPage/prevPage` (Type E), `navGoTo/navPrev/navNext` (Types D/F/G/I), and custom per-file (Type L).
- **Touch swipe:** Missing in english-22-farm and some Storybook files.
- **Speak code:** ~50 lines of duplicated speak logic in every file (~80+ copies). The shared library in courseware.js handles this.
