"""Animated section diagrams for intel.viralgrowthmedia.ai articles.

Every function returns ONE line of HTML (a <figure class="dgf">) that can be pasted
into a .md post as a raw HTML block (keep it on one line, blank line before and after).

Contract (see docs/animated-diagrams.md):
- Meaning lives in real text: SVG <title>, <text> labels and a visible <figcaption>.
- The markup with no JS / reduced motion IS the final frame. Animation is added only by
  src/styles/diagrams.css when <html> has .dg-js and the figure gets .in (IntersectionObserver
  in src/pages/blog/[...slug].astro). Counters (.cnt) hold their final value in the HTML.
- Fixed viewBox + width/height + CSS aspect-ratio: no layout shift.
- Timing per element: style="--d:<delay>s;--t:<duration>s".

CLI demo: python3 tools/diagrams.py  -> prints one of each.
"""
from html import escape

GOLD = "#d9b45a"
RED = "#e0453a"

_n = [0]

# Advance widths (SVG user units) measured in Chromium for the classes in src/styles/diagrams.css
# (DM Sans 700 13px .06em = t-s, DM Sans 600 11.5px .03em = t-xs, Cinzel 700 38px = t-big).
W = {"t-s": {"0": 9.86, "1": 5.6, "2": 8.33, "3": 8.66, "4": 9.26, "5": 8.87, "6": 9.03, "7": 7.78, "8": 9, "9": 9.03, " ": 4.3, "A": 10, "B": 9.09, "C": 10.36, "D": 9.92, "E": 8.38, "F": 8.04, "G": 10.91, "H": 10.08, "I": 4.35, "J": 7.85, "K": 9.3, "L": 8.06, "M": 12.27, "N": 10.29, "O": 10.9, "P": 8.79, "Q": 10.9, "R": 9, "S": 8.66, "T": 8.56, "U": 9.68, "V": 9.96, "W": 14.03, "X": 9.49, "Y": 9.04, "Z": 8.34, ",": 4.02, ".": 4.11, "+": 8.31, "-": 8.26, "−": 8.31, "/": 4.94, "'": 3.36, "’": 4.1, "“": 6.67, "”": 6.67, ":": 4.13, "×": 8.31, "●": 8.63, "?": 7.85, "&": 10.96}, "t-xs": {"0": 8.29, "1": 4.74, "2": 7.09, "3": 7.36, "4": 7.88, "5": 7.5, "6": 7.64, "7": 6.56, "8": 7.62, "9": 7.65, " ": 3.4, "A": 8.51, "B": 7.72, "C": 8.79, "D": 8.36, "E": 7.1, "F": 6.79, "G": 9.33, "H": 8.61, "I": 3.54, "J": 6.64, "K": 7.92, "L": 6.82, "M": 10.47, "N": 8.79, "O": 9.21, "P": 7.46, "Q": 9.21, "R": 7.65, "S": 7.35, "T": 7.24, "U": 8.21, "V": 8.48, "W": 12.08, "X": 8.07, "Y": 7.67, "Z": 7.1, ",": 3.27, ".": 3.34, "+": 7.01, "-": 6.96, "−": 7.01, "/": 4.04, "'": 2.65, "’": 3.28, "“": 5.55, "”": 5.55, ":": 3.36, "×": 7.01, "●": 7.29, "?": 6.7, "&": 9.38}, "t-big": {"0": 24.68, "1": 15.39, "2": 23.44, "3": 21.4, "4": 23.54, "5": 21.07, "6": 23.93, "7": 20.69, "8": 22.91, "9": 23.93, " ": 9.5, "A": 27.24, "B": 25.48, "C": 29.64, "D": 30.79, "E": 23.87, "F": 22.63, "G": 31.78, "H": 32.74, "I": 14.69, "J": 14.62, "K": 28.77, "L": 23.23, "M": 36.23, "N": 32.33, "O": 33.76, "P": 24.86, "Q": 33.91, "R": 28, "S": 21.97, "T": 25.95, "U": 31.21, "V": 28.49, "W": 37.11, "X": 27.72, "Y": 26.69, "Z": 25.13, ",": 8.76, ".": 8.44, "+": 18.28, "-": 14.44, "−": 18.28, "/": 16.19, "'": 7.61, "’": 9.29, "“": 16.94, "”": 16.69, ":": 8.44, "×": 15.65, "●": 22.95, "?": 17.54, "&": 30.66}}


