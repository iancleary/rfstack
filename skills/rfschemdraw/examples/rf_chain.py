"""Minimal receive-chain block diagram. Render with `uv run --with schemdraw python rf_chain.py`."""

import schemdraw
import schemdraw.elements as elm
from schemdraw import flow


def build():
    schemdraw.use("svg")
    drawing = schemdraw.Drawing()
    drawing.config(fontsize=11)

    with drawing:
        antenna = flow.Box(w=2.0, h=1.0).label("Antenna\n50 Ω")
        preselector = flow.Box(w=2.2, h=1.0).right().label("Preselector\nTBD band")
        lna = flow.Box(w=1.8, h=1.0).right().label("LNA\nGain TBD")
        mixer = flow.Box(w=1.8, h=1.0).right().label("Mixer\nRF → IF")
        if_filter = flow.Box(w=2.0, h=1.0).right().label("IF Filter\nTBD BW")
        adc = flow.Box(w=1.8, h=1.0).right().label("ADC\nFs TBD")

        for start, end in (
            (antenna, preselector),
            (preselector, lna),
            (lna, mixer),
            (mixer, if_filter),
            (if_filter, adc),
        ):
            elm.Line(arrow="->").at(start.E).to(end.W)

        lo = flow.Box(w=1.8, h=0.9).down().at(mixer.S).label("LO\nTBD GHz")
        elm.Line(arrow="->").at(lo.N).to(mixer.S).label("LO", loc="right")

    return drawing


if __name__ == "__main__":
    build().save("rf_chain.svg")
