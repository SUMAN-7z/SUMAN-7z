"""
Build a neofetch-style info card SVG to sit to the RIGHT of the ASCII portrait.

Static content, hand-authored below. Lines fade/slide in on a short stagger so
it feels like the panel is printing alongside the portrait.
"""

import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 480, 376
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 92
LINE_H = 20.5

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"
SECTION = "#58a6ff"
GREEN = "#3fb950"
ACCENT = "#22d3ee"

# ---------------------------------------------------------------------
# CONTENT
# ---------------------------------------------------------------------

ROWS = [
    ("host",),

    ("kv", "Now", "MCA Student @ CUTM"),
    ("kv", "Role", "Full Stack Developer"),
    ("kv", "Focus", "MERN • AI • Deep Learning"),
    ("kv", "Location", "Odisha, India"),

    ("gap",),

    ("sec", "Stack"),
    ("kv", "Frontend", "React, HTML, CSS, JavaScript"),
    ("kv", "Backend", "Node.js, Express.js"),
    ("kv", "Database", "MongoDB, MySQL"),
    ("kv", "Tools", "Git, GitHub, Vercel, Render"),

    ("gap",),

    ("sec", "Highlights"),
    ("bul", "Built multiple Full Stack web applications"),
    ("bul", "Building AI & Deep Learning projects"),
    ("bul", "Campus Placement Management System"),
    ("bul", "Open to Software Engineering internships"),
]


def esc(s):
    return html.escape(s)


def rise(inner, i):
    """Fade + slide animation."""
    if STATIC:
        return f"<g>{inner}</g>"

    delay = 0.15 + i * 0.06

    return (
        f'<g opacity="0" transform="translate(0,5)">'
        f'{inner}'
        f'<animate attributeName="opacity" '
        f'from="0" to="1" '
        f'begin="{delay:.2f}s" '
        f'dur="0.4s" '
        f'fill="freeze"/>'
        f'<animateTransform '
        f'attributeName="transform" '
        f'type="translate" '
        f'from="0 5" '
        f'to="0 0" '
        f'begin="{delay:.2f}s" '
        f'dur="0.4s" '
        f'fill="freeze" '
        f'calcMode="spline" '
        f'keySplines="0.2 0.8 0.2 1"/>'
        f'</g>'
    )


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',

    "<defs>",

    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/>'
    f'<stop offset="1" stop-color="{BG}"/>'
    f"</linearGradient>",

    "</defs>",

    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',

    f'<rect x="0.5" y="0.5" '
    f'width="{W-1}" height="{H-1}" '
    f'rx="12" fill="none" stroke="{FRAME}"/>',

    f'<line x1="0" y1="{TITLEBAR_H}" '
    f'x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

# macOS dots
for i, color in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(
        f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{color}"/>'
    )

# Title
parts.append(
    f'<text x="{W/2}" '
    f'y="{TITLEBAR_H/2 + 4}" '
    f'fill="{MUTED}" '
    f'font-size="12" '
    f'text-anchor="middle">'
    f'suman@github: ~$ neofetch'
    f'</text>'
)

y = TITLEBAR_H + 30

for i, row in enumerate(ROWS):

    kind = row[0]

    if kind == "gap":
        y += LINE_H * 0.5
        continue

    elif kind == "host":

        inner = (
            f'<text x="{KEY_X}" y="{y:.1f}" '
            f'font-size="14" font-weight="700">'
            f'<tspan fill="{GREEN}">suman</tspan>'
            f'<tspan fill="{MUTED}">@</tspan>'
            f'<tspan fill="{ACCENT}">github</tspan>'
            f'</text>'

            f'<line '
            f'x1="{KEY_X+118}" '
            f'y1="{y-4:.1f}" '
            f'x2="{W-PAD}" '
            f'y2="{y-4:.1f}" '
            f'stroke="{FRAME}" '
            f'stroke-opacity="0.8"/>'
        )

    elif kind == "sec":

        title = esc(row[1])

        inner = (
            f'<text '
            f'x="{KEY_X}" '
            f'y="{y:.1f}" '
            f'fill="{SECTION}" '
            f'font-size="12.5" '
            f'font-weight="700">'
            f'— {title}'
            f'</text>'

            f'<line '
            f'x1="{KEY_X + 16 + len(title) * 8}" '
            f'y1="{y-4:.1f}" '
            f'x2="{W-PAD}" '
            f'y2="{y-4:.1f}" '
            f'stroke="{FRAME}" '
            f'stroke-opacity="0.8"/>'
        )

    elif kind == "kv":

        key = esc(row[1])
        value = esc(row[2])

        inner = (
            f'<text '
            f'x="{KEY_X}" '
            f'y="{y:.1f}" '
            f'fill="{KEY}" '
            f'font-size="12.5" '
            f'font-weight="700">'
            f'{key}'
            f'</text>'

            f'<text '
            f'x="{VAL_X}" '
            f'y="{y:.1f}" '
            f'fill="{INK}" '
            f'font-size="12.5">'
            f'{value}'
            f'</text>'
        )

    elif kind == "bul":

        text = esc(row[1])

        inner = (
            f'<circle '
            f'cx="{KEY_X+3}" '
            f'cy="{y-4:.1f}" '
            f'r="2.5" '
            f'fill="{GREEN}"/>'

            f'<text '
            f'x="{KEY_X+14}" '
            f'y="{y:.1f}" '
            f'fill="{INK}" '
            f'font-size="12.5">'
            f'{text}'
            f'</text>'
        )

    else:
        continue

    parts.append(rise(inner, i))
    y += LINE_H

parts.append("</svg>")

svg = "".join(parts)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(
    f"Wrote {OUT}\n"
    f"Size: {W} × {H}\n"
    f"Content bottom: {round(y)}"
)