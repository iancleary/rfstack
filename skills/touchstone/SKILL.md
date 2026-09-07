---
name: touchstone
description: Use the public Rust touchstone crate to parse, inspect, generate, resample, convert, cascade, save, or plot Touchstone S-parameter networks. Use for .sNp data and network matrices, not scalar RF conversions or abstract gain blocks.
---

# Touchstone

For uncertainty propagation from measured networks, use
[rf-monte-carlo](../rf-monte-carlo/SKILL.md) to define the sampling model and
preserve correlations before evaluating network realizations.

Use `touchstone` when measured or simulated S-parameter data is the source of
truth. Add the library with `cargo add touchstone`; install its CLI only when a
file or directory plotting workflow is requested.

## Select an entry point

- Parse a file with `Network::new(path)`.
- Parse uploaded or embedded data with `Network::from_bytes` or
  `Network::from_str`.
- Create synthetic data with `NetworkBuilder` and `SMatrix`.
- Read traces with `s_db`, `s_ri`, or `s_ma`.
- Read a complete frequency point with `s_matrix_at` or `sample_at`.
- Use `resample` for a new frequency grid.
- Use Y, Z, or ABCD conversion only when its rank and impedance assumptions fit.
- Save through `save`, `write_touchstone`, or `to_touchstone_string`.

Use `rfconversions` for scalar math, `gainlineup` for abstract hardware stages,
and `linkbudget` for end-to-end radio links.

## Preserve network semantics

- Port indices are 1-based. `s_db(2, 1)` means S21.
- Parsed and requested frequencies are in Hz, regardless of the file's declared
  display unit.
- Preserve `network.warnings`; they carry non-fatal parser diagnostics.
- Interpolate real and imaginary components. Do not interpolate wrapped phase or
  dB magnitude independently.
- Choose `Extrapolation::Error` by default. Use `Clamp` only when the caller
  accepts boundary-value extrapolation.
- Inspect `reference_impedance()`. Do not reduce per-port impedance metadata to
  the scalar `z0` field without an explicit assumption.
- ABCD conversion and ordinary cascade are two-port operations. Confirm rank,
  frequency alignment, reference impedance, and port orientation first.
- Prefer fallible parsing and serialization APIs. Do not use panic-style
  wrappers in service or batch paths.

## Verification

Test through public APIs with a small fixture. Check rank, frequency bounds,
reference impedance, warnings, and one decisive S-parameter. For round trips,
parse the serialized output and compare complex values with tolerances. For a
cascade, include a simple through or attenuator network with a known result.

The CLI can generate HTML and open a browser. Treat browser launch as a visible
side effect and use the library API when only data transformation is needed.

For current signatures, use the installed source or <https://docs.rs/touchstone>.
The upstream source is <https://github.com/iancleary/touchstone>.
