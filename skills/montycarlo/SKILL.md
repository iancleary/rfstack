---
name: montycarlo
description: Use the public Rust montycarlo crate to run sequential or parallel domain simulations and compute mean, variance, percentiles, empirical CDF, and exceedance. Use when sampling belongs in the caller's model and scalar f64 statistics are sufficient.
---

# Monty Carlo

Use `montycarlo` as a small execution and statistics layer. Keep probability
distributions and domain constraints in the caller's `Simulation`
implementation. Add the crate with `cargo add montycarlo`.

## Model contract

Implement `Simulation` with:

- `Sample`: all random inputs for one trial
- `Output`: a copyable value convertible to `f64`
- `sample`: draw inputs from the supplied RNG
- `evaluate`: deterministically map one sample to one output

Create `MonteCarloEngine::new(simulation, num_trials)`. Use `with_seed` for a
repeatable run, `run` for sequential execution, and `run_parallel` when the
default `parallel` feature is enabled and throughput matters.

## Preserve statistical meaning

- Put correlated draws in one `Sample`; do not sample related variables in
  separate runs.
- Keep units consistent across every output because results are reduced to one
  `f64` series.
- Use a nonzero trial count. Empty results produce `NaN` statistics.
- `variance` and `std_dev` are population statistics.
- `percentile` accepts 0 through 100 and uses linear interpolation between
  ranks. Values outside that range panic.
- `cdf(x)` is the fraction at or below `x`; `exceedance(x)` is the fraction
  strictly above it.
- Seeded sequential runs provide the simplest reproducibility contract.
  Parallel results can depend on execution partitioning, so record the seed,
  crate version, feature set, and runtime environment when exact replay matters.
- Reject or handle non-finite outputs in the domain model before interpreting
  percentiles or sorted values.

## Verification

First test `evaluate` with fixed samples. Then run a seeded small simulation and
assert trial count plus broad statistical bounds. Avoid brittle assertions on
exact Monte Carlo aggregates unless exact sequence reproduction is the behavior
under test. Increase trials only after the model and thresholds are correct.

Use `default-features = false` for a sequential-only dependency. For current
signatures, use the installed source or <https://docs.rs/montycarlo>. The
upstream source is <https://github.com/iancleary/montycarlo>.
