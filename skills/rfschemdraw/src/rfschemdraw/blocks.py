"""SVG-backed Schemdraw elements for RF signal-chain diagrams."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable, Union

from schemdraw.elements import ElementImage


BLOCK_ROOT = Path(__file__).resolve().parents[2] / "assets" / "blocks"


@dataclass(frozen=True)
class BlockSpec:
    """One RF block symbol and its stable lookup names."""

    id: str
    label: str
    relative_path: str
    aliases: tuple[str, ...] = ()

    @property
    def path(self) -> Path:
        return BLOCK_ROOT / self.relative_path

    def lookup_names(self) -> Iterable[str]:
        yield self.id
        yield self.relative_path
        yield Path(self.relative_path).name
        yield from self.aliases


def _load_blocks() -> tuple[BlockSpec, ...]:
    manifest = json.loads((BLOCK_ROOT / "manifest.json").read_text())
    specs = [
        BlockSpec(
            id=entry["id"],
            label=entry["label"],
            relative_path=entry["path"],
            aliases=tuple(entry.get("aliases", ())),
        )
        for entry in manifest["icons"]
    ]

    listed_paths = {spec.relative_path for spec in specs}
    for path in sorted(BLOCK_ROOT.rglob("*.svg")):
        relative_path = str(path.relative_to(BLOCK_ROOT))
        if relative_path in listed_paths:
            continue
        specs.append(
            BlockSpec(
                id=path.stem.casefold(),
                label=path.stem.replace("_", " ").replace("-", " ").title(),
                relative_path=relative_path,
                aliases=(path.name,),
            )
        )

    return tuple(specs)


_BLOCKS = _load_blocks()


def available_blocks() -> tuple[BlockSpec, ...]:
    """Return every RF block available to Schemdraw."""

    return _BLOCKS


def resolve_block(block: Union[str, BlockSpec]) -> BlockSpec:
    """Resolve a block ID, relative path, filename, or legacy alias."""

    if isinstance(block, BlockSpec):
        return block

    requested = block.casefold()
    matches = [
        spec
        for spec in _BLOCKS
        if any(requested == name.casefold() for name in spec.lookup_names())
    ]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        ids = ", ".join(spec.id for spec in matches)
        raise ValueError(f"ambiguous RF block {block!r}; matches: {ids}")

    ids = ", ".join(spec.id for spec in _BLOCKS)
    raise ValueError(f"unknown RF block {block!r}; available IDs: {ids}")


class RFBlock(ElementImage):
    """An SVG RF symbol with anchors for normal Schemdraw placement."""

    def __init__(self, block: Union[str, BlockSpec], size: float = 1.2, **kwargs):
        self.spec = resolve_block(block)
        super().__init__(
            str(self.spec.path),
            width=size,
            height=size,
            xy=(0, -size / 2),
            imgfmt="svg",
            **kwargs,
        )

        self.anchors.update(
            {
                "W": (0, 0),
                "E": (size, 0),
                "N": (size / 2, size / 2),
                "S": (size / 2, -size / 2),
                "center": (size / 2, 0),
                "start": (0, 0),
                "end": (size, 0),
            }
        )
        self.elmparams["drop"] = (size, 0)
