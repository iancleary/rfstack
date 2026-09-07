---
name: rfconversions
description: Use the public Rust rfconversions crate for scalar RF unit conversion, noise, wavelength, G/T, and compression-point math. Use when implementing or reviewing Rust RF calculations, not for hardware chains, S-parameter networks, or full link budgets.
---

# RF Conversions

Use `rfconversions` instead of rewriting common scalar RF equations. Add it with
`cargo add rfconversions`, then import the smallest module that owns the math.

## Choose the correct surface

- `power`: watts, milliwatts, dBm, dBW, and dB/linear ratios
- `frequency`: Hz/kHz/MHz/GHz/THz scaling and vacuum wavelength
- `noise`: noise figure, factor, temperature, kTB, Friis cascade, G/T, and N0
- `p1db`: input/output P1dB translation and cascade helpers
- `constants`: speed of light, Boltzmann constant, and 290 K reference temperature

Use `gainlineup` for ordered hardware stages, `touchstone` for `.sNp` data, and
`linkbudget` for an end-to-end radio link.

## Preserve RF semantics

- Read unit suffixes literally. Wavelength helpers take Hz and return meters.
- Add and subtract dB values only when the RF formula permits it.
- Convert dB ratios to linear values before multiplication or averaging.
- Distinguish dBm and dBW, which are absolute power units, from dB ratios.
- For Friis helpers, preserve the tuple contract: noise and gain are both dB in
  `cascade_noise_figure`, but noise factor and gain are linear in
  `cascade_noise_factor`.
- Treat noise temperature as kelvin and bandwidth as hertz.
- Do not silently clamp invalid physical inputs. Preserve the crate's numeric
  behavior unless the calling application defines a validation policy.

## Workflow

1. Name input variables with units, such as `frequency_hz`, `power_dbm`, and
   `temperature_k`.
2. Call the public helper directly. Avoid duplicating its equation nearby.
3. Keep intermediate quantities in one domain and convert only at boundaries.
4. Test a known RF identity and a round trip where the conversion has an inverse.
5. Use tolerances for floating-point assertions.

For current signatures, use the installed crate source or
<https://docs.rs/rfconversions>. The upstream source is
<https://github.com/iancleary/rfconversions>.
