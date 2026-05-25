# Development and maintenance

This repository follows a smaller-scale version of the engineering workflow used
in the main HyperSpy project.

## Local checks

Run the same checks locally that CI runs in GitHub Actions:

```{code-block} bash
pre-commit run --all-files
pytest --pyargs hyperspy_gui_anywidget
sphinx-build -W -b html docs docs/_build/html
```

If a change affects notebook behavior, do a quick manual verification in Jupyter
or Marimo as part of the same change.

## AI agent setup

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

## Completion checklist

Before claiming any task is complete, verify ALL of the following:

### Code Quality
- [ ] ``ruff check`` passes on all changed files — zero new errors
- [ ] ``ruff format`` applied — no formatting inconsistencies

### Testing
- [ ] Affected tests pass: ``pytest hyperspy_gui_anywidget/tests/<affected>/``
- [ ] New code has corresponding tests that mirror the source structure
  (e.g., changes in ``utils.py`` need additions in ``test_utils.py``)
- [ ] Full suite still passes: ``pytest --pyargs hyperspy_gui_anywidget``
- [ ] Coverage threshold (75 %) still met: ``pytest --pyargs hyperspy_gui_anywidget --cov=hyperspy_gui_anywidget --cov-fail-under=75``

### Changelog
- [ ] Every user-facing change has an ``upcoming_changes/<issue>.<type>.rst`` entry
- [ ] The ``<type>`` matches one of: ``new``, ``bugfix``, ``api``,
  ``deprecation``, ``doc``, ``enhancements``, ``maintenance``

### Documentation
- [ ] Non-obvious design choices are annotated with inline comments
  explaining intent
- [ ] Docs still build cleanly: ``sphinx-build -W -b html docs docs/_build/html``
- [ ] If notebook behavior changed, examples and user-guide docs are updated
- [ ] For structural changes (file moves, renames, splits, new modules),
  provide a change map: what changed, what moved where, and why

### Commits
- [ ] Commit follows best practices (atomic units, repo-consistent messages,
  no secrets)
- [ ] MUST NOT use ``Co-authored-by:`` trailer — use
  ``Assisted-by: <tool>:<model>`` instead
- [ ] Never push unless explicitly asked

### Repository Hygiene
- [ ] Never modify AGENTS.md generated sections — only add notes below
  ``<!-- MANUAL -->`` lines
- [ ] Never suppress type/lint errors with blanket ignores
  (``# type: ignore``, ``# noqa`` without justification)
- [ ] ``hyperspy_extension.yaml`` entry count must remain 33; any addition
  or removal must be justified and accounted for in tests and CI

## News fragments

User-facing and maintenance changes should add a short file under
`upcoming_changes/`.

Supported fragment types include:

- `new`
- `enhancements`
- `bugfix`
- `api`
- `deprecation`
- `doc`
- `maintenance`

Preview the rendered changelog with:

```{code-block} bash
towncrier build --draft
```

## Documentation scope

The documentation deliberately stays lightweight for this extension package, but
it should cover three areas:

1. user-facing installation and notebook usage
2. contributor workflow and release hygiene
3. API reference for the main public modules used to build and test widgets

## Design decision: keep `ipywidgets`

`anywidget` is used here for the custom widget implementations, but the package
still keeps `ipywidgets` as an explicit dependency because the Jupyter path uses
native `ipywidgets` containers (`VBox`, `HBox`, `Tab`, `Accordion`). The Marimo
path then flattens those layouts into `FlatContainer` configs.

That split is intentional:

- Jupyter gets native widget-container behavior and titles.
- Marimo gets the same logical layout through a flattened anywidget container.

If a future refactor tries to remove `ipywidgets`, it would need to replace both
the Jupyter container implementation and the flattening logic that currently
recognizes those container classes.
