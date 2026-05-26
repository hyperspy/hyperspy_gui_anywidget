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
# hyperspy-gui-anywidget = { git = "https://github.com/hyperspy/hyperspy_gui_anywidget.git", branch = "master" }
#
# [tool.uv]
# override-dependencies = ["hyperspy==2.3.0"]
# ///

import marimo

__generated_with = "0.23.5"
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
    return mo.md("### ROI widgets")


@app.cell
def _(hs, mo):
    _roi = hs.roi.SpanROI(left=5, right=15)
    _widget = _roi.gui(toolkit="anywidget", display=False)["anywidget"]["widget"]
    return mo.ui.anywidget(_widget)


@app.cell
def _(hs, mo):
    _roi = hs.roi.Point2DROI(x=2, y=3)
    _widget = _roi.gui(toolkit="anywidget", display=False)["anywidget"]["widget"]
    return mo.ui.anywidget(_widget)


@app.cell
def _(hs, mo):
    _roi = hs.roi.Line2DROI(x1=0, y1=1, x2=10, y2=4, linewidth=2)
    _widget = _roi.gui(toolkit="anywidget", display=False)["anywidget"]["widget"]
    return mo.ui.anywidget(_widget)


@app.cell
def _(hs, mo):
    _roi = hs.roi.CircleROI(cx=8, cy=6, r=4, r_inner=1)
    _widget = _roi.gui(toolkit="anywidget", display=False)["anywidget"]["widget"]
    return mo.ui.anywidget(_widget)


@app.cell
def _(mo):
    return mo.md("### Axes manager")


@app.cell
def _(hs, mo, np):
    _signal = hs.signals.Signal1D(np.random.random((2, 3, 20)))
    _widget = _signal.axes_manager.gui(toolkit="anywidget", display=False)["anywidget"]["widget"]
    return mo.ui.anywidget(_widget)


@app.cell
def _(mo):
    return mo.md("### Model components")


@app.cell
def _(hs, mo):
    _signal = hs.signals.Signal1D([1.0] * 100)
    _signal.axes_manager[0].scale = 0.1
    _model = _signal.create_model()
    _gaussian = hs.model.components1D.Gaussian(A=10, centre=5, sigma=1)
    _model.append(_gaussian)
    _component_widget = _gaussian.gui(toolkit="anywidget", display=False)["anywidget"]["widget"]
    _model_widget = _model.gui(toolkit="anywidget", display=False)["anywidget"]["widget"]
    return mo.vstack([mo.ui.anywidget(_component_widget), mo.ui.anywidget(_model_widget)])


@app.cell
def _(mo):
    return mo.md("### Signal processing tools")


@app.cell
def _(hs, mo, np):
    _signal = hs.signals.Signal1D(np.arange(100.0) ** 2)
    _widget = _signal.smooth_savitzky_golay(toolkit="anywidget", display=False)["anywidget"]["widget"]
    return mo.ui.anywidget(_widget)


@app.cell
def _(hs, mo, np):
    _signal = hs.signals.Signal1D(np.arange(100.0) ** 2)
    _widget = _signal.remove_background(toolkit="anywidget", display=False)["anywidget"]["widget"]
    return mo.ui.anywidget(_widget)


@app.cell
def _(hs, mo, np):
    _signal = hs.signals.Signal1D(np.arange(100.0) * 3.0)
    _widget = _signal.calibrate(toolkit="anywidget", display=False)["anywidget"]["widget"]
    return mo.ui.anywidget(_widget)


@app.cell
def _(mo):
    return mo.md("### Preferences")


@app.cell
def _(hs, mo):
    _widget = hs.preferences.gui(toolkit="anywidget", display=False)["anywidget"]["widget"]
    return mo.ui.anywidget(_widget)
