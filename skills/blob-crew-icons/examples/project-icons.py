"""Render the five fictional project-test configs with the original Blob Crew compositor.

Usage from the Skill directory:
    python examples/project-icons.py
    python examples/project-icons.py --output ./tmp/blob-projects
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
import crew  # noqa: E402

CONFIG_PATH = Path(__file__).with_name("project-icons.json")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("example-output/project-icons"),
        help="directory for generated PNG and SVG files",
    )
    args = parser.parse_args()
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    cases = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    for case in cases:
        config = case["config"]
        image = crew.render(config)
        image.save(output / f"{case['id']}.png")
        (output / f"{case['id']}.svg").write_text(
            crew.icon(**config, ss=1), encoding="utf-8"
        )
        print(f"rendered {case['id']} / {case['project']} / {image.size[0]}px")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
