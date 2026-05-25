import sys
from unittest.mock import patch

from ipywidgets import Accordion, HBox, Tab, VBox

from hyperspy_gui_anywidget.custom_widgets import (
    ContainerWidget,
    FlatContainer,
    FloatRangeSliderWidget,
    FloatTextWidget,
    OddIntSliderWidget,
    TextWidget,
    _apply_value,
    _extract_value,
    _flatten_widget_tree,
    _make_flat_container,
    _widget_config,
)


def test_widget_config_preserves_slider_metadata():
    widget = OddIntSliderWidget(
        value=5,
        min=3,
        max=11,
        description="Window length",
        slider_width="220px",
        visible=False,
    )

    cfg = _widget_config(widget)

    assert cfg["type"] == "slider"
    assert cfg["step"] == 2
    assert cfg["slider_width"] == "220px"
    assert cfg["visible"] is False


def test_widget_config_marks_color_text_widgets():
    widget = TextWidget(value="red", description="Color", disabled=True, visible=False)

    cfg = _widget_config(widget)

    assert cfg["type"] == "text"
    assert cfg["is_color"] is True
    assert cfg["disabled"] is True
    assert cfg["visible"] is False


def test_flatten_widget_tree_preserves_tabs_and_accordions():
    first = FloatTextWidget(description="Left")
    second = FloatTextWidget(description="Right")

    tab = Tab(children=[first, second])
    tab.set_title(0, "First")
    tab.set_title(1, "Second")

    accordion = Accordion(children=[HBox(children=[first]), VBox(children=[second])])
    accordion.set_title(0, "A")
    accordion.set_title(1, "B")

    configs = _flatten_widget_tree([tab, accordion])
    types = [cfg["type"] for cfg in configs]

    assert types.count("tab_start") == 2
    assert types.count("tab_end") == 2
    assert "accordion_start" in types
    assert "accordion_end" in types


def test_make_flat_container_syncs_children_values():
    child = FloatTextWidget(description="Left", value=1.5)
    container = _make_flat_container([child], "vertical")
    child_id = str(id(child))

    assert isinstance(container, FlatContainer)

    child.value = 2.5
    assert container._children_values[child_id] == 2.5

    container._children_values = {child_id: 3.5}
    assert child.value == 3.5


def test_container_widget_uses_flat_container_in_marimo():
    child = FloatTextWidget(description="Left", value=1.0)

    with patch.dict(sys.modules, {"marimo": object()}):
        container = ContainerWidget(children=[child], layout="horizontal")

    assert isinstance(container, FlatContainer)
    assert container._layout == "horizontal"


def test_apply_and_extract_range_slider_values():
    widget = FloatRangeSliderWidget(value=[1.0, 2.0])

    assert _extract_value(widget) == [1.0, 2.0]

    _apply_value(widget, [3.0, 4.0])

    assert list(widget.value) == [3.0, 4.0]
