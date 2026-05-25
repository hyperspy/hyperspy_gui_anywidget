# hyperspy_gui_anywidget

anywidget GUI elements for the HyperSpy framework.

This package provides GUI widgets using [anywidget](https://anywidget.dev/) for the [HyperSpy](https://hyperspy.org/) scientific data analysis library. It is explicitly supported in Jupyter Notebook / JupyterLab and in [Marimo](https://marimo.io/) without any frontend build step or bundler.

## Installation

### With pip

```bash
pip install hyperspy_gui_anywidget
```

### With optional test dependencies

```bash
pip install "hyperspy_gui_anywidget[tests]"
```

### Development install

```bash
git clone https://github.com/hyperspy/hyperspy_gui_anywidget.git
cd hyperspy_gui_anywidget
pip install -e ".[dev,tests,doc]"
```

## Usage

### Jupyter Notebook / JupyterLab

For modern Jupyter environments, installing `hyperspy_gui_anywidget` is enough. You do not
need to manually enable an anywidget extension in current JupyterLab or Notebook releases,
because `anywidget`/`ipywidgets` handle the widget integration.

In normal use, the default `display=True` behavior is what you want: calling a GUI method
displays the widget inline immediately.

HyperSpy can then use the anywidget toolkit directly:

```python
import hyperspy.api as hs

# Open preferences GUI
hs.preferences.gui(toolkit="anywidget")
```

Widgets are displayed inline using `IPython.display.display()`:

```python
roi = hs.roi.SpanROI(left=0, right=10)
roi.gui(toolkit="anywidget")
```

### Marimo

Marimo follows the same default behavior: with `display=True` (the default), the widget is
displayed inline for you.

If you need the raw widget object for manual embedding with `mo.ui.anywidget()`, pass
`display=False` and use the returned dictionary instead:

```python
import marimo as mo
import hyperspy.api as hs

roi = hs.roi.SpanROI(left=0, right=10)
res = roi.gui(toolkit="anywidget", display=False)
widget = res["anywidget"]["widget"]
mo.ui.anywidget(widget)
```

The `add_display_arg` decorator detects Marimo at runtime (via `sys.modules`) and, when
needed, flattens `VBox`/`HBox` containers before displaying them. Use `display=False` only
when you need the raw `{"widget": ..., "wdict": ...}` dictionary for embedding,
inspection, or tests.

### Supported environments

This project is explicitly tested and documented for:

- Jupyter Notebook / JupyterLab
- Marimo

Because the leaf widgets are implemented with `anywidget`, they may also work in other
frontends that support Jupyter widgets / anywidget. However, this repository does not
explicitly test or guarantee behavior in environments such as VS Code notebooks, Google
Colab, JupyterLite, or Voila.

## Architecture

This package is built on a few key design decisions:

1. **AnyWidget subclasses with inline `_esm` JavaScript** — Every widget is a Python class extending `anywidget.AnyWidget` with an inline JavaScript string. There is no npm, webpack, or build step. The JS renders standard HTML elements (`<input>`, `<select>`, `<button>`) and syncs state via traitlets.

2. **`link_traits` for bidirectional sync** — Enthought Traits (used by HyperSpy) and traitlets (used by anywidget) are bridged with `link_traits.link()`. Changes in the GUI propagate to the HyperSpy object and vice versa.

3. **ContainerWidget bridges Jupyter and Marimo** — On the Jupyter path, `ContainerWidget` deliberately uses real `ipywidgets` containers such as `VBox`, `HBox`, `Tab`, and `Accordion` so the GUI integrates with the native widget stack. On the Marimo path, those layouts are flattened into `FlatContainer` configs rendered by anywidget.

4. **Environment-aware display** — The `@add_display_arg` decorator handles the difference between Jupyter and Marimo. In Marimo it flattens `VBox`/`HBox` roots before display when needed, and `display=False` always returns the raw `{"widget": ..., "wdict": ...}` dictionary.

5. **33 widget functions** — All GUI functions return a dictionary with `"widget"` (the root AnyWidget) and `"wdict"` (a mapping of named sub-widgets). This pattern is consistent across ROI widgets, axis widgets, model widgets, tool widgets, and preference widgets.

## Running the tests

pytest is required to run the tests.

```bash
pip install "hyperspy_gui_anywidget[tests]"
pytest --pyargs hyperspy_gui_anywidget
```

## Examples

See the `examples/` directory:

- `examples/comparison_notebook.ipynb` — clean `ipywidgets` vs `anywidget` side-by-side comparison for representative HyperSpy GUIs ([GitHub](https://github.com/hyperspy/hyperspy_gui_anywidget/blob/main/examples/comparison_notebook.ipynb), [Binder](https://mybinder.org/v2/gh/hyperspy/hyperspy_gui_anywidget/HEAD?filepath=examples%2Fcomparison_notebook.ipynb))
- `examples/jupyter_anywidget_example.ipynb` — practical Jupyter Notebook / JupyterLab walkthrough using the default `display=True` flow ([GitHub](https://github.com/hyperspy/hyperspy_gui_anywidget/blob/main/examples/jupyter_anywidget_example.ipynb), [Binder](https://mybinder.org/v2/gh/hyperspy/hyperspy_gui_anywidget/HEAD?filepath=examples%2Fjupyter_anywidget_example.ipynb))
- `examples/marimo_anywidget_example.py` — equivalent Marimo app showing explicit `mo.ui.anywidget(...)` embedding via `display=False` ([GitHub](https://github.com/hyperspy/hyperspy_gui_anywidget/blob/main/examples/marimo_anywidget_example.py))

The Jupyter notebook examples link to Binder so they open in a live notebook session instead of a
static renderer. The Marimo example is currently linked as source only: this repository does not
yet publish a verified dynamic Marimo deployment for that example.

## Development

Contributions through pull requests are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md) for this repository's setup, testing, docs, and changelog workflow, and see the [HyperSpy Developer Guide](http://hyperspy.org/hyperspy-doc/current/dev_guide.html) for the broader project conventions.

When adding a new widget:

1. Create an AnyWidget subclass (or reuse one from `custom_widgets.py`)
2. Use `link_traits.link()` to sync with HyperSpy traits
3. Wrap everything in a `ContainerWidget`
4. Apply `@add_display_arg` for environment-aware display
5. Register the widget in `hyperspy_extension.yaml`
6. Add tests in `hyperspy_gui_anywidget/tests/`

`ipywidgets` is therefore an explicit runtime dependency by design: anywidget provides the custom leaf widgets, while `ipywidgets` still provides the Jupyter-native container layer that this package bridges to Marimo.

Before opening a pull request, run:

```bash
pre-commit run --all-files
pytest --pyargs hyperspy_gui_anywidget
sphinx-build -W -b html docs docs/_build/html
```

User-facing changes should also include a short news fragment in `upcoming_changes/`.

## License

This project is licensed under the GNU General Public License v3 (GPLv3).
