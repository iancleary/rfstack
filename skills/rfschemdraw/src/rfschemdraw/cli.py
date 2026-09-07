"""Command-line inspection and gallery rendering for RF blocks."""

from __future__ import annotations

import argparse
from pathlib import Path

import schemdraw

from .blocks import RFBlock, available_blocks


def render_gallery(output: Path, columns: int = 6) -> Path:
    """Render every registered RF block to one SVG gallery."""

    schemdraw.use("svg")
    drawing = schemdraw.Drawing(show=False)
    drawing.config(fontsize=7)

    for index, spec in enumerate(available_blocks()):
        column = index % columns
        row = index // columns
        drawing.add(
            RFBlock(spec, size=1.2)
            .at((column * 2.2, -row * 2.0))
            .label(spec.label, loc="bottom")
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    drawing.save(str(output))
    return output


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rfschemdraw")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="list registered RF block IDs")

    gallery = subparsers.add_parser("gallery", help="render every RF block")
    gallery.add_argument("output", type=Path)
    gallery.add_argument("--columns", type=int, default=6)
    return parser


def main() -> None:
    args = _parser().parse_args()
    if args.command == "list":
        for spec in available_blocks():
            print(f"{spec.id}\t{spec.relative_path}")
        return

    if args.columns < 1:
        raise SystemExit("--columns must be at least 1")
    print(render_gallery(args.output, columns=args.columns))