def text_w(text, cls="t-xs"):
    """Estimated rendered width of upper-case label text."""
    tbl = W[cls]
    avg = sum(tbl.values()) / len(tbl)
    return sum(tbl.get(ch, tbl.get(ch.upper(), avg)) for ch in text)


def _fit(text, cls, maxw):
    """textLength clamp when a label would overflow its slot (keeps it real, selectable text)."""
    if text_w(text, cls) > maxw:
        return f' textLength="{maxw:g}" lengthAdjust="spacingAndGlyphs"'
    return ""


def _id(prefix="dg"):
    _n[0] += 1
    return f"{prefix}{_n[0]}"


def _t(d=None, t=None, extra=""):
    parts = []
    if d is not None:
        parts.append(f"--d:{d:g}s")
    if t is not None:
        parts.append(f"--t:{t:g}s")
    if extra:
        parts.append(extra)
    return f' style="{";".join(parts)}"' if parts else ""


def _fig(kind, inner, title, caption, vb=(360, 200), uid=None):
    """Wrap SVG content in the standard figure: dark box + svg(title) + figcaption."""
    uid = uid or _id()
    w, h = vb
    cap = f'<figcaption class="dgcap">{caption}</figcaption>' if caption else ""
    return (f'<figure class="dgf" data-dg="{kind}"><div class="dg" style="aspect-ratio:{w}/{h}">'
            f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="{uid}" '
            f'xmlns="http://www.w3.org/2000/svg"><title id="{uid}">{escape(title)}</title>{inner}</svg>'
            f'</div>{cap}</figure>')


def _ring(cx, cy, r, d, color=GOLD, loop=False):
    """Expanding ring (decorative, invisible in the static frame)."""
    cls = "ring loopy" if loop else "ring"
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" class="{cls}" stroke="{color}"{_t(d)}/>'


# --------------------------------------------------------------------------- patterns

def four_peaks(caption, t1="BEFORE: ONE FALLS, ANOTHER RISES", t2="NOW: ALL FOUR AT THE PEAK AT ONCE",
               hist=("ROME", "FRANCE", "WEIMAR", "BRITAIN"), now=("CHINA", "EUROPE", "JAPAN", "U.S.")):
    """History row: a relay, each power rises then the low ones fall. Now row: all four
    rise together, a gold peak line draws over them and they pulse hot."""
    o = [f'<text x="12" y="16" class="t-s pop"{_t(0)}>{t1}</text>']
    for i, n in enumerate(hist):
        x = 22 + i * 84
        lo = i % 2 == 0
        d = 0.25 + i * 0.5
        o.append(f'<rect x="{x}" y="26" width="54" height="52" class="bar {"relay-lo" if lo else "relay-hi"}" '
                 f'fill="#3a3a3a"{_t(d, 1.0)}/>')
        o.append(f'<text x="{x+27}" y="94" text-anchor="middle" class="t-xs pop"{_t(d)}>{n}</text>')
    o.append(f'<line x1="12" y1="126" x2="348" y2="126" class="ln gold draw" pathLength="1"{_t(2.5, .9)}/>')
    o.append(f'<text x="12" y="116" class="t-s gold pop"{_t(2.6)}>{t2}</text>')
    for i, n in enumerate(now):
        x = 22 + i * 84
        o.append(f'<g class="heat"{_t(4.0 + i * .12)}><rect x="{x}" y="128" width="54" height="44" class="bar grow" '
                 f'fill="{RED}"{_t(3.0, .8)}/></g>')
        o.append(f'<text x="{x+27}" y="190" text-anchor="middle" class="t-xs pop"{_t(3.0)}>{n}</text>')
        o.append(_ring(x + 27, 128, 8, 3.8))
    title = f"{t1}: {', '.join(hist)}. {t2}: {', '.join(now)}."
    return _fig("four_peaks", "".join(o), title, caption)


