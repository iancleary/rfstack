---
name: gainlineup
description: Use the public Rust gainlineup crate to model ordered RF hardware chains with gain, noise figure, compression, IP3, dynamic range, and AM-AM or AM-PM behavior. Do not use for raw S-parameter networks or end-to-end radio links.
---

# Gain Lineup

For tolerance, yield, or probabilistic margin analysis, use
[rf-monte-carlo](../rf-monte-carlo/SKILL.md) and its hardware cascade reference.

Model an RF chain as one `Input` followed by ordered `Block` values. Add the
crate with `cargo add gainlineup`.

## Build the model

1. Define `Input` with signal power in dBm, frequency and bandwidth in Hz, and
   optional source noise temperature in kelvin.
2. Define one `Block` per stage with gain, noise figure, and optional output P1dB
   and output IP3.
3. Call `cascade_vector_return_vector` when intermediate nodes matter. Call
   `cascade_vector_return_output` when only the final result matters.
4. Use block or cascade sweep APIs for AM-AM and gain-compression curves.
5. Use `AmplifierModel` for AM-PM or richer amplifier characterization.

Use `touchstone` when stages come from `.sNp` network data, `linkbudget` for
radio-link closure, and `rfconversions` for isolated scalar conversions.

## Preserve lineup semantics

- Stage order changes cascaded noise and linearity results.
- Negative `gain_db` represents loss. A passive loss normally has an equal,
  positive `noise_figure_db` at the reference temperature.
- P1dB and IP3 fields are output-referred dBm values.
- `noise_temperature_k` belongs to the input source; it is not a block noise
  figure.
- `SignalNode` cumulative fields describe the chain through that node.
- The current compression model clamps output at output P1dB plus 1 dB. State
  this approximation when results approach compression.
- Use unit-suffixed TOML fields. Short aliases such as `pin`, `f`, and `bw` can
  hide that their units are dBm and Hz.

## Verification

Check at least one node-by-node result, not only the final output. A useful
fixture has an early LNA, a passive loss, and a later gain stage. Verify total
gain, plausible Friis noise figure, signal power, and any configured compression
or IP3 result. Use tolerances for floating-point values. Add a sweep assertion
when changing compression behavior.

The CLI reads TOML and writes HTML. Use it for reviewable lineup reports; use
the library for programmatic analysis. Enable `RUST_LOG=gainlineup=debug` when
intermediate cascade math needs diagnosis.

For current signatures, use the installed source or <https://docs.rs/gainlineup>.
The upstream source is <https://github.com/iancleary/gainlineup>.
