import sys
import types

import hyperspy.api as hs
import numpy as np
import pytest

from hyperspy_gui_anywidget.tests.utils import KWARGS


def check_axis_attributes(axes_manager, widgets_dict, index, attributes):
    for attribute in attributes:
        assert widgets_dict["axis{}".format(index)][attribute].value == getattr(
            axes_manager[index], attribute
        )


class TestAxes:
    def setup_method(self, method):
        self.s = hs.signals.Signal1D(np.empty((2, 3, 4)))
        am = self.s.axes_manager
        am[0].scale = 0.5
        am[0].name = "a"
        am[0].units = "eV"
        am[1].scale = 1000
        am[1].name = "b"
        am[1].units = "meters"
        am[2].scale = 5
        am[2].name = "c"
        am[2].units = "e"
        am.indices = (2, 1)

    def test_navigation_sliders(self):
        s = self.s
        am = self.s.axes_manager
        wd = s.axes_manager.gui_navigation_sliders(**KWARGS)["anywidget"]["wdict"]
        check_axis_attributes(
            axes_manager=am, widgets_dict=wd, index=0, attributes=("value", "index", "units")
        )
        check_axis_attributes(
            axes_manager=am, widgets_dict=wd, index=1, attributes=("value", "index", "units")
        )
        wd["axis0"]["value"].value = 1.5
        am[0].units = "cm"
        check_axis_attributes(
            axes_manager=am, widgets_dict=wd, index=0, attributes=("value", "index", "units")
        )

    def test_navigation_sliders_change_signal_index(self):
        s = hs.signals.Signal1D(np.arange(10 * 4).reshape(10, 4))
        am = s.axes_manager
        assert am.indices == (0,)  # start at index 0
        wd = s.axes_manager.gui_navigation_sliders(**KWARGS)["anywidget"]["wdict"]

        # Navigate to index 3 via the widget
        wd["axis0"]["index"].value = 3
        assert am.indices == (3,)
        assert am[0].index == 3

        # Navigate to index 7
        wd["axis0"]["index"].value = 7
        assert am.indices == (7,)
        assert am[0].index == 7

    def test_axes_manager_gui(self):
        s = self.s
        am = self.s.axes_manager
        wd = s.axes_manager.gui(**KWARGS)["anywidget"]["wdict"]
        # Verify value widget is a read-only FloatTextWidget display
        from hyperspy_gui_anywidget.custom_widgets import FloatTextWidget

        assert isinstance(wd["axis0"]["value"], FloatTextWidget)
        assert wd["axis0"]["value"].disabled is True
        check_axis_attributes(
            axes_manager=am,
            widgets_dict=wd,
            index=0,
            attributes=(
                "value",
                "index",
                "units",
                "index_in_array",
                "name",
                "size",
                "scale",
                "offset",
            ),
        )
        check_axis_attributes(
            axes_manager=am,
            widgets_dict=wd,
            index=1,
            attributes=(
                "value",
                "index",
                "units",
                "index_in_array",
                "name",
                "size",
                "scale",
                "offset",
            ),
        )
        check_axis_attributes(
            axes_manager=am,
            widgets_dict=wd,
            index=2,
            attributes=("units", "index_in_array", "name", "size", "scale", "offset"),
        )
        # widget → axis (index change cascades value to read-only text display via link_traits)
        wd["axis0"]["index"].value = 1
        wd["axis0"]["name"].value = "parrot"
        wd["axis0"]["units"].value = "cm"
        check_axis_attributes(
            axes_manager=am,
            widgets_dict=wd,
            index=0,
            attributes=(
                "value",
                "index",
                "units",
                "index_in_array",
                "name",
                "size",
                "scale",
                "offset",
            ),
        )

        # axis → widget (reverse sync)
        am[1].name = "blue"
        am[1].units = "nm"
        am[2].name = "signal_name"
        check_axis_attributes(
            axes_manager=am,
            widgets_dict=wd,
            index=1,
            attributes=("name", "units", "index_in_array", "size", "scale", "offset"),
        )
        check_axis_attributes(
            axes_manager=am,
            widgets_dict=wd,
            index=2,
            attributes=("units", "index_in_array", "name", "size", "scale", "offset"),
        )


