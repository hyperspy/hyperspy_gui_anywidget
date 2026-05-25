<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-05-25 | Updated: 2026-05-25 -->

# .github

## Purpose
This directory contains GitHub automation and collaboration metadata: CI/release workflows, issue templates, and the pull-request template that encodes repository review expectations.

## Key Files

| File | Description |
|------|-------------|
| `dependabot.yml` | Weekly update policy for GitHub Actions and pip dependencies. |
| `pull_request_template.md` | PR checklist covering tests, manual UI verification, and news fragments. |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `workflows/` | GitHub Actions CI and release pipelines (see `workflows/AGENTS.md`). |
| `ISSUE_TEMPLATE/` | Standardized bug-report and feature-request forms (see `ISSUE_TEMPLATE/AGENTS.md`). |

## For AI Agents

### Working In This Directory
- Keep workflow changes aligned with the commands documented in `CONTRIBUTING.md` and `docs/development.md`.
- Preserve pinned GitHub Action SHAs unless intentionally updating them.
- When changing contributor expectations, update the related docs and templates together.

### Testing Requirements
- Re-read workflow YAML carefully after edits; misplaced steps or indentation mistakes are common regression sources.
- When CI commands change, re-run the equivalent local commands if feasible.

### Common Patterns
- CI is split into lint, build, test, coverage, and docs jobs.
- Repository hygiene expects a news-fragment check and explicit notebook/manual verification when UI behavior changes.

## Dependencies

### Internal
- Mirrors verification commands from `README.md`, `CONTRIBUTING.md`, and `docs/development.md`.
- Workflow jobs operate on the package, docs, and examples maintained elsewhere in the repo.

### External
- GitHub Actions ecosystem for CI/release automation.
- Dependabot for update automation.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
