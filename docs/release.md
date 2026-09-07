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
uv run scripts/release.py plan --bump patch --json
```

Replace `patch` with `minor` or `major` when the change requires it. Use
`--version <version>` for an exact version or prerelease. Do not pass `--bump`
and `--version` together.

The plan returns the selected version, target commit, and configuration
checksum. Pass those values to dry-run and apply so execution rejects a stale
plan:

```sh
uv run scripts/release.py run --dry-run \
  --version <version> \
  --expected-head <target-commit> \
  --expected-config <config-sha256> \
  --json
uv run scripts/release.py run --apply \
  --version <version> \
  --expected-head <target-commit> \
  --expected-config <config-sha256> \
  --json
```

The root runner is self-contained and does not load release code from an
installed skill or another checkout.

## Release contract

The runner:

1. Requires a clean worktree.
2. Confirms that the target tag does not exist locally or on `origin`.
3. Writes the target version to `VERSION`.
4. Runs the checks declared in `release.toml` against the versioned tree.
5. Restores `VERSION` after a dry-run.
6. During apply, commits `VERSION`, creates an annotated tag, pushes the commit
   and tag, and creates the GitHub release.

GitHub generates release notes by default. Pass `--notes-file <path>` for
curated notes.

If the tag push succeeds but GitHub release creation fails, inspect the tag and
its commit. From a clean checkout of that commit, preview and apply recovery:

```sh
uv run scripts/release.py run --dry-run --resume \
  --version <version> --expected-head <tag-commit> --json
uv run scripts/release.py run --apply --resume \
  --version <version> --expected-head <tag-commit> --json
```

Resume never changes version files, commits, or tags. It reruns checks and
completes only a missing GitHub release.

Run apply from a clean `main` branch with a configured `origin` and valid GitHub
CLI authentication. Apply is the public release action.

## Agent routing

Use `create-release-process` to maintain this workflow. Use `release-runner` or
`cut-release` for an ordinary release. The checked-in files and this document
define the repository contract.

The vendored runner stays unchanged from the source revision and checksum in
`release.toml`. Put repository policy in TOML or small helper scripts. Update
the provenance fields whenever the shared runner changes.
