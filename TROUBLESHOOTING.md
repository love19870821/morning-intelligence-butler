# Troubleshooting

## `Error: Input file not found: ...`

The input path does not exist.

Fix:

- check the path spelling
- use `pwd` to confirm your current directory
- create a sample first with `morning-butler --write-sample`

## `Error: Invalid JSON in input file ...`

The file exists, but the JSON is not valid.

Fix:

- open the file in a JSON-aware editor
- check for trailing commas or missing quotes
- validate the file with a JSON formatter before running the CLI

## `morning-butler: command not found`

The package is not installed in the current environment.

Fix:

- run `python -m pip install -e .` from the repository root
- or run the tool with `python src/main.py`

## `morning-butler-smoke` fails after install

The install is incomplete or the environment is inconsistent.

Fix:

- rerun `python -m pip install -e .`
- then run `morning-butler-release-check`
- confirm that the fresh virtual environment can install the wheel and pass the smoke test

## `Error: Unable to fetch ...`

The live market price fetch failed.

Fix:

- check that the machine has outbound network access
- retry after a short delay
- confirm that the upstream price sites are reachable
- for offline runs or deterministic smoke tests, set `MORNING_BUTLER_MARKET_FIXTURE` with `gold`, `oil`, and `usd_twd`

## Output file is missing

The CLI only writes a file when `--output` is set.

Fix:

- pass a file path to `--output`
- verify that the target directory is writable

## Need a known-good input file

Use the built-in sample generator:

```bash
morning-butler --write-sample
```

See also:

- [INPUT_SCHEMA.md](INPUT_SCHEMA.md)
- [RELEASE.md](RELEASE.md)
