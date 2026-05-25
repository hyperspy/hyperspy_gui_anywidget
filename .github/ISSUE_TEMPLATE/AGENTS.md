<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-05-25 | Updated: 2026-05-25 -->

# ISSUE_TEMPLATE

## Purpose
This directory contains the issue forms that guide bug reports and feature requests into a consistent structure suitable for a small extension project.

## Key Files

| File | Description |
|------|-------------|
| `bug_report.md` | Bug-report template requesting reproduction steps, expected behavior, and environment details. |
| `feature_request.md` | Feature-request template asking for the problem statement, desired solution, and alternatives considered. |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| *(none)* | This directory only contains the current issue templates. |

## For AI Agents

### Working In This Directory
- Keep templates lightweight and focused on actionable maintenance information.
- Preserve environment/version prompts in bug reports because widget issues are often frontend- and version-sensitive.

### Testing Requirements
- No code execution is needed, but re-read rendered Markdown/YAML front matter carefully after edits.

### Common Patterns
- Templates use GitHub front matter to set the name, labels, and short description.
- Bug reports ask for OS, Python, HyperSpy, and package version details.

## Dependencies

### Internal
- Complements the PR template and repository maintenance workflow in `.github/`.

### External
- GitHub issue forms/Markdown template rendering.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
