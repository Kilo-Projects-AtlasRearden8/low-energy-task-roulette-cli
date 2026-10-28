# task-roulette

Pick one small task for low-energy or ADHD days from a local JSON list, with
tracking and export. No accounts, no keys, no network. Local-first, tested,
beginner-friendly.

Built by **Dylan Asdale** — registered nurse turned AI author and founder of
**Asdale Dynamics, LLC** (Indiana, formed October 2026). Dylan writes *The
Massive AI Manual* and runs the hub site dylanasdale.github.io, explaining AI
"like a friend would": plain English, step by step, never condescending.
Asdale Dynamics, LLC focuses on beginner-friendly AI education, practical
open-source tools, and accessible life-admin helpers such as this low-energy
productivity tool.

## Who this is for

Days when even choosing what to do feels like too much. Low energy. ADHD
brain fog. You know there are small things that would help, but deciding
which one is its own exhaustion.

`task-roulette` chooses for you: one small task, drawn at random from a local
JSON list you control, filtered to match how much energy you have today. It
also tracks what you finish and can export your history.

Nothing here is medical advice. If you're unwell, reach out to a clinician.

## Install

```bash
git clone <this-repo>
cd low-energy-task-roulette-cli
pip install -e .
```

Or run straight from the folder:

```bash
python -m task_roulette pick
```

## Quick start

```bash
# Create your data folder with a sample task list
task-roulette init

# Pick one low-energy task (the default)
task-roulette pick

# Pick with more energy to spend today
task-roulette pick --energy medium

# Reproducible pick (same seed, same choice — handy for testing)
task-roulette pick --seed 7

# Pick a task and mark it done in one step
task-roulette pick --mark-done

# Mark a task done by id
task-roulette done water-plant

# See your completion history
task-roulette history

# Export history to JSON or CSV
task-roulette export history.json
task-roulette export history.csv

# List all known tasks
task-roulette list
```

## Tasks file

Tasks live in `tasks.json` inside your data directory
(`~/.local/share/task-roulette` on Linux). Each task:

```json
{
  "id": "drink-water",
  "title": "Drink a glass of water",
  "description": "A small glass counts.",
  "category": "body",
  "energy": "low",
  "estimated_minutes": 2,
  "tags": ["hydration"]
}
```

`energy` is `low`, `medium`, or `high`. On a `--energy low` day only `low`
tasks are offered; `--energy medium` adds medium tasks; `--energy high`
offers everything. Tasks you mark done today are skipped on subsequent picks
when you use `--exclude-done`.

The default sample list includes gentle tasks like drinking water, opening the
curtains, taking five deep breaths, and stretching — small, low-stakes wins
for low-energy days.

## Testing

```bash
pytest
```

All tests cover the selection logic: energy filtering, exclusion of already-done
tasks, and deterministic picks with a seed.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

## Credit

Created by Dylan Asdale for Asdale Dynamics, LLC — beginner-friendly AI
education, books and guides, and practical open-source tools. Learn more at
dylanasdale.github.io. This is an accessibility/productivity tool, not medical
advice.
