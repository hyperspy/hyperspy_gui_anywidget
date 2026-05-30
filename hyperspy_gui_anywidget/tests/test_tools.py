import hyperspy.api as hs
import numpy as np
import pytest
from hyperspy.signal_tools import (
    ImageContrastEditor,
    Signal1DCalibration,
    Signal2DCalibration,
)
from hyperspy.utils.baseline_removal_tool import BaselineRemoval

from hyperspy_gui_anywidget.tests.utils import KWARGS


class TestTools:
    def setup_method(self, method):
        self.s = hs.signals.Signal1D(1 + np.arange(100) ** 2)
        self.s.change_dtype("float")
        self.s.axes_manager[0].offset = 10
        self.s.axes_manager[0].scale = 2
        self.s.axes_manager[0].units = "m"
        hs.preferences.Plot.cmap_signal = "viridis"
        hs.preferences.Plot.cmap_navigator = "viridis"

    def teardown_method(self, method):
        hs.preferences.Plot.cmap_signal = "viridis"
        hs.preferences.Plot.cmap_navigator = "viridis"

    def test_calibrate(self):
        s = self.s
        cal = Signal1DCalibration(s)
        cal.ss_left_value = 10
        cal.ss_right_value = 30
        wd = cal.gui(**KWARGS)["anywidget"]["wdict"]
        wd["new_left"].value = 0
        wd["new_right"].value = 10
        wd["units"].value = "nm"
        wd["apply_button"].clicks += 1
        assert s.axes_manager[0].scale == 1
        assert s.axes_manager[0].offset == 0
        assert s.axes_manager[0].units == "nm"

    def test_calibrate_from_s(self):
        s = self.s
        wd = s.calibrate(**KWARGS)["anywidget"]["wdict"]
        wd["left"].value = 10
        wd["right"].value = 30
        wd["new_left"].value = 1
        wd["new_right"].value = 11
        wd["units"].value = "nm"
        assert wd["offset"].value == 1
        assert wd["scale"].value == 1
        wd["apply_button"].clicks += 1
        assert s.axes_manager[0].scale == 1
        assert s.axes_manager[0].offset == 1
        assert s.axes_manager[0].units == "nm"

    def test_smooth_sg(self):
        s = self.s
        s.add_gaussian_noise(0.1)
        s2 = s.deepcopy()
        result = s.smooth_savitzky_golay(**KWARGS)["anywidget"]
        wd = result["wdict"]
        wd["window_length"].value = 11
        wd["polynomial_order"].value = 5
        wd["differential_order"].value = 1
        wd["color"].value = "red"
        wd["apply_button"].clicks += 1
        s2.smooth_savitzky_golay(polynomial_order=5, window_length=11, differential_order=1)
        np.testing.assert_allclose(s.data, s2.data)
        assert "color" in wd

    def test_smooth_sg_color_widget_and_slider_width(self):
        result = self.s.smooth_savitzky_golay(**KWARGS)["anywidget"]
        wd = result["wdict"]

        assert wd["window_length"].slider_width == "220px"
        assert wd["polynomial_order"].slider_width == "220px"
        assert wd["differential_order"].slider_width == "220px"
        assert "color" in wd
        assert "picker-input" in wd["color"]._esm

    def test_smooth_lowess(self):
        s = self.s
        s.add_gaussian_noise(0.1)
        s2 = s.deepcopy()
        wd = s.smooth_lowess(**KWARGS)["anywidget"]["wdict"]
        wd["smoothing_parameter"].value = 0.9
        wd["number_of_iterations"].value = 3
        wd["color"].value = "red"
        wd["apply_button"].clicks += 1
        s2.smooth_lowess(smoothing_parameter=0.9, number_of_iterations=3)
        np.testing.assert_allclose(s.data, s2.data)

    def test_smooth_tv(self):
        s = self.s
        s.add_gaussian_noise(0.1)
        s2 = s.deepcopy()
        wd = s.smooth_tv(**KWARGS)["anywidget"]["wdict"]
        wd["smoothing_parameter"].value = 300
        wd["color"].value = "red"
        wd["apply_button"].clicks += 1
        s2.smooth_tv(smoothing_parameter=300)
        np.testing.assert_allclose(s.data, s2.data)

    def test_remove_background(self):
        s = self.s
        s.add_gaussian_noise(0.1)
        s2 = s.remove_background(
            signal_range=(15.0, 50.0),
            background_type="Polynomial",
            polynomial_order=2,
            fast=False,
            zero_fill=True,
        )
        wd = s.remove_background(**KWARGS)["anywidget"]["wdict"]
        assert wd["polynomial_order"].disabled is True
        wd["background_type"].value = "Polynomial"
        assert wd["polynomial_order"].disabled is False
        wd["polynomial_order"].value = 2
        wd["fast"].value = False
        wd["zero_fill"].value = True
        wd["left"].value = 15.0
        wd["right"].value = 50.0
        wd["apply_button"].clicks += 1
        np.testing.assert_allclose(s.data[2:], s2.data[2:], atol=1e-5)
        np.testing.assert_allclose(np.zeros(2), s2.data[:2])

    def test_constrast_editor(self):
        np.random.seed(1)
        im = hs.signals.Signal2D(np.random.random((32, 32)))
        im.plot()
        ceditor = ImageContrastEditor(im._plot.signal_plot)
        ceditor.ax.figure.canvas.draw_idle()
        wd = ceditor.gui(**KWARGS)["anywidget"]["wdict"]
        assert wd["linthresh"].value == 0.01
        assert wd["linscale"].value == 0.1
        assert wd["gamma"].value == 1.0
        wd["bins"].value = 50
        assert ceditor.bins == 50
        wd["norm"].value = "Log"
        assert ceditor.norm == "Log"
        wd["norm"].value = "Symlog"
        assert ceditor.norm == "Symlog"
        assert wd["linthresh"].value == 0.01
        assert wd["linscale"].value == 0.1
        wd["linthresh"].value = 0.1
        assert ceditor.linthresh == 0.1
        wd["linscale"].value = 0.2
        assert ceditor.linscale == 0.2
        wd["norm"].value = "Linear"
        percentile = [1.0, 99.0]
        wd["percentile"].value = percentile
        assert ceditor.vmin_percentile == percentile[0]
        assert ceditor.vmax_percentile == percentile[1]
        assert im._plot.signal_plot.vmin == f"{percentile[0]}th"
        assert im._plot.signal_plot.vmax == f"{percentile[1]}th"
        wd["norm"].value = "Power"
        assert ceditor.norm == "Power"
        assert wd["gamma"].value == 1.0
        wd["gamma"].value = 0.1
        assert ceditor.gamma == 0.1
        assert wd["auto"].value is True
        wd["auto"].value = False
        assert ceditor.auto is False
        wd["left"].value = 0.2
        assert ceditor.ss_left_value == 0.2
        wd["right"].value = 0.5
        assert ceditor.ss_right_value == 0.5
        wd["apply_button"].clicks += 1
        wd["reset_button"].clicks += 1
        assert im._plot.signal_plot.vmin == "0.0th"
        assert im._plot.signal_plot.vmax == "100.0th"

    def test_eels_table_tool(self):
        exspy = pytest.importorskip("exspy")
        s = exspy.data.EELS_MnFe(True)
        s.plot()
        try:
            from exspy import _signal_tools
        except ImportError:
            from exspy import signal_tools as _signal_tools

        er = _signal_tools.EdgesRange(s)
        er.ss_left_value = 500
        er.ss_right_value = 550
        wd = er.gui(**KWARGS)["anywidget"]["wdict"]
        wd["update"].clicks += 1
        assert wd["units"].value == "eV"
        assert wd["left"].value == 500
        assert wd["right"].value == 550
        assert len(wd["gb"].children) == 44
        wd["major"].value = True
        wd["update"].clicks += 1
        assert len(wd["gb"].children) == 24
        assert wd["gb"].children[4].description == "Sb_M4"
        wd["order"].value = "ascending"
        wd["update"].clicks += 1
        assert wd["gb"].children[4].description == "V_L3"
        wd["reset"].clicks += 1
        assert len(wd["gb"].children) == 4