def split_compare(caption, lt, rt, left, right, strike=False):
    """Two columns. Rows tick in left then right; a gold current runs down the divider and
    a chevron lights per row. strike=True crosses out and dims the left column (myth vs truth)."""
    o = [f'<text x="14" y="28" class="t-s red slide"{_fit(lt, "t-s", 158)}{_t(0)}>{lt}</text>',
         f'<text x="190" y="28" class="t-s gold slider"{_fit(rt, "t-s", 160)}{_t(.15)}>{rt}</text>',
         '<line x1="180" y1="10" x2="180" y2="190" stroke="#333"/>',
         f'<line x1="180" y1="10" x2="180" y2="190" class="ln gold thin draw" pathLength="1"{_t(.3, .6 + .8 * len(left))}/>']
    for i in range(max(len(left), len(right))):
        y = 70 + i * 44
        d = .5 + i * .8
        if i < len(left):
            dim = " dimmed" if strike else ""
            lw = text_w("× " + left[i])
            o.append(f'<text x="14" y="{y}" class="t-xs slide{dim}"{_fit("× " + left[i], "t-xs", 156)}{_t(d)}>'
                     f'<tspan class="red">×</tspan> {left[i]}</text>')
            if strike:
                x0 = 14 + min(lw, 156) * text_w("× ") / lw
                o.append(f'<line x1="{x0+1:.0f}" y1="{y-4}" x2="{14+min(lw, 156)-1:.0f}" y2="{y-4}" class="ln red thin draw" '
                         f'pathLength="1"{_t(d + .35, .35)}/>')
        o.append(f'<path d="M176 {y-9} l7 5 l-7 5" class="ln gold thin pop"{_t(d + .3)}/>')
        if i < len(right):
            o.append(f'<text x="190" y="{y}" class="t-xs slider"{_fit("● " + right[i], "t-xs", 160)}{_t(d + .45)}>'
                     f'<tspan class="gold">●</tspan> {right[i]}</text>')
            o.append(_ring(194, y - 4, 4, d + .55))
    pairs = "; ".join(f"{a} -> {b}" for a, b in zip(left, right))
    title = f"{lt} versus {rt}: {pairs}."
    return _fig("split_compare", "".join(o), title, caption)


def wave_regulate(caption, l="SCARED", r="REGULATED", c="SAME BODY. DIFFERENT SIGNAL."):
    """Jagged red signal draws and jitters; a scan line sweeps; it turns into a calm gold wave."""
    jag = "M10 100 L30 60 L45 140 L60 50 L75 150 L90 70 L105 130 L120 55 L135 145 L150 80 L165 120 L180 100"
    calm = "M180 100 C 200 75, 220 75, 240 100 S 280 125, 300 100 S 330 80, 350 100"
    o = [f'<line x1="10" y1="100" x2="350" y2="100" stroke="#2a2418" stroke-dasharray="3 5"/>',
         f'<text x="12" y="24" class="t-s red pop"{_t(0)}>{l}</text>',
         f'<g class="shake"{_t(1.4)}><path d="{jag}" class="ln red draw lin" pathLength="1"{_t(.1, 1.3)}/></g>',
         f'<path d="{calm}" class="ln gold draw" pathLength="1"{_t(1.45, 1.3)}/>',
         f'<path d="{calm}" class="ln bright run" pathLength="1"{_t(2.9, 2.2)}/>',
         f'<rect x="8" y="40" width="3" height="120" rx="1.5" fill="{GOLD}" class="scan"{_t(.1, 2.8)}/>',
         f'<text x="348" y="24" text-anchor="end" class="t-s gold pop"{_t(2.4)}>{r}</text>',
         f'<text x="180" y="188" text-anchor="middle" class="t-xs pop"{_t(2.9)}>{c}</text>']
    title = f"A jagged {l.lower()} signal becoming a smooth {r.lower()} wave. {c}"
    return _fig("wave_regulate", "".join(o), title, caption)


