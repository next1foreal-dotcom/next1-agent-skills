"""Render the five approved Skill-cover vectors with the original Blob Crew compositor.

The custom bodies and faces below are the small, portable subset needed to reproduce
those covers. They are intentionally separate from the default CREW presets.

Usage from the Skill directory:
    python examples/skill-icons.py
    python examples/skill-icons.py --output ./tmp/blob-skill-covers
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
import crew  # noqa: E402

PATHS = {
    "long-nose": "M-330,-90 C-440,-220 -350,-350 -255,-310 C-183,-276 -234,-205 -160,-170 C-86,-326 130,-342 279,-230 C404,-138 408,109 302,245 C211,357 -18,360 -159,282 C-242,237 -281,150 -270,77 C-322,93 -386,53 -387,-7 C-387,-49 -365,-78 -330,-90Z",
    "clay-hatchling": "M-170,-215 C-165,-363 -61,-422 55,-361 C134,-320 147,-235 132,-155 C255,-189 367,-127 386,-11 C411,137 277,270 135,233 C68,216 40,195 -4,163 C-72,261 -191,326 -298,255 C-416,178 -413,24 -327,-59 C-282,-102 -228,-115 -178,-109 C-178,-153 -173,-184 -170,-215Z",
    "pulled-puddle": "M-315,61 C-395,-11 -341,-139 -241,-207 C-146,-272 -32,-277 89,-274 C156,-272 191,-294 220,-353 C241,-398 274,-429 315,-415 C376,-393 371,-320 334,-277 C277,-214 263,-170 276,-110 C298,-18 349,79 315,211 C288,312 201,336 136,297 C62,252 50,249 -18,294 C-109,354 -170,321 -199,268 C-230,214 -206,171 -247,133 C-271,111 -292,85 -315,61Z",
    "folded-critter": "M-310,315 C-319,204 -287,135 -300,52 C-320,-19 -300,-99 -254,-140 C-343,-143 -387,-217 -366,-288 C-347,-353 -286,-386 -224,-362 C-193,-350 -173,-328 -151,-320 C-130,-398 -56,-439 14,-408 C91,-374 109,-291 100,-224 C182,-273 277,-250 307,-182 C327,-138 306,-103 273,-74 C365,-44 388,37 346,100 C391,165 357,257 284,280 C285,347 236,382 167,369 L-238,369 Q-304,365 -310,315Z",
    "fork-tail": "M-2,-337 C116,-327 190,-242 221,-169 C266,-228 316,-287 371,-273 C445,-250 414,-145 360,-86 C420,-10 445,90 393,130 C350,164 274,138 210,99 C183,195 103,284 -28,299 C-200,319 -353,204 -370,36 C-391,-165 -232,-351 -2,-337Z",
}


def body(kind: str, color: str, _background: str) -> str:
    return f'<path fill="{color}" d="{PATHS[kind]}"/>'


def eyes(kind: str, *_args: object) -> str:
    if kind == "long-nose":
        return '<circle cx="-2" cy="-35" r="34" fill="#111111"/><circle cx="147" cy="-53" r="34" fill="#111111"/><path d="M12,66 Q73,133 137,61 Q152,129 78,148 Q8,145 12,66Z" fill="#111111"/>'
    if kind == "clay-hatchling":
        return '<ellipse cx="-149" cy="-17" rx="79" ry="103" fill="#fff"/><ellipse cx="-130" cy="-13" rx="40" ry="52" fill="#111111"/><path d="M24,-1 Q87,28 146,-8 M72,2 Q87,53 111,5" fill="none" stroke="#111111" stroke-width="29" stroke-linecap="round"/><ellipse cx="-24" cy="123" rx="28" ry="30" fill="#111111"/>'
    if kind == "pulled-puddle":
        return '<ellipse cx="-95" cy="-61" rx="59" ry="71" fill="#fff" stroke="#111111" stroke-width="15"/><ellipse cx="72" cy="-9" rx="49" ry="60" fill="#fff" stroke="#111111" stroke-width="15"/><ellipse cx="-77" cy="-72" rx="29" ry="36" fill="#111111"/><ellipse cx="58" cy="1" rx="26" ry="31" fill="#111111"/><path d="M-80,78 Q-17,67 9,103 Q-13,181 -63,151 Q-83,131 -80,78Z" fill="#111111"/>'
    if kind == "folded-critter":
        return '<circle cx="-119" cy="-99" r="28" fill="#111111"/><circle cx="12" cy="-90" r="28" fill="#111111"/><path d="M-101,3 L-25,-7" fill="none" stroke="#111111" stroke-width="25" stroke-linecap="round"/>'
    if kind == "fork-tail":
        return '<path d="M-219,-43 A119,119 0 0 0 19,-43Z" fill="#fff"/><path d="M-219,-49 Q-92,-30 19,-42 L-219,-49Z" fill="#111111"/><path d="M-219,-44 H-77 V40 Q-138,64 -180,23 Q-215,2 -219,-44Z" fill="#111111"/><path d="M-172,110 Q-129,164 -80,112" fill="none" stroke="#111111" stroke-width="28" stroke-linecap="round"/>'
    raise KeyError(kind)


crew.body = body
crew.eyes = eyes

CONFIGS = {
    "joyboy-ip": {
        "c": "#FFD60A",
        "bg": "#4B2BB5",
        "shape": "long-nose",
        "eye": "long-nose",
        "tilt": -8,
        "pos": (502, 540),
        "scale": 0.99,
        "face": (0, 0),
        "deep": True,
    },
    "monster-forge": {
        "c": "#FF6A1A",
        "bg": "#2A1E8C",
        "shape": "clay-hatchling",
        "eye": "clay-hatchling",
        "tilt": 5,
        "pos": (512, 560),
        "scale": 1.02,
        "face": (0, 0),
        "deep": True,
    },
    "blob-crew-icons": {
        "c": "#3AA8FF",
        "bg": "#FF7A1A",
        "shape": "pulled-puddle",
        "eye": "pulled-puddle",
        "tilt": 5,
        "pos": (505, 559),
        "scale": 0.98,
        "face": (0, 0),
        "deep": True,
    },
    "resume-designer": {
        "c": "#9B5CFF",
        "bg": "#C8F25A",
        "shape": "folded-critter",
        "eye": "folded-critter",
        "tilt": -5,
        "pos": (507, 545),
        "scale": 0.99,
        "face": (0, 0),
        "deep": True,
    },
    "album-cover": {
        "c": "#19D47A",
        "bg": "#3B0F5C",
        "shape": "fork-tail",
        "eye": "fork-tail",
        "tilt": -6,
        "pos": (492, 558),
        "scale": 1.0,
        "face": (0, 0),
        "deep": True,
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("example-output/skill-icons"),
        help="directory for generated PNG and SVG files",
    )
    args = parser.parse_args()
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    for name, config in CONFIGS.items():
        destination = output / name
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "icon.svg").write_text(
            crew.icon(**config, ss=1), encoding="utf-8"
        )
        image = crew.render(config)
        for size in (1024, 512, 256, 128, 64, 32):
            thumbnail = image if size == 1024 else image.resize(
                (size, size), Image.Resampling.LANCZOS
            )
            thumbnail.save(destination / f"icon-{size}.png")
        print(f"rendered {name} / 1024px + 512/256/128/64/32px")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
