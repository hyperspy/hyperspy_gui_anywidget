# Contributing

Thanks for improving `hyperspy_gui_anywidget`.

This repository follows the same general engineering habits as the main HyperSpy project, scaled to a smaller extension package: small reviewable pull requests, tests for behavior changes, lightweight documentation updates, and short changelog fragments for user-visible work.

## Getting started

```bash
git clone https://github.com/hyperspy/hyperspy_gui_anywidget.git
cd hyperspy_gui_anywidget
pip install -e ".[dev,tests,doc]"
pre-commit install
```

## Before opening a pull request

Run the local checks that match our CI:

```bash
pre-commit run --all-files
pytest --pyargs hyperspy_gui_anywidget
sphinx-build -W -b html docs docs/_build/html
```

If your change affects notebook behavior, please also do a quick manual check in Jupyter or Marimo and mention that in the pull request.

## Changelog fragments

User-facing and maintenance changes should include a short news fragment in `upcoming_changes/`.

Use the naming pattern:

```text
<issue-or-pr>.<type>.rst
```

Supported types are documented in `upcoming_changes/README.rst`.

## Tests and documentation

- Add or update tests whenever widget behavior, serialization, or trait linking changes.
- Prefer focused regression tests close to the affected module.
- Update `README.md` or `docs/` when the public workflow changes.

## Widget architecture note

This package keeps `ipywidgets` as an explicit dependency on purpose. The custom
controls are implemented with `anywidget`, but the Jupyter layout layer still
uses native `ipywidgets` containers such as `VBox`, `HBox`, `Tab`, and
`Accordion`. In Marimo, those structures are flattened into `FlatContainer`
configurations. If you change container behavior, check both the Jupyter path
and the Marimo flattening path.

## Broader HyperSpy conventions

For the wider project context, contributor expectations, and development culture, also see the HyperSpy developer guide:

- https://hyperspy.org/hyperspy-doc/current/dev_guide.html
