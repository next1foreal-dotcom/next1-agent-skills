---
name: blob-crew-icons
description: Create playful flat blob project, app, avatar, or sticker icons with vivid bodies, minimal black faces, and pale or deep squircle tiles using the portable Blob Crew SVG renderer.
---

# Blob Crew icons

Use this skill when a project needs a small, expressive icon family that stays crisp in code and remains legible at 32px. The renderer is deterministic: it builds SVG and raster PNG assets from explicit shape, eye, mouth, color, and placement parameters.

## Setup

Run these commands from the Skill directory (`skills/blob-crew-icons/` in this repository, or the directory created when this Skill is copied elsewhere):

```bash
python -m pip install -r requirements.txt
```

The Skill directory is self-contained: `scripts/crew.py`, `requirements.txt`, `examples/`, and `showcase/` travel together. The renderer has no private-path or network dependency.

## Render the built-in family

From the Skill directory:

```bash
python scripts/crew.py tint
python scripts/crew.py deep
```

The command writes `png/<theme>/<id>.png`, matching SVG files, and `sheet-<theme>.png`. Supported themes are `tint`, `deep`, `analog`, `cream`, and `black`. Run it from a disposable output directory or move the generated files into your own project after review.

For portable examples that do not depend on the built-in `CREW` preset list:

```bash
python examples/project-icons.py --output ./example-output/project-icons
python examples/skill-icons.py --output ./example-output/skill-icons
```

Both examples locate `scripts/crew.py` relative to their own Skill directory, so the copied Skill remains runnable without the original repository as a parent. The examples are reproduction fixtures, not additional renderer features.

## Visual rules

- Use a squircle tile (superellipse, `n=5`) with a warm-cream tint or an explicitly chosen deep partner color.
- Make the character one vivid, flat body color with no body gradient and no outline added by the caller. Keep it large, tilted no more than about 10 degrees, and allow controlled edge bleed.
- Choose one silhouette per project: gummy, drop, nub, scallop, bitten, box, shield, bubble, ears, play, or spiky. Add a custom path only when the concept cannot be expressed by those shapes.
- Make the face pure black. Eyes carry the personality; use dot, googly, pixel, shades, heart, x, happy, sleepy, wink, cyclops, or mask. A mouth is optional and small.
- Add at most one small black prop outside the body, normally at the top-right or bottom-right, when it improves recognition.
- In a family, vary hue, silhouette, and eye type. Avoid text, shading, decorative noise, and unrequested extra colors.
- Keep the renderer's soft blurred body shadow and 2x raster/downsample pipeline. Do not reintroduce offset flat shadows or rim-light copies.

## Color and deep tiles

The default tile is the body hue mixed 80% toward `#FFF9F0`, with a soft top-lighter linear gradient. For `deep`, choose a separate partner for each character and prioritize value contrast. Warm or light bodies can sit on deep cool tiles; mid or dark bodies can sit on bright warm tiles. Do not use a single background color for every icon in a set.

`icon()` accepts `bg=`, `prop_col=`, `flat_bg=`, and `deep=`. `themed(id, theme)` applies the built-in family palettes. For a new family, pass an explicit config to `icon()` rather than changing the renderer's geometry without a reason.

## Authoring a new icon

Add a config to the smallest local example or to your own calling script. A config normally contains `c`, `shape`, `eye`, optional `mth`, `look`, `tilt`, `pos`, `scale`, `face`, `gap`, and optional prop fields (`pr`, `prop_at`, `prop_rot`, `prop_col`). Keep coordinates in the renderer's 1024px viewBox.

Validate every new icon by parsing its SVG, rendering the 1024px PNG, checking the 64px and 32px thumbnails, and opening the generated sheet. Confirm that the output has one intended body silhouette, a readable face, no unintended extra colors or text, and no private input data.

## Distribution

This Skill can be installed manually by copying the complete `skills/blob-crew-icons/` directory into `~/.agents/skills/` or `~/.claude/skills/`. The current Skills CLI also documents:

```bash
pnpm dlx skills add next1foreal-dotcom/next1-agent-skills --skill blob-crew-icons
```

The CLI command is documented for this repository; this package review did not run the installer. Running the renderer from the copied Skill directory is the relevant local smoke check.