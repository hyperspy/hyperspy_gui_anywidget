# -*- coding: utf-8 -*-
"""Utility functions and base widgets for hyperspy_gui_anywidget.

This module provides small AnyWidget subclasses used as building blocks
throughout the package, plus helper functions for labeling, trait-to-widget
conversion, and the ``add_display_arg`` decorator.
"""

import contextvars
import functools
import sys
from threading import Timer, local

import anywidget
import IPython.display
import traitlets
from ipywidgets import HBox, VBox
from traits.api import Undefined

from hyperspy_gui_anywidget.custom_widgets import (
    _INPUT_FOCUS_JS,
    _INPUT_STYLE_CSS,
    _SELECT_FOCUS_JS,
    _SELECT_STYLE_CSS,
)


class _FloatText(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      const value = model.get("value");
      el.innerHTML = `<input type="number" step="any" value="${value}" style="__INPUT_STYLE__ width:160px; max-width:160px;" />`;
      const input = el.querySelector("input");
__INPUT_FOCUS_JS__
      input.addEventListener("change", () => {
        model.set("value", parseFloat(input.value));
        model.save_changes();
      });
      model.on("change:value", () => {
        input.value = model.get("value");
      });
    }
    export default { render };
    """.replace("__INPUT_STYLE__", _INPUT_STYLE_CSS).replace("__INPUT_FOCUS_JS__", _INPUT_FOCUS_JS)
    value = traitlets.Float(0.0).tag(sync=True)
    description_tooltip = traitlets.Unicode("").tag(sync=True)


class _Text(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      const value = model.get("value");
      const description = model.get("description");
      let html = "";
      if (description) {
        html += `<label style="margin-right: 4px;">${description}</label>`;
      }
      html += `<input type="text" value="${value}" style="__INPUT_STYLE__ width:160px; max-width:160px;" />`;
      el.innerHTML = html;
      const input = el.querySelector("input");
__INPUT_FOCUS_JS__
      input.addEventListener("change", () => {
        model.set("value", input.value);
        model.save_changes();
      });
      model.on("change:value", () => {
        input.value = model.get("value");
      });
    }
    export default { render };
    """.replace("__INPUT_STYLE__", _INPUT_STYLE_CSS).replace("__INPUT_FOCUS_JS__", _INPUT_FOCUS_JS)
    value = traitlets.Unicode("").tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)
    description_tooltip = traitlets.Unicode("").tag(sync=True)


class _Dropdown(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      const options = model.get("options");
      const value = model.get("value");
      const desc = model.get("description");
      const selectWidth = model.get("select_width");
      let html = "";
      if (desc) {
        html += `<label style="margin-right: 4px;">${desc}</label>`;
      }
      html += `<select style="__SELECT_STYLE__ width:${selectWidth}; max-width:${selectWidth};">`;
      for (const opt of options) {
        html += `<option value="${opt}" ${opt === value ? "selected" : ""}>${opt}</option>`;
      }
      html += `</select>`;
      el.innerHTML = html;
      const select = el.querySelector("select");
__SELECT_FOCUS_JS__
      select.addEventListener("change", () => {
        model.set("value", select.value);
        model.save_changes();
      });
      model.on("change:value", () => {
        select.value = model.get("value");
      });
    }
    export default { render };
    """.replace("__SELECT_STYLE__", _SELECT_STYLE_CSS).replace(
        "__SELECT_FOCUS_JS__", _SELECT_FOCUS_JS
    )
    options = traitlets.List(trait=traitlets.Unicode(), default_value=[]).tag(sync=True)
    value = traitlets.Unicode("").tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)
    description_tooltip = traitlets.Unicode("").tag(sync=True)
    # Field width rather than fixed CSS so compact toolbars can shrink
    # single rows without changing every widget in the package.
    select_width = traitlets.Unicode("160px").tag(sync=True)


class _Labeled(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      const label = model.get("label");
      const value = model.get("value");
      const tooltip = model.get("description_tooltip");
      const inputType = typeof value === "number" ? "number" : "text";
      el.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; width:100%;">
          <span style="white-space:nowrap; min-width:120px; text-align:right; margin-right:5px;">${label}</span>
          <input type="${inputType}" value="${value}" title="${tooltip}" style="__INPUT_STYLE__ flex:0 0 160px; width:160px; max-width:160px;" />
        </div>
      `;
      const input = el.querySelector("input");
__INPUT_FOCUS_JS__
      input.addEventListener("change", () => {
        const newVal = inputType === "number" ? parseFloat(input.value) : input.value;
        model.set("value", newVal);
        model.save_changes();
      });
      model.on("change:value", () => {
        input.value = model.get("value");
      });
    }
    export default { render };
    """.replace("__INPUT_STYLE__", _INPUT_STYLE_CSS).replace("__INPUT_FOCUS_JS__", _INPUT_FOCUS_JS)
    label = traitlets.Unicode("").tag(sync=True)
    value = traitlets.Any("").tag(sync=True)
    description_tooltip = traitlets.Unicode("").tag(sync=True)


