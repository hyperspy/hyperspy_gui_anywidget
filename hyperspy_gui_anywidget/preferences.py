# -*- coding: utf-8 -*-
"""Preferences widgets for HyperSpy using anywidget."""

import anywidget
import traitlets
import traits.trait_types

from link_traits import link
from hyperspy_gui_anywidget.utils import (
    add_display_arg, float2floattext, get_label, str2text,
    enum2dropdown, _Labeled
)


class _Checkbox(anywidget.AnyWidget):
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
    widget = _RangeSlider(
        min=range_trait._low,
        max=range_trait._high,
        value=0.0,
        description=label
    )
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


class _PreferencesTabs(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      const tabs = model.get("tabs");
      const titles = model.get("titles");

      el.innerHTML = `
        <div style="display:flex; flex-direction:column; width:100%;">
          <div class="tab-headers" style="display:flex; border-bottom:1px solid #ccc;"></div>
          <div class="tab-content" style="padding:10px 0;"></div>
        </div>
      `;

      const headersEl = el.querySelector(".tab-headers");
      const contentEl = el.querySelector(".tab-content");

      let activeTab = 0;

      function renderTabs() {
        headersEl.innerHTML = "";
        contentEl.innerHTML = "";
        tabs.forEach((tab, i) => {
          const btn = document.createElement("button");
          btn.textContent = titles[i];
          btn.style.padding = "8px 16px";
          btn.style.border = "none";
          btn.style.background = i === activeTab ? "#e0e0e0" : "transparent";
          btn.style.cursor = "pointer";
          btn.style.borderBottom = i === activeTab ? "2px solid #3366cc" : "none";
          btn.addEventListener("click", () => {
            activeTab = i;
            renderTabs();
          });
          headersEl.appendChild(btn);

          if (i === activeTab && model.widget_manager) {
            model.widget_manager.create_view(tab).then(view => {
              contentEl.innerHTML = "";
              contentEl.appendChild(view.el);
            });
          }
        });
      }

      renderTabs();
    }
    export default { render };
    """
    tabs = traitlets.List().tag(sync=True)
    titles = traitlets.List(trait=traitlets.Unicode()).tag(sync=True)


class _SaveButton(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      const text = model.get("text") || "Save";
      el.innerHTML = `
        <button style="padding:6px 16px; cursor:pointer;">${text}</button>
      `;
      el.querySelector("button").addEventListener("click", () => {
        model.get("on_save")();
      });
    }
    export default { render };
    """
    text = traitlets.Unicode("Save").tag(sync=True)
    on_save = traitlets.Callable().tag(sync=True)


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
        tabdict = {}
        wdict["tab_{}".format(tab)] = tabdict
        ipytab = []
        tabtraits = getattr(obj, tab).traits()

        for trait_name in getattr(obj, tab).editable_traits():
            trait = tabtraits[trait_name]
            widget = _get_widget_for_trait(trait, get_label(trait, trait_name))
            ipytab.append(widget)
            tabdict[trait_name] = widget
            link((getattr(obj, tab), trait_name), (widget, "value"))

        ipytabs[tab] = ipytab

    tabs_widget = _PreferencesTabs(
        tabs=[ipytabs[title] for title in titles],
        titles=titles
    )

    def on_save_click():
        obj.save()

    save_button = _SaveButton(on_save=on_save_click)
    wdict["save_button"] = save_button

    container = _PreferencesContainer(
        tabs_widget=tabs_widget,
        save_button=save_button
    )

    return {
        "widget": container,
        "wdict": wdict,
    }


class _PreferencesContainer(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      const tabsWidget = model.get("tabs_widget");
      const saveButton = model.get("save_button");

      el.style.display = "flex";
      el.style.flexDirection = "column";
      el.style.gap = "10px";

      if (model.widget_manager) {
        Promise.all([
          model.widget_manager.create_view(tabsWidget),
          model.widget_manager.create_view(saveButton)
        ]).then(([tabsView, buttonView]) => {
          el.appendChild(tabsView.el);
          el.appendChild(buttonView.el);
        });
      } else {
        el.innerHTML = "<span>Widget manager not available</span>";
      }
    }
    export default { render };
    """
    tabs_widget = traitlets.Any().tag(sync=True)
    save_button = traitlets.Any().tag(sync=True)