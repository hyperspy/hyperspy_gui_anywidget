# User guide

`hyperspy_gui_anywidget` provides the anywidget-backed GUI toolkit for HyperSpy.
It is explicitly supported in Jupyter Notebook / JupyterLab and in Marimo without
requiring a separate frontend build step.

## Installation

```{code-block} bash
pip install hyperspy_gui_anywidget
```

For local development, install the development, test, and docs extras together:

```{code-block} bash
pip install -e ".[dev,tests,doc]"
```

## Jupyter usage

For modern Jupyter environments, installing `hyperspy_gui_anywidget` is enough. You do not
need to manually enable a separate anywidget extension in current JupyterLab or Notebook
releases.

In normal use, `display=True` is the default and recommended path: calling a HyperSpy GUI
method displays the widget inline immediately.

```{code-block} python
import hyperspy.api as hs

hs.preferences.gui(toolkit="anywidget")
```

ROI and tool GUIs follow the same default display pattern:

```{code-block} python
import hyperspy.api as hs

signal = hs.signals.Signal1D([1, 2, 3])
signal.axes_manager.gui(toolkit="anywidget")
```

```{code-block} python
roi = hs.roi.SpanROI(left=0, right=10)
roi.gui(toolkit="anywidget")
```

Use `display=False` only when you need the raw return structure for testing,
inspection, or custom embedding:

```{code-block} python
roi = hs.roi.SpanROI(left=0, right=10)
result = roi.gui(toolkit="anywidget", display=False)
widget = result["anywidget"]["widget"]
wdict = result["anywidget"]["wdict"]
```

## Marimo usage

Marimo uses the same default behavior: with `display=True`, widgets are displayed inline.

When you need the raw widget object for explicit embedding, request it with
`display=False`:

```{code-block} python
import marimo as mo
import hyperspy.api as hs

roi = hs.roi.SpanROI(left=0, right=10)
result = roi.gui(toolkit="anywidget", display=False)
mo.ui.anywidget(result["anywidget"]["widget"])
```

For `VBox`/`HBox`-based layouts, the helper layer flattens the widget tree into a
`FlatContainer` so Marimo can render it consistently.

## Supported environments

This repository explicitly supports and tests:

- Jupyter Notebook / JupyterLab
- Marimo

The leaf widgets are built with `anywidget`, so they may also work in other frontends that
support Jupyter widgets / anywidget. However, this package does not currently claim tested
support for environments such as VS Code notebooks, Google Colab, JupyterLite, or Voila.

If you try another frontend, expect the best results when it supports the Jupyter widget
protocol end-to-end. The least portable part of the stack is the container layer, because
the Jupyter path uses `ipywidgets` containers and the Marimo path uses flattened
`FlatContainer` layouts.

## Widget model

The public GUI functions all return the same internal structure when
`display=False` is used:

- `widget`: the root AnyWidget or container widget
- `wdict`: a mapping of named child widgets used by tests and integrations

That convention is shared across ROI, axes, model, tool, preference, and
microscope-parameter UIs.

## Why `ipywidgets` is still a dependency

Although this package provides anywidget-backed GUIs, it intentionally keeps
`ipywidgets` as part of the runtime design. In Jupyter, layout containers such
as tabs, accordions, and horizontal/vertical boxes are native `ipywidgets`
objects. When the same UI needs to run in Marimo, the helper layer converts that
container structure into a `FlatContainer` representation.

In practice, that means:

- `anywidget` provides the custom widget implementations.
- `ipywidgets` provides the Jupyter-native container layer.
- the package bridges between them so the same HyperSpy GUI code works in both
  environments.
