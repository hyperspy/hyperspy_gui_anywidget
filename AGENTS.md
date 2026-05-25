<!-- Generated: 2026-05-25 | Updated: 2026-05-25 -->

# hyperspy_gui_anywidget

## Purpose
This repository provides the `anywidget`-backed HyperSpy GUI extension. It bridges HyperSpy trait-based models to notebook UIs, supports Jupyter Notebook / JupyterLab and Marimo, and keeps the package lightweight while following the same practical engineering habits as the main HyperSpy project.

## Key Files

| File | Description |
|------|-------------|
| `pyproject.toml` | Packaging metadata, runtime dependencies, pytest/coverage/Ruff/Towncrier configuration, and the HyperSpy extension entry point. |
| `README.md` | Main user-facing overview covering installation, supported environments, architecture, and example links. |
| `CONTRIBUTING.md` | Contributor workflow, local verification commands, and widget-architecture notes. |
| `readthedocs.yaml` | Read the Docs build configuration for the Sphinx site. |
| `CHANGELOG.rst` | Towncrier-managed changelog target. |
| `CODE_OF_CONDUCT.md` | Community conduct expectations for the project. |
| `.pre-commit-config.yaml` | Local hook configuration for YAML checks and Ruff. |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `hyperspy_gui_anywidget/` | Core extension package, widget implementations, registry, and tests (see `hyperspy_gui_anywidget/AGENTS.md`). |
| `docs/` | Lightweight Sphinx documentation for usage, development, and API reference (see `docs/AGENTS.md`). |
| `examples/` | User-facing Jupyter and Marimo examples for the supported workflows (see `examples/AGENTS.md`). |
| `.github/` | CI workflows, issue templates, and PR metadata (see `.github/AGENTS.md`). |
| `upcoming_changes/` | Towncrier news fragments and fragment-type guidance (see `upcoming_changes/AGENTS.md`). |

## For AI Agents

### Working In This Directory
- Treat this repository as a small HyperSpy extension, not a standalone app framework.
- Keep user-facing behavior aligned with the documented Jupyter/Marimo support model.
- Update `README.md`, `docs/`, and news fragments when public workflows or contributor expectations change.
- Ignore cache/state directories such as `.git/`, `.omc/`, `.sisyphus/`, `.pytest_cache/`, `.ruff_cache/`, `docs/_build/`, and `__pycache__/`.

### Testing Requirements
- Main local checks are `pre-commit run --all-files`, `pytest --pyargs hyperspy_gui_anywidget`, and `sphinx-build -W -b html docs docs/_build/html`.
- For narrower widget changes, run focused regression tests in `hyperspy_gui_anywidget/tests/` before full verification.
- If notebook behavior changes, manually sanity-check Jupyter or Marimo behavior in addition to automated tests.

### Common Patterns
- Public GUI builders expose a `{"widget", "wdict"}` structure when `display=False` is used.
- HyperSpy traits and traitlets are synchronized via `link_traits.link()`.
- `anywidget` supplies custom leaf widgets while `ipywidgets` supplies the Jupyter-native container layer.
- Marimo compatibility comes from flattening Jupyter container structures into `FlatContainer` configs.

### AI Agent Setup

> **Authoritative source:** `docs/development.md` — this section mirrors the
> setup documented there and will be regenerated from it during deepinit.

Before implementing any changes, verify that the development environment is
correctly configured.  Do **not** start editing files until these pass:

- ``python -c "import hyperspy_gui_anywidget"`` — confirms the package is
  installed in editable mode.  If this fails, use
  ``pip install -e ".[dev,tests,doc]"`` to set up the local environment.

- ``pre-commit install`` — activates lint and format hooks on every commit.
  If ``pre-commit`` is not installed, install it via
  ``pip install pre-commit``.

- ``pre-commit run --all-files`` — should pass cleanly.  Fix any reported
  issues before proceeding.

- **Disable ``Co-authored-by:`` injection.**  Many AI coding tools add a
  ``Co-authored-by:`` trailer to commits by default.  HyperSpy and its
  extensions expect ``Assisted-by: <tool>:<model>`` instead (added manually
  to each commit).

  For common tools:
  * **Claude Code**: set ``"includeCoAuthoredBy": false`` in settings
  * **Cursor**: disable commit-message AI attribution in Cursor Settings
  * **GitHub Copilot**: disable ``github.copilot.chat.commitMessageGeneration``

Add setup checks to the first todo item of every session — do not skip them.

### Agent Completion Checklist

> **Authoritative source:** `docs/development.md` — this section mirrors the
> checklist documented there and will be regenerated from it during deepinit.

Before claiming any task is complete, verify ALL of the following:

#### Code Quality
- [ ] ``ruff check`` passes on all changed files — zero new errors
- [ ] ``ruff format`` applied — no formatting inconsistencies

#### Testing
- [ ] Affected tests pass: ``pytest hyperspy_gui_anywidget/tests/<affected>/``
- [ ] New code has corresponding tests that mirror the source structure
  (e.g., changes in ``utils.py`` need additions in ``test_utils.py``)
- [ ] Full suite still passes: ``pytest --pyargs hyperspy_gui_anywidget``
- [ ] Coverage threshold (75 %) still met: ``pytest --pyargs hyperspy_gui_anywidget --cov=hyperspy_gui_anywidget --cov-fail-under=75``

#### Changelog
- [ ] Every user-facing change has an ``upcoming_changes/<issue>.<type>.rst`` entry
- [ ] The ``<type>`` matches one of: ``new``, ``bugfix``, ``api``,
  ``deprecation``, ``doc``, ``enhancements``, ``maintenance``

#### Documentation
- [ ] Non-obvious design choices are annotated with inline comments
  explaining intent
- [ ] Docs still build cleanly: ``sphinx-build -W -b html docs docs/_build/html``
- [ ] If notebook behavior changed, examples and user-guide docs are updated
- [ ] For structural changes (file moves, renames, splits, new modules),
  provide a change map: what changed, what moved where, and why

#### Commits
- [ ] Commit follows best practices (atomic units, repo-consistent messages,
  no secrets)
- [ ] MUST NOT use ``Co-authored-by:`` trailer — use
  ``Assisted-by: <tool>:<model>`` instead
- [ ] Never push unless explicitly asked

#### Repository Hygiene
- [ ] Never modify AGENTS.md generated sections — only add notes below
  ``<!-- MANUAL -->`` lines
- [ ] Never suppress type/lint errors with blanket ignores
  (``# type: ignore``, ``# noqa`` without justification)
- [ ] ``hyperspy_extension.yaml`` entry count must remain 33; any addition
  or removal must be justified and accounted for in tests and CI

## Dependencies

### Internal
- `hyperspy_gui_anywidget/` contains the runtime implementation registered through `hyperspy_extension.yaml`.
- `docs/` and `README.md` document the supported user workflows.
- `.github/workflows/` enforces the repository checks described in contributor docs.

### External
- HyperSpy — host framework and extension entry point target.
- anywidget — custom widget base class and browser bridge.
- ipywidgets — Jupyter container/layout primitives used on the notebook path.
- link_traits / traitlets — synchronization between HyperSpy traits and widget state.
- Sphinx, MyST, and pydata-sphinx-theme — documentation build stack.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
