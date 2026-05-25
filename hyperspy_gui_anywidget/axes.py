"""Axis and navigation slider widgets for HyperSpy using anywidget."""

from link_traits import link

from hyperspy_gui_anywidget.custom_widgets import (
    BoundedFloatTextWidget,
    CheckboxWidget,
    ContainerWidget,
    FloatSliderWidget,
    FloatTextWidget,
    IntSliderWidget,
    IntTextWidget,
    LabelWidget,
    TextWidget,
)
from hyperspy_gui_anywidget.utils import add_display_arg


@add_display_arg
def aw_navigation_sliders(obj, **kwargs):
    """Display navigation sliders for an AxesManager.

    Parameters
    ----------
    obj : hyperspy.axes.AxesManager
        Axes manager containing navigation axes.
    **kwargs
        Passed to ``get_aw_navigation_sliders``.

    Returns
    -------
    dict or None
        Result of ``get_aw_navigation_sliders`` with ``display`` handling.
    """
    return get_aw_navigation_sliders(obj, **kwargs)


def get_aw_navigation_sliders(obj, in_accordion=False, random_position_button=False, **kwargs):
    continuous_update = CheckboxWidget(value=True, description="Continuous update")
    wdict = {}
    wdict["continuous_update"] = continuous_update
    widgets = []
    for i, axis in enumerate(obj):
        axis_dict = {}
        wdict["axis{}".format(i)] = axis_dict
        iwidget = IntSliderWidget(min=0, max=axis.size - 1, description="index")
        link((continuous_update, "value"), (iwidget, "continuous_update"))
        link((axis, "index"), (iwidget, "value"))
        if hasattr(axis, "scale"):
            vwidget = BoundedFloatTextWidget(
                min=axis.low_value, max=axis.high_value, step=axis.scale, description="value"
            )
        else:
            vwidget = BoundedFloatTextWidget(
                min=0, max=axis.size - 1, disabled=True, description="value"
            )
        link((continuous_update, "value"), (vwidget, "continuous_update"))
        link((axis, "value"), (vwidget, "value"))
        link((axis, "high_value"), (vwidget, "max"))
        link((axis, "low_value"), (vwidget, "min"))
        if hasattr(axis, "scale"):
            link((axis, "scale"), (vwidget, "step"))
        name = LabelWidget(value=str(axis.name))
        units = LabelWidget(value=str(axis.units) if axis.units else "")
        link((axis, "name"), (name, "value"))
        link((axis, "units"), (units, "value"))
        bothw = ContainerWidget(children=[name, iwidget, vwidget, units], layout="horizontal")
        widgets.append(bothw)
        axis_dict["value"] = vwidget
        axis_dict["index"] = iwidget
        axis_dict["units"] = units

    widgets.append(continuous_update)
    box = ContainerWidget(children=widgets, layout="vertical")
    return {"widget": box, "wdict": wdict}


@add_display_arg
def _get_axis_widgets(obj):
    """Build widgets for a single DataAxis.

    Parameters
    ----------
    obj : hyperspy.axes.DataAxis
        The axis to build widgets for.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    widgets = []
    wd = {}
    name = TextWidget(description="Name")
    widgets.append(name)
    link((obj, "name"), (name, "value"))
    wd["name"] = name

    size = IntTextWidget(description="Size", disabled=True)
    widgets.append(size)
    link((obj, "size"), (size, "value"))
    wd["size"] = size

    index_in_array = IntTextWidget(description="Index in array", disabled=True)
    widgets.append(index_in_array)
    link((obj, "index_in_array"), (index_in_array, "value"))
    wd["index_in_array"] = index_in_array
    if obj.navigate:
        index = IntSliderWidget(min=0, max=obj.size - 1, description="Index")
        widgets.append(index)
        link((obj, "index"), (index, "value"))
        wd["index"] = index

        value = FloatSliderWidget(min=obj.low_value, max=obj.high_value, description="Value")
        wd["value"] = value
        widgets.append(value)
        link((obj, "value"), (value, "value"))
        link((obj, "high_value"), (value, "max"))
        link((obj, "low_value"), (value, "min"))
        if hasattr(obj, "scale"):
            link((obj, "scale"), (value, "step"))

    units = TextWidget(description="Units")
    widgets.append(units)
    link((obj, "units"), (units, "value"))
    wd["units"] = units

    if hasattr(obj, "scale"):
        scale = FloatTextWidget(description="Scale")
        widgets.append(scale)
        link((obj, "scale"), (scale, "value"))
        wd["scale"] = scale

    if hasattr(obj, "offset"):
        offset = FloatTextWidget(description="Offset")
        widgets.append(offset)
        link((obj, "offset"), (offset, "value"))
        wd["offset"] = offset

    if "_expression" in obj.__dict__.keys():
        expression = TextWidget(description="Expression", disabled=True)
        widgets.append(expression)
        link((obj, "_expression"), (expression, "value"))
        wd["expression"] = expression
        for i in range(len(obj.parameters_list)):
            parameter = FloatTextWidget(description=obj.parameters_list[i])
            widgets.append(parameter)
            link((obj, obj.parameters_list[i]), (parameter, "value"))
            wd["parameter"] = parameter
        if hasattr(obj.x, "scale"):
            scale = FloatTextWidget(description="x scale")
            widgets.append(scale)
            link((obj.x, "scale"), (scale, "value"))
            wd["scale"] = scale
        if hasattr(obj.x, "offset"):
            offset = FloatTextWidget(description="x offset")
            widgets.append(offset)
            link((obj.x, "offset"), (offset, "value"))
            wd["offset"] = offset

    return {"widget": ContainerWidget(children=widgets, layout="vertical"), "wdict": wd}


@add_display_arg
def aw_axes_gui(obj, **kwargs):
    """Build a tabbed GUI for an AxesManager.

    Parameters
    ----------
    obj : hyperspy.axes.AxesManager
        Axes manager to build the GUI for.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    wdict = {}
    nav_widgets = []
    sig_widgets = []
    i = 0
    for axis in obj.navigation_axes:
        wd = _get_axis_widgets(axis, display=False)
        nav_widgets.append(wd["widget"])
        wdict["axis{}".format(i)] = wd["wdict"]
        i += 1
    for j, axis in enumerate(obj.signal_axes):
        wd = _get_axis_widgets(axis, display=False)
        sig_widgets.append(wd["widget"])
        wdict["axis{}".format(i + j)] = wd["wdict"]

    nav_container = ContainerWidget(
        children=nav_widgets,
        layout="accordion",
        titles=[f"Axis {i}" for i in range(obj.navigation_dimension)],
    )
    sig_container = ContainerWidget(
        children=sig_widgets,
        layout="accordion",
        titles=[f"Axis {j + obj.navigation_dimension + 1}" for j in range(obj.signal_dimension)],
    )
    tabs = ContainerWidget(children=[nav_container, sig_container], layout="horizontal")
    return {
        "widget": tabs,
        "wdict": wdict,
    }
