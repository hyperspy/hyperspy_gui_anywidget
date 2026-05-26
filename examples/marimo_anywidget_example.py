# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "marimo",
#   "numpy",
#   "hyperspy>=1.0",
#   "anywidget>=0.9.0",
#   "ipywidgets>=7.6.0",
#   "link_traits",
#   "traitlets>=5.0",
#   "hyperspy-gui-anywidget",
# ]
#
# [tool.uv.sources]
# hyperspy = { git = "https://github.com/francisco-dlp/hyperspy.git", branch = "NEW_anywidgets_gui" }
# hyperspy-gui-anywidget = { path = "..", editable = true }
#
# [tool.uv]
# override-dependencies = ["hyperspy==2.3.0"]
# ///
import marimo

__generated_with = "0.9.30"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import hyperspy.api as hs
    import hyperspy_gui_anywidget  # noqa: F401

    hs.preferences.GUIs.enable_traitsui_gui = False
    hs.preferences.GUIs.enable_anywidget_gui = True

    return hs, mo, np


@app.cell
def _(mo):
    return (
        mo.md(
            r"""
# hyperspy_gui_anywidget in Marimo

This example shows the same kinds of widgets as the Jupyter example, but uses
`display=False` together with `mo.ui.anywidget(...)` so the notebook layout stays
explicit inside a marimo app.
"""
        ),
    )


@app.cell
def _(hs, mo):
    roi = hs.roi.SpanROI(left=5, right=15)
    _widget = roi.gui(toolkit="anywidget", display=False)["anywidget"]["widget"]
    return mo.vstack([mo.md("## SpanROI"), mo.ui.anywidget(_widget)])


@app.cell
def _(hs, mo, np):
    signal = hs.signals.Signal1D(np.random.random((4, 6, 20)))
    _widget = signal.axes_manager.gui_navigation_sliders(
        toolkit="anywidget", display=False
    )["anywidget"]["widget"]
    return mo.vstack([mo.md("## Navigation sliders"), mo.ui.anywidget(_widget)])


@app.cell
def _(hs, mo):
    model_signal = hs.signals.Signal1D([1.0] * 100)
    model_signal.axes_manager[0].scale = 0.1
    model = model_signal.create_model()
    gaussian = hs.model.components1D.Gaussian(A=10, centre=5, sigma=1)
    model.append(gaussian)
    _widget = gaussian.A.gui(toolkit="anywidget", display=False)["anywidget"]["widget"]
    return mo.vstack([mo.md("## Parameter widget"), mo.ui.anywidget(_widget)])


@app.cell
def _(hs, mo):
    _widget = hs.preferences.gui(toolkit="anywidget", display=False)["anywidget"]["widget"]
    return mo.vstack([mo.md("## Preferences"), mo.ui.anywidget(_widget)])


if __name__ == "__main__":
    app.run()
