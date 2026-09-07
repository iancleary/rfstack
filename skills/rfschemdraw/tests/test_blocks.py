import tempfile
from pathlib import Path
import unittest

from rfschemdraw import BLOCK_ROOT, RFBlock, available_blocks, resolve_block
from rfschemdraw.cli import render_gallery


class BlockRegistryTests(unittest.TestCase):
    def test_all_svg_assets_are_registered(self):
        specs = available_blocks()
        asset_paths = {
            str(path.relative_to(BLOCK_ROOT)) for path in BLOCK_ROOT.rglob("*.svg")
        }
        registered_paths = {spec.relative_path for spec in specs}
        self.assertEqual(len(specs), 46)
        self.assertEqual(len({spec.id for spec in specs}), 46)
        self.assertEqual(registered_paths, asset_paths)
        self.assertTrue(all(spec.path.is_file() for spec in specs))

    def test_manifest_ids_aliases_and_endpoints_resolve(self):
        self.assertEqual(resolve_block("lna").relative_path, "amplifiers/LNA.svg")
        self.assertEqual(resolve_block("LNA.svg").id, "lna")
        self.assertEqual(resolve_block("input").relative_path, "endpoints/input.svg")
        self.assertEqual(resolve_block("output.svg").id, "output")

    def test_rf_block_exposes_chain_anchors(self):
        block = RFBlock("bandpass-filter")
        self.assertEqual(block.anchors["W"], (0, 0))
        self.assertEqual(block.anchors["E"], (1.2, 0))
        self.assertEqual(block.elmparams["drop"], (1.2, 0))

    def test_gallery_renders_every_block(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "gallery.svg"
            render_gallery(output)
            self.assertTrue(output.is_file())
            self.assertGreater(output.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
