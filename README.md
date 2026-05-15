# hyperspy_gui_anywidget

anywidget GUI elements for the HyperSpy framework.

This package provides GUI widgets using [anywidget](https://anywidget.dev/) for the [HyperSpy](https://hyperspy.org/) scientific data analysis library. It works in both Jupyter notebooks and [Marimo](https://marimo.io/) notebooks without any build step or bundler.

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
pip install -e ".[dev,tests]"
```

## Usage

### Jupyter Notebook / JupyterLab

In a Jupyter environment, HyperSpy will automatically use the anywidget toolkit when available:

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

In Marimo, widgets are returned as dictionaries so Marimo can handle rendering via `mo.ui.anywidget()`:

```python
import marimo as mo
import hyperspy.api as hs

roi = hs.roi.SpanROI(left=0, right=10)
res = roi.gui(toolkit="anywidget")
widget = res["anywidget"]["widget"]
mo.ui.anywidget(widget)
```

The `add_display_arg` decorator detects Marimo at runtime (via `sys.modules`) and returns the widget dictionary instead of calling `IPython.display.display()`.

## Architecture

This package is built on a few key design decisions:

1. **AnyWidget subclasses with inline `_esm` JavaScript** — Every widget is a Python class extending `anywidget.AnyWidget` with an inline JavaScript string. There is no npm, webpack, or build step. The JS renders standard HTML elements (`<input>`, `<select>`, `<button>`) and syncs state via traitlets.

2. **`link_traits` for bidirectional sync** — Enthought Traits (used by HyperSpy) and traitlets (used by anywidget) are bridged with `link_traits.link()`. Changes in the GUI propagate to the HyperSpy object and vice versa.

3. **ContainerWidget for layout** — Instead of ipywidgets `VBox`/`HBox`, this package uses a single `ContainerWidget` with a `layout` trait (`"horizontal"` or `"vertical"`). Child widgets are serialized using `IPY_MODEL_` references for Jupyter, and rendered via `widget_manager.create_view()` in the browser.

4. **Environment-aware display** — The `@add_display_arg` decorator handles the difference between Jupyter (displays the widget) and Marimo (returns the widget dictionary). Pass `display=False` to always get the raw `{"widget": ..., "wdict": ...}` dictionary.

5. **33 widget functions** — All GUI functions return a dictionary with `"widget"` (the root AnyWidget) and `"wdict"` (a mapping of named sub-widgets). This pattern is consistent across ROI widgets, axis widgets, model widgets, tool widgets, and preference widgets.

## Running the tests

pytest is required to run the tests.

```bash
pip install "hyperspy_gui_anywidget[tests]"
pytest --pyargs hyperspy_gui_anywidget
```

## Examples

See the `examples/` directory:

- `examples/test_jupyter.py` — Basic SpanROI widget test for Jupyter
- `examples/test_marimo.py` — Same test with Marimo environment mocked

## Development

Contributions through pull requests are welcome. See the [HyperSpy Developer Guide](http://hyperspy.org/hyperspy-doc/current/dev_guide.html) for general contribution guidelines.

When adding a new widget:

1. Create an AnyWidget subclass (or reuse one from `custom_widgets.py`)
2. Use `link_traits.link()` to sync with HyperSpy traits
3. Wrap everything in a `ContainerWidget`
4. Apply `@add_display_arg` for environment-aware display
5. Register the widget in `hyperspy_extension.yaml`
6. Add tests in `hyperspy_gui_anywidget/tests/`

## License

This project is licensed under the GNU General Public License v3 (GPLv3).