def test_calibration_2d():
    s = hs.signals.Signal2D(np.zeros((100, 100)))
    cal2d = Signal2DCalibration(s)
    wd = cal2d.gui(**KWARGS)["anywidget"]["wdict"]
    cal2d.x0, cal2d.x1, cal2d.y0, cal2d.y1 = 50, 70, 80, 80
    wd["new_length"].value = 10
    wd["units"].value = "mm"
    wd["apply_button"].clicks += 1
    assert s.axes_manager[0].scale == 0.5
    assert s.axes_manager[1].scale == 0.5
    assert s.axes_manager[0].units == "mm"
    assert s.axes_manager[1].units == "mm"


def test_spikes_removal_tool():
    s = hs.signals.Signal1D(np.ones((2, 3, 30)))
    s.add_gaussian_noise(std=1, random_state=0)
    max_value_after_spike_removal = 10
    s.data[1, 0, 1] += 40
    s.data[0, 2, 29] += 20
    s.data[1, 2, 14] += 100
    wd = s.spikes_removal_tool(**KWARGS)["anywidget"]["wdict"]

    def next_spike():
        wd["next_button"].clicks += 1

    def previous_spike():
        wd["previous_button"].clicks += 1

    def remove():
        wd["remove_button"].clicks += 1

    wd["threshold"].value = 25
    next_spike()
    assert s.axes_manager.indices == (0, 1)
    wd["threshold"].value = 15
    assert s.axes_manager.indices == (0, 0)
    next_spike()
    assert s.axes_manager.indices == (2, 0)
    next_spike()
    assert s.axes_manager.indices == (0, 1)
    previous_spike()
    assert s.axes_manager.indices == (2, 0)
    wd["add_noise"].value = False
    remove()
    assert s.data[0, 2, 29] < max_value_after_spike_removal
    assert s.axes_manager.indices == (0, 1)
    remove()
    assert s.data[1, 0, 1] < max_value_after_spike_removal
    assert s.axes_manager.indices == (2, 1)
    np.random.seed(1)
    wd["add_noise"].value = True
    wd["spline_order"].value = 1
    remove()
    assert s.data[1, 2, 14] < max_value_after_spike_removal
    assert s.axes_manager.indices == (0, 0)


