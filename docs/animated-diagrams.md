# Animated section diagrams (Becker-style)

Every section of an article can carry one animated diagram that shows the section's point with motion: lines drawing, counters ticking, nodes lighting up, bars rising. They are built for search first:

- the meaning is real text (an SVG `<title>`, `<text>` labels and a visible `<figcaption>`);
- the static HTML is the final frame, so pages work with no JS, for crawlers and for reduced-motion users;
- motion is progressive enhancement.

## Pieces

| File | Role |
|---|---|
| `tools/diagrams.py` | Generator. Each pattern function returns ONE line of HTML. |
| `src/styles/diagrams.css` | All diagram styling and keyframes. Imported by `src/pages/blog/[...slug].astro`, so every post gets it. |
| `src/pages/blog/[...slug].astro` | Holds the two inline scripts. One sets `html.dg-js`. The other is an IntersectionObserver (about 1 KB) that adds `.in` the first time a `.dg` is 35% visible, and toggles `.on` so loops pause off-screen. It also replays `.cnt` counters. |

There is no library, no canvas and no video. Only opacity, transform and stroke-dashoffset animate, so the diagrams cause no layout shift (box size comes from `viewBox`, `width`/`height` and CSS `aspect-ratio`).

## Using it in a post (.md)

Paste the generator output as a raw HTML block: one line, with a blank line before and after. Do not put a separate `<p class="dgcap">` after it, because the caption goes inside the figure.

```python
import sys; sys.path.insert(0, "tools"); import diagrams as D
print(D.timeline_cut("You cannot break a loop you cannot see.",
                     left="THE TIMELINE YOU CAME IN WITH", cut="WHERE THE LOOP BEGAN",
                     right="THE LOOP", ghost="WHERE IT WAS HEADED"))
```

Call `D._n[0] = 0` once per post before generating. Title ids are `dg1`, `dg2`... and only need to be unique within a page.

### Patterns

| Function | Use it when the point is... | Motion |
|---|---|---|
| `four_peaks(cap, t1, t2, hist[4], now[4])` | then vs now; many things happening at once | history bars rise and fall in a relay; a peak line draws; all four "now" bars rise together and pulse |
| `split_compare(cap, lt, rt, left[], right[], strike=False)` | two columns: myth vs truth, cause vs example | rows tick in; a gold current runs down the divider; chevrons light. `strike=True` crosses out and dims the left column. Use it only for myth/truth, never when the left column is not "wrong" |
| `wave_regulate(cap, l, r, c)` | chaos turning into order; state change | a jagged red line draws and jitters; a scanline sweeps; a calm gold wave draws |
| `timeline_cut(cap, left, cut, right, ghost)` | a path interrupted at one point, then a loop | a dot travels the line; the cut slams in with a ring; a red loop draws and keeps circling; a dashed "headed" line fades in |
| `scroll_reveal(cap, rows[], unit)` | a list of parts or sections | a document unrolls; a read-head scans down; rows light up; the counter ticks to N |
| `counters(cap, [{to, pre, suf, l1, l2}])` | 1-3 hard numbers | each number counts up from 0 with a fill bar under it. The HTML holds the final value. The font auto-shrinks to fit |
| `loop_point(cap, labels[3], point)` | a repeating pattern with one root | a loop spins; each label flashes red as it is reached; a gold point pulses and drops a line to its name |
| `body_signal(cap, a, b, c, d)` | a signal moving through a system | the outline draws; heart, brain and gut fire in order; sparks keep running the circuit |
| `quote_cards(cap, [{q, who}])` | customer or source words | real-text blockquotes slide in one by one |

Labels are UPPER CASE and short. `_fit()` adds `textLength` when a label would overflow its slot. It uses glyph widths measured in Chromium (`W` table), so keep row labels under about 24 characters.

### Writing a new pattern

Use the classes below with `style="--d:<delay>s;--t:<duration>s"`:

| Class | Static (final) frame | Animated |
|---|---|---|
| `pop` / `slide` / `slider` / `zoom` / `slam` | visible | fade up / in from left / in from right / scale in / overshoot hit |
| `draw` (needs `pathLength="1"`, plus `lin` for linear) | fully drawn | stroke draws |
| `grow`, `relay-hi`, `relay-lo` | full bar (`relay-lo` sits at 42%) | bar rises; relay rises to the top, then falls |
| `unroll`, `fade`, `lit`, `flashred`, `dimmed` | visible | unroll from top / fade / glow / flash red / end dimmed |
| `ring`, `scan`, `trav`, `readhead`, `run` | hidden (decorative only) | expanding ring / sweep / traveller / read-head / dash running along a path |
| `spin`, `pulse`, `heat`, `shake` | still | loops (paused off-screen) |

Rules:

1. Never put meaning only in motion or in a decorative-only layer. The static frame must say the whole point.
2. One diagram per section, and it must show that section's point. Captions stay one plain sentence.
3. Keep the `viewBox` at 360x200 (or 360x160 for counters). No external assets.
4. Do not edit `diagrams.css` per post. Add new patterns to the shared CSS and generator.

## QA before publishing

- `npm run build` passes.
- Headless check (Playwright):
  - before scrolling, a figure has no `.in` and its `.pop` layers are at opacity 0;
  - after scrolling plus 5 s, nothing is hidden, every `.draw` has dashoffset 0, and counters show their final value;
  - with `reduced_motion="reduce"` and with JS disabled, the end state shows immediately;
  - CLS from figures is 0.
- Script: `tools/verify_diagrams.py "<url pattern with {}>" default|reduced|nojs|video` (run with ~/.st-work/scrapling-venv/bin/python). Its screenshots and recordings are in `~/.st-work/glennbeck-ads/intel/anim/`.
