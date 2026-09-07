"""Minimal receive-chain block diagram using the bundled RF symbols."""

import schemdraw
import schemdraw.elements as elm

from rfschemdraw import RFBlock


def build():
    schemdraw.use("svg")
    drawing = schemdraw.Drawing(show=False)
    drawing.config(fontsize=8)

    with drawing:
        for block_id, label in (
            ("input", "Antenna\n50 Ω"),
            ("bandpass-filter", "Preselector\nTBD band"),
            ("lna", "LNA\nGain TBD"),
            ("mixer", "Mixer\nRF → IF"),
            ("bandpass-filter", "IF Filter\nTBD BW"),
            ("output", "ADC\nFs TBD"),
        ):
            drawing.add(RFBlock(block_id).label(label, loc="bottom"))
            drawing.add(elm.Line(arrow="->").right().length(0.9))

    return drawing


if __name__ == "__main__":
    build().save("rf_chain.svg")