def test_remove_baseline():
    pytest.importorskip("pybaselines")
    s = hs.data.two_gaussians().inav[:5, :5]
    s.plot()
    br = BaselineRemoval(s)
    wd = br.gui(**KWARGS)["anywidget"]["wdict"]
    br.algorithm = "Asymmetric Least Squares"
    assert wd["algorithm"].value == "Asymmetric Least Squares"
    br.algorithm = "Adaptive Smoothness Penalized Least Squares"
    br.lam = 1e7
    assert wd["lam"].value == 1e7
    br.apply()
    assert s.isig[:10].data.mean() < 5


def test_calibrate_left_right_are_read_only():
    s = hs.signals.Signal1D(1 + np.arange(100) ** 2)
    s.change_dtype("float")
    cal = Signal1DCalibration(s)
    wd = cal.gui(**KWARGS)["anywidget"]["wdict"]
    assert wd["left"].disabled is True
    assert wd["right"].disabled is True
    assert wd["new_left"].disabled is False
    assert wd["new_right"].disabled is False


def test_remove_background_polynomial_order_visibility_flag():
    s = hs.signals.Signal1D(1 + np.arange(100) ** 2)
    s.change_dtype("float")
    wd = s.remove_background(**KWARGS)["anywidget"]["wdict"]
    assert wd["polynomial_order"].visible is False
    wd["background_type"].value = "Polynomial"
    assert wd["polynomial_order"].visible is True
