# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "hyperspy-gui-anywidget @ git+https://github.com/hyperspy/hyperspy_gui_anywidget",
#     "hyperspy",
#     "marimo>=0.23.8",
# ]
#
# [tool.uv.sources]
# hyperspy = { git = "https://github.com/francisco-dlp/hyperspy.git", branch = "NEW_anywidgets_gui" }
#
# [tool.uv]
# # The git branch builds as a pre-release (2.4.1.dev60+g...) which uv
# # excludes by default when evaluating hyperspy-gui-anywidget's >=2.3.0
# # constraint. This override lets the dev version satisfy it.
# override-dependencies = ["hyperspy>=2.4.1.dev0"]
# ///

import marimo

__generated_with = "0.23.5"
app = marimo.App(
    css_file="/usr/local/_marimo/custom.css",
    auto_download=["html"],
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # hyperspy_gui_anywidget in Marimo

    This notebook shows the normal Marimo workflow for this project.

    """)
    return


@app.cell
def _():
    import marimo as mo

    import numpy as np
    import hyperspy.api as hs
    import hyperspy_gui_anywidget  # noqa: F401

    hs.preferences.GUIs.enable_traitsui_gui = False
    hs.preferences.GUIs.enable_anywidget_gui = True
    hs.preferences.GUIs.enable_ipywidgets_gui = False
    return hs, mo, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Preferences

    A simple way to confirm the toolkit is working is to open the HyperSpy preferences dialog.
    """)
    return


@app.cell
def _(hs):
    hs.preferences.gui()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ROI widgets

    """)
    return


@app.cell
def _(hs, np):
    s1_roi = hs.signals.Signal1D(np.arange(100))
    roi = hs.roi.SpanROI(left=5, right=15)
    s1_roi.plot()
    roi.add_widget(s1_roi)
    roi.gui()
    return


@app.cell
def _(hs):
    import scipy
    im = hs.signals.Signal2D(scipy.datasets.ascent())
    rectangular_roi = hs.roi.RectangularROI()
    im.plot()
    rectangular_roi.add_widget(im)
    rectangular_roi.gui()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Axes manager

    Axes-manager widgets are useful when navigating multidimensional signals.
    """)
    return


@app.cell
def _(hs, np):
    signal = hs.signals.Signal1D(np.random.random((4, 6, 20)))
    signal.plot()
    signal.axes_manager.gui()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Model parameter

    Model parameters use the same widget bridge and are a good example of numeric synchronization.
    """)
    return


@app.cell
def _(hs, np):
    model_signal = hs.signals.Signal1D(np.ones(100))
    model_signal.axes_manager[0].scale = 0.1
    model = model_signal.create_model()
    gaussian = hs.model.components1D.Gaussian(A=10, centre=5, sigma=1)
    model.append(gaussian)
    model.plot()
    model.gui()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tool widget

    Tool GUIs also use the same default inline-display behavior.
    """)
    return


@app.cell
def _(hs, np):
    smooth_signal = hs.signals.Signal1D(1 + np.arange(100.0) ** 2)
    smooth_signal.add_gaussian_noise(50)
    smooth_signal.change_dtype("float")
    smooth_signal.smooth_savitzky_golay()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## When to use `display=False`

    Use `display=False` only when you need the raw `{widget, wdict}` dictionary for testing, custom embedding, or direct widget inspection.
    """)
    return


@app.cell
def _(hs):
    result = hs.roi.Point2DROI(x=3, y=7).gui(display=False)
    result["anywidget"].keys()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Background removal and calibration

    Tool widgets are useful for common preprocessing workflows like background removal and axis calibration.
    """)
    return


@app.cell
def _(hs, np):
    power_law_signal = hs.signals.Signal1D(50 + 1000 / (np.arange(1, 101.0) ** 1.5))
    power_law_signal.change_dtype("float")
    power_law_signal.remove_background()
    return


@app.cell
def _(hs, np):


    wrong_calibration = hs.signals.Signal1D(np.arange(100.0) * 3.0)
    wrong_calibration.axes_manager[0].offset = 10
    wrong_calibration.axes_manager[0].scale = 2
    wrong_calibration.axes_manager[0].units = "nm"
    wrong_calibration.calibrate()
    return


if __name__ == "__main__":
    app.run()
