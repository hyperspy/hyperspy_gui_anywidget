# -*- coding: utf-8 -*-
"""Preferences widgets for HyperSpy using anywidget."""

import anywidget
import traitlets
import traits.trait_types
from ipywidgets import Accordion, Tab, VBox
from link_traits import link

try:
    from hyperspy.misc.utils import grouped_editable_traits
except ImportError:
    grouped_editable_traits = None

from hyperspy_gui_anywidget.custom_widgets import CheckboxWidget
from hyperspy_gui_anywidget.utils import (
    _Labeled,
    add_display_arg,
    enum2dropdown,
    float2floattext,
    get_label,
    str2text,
)


class _Checkbox(CheckboxWidget):
    _esm = """
    function render({ model, el }) {
      const value = model.get("value");
      const desc = model.get("description");
      el.innerHTML = `
        <label style="display:flex; align-items:center; gap:8px; cursor:pointer;">
          <input type="checkbox" ${value ? "checked" : ""} />
          <span>${desc}</span>
        </label>
      `;
      const input = el.querySelector("input");
      input.addEventListener("change", () => {
        model.set("value", input.checked);
        model.save_changes();
      });
      model.on("change:value", () => {
        input.checked = model.get("value");
      });
      model.on("change:description", () => {
        el.querySelector("span").textContent = model.get("description");
      });
    }
    export default { render };
    """
    value = traitlets.Bool(False).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)


class _RangeSlider(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      const min = model.get("min");
      const max = model.get("max");
      const value = model.get("value");
      const desc = model.get("description");
      el.innerHTML = `
        <div style="display:flex; flex-direction:column; gap:4px; width:100%;">
          <div style="display:flex; justify-content:space-between;">
            <span>${desc}</span>
            <span>${value}</span>
          </div>
          <input type="range" min="${min}" max="${max}" value="${value}" style="width:100%;" />
        </div>
      `;
      const input = el.querySelector("input");
      const display = el.querySelector("span:last-child");
      input.addEventListener("input", () => {
        display.textContent = input.value;
      });
      input.addEventListener("change", () => {
        model.set("value", parseFloat(input.value));
        model.save_changes();
      });
      model.on("change:value", () => {
        input.value = model.get("value");
        display.textContent = model.get("value");
      });
    }
    export default { render };
    """
    min = traitlets.Float(0.0).tag(sync=True)
    max = traitlets.Float(1.0).tag(sync=True)
    value = traitlets.Float(0.0).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)


def bool2checkbox(trait, label):
    """Convert a boolean trait into a checkbox widget.

    Parameters
    ----------
    trait : traits.api.TraitType
        The trait to convert.
    label : str
        Label text for the widget.

    Returns
    -------
    _Checkbox
        A checkbox widget.
    """
    return _Checkbox(description=label, value=False)


def directory2unicode(trait, label):
    """Convert a directory/file trait into a labeled text widget.

    Parameters
    ----------
    trait : traits.api.TraitType
        The trait to convert.
    label : str
        Label text for the widget.

    Returns
    -------
    _Labeled
        A labeled text widget.
    """
    widget = _Labeled(label=label, value="", description_tooltip=trait.desc or "")
    return widget


def range2floatrangeslider(trait, label):
    """Convert a Range trait into a range slider widget.

    Parameters
    ----------
    trait : traits.api.TraitType
        The trait to convert.
    label : str
        Label text for the widget.

    Returns
    -------
    _RangeSlider
        A range slider widget.
    """
    range_trait = trait.trait_type
    widget = _RangeSlider(min=range_trait._low, max=range_trait._high, value=0.0, description=label)
    return widget


TRAITS2IPYWIDGETS = {
    traits.trait_types.CBool: bool2checkbox,
    traits.trait_types.Bool: bool2checkbox,
    traits.trait_types.CFloat: float2floattext,
    traits.trait_types.Directory: directory2unicode,
    traits.trait_types.File: directory2unicode,
    traits.trait_types.Range: range2floatrangeslider,
    traits.trait_types.Enum: enum2dropdown,
    traits.trait_types.Str: str2text,
}


def _get_widget_for_trait(trait, label):
    """Return the appropriate widget for a given trait.

    Parameters
    ----------
    trait : traits.api.TraitType
        The trait to convert.
    label : str
        Label text for the widget.

    Returns
    -------
    anywidget.AnyWidget
        A widget instance matching the trait type.
    """
    trait_type = type(trait.trait_type)
    widget_func = TRAITS2IPYWIDGETS.get(trait_type)
    if widget_func is None:
        widget_func = str2text
    return widget_func(trait, label)


class _SaveButton(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      const text = model.get("text") || "Save";
      el.innerHTML = `
        <button style="padding:6px 16px; cursor:pointer;">${text}</button>
      `;
      el.querySelector("button").addEventListener("click", () => {
        model.set("clicks", model.get("clicks") + 1);
        model.save_changes();
      });
    }
    export default { render };
    """
    text = traitlets.Unicode("Save").tag(sync=True)
    clicks = traitlets.Int(0).tag(sync=True)


