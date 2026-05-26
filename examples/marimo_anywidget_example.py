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
    return mo.md(
        """## hyperspy_gui_anywidget in Marimo

This app mirrors the Jupyter example as closely as possible while using Marimo's layout model.

Most users should keep the default `display=True`, which displays the widget inline as soon as you call the GUI method."""
    )


@app.cell
def _(mo):
    return mo.md("## Preferences")


@app.cell
def _(hs):
    return hs.preferences.gui(toolkit="anywidget", display=True)


@app.cell
def _(mo):
    return mo.md("## SpanROI")


@app.cell
def _(hs):
    _roi = hs.roi.SpanROI(left=5, right=15)
    return _roi.gui(toolkit="anywidget", display=True)


@app.cell
def _(mo):
    return mo.md("## More ROIs")


@app.cell
def _(hs):
    _point_roi = hs.roi.Point2DROI(x=3, y=7)
    _line_roi = hs.roi.Line2DROI(x1=0, y1=0, x2=10, y2=10, linewidth=2)
    _circle_roi = hs.roi.CircleROI(cx=5, cy=5, r=3, r_inner=1)
    return (
        _point_roi.gui(toolkit="anywidget", display=True),
        _line_roi.gui(toolkit="anywidget", display=True),
        _circle_roi.gui(toolkit="anywidget", display=True),
    )


@app.cell
def _(mo):
    return mo.md("## Axes manager")


@app.cell
def _(hs, np):
    _signal = hs.signals.Signal1D(np.random.random((4, 6, 20)))
    return _signal.axes_manager.gui(toolkit="anywidget", display=True)


@app.cell
def _(mo):
    return mo.md("## Signal plot")


@app.cell
def _(hs, np):
    _signal = hs.signals.Signal1D(np.arange(100.0))
    _signal.plot()
    return


@app.cell
def _(mo):
    return mo.md("## Model parameter")


@app.cell
def _(hs, np):
    _signal = hs.signals.Signal1D(np.ones(100))
    _signal.axes_manager[0].scale = 0.1
    _model = _signal.create_model()
    _gaussian = hs.model.components1D.Gaussian(A=10, centre=5, sigma=1)
    _model.append(_gaussian)
    return _gaussian.A.gui(toolkit="anywidget", display=True)


@app.cell
def _(mo):
    return mo.md("## Model plot + component GUI")


@app.cell
def _(hs, np):
    _signal = hs.signals.Signal1D(np.ones(100))
    _signal.axes_manager[0].scale = 0.1
    _model = _signal.create_model()
    _gaussian = hs.model.components1D.Gaussian(A=10, centre=5, sigma=1)
    _model.append(_gaussian)
    _model.plot()
    return _gaussian.gui(toolkit="anywidget", display=True)


@app.cell
def _(mo):
    return mo.md("## Smooth Savitzky-Golay")


@app.cell
def _(hs, np):
    _smooth_signal = hs.signals.Signal1D(1 + np.arange(100.0) ** 2)
    _smooth_signal.add_gaussian_noise(50)
    _smooth_signal.change_dtype("float")
    return _smooth_signal.smooth_savitzky_golay(toolkit="anywidget", display=True)


@app.cell
def _(mo):
    return mo.md("## Background removal + calibrate")


@app.cell
def _(hs, np):
    _power_law_signal = hs.signals.Signal1D(50 + 1000 / (np.arange(1, 101.0) ** 1.5))
    _power_law_signal.change_dtype("float")
    _power_law_signal.remove_background(toolkit="anywidget", display=True)

    _wrong_calibration = hs.signals.Signal1D(np.arange(100.0) * 3.0)
    _wrong_calibration.axes_manager[0].offset = 10
    _wrong_calibration.axes_manager[0].scale = 2
    _wrong_calibration.axes_manager[0].units = "nm"
    return _wrong_calibration.calibrate(toolkit="anywidget", display=True)


@app.cell
def _(mo):
    return mo.md("## display=False example")


@app.cell
def _(hs):
    _result = hs.roi.Point2DROI(x=3, y=7).gui(toolkit="anywidget", display=False)
    return _result["anywidget"].keys()


@app.cell
def _(mo):
    return mo.md("### Marimo-native features (bonus)")


@app.cell
def _(hs, mo):
    _roi = hs.roi.SpanROI(left=5, right=15)
    _res = _roi.gui(toolkit="anywidget", display=False)
    _widget = _res["anywidget"]["widget"]
    _w = mo.ui.anywidget(_widget)
    return mo.vstack([
        _w,
        mo.md(f"Current ROI: {_w.value}"),
    ])
