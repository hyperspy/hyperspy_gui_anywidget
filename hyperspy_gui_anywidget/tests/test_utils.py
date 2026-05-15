# -*- coding: utf-8 -*-

import sys
from unittest.mock import MagicMock, patch

import anywidget
import traitlets

from hyperspy_gui_anywidget import utils


class _DummyWidget(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      el.textContent = "dummy";
    }
    export default { render };
    """
    value = traitlets.Any("").tag(sync=True)


class _MockTrait:
    def __init__(self, values=None, desc="", label=""):
        self.trait_type = MagicMock()
        self.trait_type.values = values or []
        self.desc = desc
        self.label = label


def test_add_display_arg_returns_wdict_when_display_false():
    expected_widget = MagicMock()

    @utils.add_display_arg
    def dummy():
        return {"widget": expected_widget, "wdict": {"key": "value"}}

    result = dummy(display=False)
    assert result == {"widget": expected_widget, "wdict": {"key": "value"}}


def test_add_display_arg_displays_widget_in_jupyter():
    @utils.add_display_arg
    def dummy():
        w = MagicMock()
        return {"widget": w, "wdict": {}}

    with patch("IPython.display.display") as mock_display:
        orig_marimo = sys.modules.pop("marimo", None)
        try:
            result = dummy(display=True)
            mock_display.assert_called_once()
            assert result is None
        finally:
            if orig_marimo is not None:
                sys.modules["marimo"] = orig_marimo


def test_add_display_arg_does_not_display_in_marimo():
    expected_widget = MagicMock()

    @utils.add_display_arg
    def dummy():
        return {"widget": expected_widget, "wdict": {"a": 1}}

    fake_marimo = MagicMock()
    with patch("IPython.display.display") as mock_display:
        with patch.dict(sys.modules, {"marimo": fake_marimo}):
            result = dummy(display=True)
            mock_display.assert_not_called()
            assert result == {"widget": expected_widget, "wdict": {"a": 1}}


def test_labelme_creates_labeled_widget():
    inner = _DummyWidget(value=42)
    lw = utils.labelme("My Label", inner)
    assert isinstance(lw, anywidget.AnyWidget)
    assert lw.label == "My Label"
    assert lw.value == 42


def test_labelme_undefined_label():
    from traits.api import Undefined

    inner = _DummyWidget(value="x")
    lw = utils.labelme(Undefined, inner)
    assert lw.label == ""
    assert lw.value == "x"


def test_labelme_sandwich_creates_labeled_widget():
    inner = _DummyWidget(value=3.14)
    lw = utils.labelme_sandwich("Left", inner, "Right")
    assert isinstance(lw, anywidget.AnyWidget)
    assert lw.label1 == "Left"
    assert lw.label2 == "Right"
    assert lw.value == 3.14


def test_get_label_falls_back_to_formatted_name():
    trait = _MockTrait(label="")
    assert utils.get_label(trait, "some_trait") == "Some trait"


def test_get_label_uses_trait_label():
    trait = _MockTrait(label="Custom Label")
    assert utils.get_label(trait, "some_trait") == "Custom Label"


def test_enum2dropdown_creates_dropdown():
    trait = _MockTrait(values=["opt1", "opt2", "opt3"])
    dd = utils.enum2dropdown(trait)
    assert isinstance(dd, anywidget.AnyWidget)
    assert dd.options == ["opt1", "opt2", "opt3"]
    assert dd.value == "opt1"


def test_enum2dropdown_with_description():
    trait = _MockTrait(values=["a", "b"], desc="tooltip text")
    dd = utils.enum2dropdown(trait, description="Choose")
    assert dd.description == "Choose"
    assert dd.description_tooltip == "tooltip text"


def test_float2floattext_creates_widget():
    trait = _MockTrait(desc="float desc")
    w = utils.float2floattext(trait, "my_float")
    assert isinstance(w, anywidget.AnyWidget)
    assert w.label == "my_float"
    assert w.value == 0.0
    assert w.description_tooltip == "float desc"


def test_str2text_creates_widget():
    trait = _MockTrait(desc="str desc")
    w = utils.str2text(trait, "my_str")
    assert isinstance(w, anywidget.AnyWidget)
    assert w.label == "my_str"
    assert w.value == ""
    assert w.description_tooltip == "str desc"


def test_set_title_container_with_set_title():
    container = MagicMock()
    container.set_title = MagicMock()
    utils.set_title_container(container, ["Tab A", "Tab B"])
    container.set_title.assert_any_call(0, "Tab A")
    container.set_title.assert_any_call(1, "Tab B")


def test_set_title_container_fallback_to_titles_attribute():
    container = MagicMock()
    del container.set_title
    utils.set_title_container(container, ["Tab A", "Tab B"])
    assert container.titles == ("Tab A", "Tab B")
