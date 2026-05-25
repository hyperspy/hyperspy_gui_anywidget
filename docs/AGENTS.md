<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-05-25 | Updated: 2026-05-25 -->

# docs

## Purpose
This directory contains the lightweight Sphinx documentation for the extension. It documents installation and supported environments, contributor workflow, key design decisions, and API reference for the modules that make up the anywidget integration.

## Key Files

| File | Description |
|------|-------------|
| `index.md` | Docs landing page and toctree for the user guide, development guide, and API reference. |
| `user-guide.md` | User-facing installation, Jupyter/Marimo usage, supported environments, and runtime model. |
| `development.md` | Maintenance workflow, local checks, news-fragment policy, and architecture notes such as why `ipywidgets` remains a dependency. |
| `api.rst` | Autodoc entry point for the main public modules in the package. |
| `conf.py` | Sphinx configuration, enabled extensions, and theme selection. |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `_build/` | Generated Sphinx output; ignore for edits and AGENTS coverage. |

## For AI Agents

### Working In This Directory
- Keep docs aligned with the real runtime behavior in `README.md` and the package modules.
- Do not reintroduce outdated guidance such as manual anywidget extension loading in modern Jupyter.
- Prefer concise docs updates that preserve the repo’s lightweight-docs goal.

### Testing Requirements
- Always run `sphinx-build -W -b html docs docs/_build/html` after editing docs.
- If documentation describes changed widget behavior, also ensure the underlying tests still pass.

### Common Patterns
- User docs emphasize default `display=True` behavior and treat `display=False` as the opt-in embedding/testing path.
- The docs distinguish explicit support (Jupyter Notebook/JupyterLab, Marimo) from unverified widget-capable frontends.
- API reference uses Sphinx autodoc against `hyperspy_gui_anywidget.*` modules.

## Dependencies

### Internal
- Mirrors public behavior from `README.md` and the package modules.
- Contributor workflow references `CONTRIBUTING.md` and CI checks from `.github/workflows/ci.yml`.

### External
- Sphinx, MyST parser, and pydata-sphinx-theme power the docs build.
- HyperSpy imports during autodoc may emit runtime warnings; the build still needs to pass with `-W`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
