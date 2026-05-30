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
        # widget → axis
        wd["axis0"]["value"].value = 1.0
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

        # axis → widget (reverse — use non-value text attrs to avoid
        # FloatSlider value validator feedback loop)
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
