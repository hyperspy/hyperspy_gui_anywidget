<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-05-25 | Updated: 2026-05-25 -->

# upcoming_changes

## Purpose
This directory holds Towncrier news fragments that are collected into `CHANGELOG.rst`. It is small, but it documents an important part of the repo’s release hygiene and contributor workflow.

## Key Files

| File | Description |
|------|-------------|
| `README.rst` | Fragment naming rules and supported fragment types (`new`, `enhancements`, `bugfix`, `api`, `deprecation`, `doc`, `maintenance`). |
| `0.maintenance.rst` | Current maintenance fragment describing the recent repo-hygiene, docs, CI, and regression-test improvements. |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| *(none)* | Fragments live directly in this directory. |

## For AI Agents

### Working In This Directory
- Add short user-focused fragments for user-visible or maintenance-relevant changes.
- Follow the `<issue-or-pr>.<type>.rst` naming rule exactly.
- Avoid editing old fragments unless the related change is being intentionally rewritten.

### Testing Requirements
- Preview combined release notes with `towncrier build --draft` when fragment wording or types change.
- Ensure fragment types stay in sync with `pyproject.toml` and contributor docs.

### Common Patterns
- Maintenance-only changes can still require fragments when they affect contributor workflow, CI, or release hygiene.
- The fragment taxonomy is intentionally small and documented both here and in `docs/development.md`.

## Dependencies

### Internal
- Feeds into `CHANGELOG.rst` via Towncrier configuration in `pyproject.toml`.
- Contributor workflow in `CONTRIBUTING.md` points here for fragment guidance.

### External
- Towncrier for changelog assembly.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
