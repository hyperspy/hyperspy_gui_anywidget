# hyperspy_gui_anywidget

`hyperspy_gui_anywidget` provides anywidget-based GUI components for HyperSpy and
aims to follow the same practical engineering habits as the main HyperSpy
project while staying lightweight enough for a focused extension package.

```{toctree}
:maxdepth: 2
:caption: Contents

user-guide
development
api
```

## What lives here

- notebook widgets for HyperSpy tools, models, ROI builders, and preferences
- shared anywidget primitives in `hyperspy_gui_anywidget/custom_widgets.py`
- tests that verify bidirectional trait sync, widget layout behavior, and parity
  with the sibling ipywidgets implementation

## Project resources

- [README on GitHub](https://github.com/hyperspy/hyperspy_gui_anywidget/blob/main/README.md)
- [Contributing guide](https://github.com/hyperspy/hyperspy_gui_anywidget/blob/main/CONTRIBUTING.md)
- [Issue tracker](https://github.com/hyperspy/hyperspy_gui_anywidget/issues)

## Development checks

```{code-block} bash
pre-commit run --all-files
pytest --pyargs hyperspy_gui_anywidget
sphinx-build -W -b html docs docs/_build/html
```
