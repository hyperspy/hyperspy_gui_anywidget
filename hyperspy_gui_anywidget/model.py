"""Model, component, and parameter widgets for HyperSpy using anywidget."""

import numpy as np
from link_traits import dlink, link

from hyperspy_gui_anywidget.custom_widgets import (
    ButtonWidget,
    CheckboxWidget,
    ContainerWidget,
    FloatSliderWidget,
    FloatTextWidget,
    LabelWidget,
)
from hyperspy_gui_anywidget.utils import (
    add_display_arg,
    enum2dropdown,
    labelme,
)


def _interactive_slider_bounds(obj, index=None):
    """Compute min, max, and step for an interactive parameter slider.

    Parameters
    ----------
    obj : hyperspy.component.Parameter
        The parameter to compute bounds for.
    index : int, optional
        For tuple-valued parameters, the element index.

    Returns
    -------
    dict
        Dictionary with keys ``"min"``, ``"max"``, and ``"step"``.
    """
    pad = 10.0
    _min, _max, step = None, None, None
    value = obj.value if index is None else obj.value[index]
    if obj.bmin is not None:
        _min = obj.bmin
    if obj.bmax is not None:
        _max = obj.bmax
    if _max is None and _min is not None:
        _max = value + pad
    if _min is None and _max is not None:
        _min = value - pad
    if _min is None and _max is None:
        if obj.component and obj is obj.component._position and obj._axes_manager is not None:
            axis = obj._axes_manager.signal_axes[-1]
            _min = axis.axis.min()
            _max = axis.axis.max()
            step = np.abs(axis.scale)
        else:
            _max = value + pad
            _min = value - pad
    if step is None:
        step = (_max - _min) * 0.001
    return {"min": _min, "max": _max, "step": step}


