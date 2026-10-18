# -*- coding: utf-8 -*-

import contextvars
import sys
import time
import types
from unittest.mock import MagicMock, patch

import anywidget
import pytest
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


def test_add_display_arg_displays_in_marimo():
    expected_widget = MagicMock()

    @utils.add_display_arg
    def dummy():
        return {"widget": expected_widget, "wdict": {"a": 1}}

    fake_marimo = MagicMock()
    with patch("IPython.display.display") as mock_display:
        with patch.dict(sys.modules, {"marimo": fake_marimo}):
            result = dummy(display=True)
            mock_display.assert_called_once_with(expected_widget)
            assert result is None


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


def test_enum2dropdown_falls_back_to_text_widget():
    trait = _MockTrait(values=None, desc="free form")
    widget = utils.enum2dropdown(trait, description="Custom")
    assert widget.description == "Custom"
    assert widget.description_tooltip == "free form"
    assert widget.value == ""


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


def test_debounce_cancels_intermediate_calls():
    calls = []

    @utils.debounce(0.02)
    def fn(value):
        calls.append(value)

    fn(1)
    time.sleep(0.2)
    fn(2)
    fn(3)
    fn(4)
    fn(5)
    time.sleep(0.5)
    assert calls == [1, 5]
    calls.clear()
    fn(10)
    fn(11)
    fn(12)
    time.sleep(0.5)
    assert calls == [12]


def test_debounce_waits_for_last_invocation():
    calls = []

    @utils.debounce(0.5)
    def fn(value):
        calls.append(value)

    fn(1)
    time.sleep(0.2)
    assert calls == []
    time.sleep(0.6)
    assert calls == [1]


def test_debounce_runs_with_context_captured_at_call_time():
    var = contextvars.ContextVar("test_var")
    calls = []

    @utils.debounce(0.1)
    def fn():
        calls.append(var.get())

    var.set(1)
    fn()
    var.set(2)
    time.sleep(0.3)
    assert calls == [1]


def test_marimo_off_cell_lifecycle_fix_resolves_items_without_running_cell():
    """marimo's CellLifecycleRegistry.add silently strands lifecycle items
    when a context exists but no cell is running (e.g. widget construction
    from a debounce Timer thread), which later raises
    ``assert self._virtual_file is not None`` in marimo's virtual_file.py.
    The package patch must create such items eagerly and inject them into
    the debounce owner cell so they are still disposed."""
    pytest.importorskip("marimo")
    from marimo._runtime.cell_lifecycle_registry import CellLifecycleRegistry

    class FakeItem:
        def __init__(self):
            self.created_with = []

        def create(self, context):
            self.created_with.append(context)

        def dispose(self, context, deletion):
            return True

    off_cell_ctx = types.SimpleNamespace(cell_id=None)
    running_ctx = types.SimpleNamespace(cell_id="cell-running")
    registry = CellLifecycleRegistry()

    utils._install_marimo_off_cell_widget_fix()

    no_owner = FakeItem()
    with patch("marimo._runtime.context.get_context", return_value=off_cell_ctx):
        registry.add(no_owner)
    # Created (so it is never dereferenced uncreated) but attached to no
    # cell because no debounce owner is published on this thread.
    assert no_owner.created_with == [off_cell_ctx]
    assert registry.registry == {}

    owned = FakeItem()
    utils._MARIMO_DEBOUNCE_OWNER_CELL.cell_id = "cell-owner"
    try:
        with patch("marimo._runtime.context.get_context", return_value=off_cell_ctx):
            registry.add(owned)
    finally:
        utils._MARIMO_DEBOUNCE_OWNER_CELL.cell_id = None
    # Injected into the owning cell so a re-run of that cell disposes it.
    assert owned.created_with == [off_cell_ctx]
    assert registry.registry["cell-owner"] == {owned}

    on_cell = FakeItem()
    with patch("marimo._runtime.context.get_context", return_value=running_ctx):
        registry.add(on_cell)
    assert on_cell.created_with == [running_ctx]
    assert registry.registry["cell-running"] == {on_cell}

    # Installing twice must not wrap the patch twice (one create per add).
    utils._install_marimo_off_cell_widget_fix()
    again = FakeItem()
    with patch("marimo._runtime.context.get_context", return_value=running_ctx):
        registry.add(again)
    assert again.created_with == [running_ctx]


def test_debounce_propagates_marimo_context_to_timer_thread(monkeypatch):
    """Widget state broadcasts from a debounced callback must reach the
    marimo frontend, which requires marimo's thread-local runtime context to
    be re-installed on the ``threading.Timer`` thread (contextvars alone do
    not carry it)."""
    # The package detects marimo via sys.modules, so the real import done
    # here must not leak into other tests.
    marimo_modules_before = {k for k in sys.modules if k.partition(".")[0] == "marimo"}
    try:
        pytest.importorskip("marimo")
        import marimo._runtime.context as context_mod
        import marimo._runtime.context.types as context_types
        from marimo._runtime.context import ContextNotInitializedError, get_context

        sentinel = object()
        monkeypatch.setattr(context_mod, "safe_get_context", lambda: sentinel)
        monkeypatch.setattr(
            context_types,
            "_THREAD_LOCAL_CONTEXT",
            context_types._ThreadLocalContext(),
        )

        seen = []

        @utils.debounce(0.05)
        def fn():
            try:
                seen.append(get_context())
            except ContextNotInitializedError:
                seen.append("no-context")

        fn()
        time.sleep(0.4)
        assert seen == [sentinel]
    finally:
        for key in [
            k
            for k in sys.modules
            if k.partition(".")[0] == "marimo" and k not in marimo_modules_before
        ]:
            del sys.modules[key]


def test_set_title_container_fallback_to_titles_attribute():
    container = MagicMock()
    del container.set_title
    utils.set_title_container(container, ["Tab A", "Tab B"])
    assert container.titles == ("Tab A", "Tab B")
