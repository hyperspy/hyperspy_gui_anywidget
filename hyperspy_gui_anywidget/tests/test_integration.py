import importlib
from pathlib import Path

import numpy as np
import pytest
import yaml

import hyperspy.api as hs
from hyperspy_gui_anywidget.tests.utils import KWARGS


class TestWidgetRegistry:
    """Verify all 33 widget functions are registered and importable."""

    def test_all_widgets_registered(self):
        yaml_path = Path(__file__).parent.parent / "hyperspy_extension.yaml"
        data = yaml.safe_load(yaml_path.read_text())
        widgets = data["GUI"]["widgets"]["anywidget"]
        assert len(widgets) == 33, f"Expected 33 widgets, got {len(widgets)}"

        for toolkey, mapping in widgets.items():
            module_name = mapping["module"]
            function_name = mapping["function"]
            module = importlib.import_module(module_name)
            func = getattr(module, function_name, None)
            assert callable(func), (
                f"{module_name}.{function_name} is not callable "
                f"for toolkey '{toolkey}'"
            )

    def test_import_all_modules(self):
        import hyperspy_gui_anywidget
        import hyperspy_gui_anywidget.axes
        import hyperspy_gui_anywidget.custom_widgets
        import hyperspy_gui_anywidget.microscope_parameters
        import hyperspy_gui_anywidget.model
        import hyperspy_gui_anywidget.preferences
        import hyperspy_gui_anywidget.roi
        import hyperspy_gui_anywidget.tools
        import hyperspy_gui_anywidget.utils


class TestEndToEnd:
    """End-to-end integration tests for key widget workflows."""

    def test_roi_end_to_end(self):
        roi = hs.roi.SpanROI(left=0, right=10)
        result = roi.gui(**KWARGS)

        wd = result["anywidget"]["wdict"]
        assert "left" in wd
        assert "right" in wd
        assert wd["left"].value == 0
        assert wd["right"].value == 10

        # Widget -> HyperSpy sync
        wd["left"].value = -10
        wd["right"].value = 20
        assert roi.left == -10
        assert roi.right == 20

        # HyperSpy -> widget sync
        roi.left = 5
        roi.right = 15
        assert wd["left"].value == 5
        assert wd["right"].value == 15

    def test_model_end_to_end(self):
        s = hs.signals.Signal1D([0])
        m = s.create_model()
        g = hs.model.components1D.Gaussian()
        m.append(g)

        result = g.gui(**KWARGS)
        wd = result["anywidget"]["wdict"]

        # Gaussian has A, centre, sigma parameters
        assert "parameter_A" in wd
        assert "parameter_centre" in wd
        assert "parameter_sigma" in wd

        # Verify bidirectional sync on a parameter
        param_wd = wd["parameter_A"]
        param_wd["value"].value = 5.0
        assert g.A.value == 5.0

        g.A.value = 7.0
        assert param_wd["value"].value == 7.0

    def test_axes_end_to_end(self):
        s = hs.signals.Signal2D([[1, 2], [3, 4]])
        result = s.axes_manager.gui(**KWARGS)

        wd = result["anywidget"]["wdict"]
        assert "axis0" in wd
        assert "axis1" in wd

        # Verify axis widgets exist for 2D signal
        axis0 = wd["axis0"]
        assert "name" in axis0

    def test_tools_end_to_end(self):
        s = hs.signals.Signal1D(1 + np.arange(100) ** 2)
        s.change_dtype("float")

        result = s.smooth_savitzky_golay(**KWARGS)
        wd = result["anywidget"]["wdict"]

        assert "window_length" in wd
        assert "polynomial_order" in wd
        assert "differential_order" in wd
        assert "color" in wd

        # Modify widget values
        wd["window_length"].value = 11
        wd["polynomial_order"].value = 5
        wd["differential_order"].value = 1
        wd["color"].value = "red"

        # Verify the operation was applied
        s2 = s.deepcopy()
        s2.smooth_savitzky_golay(
            polynomial_order=5, window_length=11, differential_order=1
        )

        # Click apply
        wd["apply_button"].clicks += 1
        np.testing.assert_allclose(s.data, s2.data)
