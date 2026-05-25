"""Microscope parameter widgets for EELS and EDS using anywidget."""

import traitlets
from anywidget.widget import AnyWidget
from link_traits import link
from traits.api import Undefined

from hyperspy_gui_anywidget.custom_widgets import ContainerWidget, FloatTextWidget
from hyperspy_gui_anywidget.utils import add_display_arg, get_label


class ButtonWidget(AnyWidget):
    _esm = """
    function render({ model, el }) {
      const description = model.get("description");
      const tooltip = model.get("tooltip");
      el.innerHTML = `<button title="${tooltip}">${description}</button>`;
      const button = el.querySelector("button");
      button.addEventListener("click", () => {
        model.set("clicks", model.get("clicks") + 1);
        model.save_changes();
      });
    }
    export default { render };
    """
    description = traitlets.Unicode("Button").tag(sync=True)
    tooltip = traitlets.Unicode("").tag(sync=True)
    clicks = traitlets.Int(0).tag(sync=True)


def _set_microscope_parameters(obj, **kwargs):
    """Build a widget for editing microscope parameters.

    Parameters
    ----------
    obj : hyperspy.microscope_parameters.MicroscopeParameters
        The microscope parameters object.
    **kwargs
        Ignored. Kept for API compatibility.

    Returns
    -------
    dict
        ``{"widget": ContainerWidget, "wdict": {...}}``.
    """
    traits = obj.traits()
    widgets = []
    wdict = {}
    for trait_name in obj.editable_traits():
        if trait_name in ("mapping", "signal"):
            continue
        trait = traits[trait_name]
        label = get_label(trait, trait_name)
        value = getattr(obj, trait_name)
        widget = FloatTextWidget(description=label)
        if value is Undefined:
            value = 0.0
        widget.value = value
        link((obj, trait_name), (widget, "value"))
        widgets.append(widget)
        wdict[trait_name] = widget

    store_button = ButtonWidget(
        description="Store",
        tooltip="Store the values in metadata",
    )

    def on_click(change):
        obj.store()

    store_button.observe(on_click, names="clicks")
    wdict["store_button"] = store_button

    container = ContainerWidget(
        children=widgets + [store_button],
        layout="vertical",
    )

    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def eels_microscope_parameter_aw(obj, **kwargs):
    """Build a widget for EELS microscope parameters.

    Parameters
    ----------
    obj : hyperspy.microscope_parameters.MicroscopeParameters
        The EELS microscope parameters object.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    return _set_microscope_parameters(obj=obj, **kwargs)


@add_display_arg
def eds_sem_microscope_parameter_aw(obj, **kwargs):
    """Build a widget for EDS SEM microscope parameters.

    Parameters
    ----------
    obj : hyperspy.microscope_parameters.MicroscopeParameters
        The EDS SEM microscope parameters object.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    return _set_microscope_parameters(obj=obj, **kwargs)


@add_display_arg
def eds_tem_microscope_parameter_aw(obj, **kwargs):
    """Build a widget for EDS TEM microscope parameters.

    Parameters
    ----------
    obj : hyperspy.microscope_parameters.MicroscopeParameters
        The EDS TEM microscope parameters object.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    return _set_microscope_parameters(obj=obj, **kwargs)
