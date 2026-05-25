<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-05-25 | Updated: 2026-05-25 -->

# workflows

## Purpose
This directory contains the GitHub Actions workflows that enforce linting, testing, coverage, docs building, and release publishing for the extension.

## Key Files

| File | Description |
|------|-------------|
| `ci.yml` | Main continuous-integration workflow running Ruff, import/build checks, the cross-platform pytest matrix, coverage upload, and Sphinx docs builds. |
| `release.yml` | Trusted-publishing workflow that builds the package and publishes tagged releases to PyPI. |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| *(none)* | This directory contains only top-level workflow files. |

## For AI Agents

### Working In This Directory
- Keep action SHAs pinned and note the corresponding action version in comments.
- Match local contributor commands when editing workflow steps (`ruff`, `pytest`, coverage, docs build).
- Be cautious with multiline shell snippets; YAML indentation errors can silently break jobs.

### Testing Requirements
- After edits, re-read the whole workflow file to confirm steps remain under the intended job.
- Re-run the corresponding local command(s) when practical, especially for lint/docs/test changes.

### Common Patterns
- CI installs extras via `-e ".[dev]"`, `-e ".[tests]"`, or `-e ".[doc]"` instead of ad hoc dependency lists.
- Coverage enforces `--cov-fail-under=75`.
- Build verification includes checking importability and asserting the `hyperspy_extension.yaml` anywidget entry count.

## Dependencies

### Internal
- Reads commands and metadata from `pyproject.toml`.
- Verifies the package modules and `hyperspy_extension.yaml` maintained under `hyperspy_gui_anywidget/`.

### External
- GitHub Actions: checkout, setup-python, cache, upload-artifact, codecov, and PyPI publish actions.
- Codecov for coverage uploads.
- PyPI trusted publishing for release deployment.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