def timeline_cut(caption, left="THE TIMELINE YOU CAME IN WITH", cut="ONE EXACT POINT",
                 right="THE LOOP SINCE", ghost="WHERE IT WAS HEADED"):
    """A dot travels the gold timeline, hits the cut (flash), falls into a red loop that keeps
    circling; the dashed line it was on fades in toward where it was headed."""
    loop = "M190 100 C 215 60, 245 60, 255 100 S 300 140, 300 100 S 270 60, 255 100 S 225 140, 210 100"
    o = [f'<text x="12" y="34" class="t-s pop"{_fit(left, "t-s", 330)}{_t(0)}>{left}</text>',
         f'<line x1="12" y1="100" x2="170" y2="100" class="ln gold draw lin" pathLength="1"{_t(.2, 1.0)}/>',
         f'<circle cx="12" cy="100" r="5" fill="#fff6d8" class="trav"{_t(.2, 1.0, "--x:160px")}/>',
         f'<line x1="176" y1="100" x2="340" y2="100" class="ln ghost fade" pathLength="1" stroke-dasharray="0.02 0.02"{_t(2.9, .8)}/>',
         _ring(176, 100, 9, 1.2, RED),
         f'<g class="slam"{_t(1.15, .45)}><circle cx="176" cy="100" r="9" fill="{RED}"/>'
         f'<line x1="166" y1="84" x2="186" y2="116" stroke="#000" stroke-width="3"/></g>',
         f'<text x="176" y="140" text-anchor="middle" class="t-s red pop"{_t(1.3)}>{cut}</text>',
         f'<path d="{loop}" class="ln red draw" pathLength="1"{_t(1.5, 1.3)}/>',
         f'<path d="{loop}" class="ln hot run" pathLength="1"{_t(2.8, 1.8)}/>',
         f'<text x="348" y="60" text-anchor="end" class="t-s red pop"{_fit(right, "t-s", 150)}{_t(1.9)}>{right}</text>',
         f'<text x="340" y="188" text-anchor="end" class="t-s gold pop"{_t(3.2)}>{ghost}</text>']
    title = f"{left}, cut at {cut}, then {right}. The dashed line shows {ghost.lower()}."
    return _fig("timeline_cut", "".join(o), title, caption)


def scroll_reveal(caption, rows=("CORE IDENTITY PATTERN", "RELATIONSHIP LOOP", "MONEY / VALUE PATTERN",
                                 "TIMING + DELAY", "SELF-SABOTAGE SIGNATURE", "VISIBILITY / EXPRESSION",
                                 "NERVOUS SYSTEM DISTORTION", "HIGHEST TIMELINE"), unit="SECTIONS"):
    """The document unrolls, a gold read-head scans down, each section lights up as it passes,
    and the section counter ticks up beside it."""
    step = .3
    o = [f'<rect x="72" y="14" width="216" height="176" rx="6" class="unroll" fill="#141414" stroke="{GOLD}"{_t(0, .8)}/>',
         f'<rect x="76" y="24" width="208" height="17" rx="3" fill="{GOLD}" class="readhead"'
         f'{_t(.7, step * len(rows), f"--y:{(len(rows)-1)*19}px")}/>']
    for i, x in enumerate(rows):
        d = .7 + i * step
        o.append(f'<g class="pop"{_t(d)}><circle cx="90" cy="{34+i*19}" r="4" fill="{GOLD}"/>'
                 f'<text x="102" y="{38+i*19}" class="t-xs lit"{_t(d, .9)}>{x}</text></g>')
    end = .7 + step * len(rows)
    o.append(f'<text x="324" y="104" text-anchor="middle" class="t-big gold pop cnt" data-to="{len(rows)}" '
             f'data-ms="{int(step*len(rows)*1000)}"{_t(.6)}>{len(rows)}</text>')
    o.append(f'<text x="324" y="126" text-anchor="middle" class="t-xs pop"{_t(.6)}>{unit}</text>')
    o.append(_ring(324, 92, 14, end))
    title = f"The {len(rows)} sections of a Scroll: {', '.join(r.title() for r in rows)}."
    return _fig("scroll_reveal", "".join(o), title, caption)