class _LabeledSandwich(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      const label1 = model.get("label1");
      const label2 = model.get("label2");
      const value = model.get("value");
      const tooltip = model.get("description_tooltip");
      const inputType = typeof value === "number" ? "number" : "text";
      el.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; width:100%;">
           <span style="white-space:nowrap; min-width:120px; text-align:right; margin-right:5px;">${label1}</span>
           <input type="${inputType}" value="${value}" title="${tooltip}" style="__INPUT_STYLE__ flex:0 0 160px; width:160px; max-width:160px;" />
           <span style="white-space:nowrap; min-width:120px; text-align:left; margin-left:5px;">${label2}</span>
        </div>
      `;
      const input = el.querySelector("input");
__INPUT_FOCUS_JS__
      input.addEventListener("change", () => {
        const newVal = inputType === "number" ? parseFloat(input.value) : input.value;
        model.set("value", newVal);
        model.save_changes();
      });
      model.on("change:value", () => {
        input.value = model.get("value");
      });
    }
    export default { render };
    """.replace("__INPUT_STYLE__", _INPUT_STYLE_CSS).replace("__INPUT_FOCUS_JS__", _INPUT_FOCUS_JS)
    label1 = traitlets.Unicode("").tag(sync=True)
    label2 = traitlets.Unicode("").tag(sync=True)
    value = traitlets.Any("").tag(sync=True)
    description_tooltip = traitlets.Unicode("").tag(sync=True)


def labelme(label, widget):
    """Wrap a widget with a left-side label using ``_Labeled``.

    Parameters
    ----------
    label : str
        Text to display on the left of the widget.
    widget : anywidget.AnyWidget
        Widget instance whose ``value`` and ``description_tooltip`` are
        copied into the wrapper.

    Returns
    -------
    _Labeled
        A labeled AnyWidget instance.
    """
    if label is Undefined:
        label = ""
    if not isinstance(label, str):
        label = str(label)
    value = getattr(widget, "value", "")
    tooltip = getattr(widget, "description_tooltip", "")
    return _Labeled(label=label, value=value, description_tooltip=tooltip)


def labelme_sandwich(label1, widget, label2):
    """Wrap a widget with labels on both sides using ``_LabeledSandwich``.

    Parameters
    ----------
    label1 : str
        Text to display on the left of the widget.
    widget : anywidget.AnyWidget
        Widget instance whose ``value`` and ``description_tooltip`` are
        copied into the wrapper.
    label2 : str
        Text to display on the right of the widget.

    Returns
    -------
    _LabeledSandwich
        A sandwich-labeled AnyWidget instance.
    """
    if label1 is Undefined:
        label1 = ""
    if label2 is Undefined:
        label2 = ""
    if not isinstance(label1, str):
        label1 = str(label1)
    if not isinstance(label2, str):
        label2 = str(label2)
    value = getattr(widget, "value", "")
    tooltip = getattr(widget, "description_tooltip", "")
    return _LabeledSandwich(label1=label1, label2=label2, value=value, description_tooltip=tooltip)


def get_label(trait, label):
    """Return a human-readable label for a trait.

    If the trait defines a ``label``, it is used. Otherwise the supplied
    ``label`` is formatted (underscores become spaces, first letter
    capitalised).

    Parameters
    ----------
    trait : traits.api.TraitType
        The trait object to inspect.
    label : str
        Fallback label text.

    Returns
    -------
    str
        Formatted label string.
    """
    label = label.replace("_", " ").capitalize() if not trait.label else trait.label
    return label


def enum2dropdown(trait, description=None, **kwargs):
    """Convert an Enum trait into a ``_Dropdown`` widget.

    Parameters
    ----------
    trait : traits.api.TraitType
        Trait whose ``trait_type.values`` defines the dropdown options.
    description : str, optional
        Description text for the widget.
    **kwargs
        Forwarded to the underlying ``_Dropdown`` when the trait has
        enumerated values (for example ``select_width``); ignored for
        non-enum traits, which return a plain text widget.

    Returns
    -------
    _Dropdown or _Text
        A dropdown widget if the trait has enumerated values, otherwise a
        plain text widget.
    """
    values = trait.trait_type.values
    if values is None:
        widget = _Text(value="", description=description or "")
        if description is not None:
            widget.description_tooltip = trait.desc if trait.desc else ""
        return widget
    widget = _Dropdown(
        options=list(values),
        value=values[0] if values else "",
        **kwargs,
    )
    if description is not None:
        description_tooltip = trait.desc if trait.desc else ""
        widget.description = description
        widget.description_tooltip = description_tooltip
    return widget


def float2floattext(trait, label):
    """Convert a float trait into a labeled ``_FloatText`` widget.

    Parameters
    ----------
    trait : traits.api.TraitType
        Trait to convert.
    label : str
        Label text for the widget.

    Returns
    -------
    _Labeled
        A labeled float text widget.
    """
    description_tooltip = trait.desc if trait.desc else ""
    widget = _FloatText()
    widget.description_tooltip = description_tooltip
    return labelme(widget=widget, label=label)


def str2text(trait, label):
    """Convert a string trait into a labeled ``_Text`` widget.

    Parameters
    ----------
    trait : traits.api.TraitType
        Trait to convert.
    label : str
        Label text for the widget.

    Returns
    -------
    _Labeled
        A labeled text widget.
    """
    description = trait.desc if trait.desc else ""
    widget = _Text()
    widget.description_tooltip = description
    return labelme(widget=widget, label=label)


def add_display_arg(f):
    """Decorator that adds a ``display`` keyword argument to a widget function.

    When ``display=True`` (the default):

    * In Jupyter: the root widget is shown via ``IPython.display.display``
      and ``None`` is returned.
    * In Marimo: the widget is displayed via ``IPython.display.display``. If the
      root widget is a ``VBox``/``HBox``, it is flattened to a ``FlatContainer``
      first so Marimo can render it correctly.

    When ``display=False``: the raw ``{"widget": ..., "wdict": ...}`` dictionary
    is always returned unchanged.

    Parameters
    ----------
    f : callable
        Widget builder function that returns a dict with ``"widget"`` and
        ``"wdict"`` keys.

    Returns
    -------
    callable
        Wrapped function with an extra ``display`` keyword argument.
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        display = kwargs.pop("display", True)
        wdict = f(*args, **kwargs)
        if display:
            if "marimo" in sys.modules:
                widget = wdict["widget"]
                if isinstance(widget, (VBox, HBox)):
                    from hyperspy_gui_anywidget.custom_widgets import _make_flat_container

                    widget = _make_flat_container(
                        widget.children, "column" if isinstance(widget, VBox) else "row"
                    )
                IPython.display.display(widget)
            else:
                IPython.display.display(wdict["widget"])
        else:
            return wdict

    return wrapper


def _snapshot_marimo_context():
    """Capture marimo's runtime context for use on another thread.

    marimo stores its runtime context in a ``threading.local`` rather than in
    a ``contextvar``, so it is not carried into ``threading.Timer`` threads by
    ``contextvars.copy_context()``.  Without the context, marimo's
    ``broadcast_notification`` silently drops anywidget model updates
    (``ModelLifecycleNotification``), which breaks widget state sync from
    debounced callbacks: the X-ray lines table rebuild runs in the timer
    thread and its ``_children_config`` update never reaches the frontend.

    Returns ``(context, thread_local)`` when running inside a marimo kernel
    with an initialized context, otherwise ``None``.  Import failures of the
    marimo internals are tolerated (returns ``None``) so this stays a no-op
    against future marimo refactors and non-marimo environments.
    """
    if "marimo" not in sys.modules:
        return None
    try:
        from marimo._runtime.context import safe_get_context
        from marimo._runtime.context.types import _THREAD_LOCAL_CONTEXT
    except ImportError:
        return None
    context = safe_get_context()
    if context is None:
        return None
    return context, _THREAD_LOCAL_CONTEXT


def _restore_marimo_context(snapshot):
    """Re-install a context captured by ``_snapshot_marimo_context``.

    Only initializes the thread-local when it is unset so a thread that
    already owns a context (e.g. the main kernel thread) is never
    overwritten.
    """
    if snapshot is None:
        return
    context, thread_local = snapshot
    if thread_local.runtime_context is None:
        thread_local.runtime_context = context


_MARIMO_DEBOUNCE_OWNER_CELL = local()
_marimo_lifecycle_patch_installed = False


def _current_marimo_cell_id():
    """Return the id of the marimo cell running on this thread, if any."""
    if "marimo" not in sys.modules:
        return None
    try:
        from marimo._runtime.context import safe_get_context
    except ImportError:
        return None
    context = safe_get_context()
    if context is None:
        return None
    return getattr(context, "cell_id", None)


def _install_marimo_off_cell_widget_fix():
    """Let marimo resolve widget lifecycle items created off the cell thread.

    marimo (at least up to 0.25.1) makes ``CellLifecycleRegistry.add`` a
    silent no-op when a runtime context exists but no cell is running
    (``ctx.cell_id is None``): the item is neither created nor registered,
    yet callers such as ``marimo._output.data`` dereference
    ``item.virtual_file`` immediately afterwards. Constructing any
    anywidget under marimo stores its inline ESM as exactly such a virtual
    file (``EsmSpec.from_esm``), so building widgets from a debounced
    callback — which runs in a ``threading.Timer`` with a restored context
    but no running cell — leaves the item uncreated and the next
    dereference raises ``AssertionError`` (``assert self._virtual_file is
    not None``). The X-ray lines table hits this on every rebuild because
    each new row constructs widgets.

    The patch preserves upstream behaviour for running cells. Off-cell it
    creates the item against the real context (so virtual files register
    and serve normally) and injects it into the marimo cell that owns the
    debounced GUI — recorded in ``_MARIMO_DEBOUNCE_OWNER_CELL`` by
    ``debounce`` — so a re-run of that cell still disposes the items.
    Remove this once marimo handles the no-running-cell case itself.
    """
    # Importing marimo here would flip every "marimo" in sys.modules check
    # in the package and degrade Jupyter sessions to the flat path, so only
    # act when marimo is already active.
    if "marimo" not in sys.modules:
        return
    global _marimo_lifecycle_patch_installed
    if _marimo_lifecycle_patch_installed:
        return
    try:
        from marimo._runtime.cell_lifecycle_registry import CellLifecycleRegistry
    except ImportError:
        return
    _marimo_lifecycle_patch_installed = True

    def add(self, item):
        from marimo._runtime.context import get_context

        ctx = get_context()
        if ctx.cell_id is None:
            owner = getattr(_MARIMO_DEBOUNCE_OWNER_CELL, "cell_id", None)
            item.create(ctx)
            if owner is not None:
                return self.inject(owner, item)
            return
        item.create(ctx)
        return self.inject(ctx.cell_id, item)

    CellLifecycleRegistry.add = add


def debounce(wait):
    """Postpone a function's execution until after `wait` seconds.

    The decorated function is postponed until after `wait` seconds have
    elapsed since the last time it was invoked, which avoids running it
    (and its side effects) repeatedly while a trait changes rapidly.

    Adapted from https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Events.html#debouncing

    Parameters
    ----------
    wait : float
        The debounce interval in seconds.

    Returns
    -------
    callable
        A decorator that wraps a function with the debouncing behavior.
    """

    def decorator(fn):
        timer = None
        owner_cell_id = None

        def debounced(*args, **kwargs):
            nonlocal timer, owner_cell_id

            def call_it():
                # Restore the marimo thread-local first: the callback
                # typically broadcasts widget state, which marimo only
                # delivers when the calling thread has a runtime context.
                _restore_marimo_context(marimo_context)
                # Publishing the owning cell lets the patched
                # CellLifecycleRegistry.add attach items built here to
                # that cell, so they are still disposed on its re-run.
                _MARIMO_DEBOUNCE_OWNER_CELL.cell_id = owner_cell_id
                try:
                    fn(*args, **kwargs)
                finally:
                    _MARIMO_DEBOUNCE_OWNER_CELL.cell_id = None

            if timer is not None:
                timer.cancel()
            # Capture the cell that owns this debounced GUI while it is
            # still running; widgets constructed later in the timer thread
            # inherit it as their disposal owner (marimo cannot see one
            # there because no cell is executing).
            cell_id = _current_marimo_cell_id()
            if cell_id is not None:
                owner_cell_id = cell_id
            _install_marimo_off_cell_widget_fix()
            # Capture the contextvars context at call time and run the
            # callback inside it.  Without this, callbacks scheduled from
            # a Jupyter kernel crash when they create ipywidget comms:
            # ipykernel resolves the current cell through contextvars
            # that only exist in the cell execution context.
            context = contextvars.copy_context()
            marimo_context = _snapshot_marimo_context()
            timer = Timer(wait, context.run, (call_it,))
            timer.start()

        return debounced

    return decorator


def set_title_container(container, titles):
    """Set titles on a container widget.

    Tries ``container.set_title(index, title)`` first, and falls back to
    setting ``container.titles`` as a tuple.

    Parameters
    ----------
    container : anywidget.AnyWidget
        Container widget that supports titles.
    titles : list of str
        Titles to assign to each child.
    """
    try:
        for index, title in enumerate(titles):
            container.set_title(index, title)
    except AttributeError:
        container.titles = tuple(titles)
