---
name: rf-monte-carlo
description: Build and interpret RF Monte Carlo tolerance, yield, and margin analyses with the public gainlineup, linkbudget, touchstone, rfconversions, and montycarlo Rust crates. Use when RF inputs have specified uncertainty or distributions and the result needs probabilities or percentiles.
---

# RF Monte Carlo

Build a deterministic RF model first, then wrap its uncertain inputs in a
`montycarlo::Simulation`. Keep the sampling assumptions, RF metric, and decision
threshold visible beside the result.

## Select the domain model

- For hardware cascades, read [references/gainlineup.md](references/gainlineup.md).
- For receiver or full-link margin, read [references/linkbudget.md](references/linkbudget.md).
- For measured networks, use `touchstone` to parse and align the data. Sample
  complete measured realizations when available. Independent perturbations of
  matrix entries can violate passivity, reciprocity, or frequency correlation;
  use them only with a justified uncertainty model and the relevant checks.
- Use `rfconversions` for unit and noise conversions within the evaluator.
- Use the `montycarlo` skill for execution and result API details. If it is not
  installed, consult the resolved crate source or <https://docs.rs/montycarlo>.

Read only the domain reference needed for the task. Crate-specific skills retain
their API and RF conventions; this skill owns the shared analysis method.

## Define the experiment

Establish the metric, its units, the reference plane, and an explicit pass rule.
For a minimum required SNR, use `margin_db = actual_snr_db - required_snr_db`.
For a maximum allowed level, reverse the subtraction so positive margin still
means better performance. State whether zero margin passes.

List each uncertain parameter with its units, distribution, parameters, bounds,
source, and dependencies. Separate manufacturing variation, operating scenarios,
and measurement uncertainty. Their mixture needs explicit weights if it is to
represent one population. A datasheet min/max interval alone does not establish
a uniform distribution. Label assumed distributions as assumptions; ask for
missing consequential inputs, or present conditional scenarios with stated
assumptions when useful.

Sample shared causes once per trial. For example, one temperature realization
can affect several stage gains and noise figures. Putting independent draws in
one struct does not make them correlated. Derive dependent parameters from the
shared sample, or use a supported joint distribution.

Distinguish the distribution domain from the reporting unit. A normal draw in
dB is not a normal draw in watts. Specify physical bounds before sampling.
Truncation, rejection, and clipping produce different distributions; choose and
document the intended behavior. Use bounded retries if rejection sampling is
needed. Do not silently discard failed evaluations or replace them with zero.

## Implement one trial

Use a named `Sample` struct with unit-suffixed fields. Draw all randomness in
`sample` from the supplied RNG. Make `evaluate` deterministic and return one
finite scalar metric. Construct the domain model from the sample and call its
public APIs. Preserve stage order, port orientation, and reference planes.

`MonteCarloResult` retains sorted scalar outputs, not the inputs or trial order.
If sensitivity analysis, several metrics, or failure diagnosis requires paired
data, retain trial IDs, inputs, and outputs in a separate caller-owned trace.
Do not pair independently sorted result vectors. Avoid mutable logging inside a
parallel evaluator; collect traces through an explicit workflow when needed.
For joint yield, evaluate all requirements on the same sample and record their
combined pass event rather than multiplying marginal yields.

Start with seeded sequential execution. Record the seed, trial count, resolved
crate versions, feature set, execution mode, and model configuration. Keep the
consumer's dependency versions unless the task requires an update. Verify
examples against those resolved versions before adopting APIs from upstream.

## Verify and size the run

1. Test fixed samples at nominal conditions and decisive boundaries. Compare
   with a hand-checkable RF result before adding randomness.
2. Run a small seeded pilot. Check units, bounds, finite outputs, and expected
   direction of change when one parameter changes.
3. Choose the trial budget from the decision's required precision. Compare
   increasing sample counts and independent seeds for the decisive probability
   or percentile; a stable mean alone does not establish tail convergence.
4. Report uncertainty on estimated yield or failure probability with a stated
   binomial interval method and confidence level for independent trials. Use
   appropriate resampling or independent-run evidence for percentile uncertainty.
   Correlated trials need an uncertainty method that accounts for dependence.

Zero observed failures does not prove zero failure probability. State the trial
count and an upper confidence bound. Finite Monte Carlo results do not establish
worst-case bounds. If a rare event is too poorly sampled for the decision,
report that limitation rather than asserting that the target is demonstrated.

## Summarize the result

`cdf(0.0)` counts margins at or below zero; `exceedance(0.0)` and
`1.0 - cdf(0.0)` count margins strictly above zero. For an inclusive pass rule
`margin >= 0`, count values satisfying that predicate in `sorted_values()`.
Equality matters for deterministic and discrete samples.

Deliver the model source and rerun command, assumptions, seed and trial count,
nominal result, selected percentiles, pass/failure counts and probability,
uncertainty estimate, and any invalid or excluded trials. Explain whether
exclusions change the population being reported. A histogram or empirical CDF
with the threshold marked is useful when the distribution affects the decision.
Name exported sorted data as sorted; it cannot support input-output correlation.

All probabilities are conditional on the stated model and sampling assumptions.
Retain that qualification in the report, especially when inputs lack measured
distributions.
