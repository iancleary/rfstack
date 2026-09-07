# rfstack

Codex skills for RF engineering workflows.

The repository uses a checked-in release process. See
[`docs/release.md`](docs/release.md) for version policy, validation, dry-run,
guarded planning, recovery, and publishing commands. The unchanged shared
runner is pinned by source commit and checksum in `release.toml`.

- `gainlineup`: Model ordered RF hardware chains and cascaded performance.
- `linkbudget`: Analyze end-to-end terrestrial and satellite radio links.
- `montycarlo`: Run domain-specific Monte Carlo simulations in Rust.
- `rf-monte-carlo`: Combine RF models with uncertainty sampling, yield, and margin analysis.
- `rfconversions`: Apply scalar RF conversions and noise calculations.
- `rfschemdraw`: Render reproducible RF signal-chain diagrams.
- `touchstone`: Parse, analyze, generate, and cascade S-parameter networks.
