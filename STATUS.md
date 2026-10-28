# STATUS.md

## What was built

**task-roulette** — a small, local-first Python CLI for low-energy or ADHD
days. It picks one small task at random from a local JSON list you control,
filtered by your energy level (low / medium / high). It tracks completions and
exports history to JSON or CSV. No accounts, no API keys, no network access.

### Project layout

```
pyproject.toml          # packaging + console script entry point
LICENSE                 # MIT, Copyright (c) 2026 Asdale Dynamics, LLC
README.md               # usage + credit to Asdale Dynamics, LLC
tasks.json              # sample task list (12 gentle low/medium tasks)
src/task_roulette/
  __init__.py           # package marker + version
  __main__.py           # python -m task_roulette entry point
  cli.py                # argparse CLI: pick, list, done, history, export, init
  tasks.py              # Task model, loading, energy-filtered selection
  tracking.py           # completion history store + JSON/CSV export
  defaults.py           # default data dir + built-in sample tasks
tests/test_selection.py # selection-logic tests
.gitignore
```

## How to run it

```bash
# Install
pip install -e .

# Or run from the folder without installing
python -m task_roulette pick

# Initialize data folder with sample tasks
task-roulette init

# Pick one low-energy task
task-roulette pick

# Pick with more energy
task-roulette pick --energy medium

# Reproducible pick
task-roulette pick --seed 7

# Pick and mark done
task-roulette pick --mark-done

# Mark a task done by id
task-roulette done water-plant

# View history
task-roulette history

# Export history
task-roulette export history.json
task-roulette export history.csv

# List tasks
task-roulette list
```

Data lives by default in `~/.local/share/task-roulette` (Linux). Use
`--data-dir` to point elsewhere.

## Verification results

- `pytest`: **6 passed** — selection logic tests cover empty list, low-energy
  filtering, medium/high energy inclusion, id exclusion, and deterministic
  seeded picks.
- `pip install -e .`: succeeds; console script `task-roulette` installed.
- `task-roulette init / pick / list / done / history / export (json + csv)`:
  all exercised end-to-end with a temp data directory; output correct.
- `python -m task_roulette pick`: works via `__main__.py`.
- LICENSE contains exactly `Copyright (c) 2026 Asdale Dynamics, LLC`.
- README credits Asdale Dynamics, LLC (4 mentions).
- No `.github/workflows`, no secrets, no API keys, no personal data.

## Known gaps

- No test coverage yet for the CLI layer or tracking/export (only selection
  logic is tested, as originally requested).
- `done_today_ids` uses UTC date; local-timezone users may see "today"
  boundaries shifted.
- No configuration file beyond `--data-dir` and `tasks.json`.
- No "undo" for marking a task done.
- Not packaged/published to PyPI (by design — local-first, no publish).
- Single-file `tasks.json` has no schema validation beyond field defaults.