def test_non_uniform_axes():
    try:
        import hyperspy.axes

        if not hasattr(hyperspy.axes, "UniformDataAxis"):
            pytest.skip("HyperSpy version doesn't support non-uniform axis")
    except ImportError:
        pytest.skip("HyperSpy version doesn't support non-uniform axis")

    dict0 = {
        "scale": 1.0,
        "size": 2,
    }
    dict1 = {
        "expression": "a / (x+b)",
        "a": 1240,
        "b": 1,
        "size": 3,
        "name": "plumage",
        "units": "beautiful",
    }
    dict2 = {"axis": np.arange(4), "name": "norwegianblue", "units": "ex"}
    dict3 = {
        "expression": "a / (x+b)",
        "a": 1240,
        "b": 1,
        "x": dict2,
        "name": "pushing up",
        "units": "the daisies",
    }
    s = hs.signals.Signal1D(np.empty((3, 2, 4, 4)), axes=[dict0, dict1, dict2, dict3])
    s.axes_manager[0].navigate = False

    am = s.axes_manager
    wd = s.axes_manager.gui(**KWARGS)["anywidget"]["wdict"]
    check_axis_attributes(
        axes_manager=am,
        widgets_dict=wd,
        index=0,
        attributes=(
            "name",
            "units",
            "size",
            "index",
            "value",
            "index_in_array",
        ),
    )
    check_axis_attributes(
        axes_manager=am,
        widgets_dict=wd,
        index=2,
        attributes=("name", "units", "size", "index_in_array"),
    )
    check_axis_attributes(
        axes_manager=am,
        widgets_dict=wd,
        index=3,
        attributes=("name", "units", "size", "index_in_array"),
    )
    s.axes_manager.gui_navigation_sliders(**KWARGS)
    check_axis_attributes(
        axes_manager=am,
        widgets_dict=wd,
        index=0,
        attributes=(
            "name",
            "units",
            "size",
            "index",
            "value",
            "index_in_array",
        ),
    )
    check_axis_attributes(
        axes_manager=am,
        widgets_dict=wd,
        index=2,
        attributes=("name", "units", "size", "index_in_array"),
    )
    check_axis_attributes(
        axes_manager=am,
        widgets_dict=wd,
        index=3,
        attributes=("name", "units", "size", "index_in_array"),
    )


def test_axes_manager_titles_follow_ipywidgets_numbering():
    s = hs.signals.Signal1D(np.empty((2, 3, 4)))
    result = s.axes_manager.gui(**KWARGS)["anywidget"]["widget"]
    nav_container, sig_container = result.children
    assert nav_container.get_title(0) == "Axis 0"
    assert nav_container.get_title(1) == "Axis 1"
    assert sig_container.get_title(0) == "Axis 3"