@add_display_arg
def show_preferences_widget(obj, **kwargs):
    """Display the HyperSpy preferences widget.

    Parameters
    ----------
    obj : hyperspy.preferences.Preferences
        The preferences object.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    return _build_preferences_widget(obj, ["General", "GUIs", "Plot"])


@add_display_arg
def show_exspy_preferences_widget(obj, **kwargs):
    """Display the exspy preferences widget.

    Parameters
    ----------
    obj : hyperspy.preferences.Preferences
        The exspy preferences object.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    return _build_preferences_widget(obj, ["EELS", "EDS"])


def _build_preferences_widget(obj, titles):
    ipytabs = {}
    wdict = {}

    for tab in obj.editable_traits():
        tab_obj = getattr(obj, tab)
        tabdict = {}
        wdict["tab_{}".format(tab)] = tabdict
        tabtraits = tab_obj.traits()
        grouped = grouped_editable_traits(tab_obj) if grouped_editable_traits else None

        if grouped is None:
            # hyperspy < 2.5: flat rendering fallback
            ipytab_parts = []
            for trait_name in tab_obj.editable_traits():
                trait = tabtraits[trait_name]
                widget = _get_widget_for_trait(trait, get_label(trait, trait_name))
                ipytab_parts.append(widget)
                tabdict[trait_name] = widget
                link((tab_obj, trait_name), (widget, "value"))
            ipytabs[tab] = {"General": ipytab_parts}
            continue

        tab_groups = {}
        for group_label, trait_names in grouped.items():
            group_widgets = []
            for trait_name in trait_names:
                trait = tabtraits[trait_name]
                widget = _get_widget_for_trait(trait, get_label(trait, trait_name))
                group_widgets.append(widget)
                tabdict[trait_name] = widget
                link((tab_obj, trait_name), (widget, "value"))
            tab_groups[group_label] = group_widgets

        ipytabs[tab] = tab_groups

    save_button = _SaveButton()
    save_button.observe(lambda _: obj.save(), names="clicks")
    wdict["save_button"] = save_button

    import sys

    if "marimo" in sys.modules:
        from hyperspy_gui_anywidget.custom_widgets import (
            FlatContainer,
            _widget_config,
            _wire_flat_sync,
        )

        configs = []
        all_kids = []

        for title in titles:
            configs.append({"type": "tab_start", "title": str(title)})
            tab_groups = ipytabs[title]
            for group_label, group_widgets in tab_groups.items():
                if len(tab_groups) > 1:
                    configs.append({"type": "accordion_start", "titles": [group_label]})
                configs.append({"type": "layout_start", "direction": "column"})
                for widget in group_widgets:
                    configs.append(_widget_config(widget))
                configs.append({"type": "layout_end"})
                if len(tab_groups) > 1:
                    configs.append({"type": "accordion_end"})
                all_kids.extend(group_widgets)
            configs.append({"type": "tab_end"})

        configs.append({"type": "layout_start", "direction": "column"})
        configs.append(_widget_config(save_button))
        configs.append({"type": "layout_end"})
        all_kids.append(save_button)

        container = FlatContainer(_children_config=configs, _layout="vertical")
        _wire_flat_sync(container, all_kids)
    else:
        tab_widgets = []
        for title in titles:
            tab_groups = ipytabs[title]
            if len(tab_groups) > 1:
                accordion_children = [VBox(children=widgets) for widgets in tab_groups.values()]
                accordion = Accordion(children=accordion_children)
                for i, label in enumerate(tab_groups.keys()):
                    accordion.set_title(i, str(label))
                tab_widgets.append(accordion)
            else:
                tab_widgets.append(VBox(children=list(tab_groups.values())[0]))
        tabs_widget = Tab(children=tab_widgets)
        for i, title in enumerate(titles):
            tabs_widget.set_title(i, str(title))
        container = VBox(children=[tabs_widget, save_button])

    return {
        "widget": container,
        "wdict": wdict,
    }
