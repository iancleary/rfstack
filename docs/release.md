# Release Process

This repository uses Semantic Versioning with `v`-prefixed Git tags. A release
publishes the repository's skill collection as one versioned unit.

## Version policy

[`VERSION`](../VERSION) is the version source. It contains the latest released
version without the `v` prefix.

- Patch releases correct compatible skill guidance, assets, tests, or docs.
- Minor releases add skills, compatible workflow guidance, or other features.
- Major releases make incompatible skill-routing, artifact, or command changes.

The initial `0.0.0` value is an unreleased baseline. Use `--bump minor` for the
first `v0.1.0` release.

## Commands

Use the checked-in [`release.toml`](../release.toml) contract through the local
runner:

```sh
uv run scripts/release.py check --json
uv run scripts/release.py plan --json
uv run scripts/release.py run --dry-run --bump patch --json
uv run scripts/release.py run --apply --bump patch --json
```

Replace `patch` with `minor` or `major` when the change requires it. Use
`--version <version>` for an exact version or prerelease. Do not pass `--bump`
and `--version` together.

The root runner is self-contained and does not load release code from an
installed skill or another checkout.

## Release contract

The runner:

1. Requires a clean worktree.
2. Confirms that the target tag does not exist locally or on `origin`.
3. Writes the target version to `VERSION`.
4. Runs `./scripts/check.sh` against the versioned tree.
5. Restores `VERSION` after a dry-run.
6. During apply, commits `VERSION`, creates an annotated tag, pushes the commit
   and tag, and creates the GitHub release.

GitHub generates release notes by default. Pass `--notes-file <path>` for
curated notes.

Run apply from a clean `main` branch with a configured `origin` and valid GitHub
CLI authentication. Apply is the public release action.

## Agent routing

Use `create-release-process` to maintain this workflow. Use `release-runner` or
`cut-release` for an ordinary release. The checked-in files and this document
define the repository contract.