class TestMarimoPaths:
    """Tests for the Marimo FlatContainer path."""

    def setup_method(self, method):
        # Simulate Marimo being present for the duration of each test.
        sys.modules["marimo"] = types.ModuleType("marimo")

    def teardown_method(self, method):
        sys.modules.pop("marimo", None)

    def test_axes_manager_gui_marimo_returns_flat_container(self):
        from hyperspy_gui_anywidget.custom_widgets import FlatContainer

        s = hs.signals.Signal1D(np.arange(3 * 4).reshape(3, 4))
        result = s.axes_manager.gui(**KWARGS)["anywidget"]
        assert isinstance(result["widget"], FlatContainer)

    def test_axes_manager_gui_marimo_widget_to_axis_sync(self):
        """Simulated browser update on the outer FlatContainer propagates to the axis."""
        s = hs.signals.Signal1D(np.arange(3 * 4).reshape(3, 4))
        am = s.axes_manager
        assert am[0].index == 0

        result = s.axes_manager.gui(**KWARGS)["anywidget"]
        outer = result["widget"]
        wd = result["wdict"]
        index_widget = wd["axis0"]["index"]

        # Simulate the browser sending a slider update to the outermost FlatContainer.
        slider_id = str(id(index_widget))
        new_vals = dict(outer._children_values)
        new_vals[slider_id] = 2
        outer._children_values = new_vals

        assert index_widget.value == 2
        assert am[0].index == 2

    def test_axes_manager_gui_marimo_axis_to_widget_sync(self):
        """Python-side axis change propagates back to the outer FlatContainer."""
        s = hs.signals.Signal1D(np.arange(3 * 4).reshape(3, 4))
        am = s.axes_manager
        result = s.axes_manager.gui(**KWARGS)["anywidget"]
        outer = result["widget"]
        wd = result["wdict"]
        index_widget = wd["axis0"]["index"]

        am[0].index = 2

        assert index_widget.value == 2
        slider_id = str(id(index_widget))
        assert outer._children_values.get(slider_id) == 2

    def test_axes_manager_gui_marimo_second_drag_updates_axis(self):
        """Second simulated drag must update the axis (regression: slider was sticky after first drag)."""
        s = hs.signals.Signal1D(np.arange(3 * 4).reshape(3, 4))
        am = s.axes_manager
        assert am[0].index == 0

        result = s.axes_manager.gui(**KWARGS)["anywidget"]
        outer = result["widget"]
        wd = result["wdict"]
        index_widget = wd["axis0"]["index"]
        slider_id = str(id(index_widget))

        # First drag: 0 → 1
        new_vals = dict(outer._children_values)
        new_vals[slider_id] = 1
        outer._children_values = new_vals
        assert am[0].index == 1

        # Second drag: 1 → 2
        new_vals = dict(outer._children_values)
        new_vals[slider_id] = 2
        outer._children_values = new_vals
        assert index_widget.value == 2
        assert am[0].index == 2
        assert outer._children_values.get(slider_id) == 2

        # Third drag: 2 → 0 (going backwards must also work)
        new_vals = dict(outer._children_values)
        new_vals[slider_id] = 0
        outer._children_values = new_vals
        assert index_widget.value == 0
        assert am[0].index == 0
        assert outer._children_values.get(slider_id) == 0

    def test_axes_manager_gui_marimo_button_click_increments_clicks(self):
        """Simulated button click via _children_values increments ButtonWidget.clicks."""
        from hyperspy_gui_anywidget.custom_widgets import ButtonWidget

        btn = ButtonWidget(description="Click me")
        clicks_seen = []
        btn.observe(lambda c: clicks_seen.append(c["new"]), names="clicks")

        from hyperspy_gui_anywidget.custom_widgets import _make_flat_container

        # Build a minimal FlatContainer wired to the button
        flat = _make_flat_container([btn], layout="vertical")
        btn_id = str(id(btn))

        assert btn.clicks == 0
        # Simulate a browser click (JS increments the value to 1)
        new_vals = dict(flat._children_values)
        new_vals[btn_id] = 1
        flat._children_values = new_vals
        assert btn.clicks == 1
        assert clicks_seen == [1]

        # Second click
        new_vals = dict(flat._children_values)
        new_vals[btn_id] = 2
        flat._children_values = new_vals
        assert btn.clicks == 2

    def test_axes_manager_gui_marimo_continuous_update_propagates(self):
        """Changing continuous_update on the Python widget updates the _cu key."""
        from hyperspy_gui_anywidget.custom_widgets import IntSliderWidget, _make_flat_container

        slider = IntSliderWidget(min=0, max=10, value=0)
        flat = _make_flat_container([slider], layout="vertical")
        slider_id = str(id(slider))
        cu_key = slider_id + "_cu"

        # Initially the _cu key is absent (pushed only on change)
        assert slider.continuous_update is True

        # Changing continuous_update on the Python side should push the _cu key
        slider.continuous_update = False
        assert flat._children_values.get(cu_key) is False

        slider.continuous_update = True
        assert flat._children_values.get(cu_key) is True

    def test_marimo_toggle_second_click_reverses(self):
        """Two consecutive toggle updates via _children_values toggle correctly."""
        from hyperspy_gui_anywidget.custom_widgets import ToggleButtonWidget, _make_flat_container

        toggle = ToggleButtonWidget(value=False)
        flat = _make_flat_container([toggle], layout="vertical")
        toggle_id = str(id(toggle))

        # First toggle: False → True
        new_vals = dict(flat._children_values)
        new_vals[toggle_id] = True
        flat._children_values = new_vals
        assert toggle.value is True

        # Second toggle: True → False
        new_vals = dict(flat._children_values)
        new_vals[toggle_id] = False
        flat._children_values = new_vals
        assert toggle.value is False
