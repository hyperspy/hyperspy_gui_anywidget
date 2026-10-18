import sys
from unittest.mock import patch

import pytest
from ipywidgets import Accordion, GridBox, HBox, Tab, VBox

from hyperspy_gui_anywidget.custom_widgets import (
    BoundedFloatTextWidget,
    ContainerWidget,
    FlatContainer,
    FloatRangeSliderWidget,
    FloatTextWidget,
    OddIntSliderWidget,
    TextWidget,
    ToggleButtonWidget,
    _apply_value,
    _build_flat_configs,
    _extract_value,
    _flatten_widget_tree,
    _make_flat_container,
    _widget_config,
)
from hyperspy_gui_anywidget.utils import _Dropdown


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


def test_number_and_dropdown_width_reach_flat_config():
    number = BoundedFloatTextWidget(input_width="90px")
    assert _widget_config(number)["input_width"] == "90px"
    assert BoundedFloatTextWidget().input_width == "160px"
    assert BoundedFloatTextWidget().label_min_width == "120px"

    dropdown = _Dropdown(options=["a", "b"], select_width="120px")
    assert _widget_config(dropdown)["select_width"] == "120px"
    assert _Dropdown(options=["a", "b"]).select_width == "160px"

    toggle = ToggleButtonWidget(button_width="75px")
    assert _widget_config(toggle)["button_width"] == "75px"
    assert ToggleButtonWidget().button_width == ""


def test_container_max_width_caps_both_toolkit_paths():
    vbox = ContainerWidget(children=[], layout="vertical", max_width="440px")
    assert vbox.layout.max_width == "440px"

    hbox = ContainerWidget(children=[], layout="horizontal", max_width="300px")
    assert hbox.layout.max_width == "300px"

    flat = _make_flat_container([], "vertical", max_width="440px")
    assert flat._max_width == "440px"


@pytest.mark.parametrize("is_color", [True, False])
def test_widget_config_marks_color_text_widgets(is_color):
    widget = TextWidget(
        value="red", description="Color", disabled=True, visible=False, is_color=is_color
    )

    cfg = _widget_config(widget)

    assert cfg["type"] == "text"
    assert cfg["is_color"] is is_color
    assert cfg["disabled"] is True
    assert cfg["visible"] is False


def test_widget_config_passes_decimals_for_bounded_float():
    widget = BoundedFloatTextWidget(min=0, step=0.01, decimals=2)

    cfg = _widget_config(widget)

    assert cfg["type"] == "number"
    assert cfg["decimals"] == 2


def test_bounded_float_rounds_value_to_decimals():
    widget = BoundedFloatTextWidget(min=0, step=0.01, decimals=2)

    widget.value = 9.923874
    assert widget.value == 9.92

    widget.decimals = None
    widget.value = 9.923874
    assert widget.value == 9.923874


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


def test_flatten_widget_tree_carries_accordion_selected_index():
    first = FloatTextWidget(description="A")
    accordion = Accordion(children=[VBox(children=[first])])
    accordion.set_title(0, "Help")

    configs = _flatten_widget_tree([accordion])
    start = next(cfg for cfg in configs if cfg["type"] == "accordion_start")

    # ipywidgets 8 defaults selected_index to None, which renders every
    # section closed; the flat config must carry that state unchanged.
    assert start["selected_index"] is None

    accordion.selected_index = 0
    configs = _flatten_widget_tree([accordion])
    start = next(cfg for cfg in configs if cfg["type"] == "accordion_start")
    assert start["selected_index"] == 0


def test_build_flat_configs_accordion_selected_index_default_closed():
    child = FloatTextWidget(description="Left", value=1.0)

    configs, layout = _build_flat_configs([child], "accordion", titles=["Help"])

    assert layout == "vertical"
    assert configs[0]["type"] == "accordion_start"
    assert configs[0]["titles"] == ["Help"]
    assert configs[0]["selected_index"] is None

    configs, _ = _build_flat_configs([child], "accordion", titles=["Help"], selected_index=0)
    assert configs[0]["selected_index"] == 0


def test_container_widget_marimo_accordion_selected_index():
    with patch.dict(sys.modules, {"marimo": object()}):
        closed = ContainerWidget(
            children=[FloatTextWidget(description="Left", value=1.0)],
            layout="accordion",
            titles=["Help"],
        )
        opened = ContainerWidget(
            children=[FloatTextWidget(description="Right", value=2.0)],
            layout="accordion",
            titles=["Help"],
            selected_index=0,
        )

    assert isinstance(closed, FlatContainer)
    assert closed._children_config[0]["selected_index"] is None
    assert opened._children_config[0]["selected_index"] == 0


def test_container_widget_grid_layout_builds_gridbox():
    cell = FloatTextWidget(description="Element")

    container = ContainerWidget(children=[cell], layout="grid", grid_template_columns="70px 100px")

    assert isinstance(container, GridBox)
    assert container.layout.grid_template_columns == "70px 100px"
    assert container.layout.grid_template_rows == "auto"


def test_flatten_widget_tree_preserves_grid_columns():
    first = FloatTextWidget(description="Element")
    second = FloatTextWidget(description="Line")
    grid = GridBox(children=[first, second])
    grid.layout.grid_template_columns = "70px 100px"

    configs = _flatten_widget_tree([grid])

    grid_starts = [cfg for cfg in configs if cfg.get("direction") == "grid"]
    assert len(grid_starts) == 1
    assert grid_starts[0]["grid_template_columns"] == "70px 100px"
    assert [cfg["type"] for cfg in configs].count("layout_end") == 1


def test_make_flat_container_wraps_root_grid_in_layout_markers():
    child = FloatTextWidget(description="Element", value=1.0)

    container = _make_flat_container([child], "grid", grid_template_columns="70px 100px")

    directions = [cfg.get("direction") for cfg in container._children_config]
    assert "grid" in directions
    assert container._layout == "vertical"


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