def counters(caption, items):
    """1-3 big numbers that count up from zero with a gold bar filling underneath.
    items: [{"to": 16000, "pre": "", "suf": "+", "l1": "SCROLL SCANS", "l2": "ORDERED"}]"""
    w = 360 // max(1, len(items))
    o = []
    for i, it in enumerate(items):
        cx = w * i + w // 2
        d = .1 + i * .35
        pre, suf = it.get("pre", ""), it.get("suf", "")
        fin = f'{pre}{it["to"]:,}{suf}'
        size = min(1.0, (w - 14) / max(1, text_w(fin, "t-big")))
        fs = f"font-size:{38 * size:.1f}px" if size < 1 else ""
        o.append(f'<text x="{cx}" y="84" text-anchor="middle" class="t-big gold pop cnt" data-to="{it["to"]}" '
                 f'data-pre="{pre}" data-suf="{suf}"{_t(d, extra=fs)}>{fin}</text>')
        o.append(f'<line x1="{cx-44}" y1="102" x2="{cx+44}" y2="102" stroke="#2a2418" stroke-width="4" stroke-linecap="round"/>')
        o.append(f'<line x1="{cx-44}" y1="102" x2="{cx+44}" y2="102" class="ln gold draw" pathLength="1"{_t(d, 1.4)}/>')
        o.append(f'<text x="{cx}" y="126" text-anchor="middle" class="t-xs pop"{_t(d + .3)}>{it["l1"]}</text>')
        o.append(f'<text x="{cx}" y="142" text-anchor="middle" class="t-xs pop"{_t(d + .4)}>{it.get("l2","")}</text>')
    title = "; ".join(f'{it.get("pre","")}{it["to"]:,}{it.get("suf","")} {it["l1"].lower()} {it.get("l2","").lower()}'.strip()
                      for it in items) + "."
    return _fig("counters", "".join(o), title, caption, vb=(360, 160))


def loop_point(caption, labels=("SAME PERSON, NEW FACE", "MONEY COMES CLOSE", "PROGRESS, THEN SABOTAGE"),
               point="THE POINT IT ALL STARTED"):
    """A red loop keeps circling; each repeat flashes as the arrow passes it; then the gold point
    underneath lights up and a line drops to its name."""
    pos = [(180, 36, "middle"), (352, 168, "end"), (8, 168, "start")]
    o = [f'<g class="zoom"{_t(0, .6)}><g class="spin" style="transform-origin:180px 105px">'
         f'<circle cx="180" cy="105" r="52" class="ln red" stroke-dasharray="8 6"/>'
         f'<path d="M232 105 l-8 -10 l16 0 z" fill="{RED}"/></g></g>']
    for i, ((x, y, an), lab) in enumerate(zip(pos, labels)):
        d = .5 + i * .55
        o.append(f'<text x="{x}" y="{y}" text-anchor="{an}" class="t-xs pop flashred"{_t(d, 1.0)}>{lab}</text>')
    o += [_ring(180, 105, 7, 2.3, GOLD, loop=True),
          f'<g class="pop"{_t(2.2)}><circle cx="180" cy="105" r="7" fill="{GOLD}" class="pulse"/></g>',
          f'<line x1="180" y1="114" x2="180" y2="178" class="ln gold thin draw" pathLength="1"{_t(2.4, .5)}/>',
          f'<text x="180" y="196" text-anchor="middle" class="t-s gold pop"{_t(2.8)}>{point}</text>']
    title = f"A loop that repeats: {', '.join(labels)}. Underneath it: {point}."
    return _fig("loop_point", "".join(o), title, caption)


