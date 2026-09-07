# Hardware cascade margin

Use this reference when uncertain component or source parameters affect a gain
lineup. The deterministic evaluator owns one `Input` and an ordered `Vec<Block>`.

## Trial mapping

- Source sample: `Input::power_dbm`, `frequency_hz`, `bandwidth_hz`, and
  `noise_temperature_k`. Set temperature explicitly for reproducible assumptions.
- Stage sample: `Block::gain_db`, `noise_figure_db`, and optional
  `output_p1db_dbm` or `output_ip3_dbm`.
- Final output: `cascade_vector_return_output(input, blocks)`.
- Intermediate outputs: `cascade_vector_return_vector(input, blocks)`.
- SNR metric: the output node's `signal_to_noise_ratio_db()`.
- SNR margin: output SNR minus the required SNR in dB.

Use a named sample struct rather than positional tuples in a maintained model.
Keep fixed parameters in the simulation configuration. A randomized frequency
requires the stage characteristics to vary with frequency when the model claims
to capture that effect; changing the input label alone is insufficient.

## Coupling and model limits

For a passive loss at the reference temperature, derive negative gain and
positive noise figure from the same sampled loss. Do not independently randomize
them unless the physical model supports it. Share temperature or batch variation
across components when justified by the data.

P1dB and IP3 inputs are output-referred. The block compression approximation
clamps output at output P1dB plus 1 dB. Report this limitation if compressed trials
affect yield. Missing optional linearity specifications do not establish that
the hardware meets a linearity requirement.

If the requirement applies to every node, compute the minimum node margin within
one trial. Record the limiting node in a paired trace when attribution matters.
Do not infer chain yield from independently sampled per-node yields.

## Public starting point

[The upstream cascade SNR example](https://github.com/iancleary/gainlineup/tree/main/examples/montecarlo-gain-target)
implements `Simulation`, varies stage gain/NF and source power/temperature,
evaluates output SNR, and writes sorted margins and a summary.

Read its `src/main.rs` and `Cargo.toml` when adapting it. Its distributions and
target are demonstration assumptions. Its `1.0 - result.cdf(0.0)` statistic
means strictly positive margin. Select the requirement's equality rule explicitly.

## Focused proof

Check a fixed linear cascade's gain and Friis noise behavior. Show that a known
source power change produces the expected SNR change while the chain remains
linear. Include a threshold-equality case and a compression case when relevant.
Then verify that zero-width uncertainty represented by constant samples produces
the same deterministic result on every trial.
