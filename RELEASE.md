# Release checklist

Use this before publishing a new version.

## Pre-release checks

- [ ] README start path is correct: install -> verify -> demo -> real use
- [ ] CHANGELOG notes the release highlights
- [ ] LICENSE is present and correct
- [ ] `pyproject.toml` metadata matches the current release
- [ ] `python -m pytest tests -q` passes
- [ ] `python -m pip install -e .` passes
- [ ] `morning-butler-release-check` passes locally

## Artifact checks

- [ ] Wheel builds successfully
- [ ] Wheel installs in a fresh virtual environment
- [ ] Installed `morning-butler-smoke` passes in the fresh environment

## Publish checks

- [ ] Version number is updated in source of truth
- [ ] Git tag or release name matches the version
- [ ] Release notes summarize what changed for users
- [ ] No build artifacts are committed

## After publish

- [ ] Verify the release page is readable
- [ ] Confirm install instructions still match the packaged CLI
- [ ] Confirm the smoke test command still works from a fresh install
