# AGENTS.md

This repository contains Codex skills for RF engineering workflows.

## Before editing

- Check `git status --short --branch`.
- Read the target skill and its linked references before changing it.
- Keep skill names and frontmatter descriptions narrow enough for reliable
  routing.
- Preserve user-authored changes outside the task.

## Validation

Run the repository check after changing a skill, reference, asset, release file,
or validator:

```sh
./scripts/check.sh
```

The check validates every skill package, parses the release contract, compiles
the checked-in Python tools, runs the `rfschemdraw` unit tests, and checks Git
whitespace.

## Releases

Read [`docs/release.md`](docs/release.md) before release work.

- Use `create-release-process` to create, audit, or change the workflow.
- Use `release-runner` or `cut-release` for an ordinary release.
- Inspect with `uv run scripts/release.py check --json` and
  `uv run scripts/release.py plan --bump <level> --json`.
- Pass the plan's version, target commit, and configuration checksum to dry-run
  and apply. This prevents execution from using stale release intent.
- Apply only when the user explicitly asks to publish a release.

The release runner owns `VERSION`. A real release commits that file, creates and
pushes a `v`-prefixed tag, and creates the GitHub release as its final action.
Keep repository policy in `release.toml` and small helpers. Keep the shared
runner unchanged, and update `[runner_source]` when vendoring a new revision.