def _get_value_widget(obj, index=None):
    """Build a slider widget for a single parameter value.

    Parameters
    ----------
    obj : hyperspy.component.Parameter
        The parameter to create a widget for.
    index : int, optional
        For tuple-valued parameters, the element index.

    Returns
    -------
    dict
        ``{"widget": ContainerWidget, "wdict": {...}}``.
    """
    wdict = {}
    widget_bounds = _interactive_slider_bounds(obj, index=index)

    step = widget_bounds.get("step", 1.0)
    if step and step > 0:
        decimals = max(0, -int(np.floor(np.log10(abs(step)))) + 1)
    else:
        decimals = 4

    thismin = FloatTextWidget(value=round(widget_bounds["min"], decimals), description="min")
    thismax = FloatTextWidget(value=round(widget_bounds["max"], decimals), description="max")

    current_value = obj.value if index is None else obj.value[index]
    if index is None:
        current_name = obj.name
    else:
        current_name = "{}".format(index)

    widget = FloatSliderWidget(
        value=current_value,
        min=thismin.value,
        max=thismax.value,
        step=widget_bounds["step"],
        description=current_name,
        readout_format=".2f",
    )

    def on_min_change(change):
        if widget.max > change["new"]:
            widget.min = change["new"]
            widget.step = np.abs(widget.max - widget.min) * 0.001

    def on_max_change(change):
        if widget.min < change["new"]:
            widget.max = change["new"]
            widget.step = np.abs(widget.max - widget.min) * 0.001

    thismin.observe(on_min_change, names="value")
    thismax.observe(on_max_change, names="value")

    thismin._link = dlink((obj, "bmin"), (thismin, "value"))
    thismax._link = dlink((obj, "bmax"), (thismax, "value"))

    if index is not None:

        def _interactive_tuple_update(change):
            obj.value = obj.value[:index] + (change["new"],) + obj.value[index + 1 :]

        widget.observe(_interactive_tuple_update, names="value")
    else:
        link((obj, "value"), (widget, "value"))

    container = ContainerWidget(children=[thismin, widget, thismax], layout="horizontal")
    wdict["value"] = widget
    wdict["min"] = thismin
    wdict["max"] = thismax
    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def get_parameter_widget(obj, **kwargs):
    """Build a widget for a HyperSpy component parameter.

    Parameters
    ----------
    obj : hyperspy.component.Parameter
        The parameter to build a widget for.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    if obj._number_of_elements == 1:
        return _get_value_widget(obj)
    else:
        wdict = {}
        par_widgets = []
        for i in range(obj._number_of_elements):
            thiswd = _get_value_widget(obj=obj, index=i)
            par_widgets.append(thiswd["widget"])
            wdict["element{}".format(i)] = thiswd["wdict"]

        update = ButtonWidget(
            description="Update",
            tooltip="Unlike most other widgets, the multivalue parameter widgets do not update automatically when the value of the changes by other means. Use this button to update the values manually",
        )

        def on_update_clicked(change):
            for i, value in enumerate(obj.value):
                element_wd = wdict["element{}".format(i)]
                minwidget = element_wd["min"]
                vwidget = element_wd["value"]
                maxwidget = element_wd["max"]
                if value < vwidget.min:
                    minwidget.value = value
                elif value > vwidget.max:
                    maxwidget.value = value
                vwidget.value = value

        update.observe(on_update_clicked, names="clicks")
        wdict["update_button"] = update

        container = ContainerWidget(
            children=[update] + par_widgets, layout="accordion", titles=[obj.name]
        )

    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def get_component_widget(obj, **kwargs):
    """Build a widget for a HyperSpy model component.

    Parameters
    ----------
    obj : hyperspy.component.Component
        The component to build a widget for.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    wdict = {}
    active = CheckboxWidget(description="active", value=obj.active)
    wdict["active"] = active
    link((obj, "active"), (active, "value"))

    children = [active]
    for parameter in obj.parameters:
        pardict = parameter.gui(toolkit="anywidget", display=False)["anywidget"]
        wdict["parameter_{}".format(parameter.name)] = pardict["wdict"]
        children.append(pardict["widget"])

    container = ContainerWidget(children=children, layout="vertical")

    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def get_model_widget(obj, **kwargs):
    """Build a widget for a HyperSpy model.

    Parameters
    ----------
    obj : hyperspy.model.BaseModel
        The model to build a widget for.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    children = []
    wdict = {}
    for component in obj:
        idict = component.gui(display=False, toolkit="anywidget")["anywidget"]
        children.append(idict["widget"])
        wdict["component_{}".format(component.name)] = idict["wdict"]

    container = ContainerWidget(
        children=children, layout="accordion", titles=[comp.name for comp in obj]
    )
    return {"widget": container, "wdict": wdict}


@add_display_arg
def get_eelscl_widget(obj, **kwargs):
    """Build a widget for an EELS core-loss edge component.

    Parameters
    ----------
    obj : hyperspy.component.Component
        The EELS core-loss edge component.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    wdict = {}
    active = CheckboxWidget(description="active", value=obj.active)
    fine_structure = CheckboxWidget(description="Fine structure", value=obj.fine_structure_active)
    fs_smoothing = FloatSliderWidget(
        description="Fine structure smoothing",
        min=0,
        max=1,
        step=0.001,
        value=obj.fine_structure_smoothing,
    )

    link((obj, "active"), (active, "value"))
    link((obj, "fine_structure_active"), (fine_structure, "value"))
    link((obj, "fine_structure_smoothing"), (fs_smoothing, "value"))

    children = [active, fine_structure, fs_smoothing]
    wdict["active"] = active
    wdict["fine_structure"] = fine_structure
    wdict["fs_smoothing"] = fs_smoothing

    for parameter in [obj.intensity, obj.effective_angle, obj.onset_energy]:
        pdict = parameter.gui(toolkit="anywidget", display=False)["anywidget"]
        children.append(pdict["widget"])
        wdict["parameter_{}".format(parameter.name)] = pdict["wdict"]

    container = ContainerWidget(children=children, layout="vertical")
    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def get_scalable_fixed_patter_widget(obj, **kwargs):
    """Build a widget for a ScalableFixedPattern component.

    Parameters
    ----------
    obj : hyperspy.component.Component
        The ScalableFixedPattern component.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    wdict = {}
    active = CheckboxWidget(description="active", value=obj.active)
    wdict["active"] = active
    link((obj, "active"), (active, "value"))

    interpolate = CheckboxWidget(description="interpolate", value=obj.interpolate)
    wdict["interpolate"] = interpolate
    link((obj, "interpolate"), (interpolate, "value"))

    children = [active, interpolate]
    for parameter in obj.parameters:
        pardict = parameter.gui(toolkit="anywidget", display=False)["anywidget"]
        wdict["parameter_{}".format(parameter.name)] = pardict["wdict"]
        children.append(pardict["widget"])

    container = ContainerWidget(children=children, layout="vertical")
    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def fit_component_aw(obj, **kwargs):
    """Build a widget for fitting a single component in a selected range.

    Parameters
    ----------
    obj : hyperspy.model.ComponentFit
        The component fit tool instance.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    wdict = {}
    only_current = CheckboxWidget(description="Only current")
    iterpath = enum2dropdown(obj.traits()["iterpath"])

    def disable_iterpath(change):
        iterpath.disabled = change.new

    only_current.observe(disable_iterpath, names="value")

    wdict["only_current"] = only_current
    wdict["iterpath"] = iterpath

    help_text = LabelWidget(
        value="Click on the signal figure and drag to the right to select a range. Press `Fit` to fit the component in that range. If only current is unchecked the fit is performed in the whole dataset."
    )
    wdict["help_text"] = help_text

    help_container = ContainerWidget(children=[help_text], layout="accordion", titles=["Help"])

    link((obj, "only_current"), (only_current, "value"))
    link((obj, "iterpath"), (iterpath, "value"))

    fit = ButtonWidget(description="Fit", tooltip="Fit in the selected signal range")
    close = ButtonWidget(
        description="Close", tooltip="Close widget and remove span selector from the signal figure."
    )

    wdict["close_button"] = close
    wdict["fit_button"] = fit

    def on_fit_clicked(change):
        obj._fit_fired()

    fit.observe(on_fit_clicked, names="clicks")

    box = ContainerWidget(
        children=[
            only_current,
            labelme("Iterpath", iterpath),
            help_container,
            ContainerWidget(children=[fit, close], layout="horizontal"),
        ],
        layout="vertical",
    )

    def on_close_clicked(change):
        obj.span_selector_switch(False)
        if hasattr(box, "close"):
            box.close()

    close.observe(on_close_clicked, names="clicks")

    return {
        "widget": box,
        "wdict": wdict,
    }
