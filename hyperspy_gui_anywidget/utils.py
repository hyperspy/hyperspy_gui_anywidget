# -*- coding: utf-8 -*-
"""Utility functions and base widgets for hyperspy_gui_anywidget.

This module provides small AnyWidget subclasses used as building blocks
throughout the package, plus helper functions for labeling, trait-to-widget
conversion, and the ``add_display_arg`` decorator.
"""

import functools
import sys

import anywidget
import IPython.display
import traitlets
from traits.api import Undefined


class _FloatText(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      const value = model.get("value");
      el.innerHTML = `<input type="number" step="any" value="${value}" style="width:100%;" />`;
      const input = el.querySelector("input");
      input.addEventListener("change", () => {
        model.set("value", parseFloat(input.value));
        model.save_changes();
      });
      model.on("change:value", () => {
        input.value = model.get("value");
      });
    }
    export default { render };
    """
    value = traitlets.Float(0.0).tag(sync=True)
    description_tooltip = traitlets.Unicode("").tag(sync=True)


class _Text(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      const value = model.get("value");
      el.innerHTML = `<input type="text" value="${value}" style="width:100%;" />`;
      const input = el.querySelector("input");
      input.addEventListener("change", () => {
        model.set("value", input.value);
        model.save_changes();
      });
      model.on("change:value", () => {
        input.value = model.get("value");
      });
    }
    export default { render };
    """
    value = traitlets.Unicode("").tag(sync=True)
    description_tooltip = traitlets.Unicode("").tag(sync=True)


class _Dropdown(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      const options = model.get("options");
      const value = model.get("value");
      const desc = model.get("description");
      let html = "";
      if (desc) {
        html += `<label>${desc}</label>`;
      }
      html += `<select style="width:100%;">`;
      for (const opt of options) {
        html += `<option value="${opt}" ${opt === value ? "selected" : ""}>${opt}</option>`;
      }
      html += `</select>`;
      el.innerHTML = html;
      const select = el.querySelector("select");
      select.addEventListener("change", () => {
        model.set("value", select.value);
        model.save_changes();
      });
      model.on("change:value", () => {
        select.value = model.get("value");
      });
    }
    export default { render };
    """
    options = traitlets.List(trait=traitlets.Unicode(), default_value=[]).tag(sync=True)
    value = traitlets.Unicode("").tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)
    description_tooltip = traitlets.Unicode("").tag(sync=True)


class _Labeled(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      const label = model.get("label");
      const value = model.get("value");
      const tooltip = model.get("description_tooltip");
      const inputType = typeof value === "number" ? "number" : "text";
      el.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; width:100%;">
          <span style="white-space:nowrap;">${label}</span>
          <input type="${inputType}" value="${value}" title="${tooltip}" style="flex:1;" />
        </div>
      `;
      const input = el.querySelector("input");
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
    """
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
          <span style="white-space:nowrap;">${label1}</span>
          <input type="${inputType}" value="${value}" title="${tooltip}" style="flex:1;" />
          <span style="white-space:nowrap;">${label2}</span>
        </div>
      `;
      const input = el.querySelector("input");
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
    """
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
    label = (label.replace("_", " ").capitalize()
             if not trait.label else trait.label)
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
        Ignored. Kept for API compatibility.

    Returns
    -------
    _Dropdown or _Text
        A dropdown widget if the trait has enumerated values, otherwise a
        plain text widget.
    """
    values = trait.trait_type.values
    if values is None:
        return _Text(value="", description=description or "")
    widget = _Dropdown(
        options=list(values),
        value=values[0] if values else "",
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
    * In Marimo: the raw ``{"widget": ..., "wdict": ...}`` dictionary is
      returned so Marimo can render it with ``mo.ui.anywidget()``.

    When ``display=False``: the dictionary is always returned unchanged.

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
                return wdict
            IPython.display.display(wdict["widget"])
        else:
            return wdict
    return wrapper


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
