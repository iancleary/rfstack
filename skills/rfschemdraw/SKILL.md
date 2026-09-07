---
name: rfschemdraw
description: Render clear RF signal-chain block diagrams with Schemdraw when a design, review, or test document needs a reproducible functional view of the RF path. Do not use for circuit-level schematics, PCB layout, or EM models.
---

# RF Schemdraw

Create RF-chain block diagrams as repo-local Python and SVG artifacts. Show the
functional signal path, its important operating conditions, and the boundaries
that matter to a reviewer.

## Use this skill when

- the document needs a receive, transmit, transceiver, frequency-conversion, or
  test signal-chain diagram
- the diagram should show stages such as antenna, filter, limiter, LNA, mixer,
  LO, IF gain, ADC/DAC, PA, coupler, switch, or load
- the artifact must be reproducible from a checked-in Python source file

Do not use this skill for circuit schematics with component values, PCB routing,
S-parameter plots, impedance-matching networks, or physical mechanical layout.

## Diagram contract

Before drawing, establish only the information the diagram needs:

- signal direction and whether the path is RX, TX, bidirectional, or test-only
- the stage order and any branches, bypasses, or calibration injection points
- operating band or center frequency, where it changes
- interface impedance and reference plane when it matters, normally `50 Ω`
- the decisive performance labels: gain/loss, noise figure, output power,
  bandwidth, conversion frequency, or sample rate

State unknown values as `TBD`; do not invent electrical performance.

## Drawing rules

- Draw the main RF path left to right. Use arrows only in the signal direction.
- Use one rounded block per functional stage. Keep each block label to a role
  plus at most two decisive values.
- Put frequency conversion and local-oscillator injection on a separate branch.
- Label ports and boundaries explicitly: antenna, cable, test port, 50 Ω load,
  ADC, DAC, or baseband.
- Use a consistent visual distinction for RF, LO, IF, and digital paths when
  color is requested. The diagram must still make sense without color.
- Use notes below or beside the path for assumptions. Do not cram prose into
  blocks.
- Treat the diagram as a functional block diagram, not proof of electrical
  correctness.

## RF block asset library

`assets/blocks/` contains the RF block SVG library copied from `rfsystems`.
The local `rfschemdraw` Python package registers every SVG as an `RFBlock`
Schemdraw element with `W`, `E`, `N`, `S`, `center`, `start`, and `end` anchors.
Use these elements in diagrams instead of treating the SVGs as loose images.

Keep the category paths and `manifest.json` intact so asset IDs continue to map
to the same symbols. `input` and `output` are registered from their SVG paths
because the upstream manifest does not list them.

The library includes amplifiers, attenuators, filters, mixers, switches,
splitters, combiners, couplers, phase blocks, endpoints, and a generic block.
Use the generic block only when no specific symbol exists.

## Workflow

1. Start from `examples/rf_chain.py` and import `RFBlock` from `rfschemdraw`.
2. Keep the source beside its consumer, usually under `docs/diagrams/`.
3. Export SVG by default. Commit the Python source and SVG together when the
   SVG is published or reviewed.
4. Render with a project-managed environment. A simple local invocation is:

   ```sh
   uv run --project <path-to-skill>/skills/rfschemdraw \
     python docs/diagrams/<name>.py
   ```

5. List or preview the integrated RF symbols when needed:

   ```sh
   uv run --project <path-to-skill>/skills/rfschemdraw rfschemdraw list
   uv run --project <path-to-skill>/skills/rfschemdraw \
     rfschemdraw gallery /tmp/rf-block-gallery.svg
   ```

6. Inspect the rendered SVG. Verify stage order, arrow direction, labels, and
   legibility at the document's normal display size.

## Output contract

Return the source path, render command, SVG path, and any values left as `TBD`.
