---
name: linkbudget
description: Use the public Rust linkbudget crate for end-to-end satellite or terrestrial RF links, including EIRP, FSPL, G/T, C/No, Eb/No, BER, margin, modulation, FEC, sensitivity, Doppler, PFD, orbit geometry, EVM, and quantization.
---

# Link Budget

For uncertain receiver or link parameters and probabilistic margin, use
[rf-monte-carlo](../rf-monte-carlo/SKILL.md) and its receiver/link reference.

Use `LinkBudget` with `Transmitter`, `PathLoss`, and `Receiver` when the whole
link must close. Use a focused module directly when the task asks for one
formula. Add the crate with `cargo add linkbudget`.

Use `touchstone` for `.sNp` networks, `gainlineup` for ordered hardware stages,
and `rfconversions` for standalone scalar conversions.

## Keep quantities explicit

- Powers use dBm or dBW as named; antenna gains use dBi.
- Frequencies and bandwidths use Hz. Distances use meters.
- C/No uses dB-Hz. SNR, Eb/No, coding gain, losses, and margins use dB.
- Separate noise bandwidth, occupied bandwidth, bit rate, symbol rate, and code
  rate. Do not substitute one for another because their numbers look similar.
- Treat `frequency_dependent_loss` as an added link loss, such as rain fade.
- Choose signs from the API contract. Do not pre-negate losses before passing
  them to a field that already represents loss.

## Choose the smallest model

- Full link: `LinkBudget`
- EIRP: `Transmitter`
- receiver noise and G/T: `Receiver`
- free-space loss: `PathLoss`
- modulation and bandwidth: `Modulation`
- coded performance: `CodedModulation`, `FecCode`, or DVB-S2 presets
- C/No, Eb/No, Es/No, and Ec/No: `energy`
- BER and required Eb/No: `ber`
- receiver MDS: `sensitivity`
- motion and geometry: `doppler` and `orbits`
- regulatory flux: `pfd`
- implementation metrics: `evm` and `quantization`

Select matched-filter or bandpass sensitivity deliberately. The matched-filter
model does not add raised-cosine roll-off penalty; the bandpass model does.
Treat theoretical BER and nominal coding-gain outputs as model results, not as a
substitute for measured modem performance.

## Verification

Build a named link and report the assumptions beside the result. Verify at
least EIRP, FSPL, received power, G/T or noise floor, C/No, Eb/No, BER target,
and margin when they apply. Cross-check one value with a dimensional identity,
such as C/No minus bit-rate-in-dB-Hz equals Eb/No. Use scenario tests and
floating-point tolerances.

For current signatures, use the installed source or <https://docs.rs/linkbudget>.
The upstream source is <https://github.com/iancleary/linkbudget>.
