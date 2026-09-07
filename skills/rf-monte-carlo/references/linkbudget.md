# Receiver and link margin

Use this reference for uncertain receiver performance or end-to-end link closure.
Choose the reference plane before sampling: power already at the receiver input
must not receive antenna gain or propagation loss a second time.

## Trial mapping

For receiver-only analysis, construct `Receiver` with sampled `temperature`,
`noise_figure`, and `bandwidth`, then call `calculate_snr(input_power_dbm)`.
Its current implementation computes kTB from temperature and bandwidth and adds
noise figure in dB. Check the physical meaning of the supplied temperature so
receiver noise is not counted twice. The `gain` field is used by G/T; it is not
added by `calculate_snr`.

For a complete link, construct `LinkBudget` with `Transmitter`, `PathLoss`, and
`Receiver`, plus any supported extra loss. Sample underlying causes such as
distance or rain attenuation, then derive received power through the model.
Do not independently sample received power as well unless it represents a
separate, defined residual uncertainty.

Keep bandwidth fields consistent when they represent the same channel. If they
represent different quantities, document the relationship. Discrete waveform
configurations need explicit scenario probabilities or separate reports.

## Compare like metrics

For a stated SNR threshold, return actual SNR minus required SNR. For an Eb/No
requirement with information bit rate `R_b` and noise bandwidth `B_n`, use:

```text
C/No [dB-Hz] = SNR [dB] + 10 log10(B_n [Hz])
Eb/No [dB] = C/No [dB-Hz] - 10 log10(R_b [bit/s])
margin [dB] = actual Eb/No - required Eb/No
```

Use `linkbudget::energy` helpers for these conversions. Preserve the code-rate
and information/coded-bit convention used by the BER requirement. SNR and Eb/No
are numerically equal only when `R_b / B_n = 1`. Recompute the conversion per
trial if the rate or noise bandwidth changes.

Use the crate's BER or coded-modulation helpers for required Eb/No when their
assumptions match the task. Handle a missing result explicitly; do not replace it
with a plausible constant. Inspect rate assumptions in `LinkBudget` convenience
methods before using them for a specified waveform. Treat coding gain as an
approximation unless supported by the modem's measured performance.

## Public starting point

[The upstream receiver example](https://github.com/iancleary/linkbudget/tree/main/examples/montecarlo-cn0-target)
varies receiver inputs and returns SNR margin despite the directory's C/No name.
Read `src/main.rs` and `Cargo.toml` when adapting it.

The example uses required QPSK Eb/No as an SNR target under a stated 1 bit/s/Hz
simplification and supplies a fallback when the BER helper returns no result.
Replace these demonstration choices with the task's explicit rate conversion
and error handling. Its sampled ranges are examples, not measured uncertainty.

## Focused proof

Check a nominal receiver or link against a known calculation. In the linear
model, an extra 1 dB propagation loss should reduce the corresponding link
margin by 1 dB. At fixed received power and temperature, doubling noise bandwidth
reduces SNR by approximately 3.0103 dB; at fixed information bit rate, converting
that SNR to Eb/No should cancel the bandwidth change. Test threshold equality
and any error returned for an unsupported requirement.