def body_signal(caption, a="BRAIN", b="HEART", c="GUT", d="ONE ELECTRICAL SYSTEM"):
    """The body outline draws; heart fires first, the signal runs up to the brain, then down to
    the gut; each node lights as it is reached and sparks keep running the circuit."""
    up = "M172 92 C 150 70, 160 50, 180 40"
    down = "M180 40 C 205 70, 205 110, 180 128"
    o = [f'<circle cx="180" cy="40" r="22" class="ln gold draw" pathLength="1"{_t(0, .7)}/>',
         f'<path d="M180 62 L180 150 M140 85 L220 85 M180 150 L150 195 M180 150 L210 195" class="ln gold draw" pathLength="1"{_t(.3, 1.0)}/>',
         # leaders from labels to nodes
         f'<line x1="68" y1="92" x2="160" y2="92" class="ln ghost thin draw" pathLength="1"{_t(1.0, .4)}/>',
         f'<line x1="64" y1="40" x2="150" y2="40" class="ln ghost thin draw" pathLength="1"{_t(1.9, .4)}/>',
         f'<line x1="50" y1="128" x2="168" y2="128" class="ln ghost thin draw" pathLength="1"{_t(2.8, .4)}/>',
         _ring(172, 92, 6, 1.0, RED),
         f'<g class="pop"{_t(1.0)}><circle cx="172" cy="92" r="6" fill="{RED}" class="pulse"/></g>',
         f'<text x="16" y="96" class="t-xs pop"{_t(1.0)}>{b}</text>',
         f'<path d="{up}" class="ln red draw" pathLength="1"{_t(1.2, .7)}/>',
         _ring(180, 40, 5, 1.9),
         f'<g class="pop"{_t(1.9)}><circle cx="180" cy="40" r="5" fill="{GOLD}" class="pulse"/></g>',
         f'<text x="16" y="44" class="t-xs pop"{_t(1.9)}>{a}</text>',
         f'<path d="{down}" class="ln gold draw" pathLength="1"{_t(2.1, .7)}/>',
         _ring(180, 128, 5, 2.8),
         f'<g class="pop"{_t(2.8)}><circle cx="180" cy="128" r="5" fill="{GOLD}" class="pulse"/></g>',
         f'<text x="16" y="132" class="t-xs pop"{_t(2.8)}>{c}</text>',
         f'<path d="{up}" class="ln hot run" pathLength="1"{_t(3.2, 1.2)}/>',
         f'<path d="{down}" class="ln bright run" pathLength="1"{_t(3.8, 1.2)}/>',
         f'<text x="348" y="114" text-anchor="end" class="t-xs gold pop"{_fit(d, "t-xs", 120)}{_t(3.2)}>{d}</text>']
    title = f"The body as {d.lower()}: a signal runs from the {b.lower()} to the {a.lower()} to the {c.lower()}."
    return _fig("body_signal", "".join(o), title, caption)


def quote_cards(caption, quotes):
    """Real-text testimonial cards that slide in one by one; the gold rule grows down each card.
    quotes: [{"q": "...", "who": "..."}] (q may contain HTML entities)."""
    cards = "".join(f'<blockquote class="qc slide"{_t(.15 + i * .5, .6)}><p>&ldquo;{q["q"]}&rdquo;</p>'
                    f'<cite>{q["who"]}</cite></blockquote>' for i, q in enumerate(quotes))
    cap = f'<figcaption class="dgcap">{caption}</figcaption>' if caption else ""
    return f'<figure class="dgf" data-dg="quote_cards"><div class="dg qwrap">{cards}</div>{cap}</figure>'


PATTERNS = {f.__name__: f for f in [four_peaks, split_compare, wave_regulate, timeline_cut, scroll_reveal,
                                     counters, loop_point, body_signal, quote_cards]}

if __name__ == "__main__":
    print(timeline_cut("You cannot break a loop you cannot see."))
    print(counters("Measured numbers.", [{"to": 37, "suf": "T", "l1": "CELLS, UPPER", "l2": "ESTIMATE"}]))
