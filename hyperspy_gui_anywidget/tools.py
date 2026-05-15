import traits.api as t

from link_traits import link
from hyperspy.signal_tools import (
    SPIKES_REMOVAL_INSTRUCTIONS,
    IMAGE_CONTRAST_EDITOR_HELP_IPYWIDGETS,
)

from hyperspy_gui_anywidget.utils import (
    labelme, enum2dropdown, add_display_arg, set_title_container, _Dropdown
)
from hyperspy_gui_anywidget.custom_widgets import (
    FloatTextWidget, TextWidget, IntTextWidget, IntSliderWidget,
    FloatSliderWidget, CheckboxWidget, LabelWidget,
    ContainerWidget, ButtonWidget, HTMLWidget, IntProgressWidget,
    ToggleButtonWidget, FloatRangeSliderWidget, OddIntSliderWidget,
)


@add_display_arg
def interactive_range_aw(obj, **kwargs):
    wdict = {}
    axis = obj.axis
    left = FloatTextWidget(disabled=True, description="Left")
    right = FloatTextWidget(disabled=True, description="Right")
    units = LabelWidget()
    help_text = HTMLWidget(
        value=(
            "Click on the signal figure and drag to the right to select a signal "
            "range. Press `Apply` to perform the operation or `Close` to cancel."
        )
    )
    help = ContainerWidget(children=[help_text], layout="vertical")
    set_title_container(help, ["Help"])
    close = ButtonWidget(
        description="Close",
        tooltip="Close widget and remove span selector from the signal figure.",
    )
    apply = ButtonWidget(
        description="Apply",
        tooltip="Perform the operation using the selected range.",
    )
    wdict["left"] = left
    wdict["right"] = right
    wdict["units"] = units
    wdict["help_text"] = help_text
    wdict["close_button"] = close
    wdict["apply_button"] = apply

    link((obj, "ss_left_value"), (left, "value"))
    link((obj, "ss_right_value"), (right, "value"))
    link((axis, "units"), (units, "value"))

    def on_apply_clicked(change):
        if obj.ss_left_value != obj.ss_right_value:
            obj.span_selector_switch(False)
            for method, cls in obj.on_close:
                method(cls, obj.ss_left_value, obj.ss_right_value)
            obj.span_selector_switch(True)

    apply.observe(on_apply_clicked, names="clicks")

    def on_close_clicked(change):
        obj.span_selector_switch(False)

    close.observe(on_close_clicked, names="clicks")

    box = ContainerWidget(
        children=[
            ContainerWidget(children=[left, units, LabelWidget(value="-"), right, units], layout="horizontal"),
            help,
            ContainerWidget(children=[apply, close], layout="horizontal"),
        ],
        layout="vertical",
    )

    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def calibrate2d_aw(obj, **kwargs):
    wdict = {}
    length = FloatTextWidget(disabled=True, description="Current length")
    scale = FloatTextWidget(disabled=True, description="Scale")
    new_length = FloatTextWidget(disabled=False, description="New length")
    units = TextWidget(description="Units")
    unitsl = LabelWidget()
    help_text = HTMLWidget(
        value=(
            "Click on the signal figure and drag line to some feature with a "
            "known size. Set the new length, then press `Apply` to update both "
            "the x- and y-dimensions in the signal, or press `Close` to cancel. "
            "The units can also be set with `Units`"
        )
    )
    wdict["help_text"] = help_text
    help = ContainerWidget(children=[help_text], layout="vertical")
    set_title_container(help, ["Help"])
    close = ButtonWidget(
        description="Close",
        tooltip="Close widget and remove line from the signal figure.",
    )
    apply = ButtonWidget(
        description="Apply",
        tooltip="Set the x- and y-scaling with the `scale` value.",
    )

    link((obj, "length"), (length, "value"))
    link((obj, "new_length"), (new_length, "value"))
    link((obj, "units"), (units, "value"))
    link((obj, "units"), (unitsl, "value"))
    link((obj, "scale"), (scale, "value"))

    def on_apply_clicked(change):
        obj.apply()
        obj.on = False

    apply.observe(on_apply_clicked, names="clicks")

    def on_close_clicked(change):
        obj.on = False

    close.observe(on_close_clicked, names="clicks")

    box = ContainerWidget(
        children=[
            ContainerWidget(children=[new_length, unitsl], layout="horizontal"),
            length,
            scale,
            units,
            help,
            ContainerWidget(children=[apply, close], layout="horizontal"),
        ],
        layout="vertical",
    )

    wdict["length"] = length
    wdict["scale"] = scale
    wdict["new_length"] = new_length
    wdict["units"] = units
    wdict["close_button"] = close
    wdict["apply_button"] = apply

    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def calibrate_aw(obj, **kwargs):
    wdict = {}
    left = FloatTextWidget(disabled=True, description="Left")
    right = FloatTextWidget(disabled=True, description="Right")
    offset = FloatTextWidget(disabled=True, description="Offset")
    scale = FloatTextWidget(disabled=True, description="Scale")
    new_left = FloatTextWidget(disabled=False, description="New left")
    new_right = FloatTextWidget(disabled=False, description="New right")
    units = TextWidget(description="Units")
    unitsl = LabelWidget()
    help_text = HTMLWidget(
        value=(
            "Click on the signal figure and drag to the right to select a signal "
            "range. Set the new left and right values and press `Apply` to update "
            "the calibration of the axis with the new values or press "
            " `Close` to cancel."
        )
    )
    wdict["help_text"] = help_text
    help = ContainerWidget(children=[help_text], layout="vertical")
    set_title_container(help, ["Help"])
    close = ButtonWidget(
        description="Close",
        tooltip="Close widget and remove span selector from the signal figure.",
    )
    apply = ButtonWidget(
        description="Apply",
        tooltip="Set the axis calibration with the `offset` and `scale` values above.",
    )

    link((obj, "ss_left_value"), (left, "value"))
    link((obj, "ss_right_value"), (right, "value"))
    link((obj, "left_value"), (new_left, "value"))
    link((obj, "right_value"), (new_right, "value"))
    link((obj, "units"), (units, "value"))
    link((obj, "units"), (unitsl, "value"))
    link((obj, "offset"), (offset, "value"))
    link((obj, "scale"), (scale, "value"))

    def on_apply_clicked(change):
        if (new_left.value, new_right.value) != (0, 0):
            if new_left.value == 0 and obj.left_value is t.Undefined:
                obj.left_value = 0
            elif new_right.value == 0 and obj.right_value is t.Undefined:
                obj.right_value = 0
        obj.apply()

    apply.observe(on_apply_clicked, names="clicks")

    def on_close_clicked(change):
        obj.span_selector_switch(False)

    close.observe(on_close_clicked, names="clicks")

    box = ContainerWidget(
        children=[
            ContainerWidget(children=[new_left, unitsl], layout="horizontal"),
            ContainerWidget(children=[new_right, unitsl], layout="horizontal"),
            ContainerWidget(children=[left, unitsl], layout="horizontal"),
            ContainerWidget(children=[right, unitsl], layout="horizontal"),
            ContainerWidget(children=[offset, unitsl], layout="horizontal"),
            scale,
            units,
            help,
            ContainerWidget(children=[apply, close], layout="horizontal"),
        ],
        layout="vertical",
    )

    wdict["left"] = left
    wdict["right"] = right
    wdict["offset"] = offset
    wdict["scale"] = scale
    wdict["new_left"] = new_left
    wdict["new_right"] = new_right
    wdict["units"] = units
    wdict["close_button"] = close
    wdict["apply_button"] = apply

    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def print_edges_table_aw(obj, **kwargs):
    wdict = {}
    axis = obj.axis
    left = FloatTextWidget(disabled=True, description="Left")
    right = FloatTextWidget(disabled=True, description="Right")
    units = LabelWidget()
    major = CheckboxWidget(value=False, description="Only major edge")
    complmt = CheckboxWidget(value=False, description="Complementary edge")
    order = enum2dropdown(obj.traits()["order"])
    order.description = "Sort energy by"
    update = ButtonWidget(description="Refresh table")
    gb = ContainerWidget(children=[], layout="vertical")
    help_text = HTMLWidget(
        value=(
            "Click on the signal figure and drag to the right to select a signal "
            "range. Drag the rectangle or change its border to display edges in "
            "different signal range. Select edges to show their positions "
            "on the signal."
        )
    )
    help = ContainerWidget(children=[help_text], layout="vertical")
    set_title_container(help, ["Help"])
    close = ButtonWidget(description="Close", tooltip="Close the widget.")
    reset = ButtonWidget(description="Reset", tooltip="Reset the span selector.")

    header = ('<p style="padding-left: 1em; padding-right: 1em; '
              'text-align: center; vertical-align: top; '
              'font-weight:bold">{}</p>')
    entry = ('<p style="padding-left: 1em; padding-right: 1em; '
             'text-align: center; vertical-align: top">{}</p>')

    wdict["left"] = left
    wdict["right"] = right
    wdict["units"] = units
    wdict["help"] = help
    wdict["major"] = major
    wdict["update"] = update
    wdict["complmt"] = complmt
    wdict["order"] = order
    wdict["gb"] = gb
    wdict["reset"] = reset
    wdict["close"] = close

    link((obj, "ss_left_value"), (left, "value"))
    link((obj, "ss_right_value"), (right, "value"))
    link((axis, "units"), (units, "value"))
    link((obj, "only_major"), (major, "value"))
    link((obj, "complementary"), (complmt, "value"))
    link((obj, "order"), (order, "value"))

    def update_table(change):
        edges, energy, relevance, description = obj.update_table()

        items = [
            HTMLWidget(value=header.format("edge")),
            HTMLWidget(value=header.format("onset energy (eV)")),
            HTMLWidget(value=header.format("relevance")),
            HTMLWidget(value=header.format("description")),
        ]

        obj.btns = []
        for k, edge in enumerate(edges):
            if edge in obj.active_edges or edge in obj.active_complementary_edges:
                btn_state = True
            else:
                btn_state = False

            btn = ToggleButtonWidget(value=btn_state, description=edge)
            btn.observe(obj.update_active_edge, names="value")
            obj.btns.append(btn)

            wenergy = HTMLWidget(value=entry.format(str(energy[k])))
            wrelv = HTMLWidget(value=entry.format(str(relevance[k])))
            wdes = HTMLWidget(value=entry.format(str(description[k])))
            items.extend([btn, wenergy, wrelv, wdes])

        gb.children = items

    update.observe(update_table, names="clicks")
    major.observe(update_table, names="value")

    def on_complementary_toggled(change):
        obj.update_table()
        obj.check_btn_state()

    complmt.observe(on_complementary_toggled, names="value")

    def on_order_changed(change):
        obj._get_edges_info_within_energy_axis()
        update_table(change)

    order.observe(on_order_changed, names="value")

    def on_close_clicked(change):
        obj.span_selector_switch(False)

    close.observe(on_close_clicked, names="clicks")

    def on_reset_clicked(change):
        obj._clear_markers()
        obj.span_selector_switch(False)
        left.value = 0
        right.value = 0
        obj.span_selector_switch(True)
        update_table(change)

    reset.observe(on_reset_clicked, names="clicks")

    energy_box = ContainerWidget(
        children=[left, units, LabelWidget(value="-"), right, units],
        layout="horizontal",
    )
    check_box = ContainerWidget(children=[major, complmt], layout="horizontal")
    control_box = ContainerWidget(
        children=[energy_box, update, order, check_box],
        layout="vertical",
    )

    box = ContainerWidget(
        children=[
            ContainerWidget(children=[gb, control_box], layout="horizontal"),
            help,
            ContainerWidget(children=[reset, close], layout="horizontal"),
        ],
        layout="vertical",
    )

    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def smooth_savitzky_golay_aw(obj, **kwargs):
    wdict = {}
    window_length = OddIntSliderWidget(
        value=3, step=2, min=3, max=max(int(obj.axis.size * 0.25), 3), description="Window length"
    )
    polynomial_order = IntSliderWidget(value=3, min=1, max=window_length.value - 1, description="Polynomial order")

    def update_bound(change):
        polynomial_order.max = change.new - 1

    window_length.observe(update_bound, names="value")
    differential_order = IntSliderWidget(value=0, min=0, max=10, description="Differential order")
    color = TextWidget(description="Color")
    close = ButtonWidget(
        description="Close",
        tooltip="Close widget and remove the smoothed line from the signal figure.",
    )
    apply = ButtonWidget(
        description="Apply",
        tooltip="Perform the operation using the selected range.",
    )
    link((obj, "polynomial_order"), (polynomial_order, "value"))
    link((obj, "window_length"), (window_length, "value"))
    link((obj, "differential_order"), (differential_order, "value"))

    def update_diff_max(change):
        differential_order.max = change.new

    polynomial_order.observe(update_diff_max, names="value")
    link((obj, "line_color_ipy"), (color, "value"))

    box = ContainerWidget(
        children=[
            labelme("Window length", window_length),
            labelme("polynomial order", polynomial_order),
            labelme("Differential order", differential_order),
            labelme("Color", color),
            ContainerWidget(children=[apply, close], layout="horizontal"),
        ],
        layout="vertical",
    )

    wdict["window_length"] = window_length
    wdict["polynomial_order"] = polynomial_order
    wdict["differential_order"] = differential_order
    wdict["color"] = color
    wdict["close_button"] = close
    wdict["apply_button"] = apply

    def on_apply_clicked(change):
        obj.apply()

    apply.observe(on_apply_clicked, names="clicks")

    def on_close_clicked(change):
        obj.close()

    close.observe(on_close_clicked, names="clicks")

    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def smooth_lowess_aw(obj, **kwargs):
    wdict = {}
    smoothing_parameter = FloatSliderWidget(min=0, max=1, description="Smoothing parameter")
    number_of_iterations = IntTextWidget(description="Number of iterations")
    color = TextWidget(description="Color")
    close = ButtonWidget(
        description="Close",
        tooltip="Close widget and remove the smoothed line from the signal figure.",
    )
    apply = ButtonWidget(
        description="Apply",
        tooltip="Perform the operation using the selected range.",
    )
    link((obj, "smoothing_parameter"), (smoothing_parameter, "value"))
    link((obj, "number_of_iterations"), (number_of_iterations, "value"))
    link((obj, "line_color_ipy"), (color, "value"))

    box = ContainerWidget(
        children=[
            labelme("Smoothing parameter", smoothing_parameter),
            labelme("Number of iterations", number_of_iterations),
            labelme("Color", color),
            ContainerWidget(children=[apply, close], layout="horizontal"),
        ],
        layout="vertical",
    )
    wdict["smoothing_parameter"] = smoothing_parameter
    wdict["number_of_iterations"] = number_of_iterations
    wdict["color"] = color
    wdict["close_button"] = close
    wdict["apply_button"] = apply

    def on_apply_clicked(change):
        obj.apply()

    apply.observe(on_apply_clicked, names="clicks")

    def on_close_clicked(change):
        obj.close()

    close.observe(on_close_clicked, names="clicks")

    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def smooth_tv_aw(obj, **kwargs):
    wdict = {}
    smoothing_parameter = FloatSliderWidget(min=0.1, max=1000, description="Weight")
    smoothing_parameter_max = FloatTextWidget(value=smoothing_parameter.max, description="Weight max")
    color = TextWidget(description="Color")
    close = ButtonWidget(
        description="Close",
        tooltip="Close widget and remove the smoothed line from the signal figure.",
    )
    apply = ButtonWidget(
        description="Apply",
        tooltip="Perform the operation using the selected range.",
    )
    link((obj, "smoothing_parameter"), (smoothing_parameter, "value"))
    link((smoothing_parameter_max, "value"), (smoothing_parameter, "max"))
    link((obj, "line_color_ipy"), (color, "value"))
    wdict["smoothing_parameter"] = smoothing_parameter
    wdict["smoothing_parameter_max"] = smoothing_parameter_max
    wdict["color"] = color
    wdict["close_button"] = close
    wdict["apply_button"] = apply

    box = ContainerWidget(
        children=[
            labelme("Weight", smoothing_parameter),
            labelme("Weight max", smoothing_parameter_max),
            labelme("Color", color),
            ContainerWidget(children=[apply, close], layout="horizontal"),
        ],
        layout="vertical",
    )

    def on_apply_clicked(change):
        obj.apply()

    apply.observe(on_apply_clicked, names="clicks")

    def on_close_clicked(change):
        obj.close()

    close.observe(on_close_clicked, names="clicks")

    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def remove_background_aw(obj, **kwargs):
    wdict = {}
    left = FloatTextWidget(disabled=True, description="Left")
    right = FloatTextWidget(disabled=True, description="Right")
    red_chisq = FloatTextWidget(disabled=True, description="red-chi2")
    link((obj, "ss_left_value"), (left, "value"))
    link((obj, "ss_right_value"), (right, "value"))
    link((obj, "red_chisq"), (red_chisq, "value"))
    fast = CheckboxWidget(description="Fast")
    zero_fill = CheckboxWidget(description="Zero Fill")
    help_text = HTMLWidget(
        value=(
            "Click on the signal figure and drag to the right to select a "
            "range. Press `Apply` to remove the background in the whole dataset. "
            'If "Fast" is checked, the background parameters are estimated '
            "using a fast (analytical) method that can compromise accuracy. "
            "When unchecked, non-linear least squares is employed instead. "
            'If "Zero Fill" is checked, all the channels prior to the fitting '
            "region will be set to zero. "
            "Otherwise the background subtraction will be performed in the "
            "pre-fitting region as well."
        )
    )
    wdict["help_text"] = help_text
    help = ContainerWidget(children=[help_text], layout="vertical")
    set_title_container(help, ["Help"])
    close = ButtonWidget(
        description="Close",
        tooltip="Close widget and remove span selector from the signal figure.",
    )
    apply = ButtonWidget(
        description="Apply",
        tooltip="Remove the background in the whole dataset.",
    )

    polynomial_order = IntTextWidget(description="Polynomial order")
    background_type = enum2dropdown(obj.traits()["background_type"])
    background_type.description = "Background type"

    def enable_poly_order(change):
        if change.new == "Polynomial":
            polynomial_order.disabled = False
        else:
            polynomial_order.disabled = True

    background_type.observe(enable_poly_order, names="value")
    link((obj, "background_type"), (background_type, "value"))

    class Dummy:
        new = background_type.value

    enable_poly_order(change=Dummy())
    link((obj, "polynomial_order"), (polynomial_order, "value"))
    link((obj, "fast"), (fast, "value"))
    link((obj, "zero_fill"), (zero_fill, "value"))
    wdict["left"] = left
    wdict["right"] = right
    wdict["red_chisq"] = red_chisq
    wdict["fast"] = fast
    wdict["zero_fill"] = zero_fill
    wdict["polynomial_order"] = polynomial_order
    wdict["background_type"] = background_type
    wdict["apply_button"] = apply

    box = ContainerWidget(
        children=[
            left, right, red_chisq,
            background_type,
            polynomial_order,
            fast,
            zero_fill,
            help,
            ContainerWidget(children=[apply, close], layout="horizontal"),
        ],
        layout="vertical",
    )

    def on_apply_clicked(change):
        obj.apply()
        obj.span_selector_switch(False)

    apply.observe(on_apply_clicked, names="clicks")

    def on_close_clicked(change):
        obj.span_selector_switch(False)

    close.observe(on_close_clicked, names="clicks")

    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def image_constast_editor_aw(obj, **kwargs):
    wdict = {}
    left = FloatTextWidget(disabled=True, description="Vmin")
    right = FloatTextWidget(disabled=True, description="Vmax")
    bins = IntTextWidget(description="Bins")
    norm = enum2dropdown(obj.traits()["norm"])
    norm.description = "Norm"
    norm.value = obj.norm
    percentile = FloatRangeSliderWidget(
        value=[0.0, 100.0], min=0.0, max=100.0, step=0.1, description="Vmin/vmax percentile"
    )
    gamma = FloatSliderWidget(value=1.0, min=0.1, max=3.0, description="Gamma")
    linthresh = FloatSliderWidget(value=0.01, min=0.001, max=1.0, step=0.001, description="Linear threshold")
    linscale = FloatSliderWidget(value=0.1, min=0.001, max=10.0, step=0.001, description="Linear scale")
    auto = CheckboxWidget(value=True, description="Auto")
    help_text = HTMLWidget(value=IMAGE_CONTRAST_EDITOR_HELP_IPYWIDGETS)
    wdict["help_text"] = help_text
    help = ContainerWidget(children=[help_text], layout="vertical")
    set_title_container(help, ["Help"])
    close = ButtonWidget(description="Close", tooltip="Close widget.")
    apply = ButtonWidget(description="Apply", tooltip="Use the selected range to re-calculate the histogram.")
    reset = ButtonWidget(description="Reset", tooltip="Reset the settings to their initial values.")
    wdict["left"] = left
    wdict["right"] = right
    wdict["bins"] = bins
    wdict["norm"] = norm
    wdict["percentile"] = percentile
    wdict["gamma"] = gamma
    wdict["linthresh"] = linthresh
    wdict["linscale"] = linscale
    wdict["auto"] = auto
    wdict["close_button"] = close
    wdict["apply_button"] = apply
    wdict["reset_button"] = reset

    link((obj, "ss_left_value"), (left, "value"))
    link((obj, "ss_right_value"), (right, "value"))
    link((obj, "bins"), (bins, "value"))
    link((obj, "norm"), (norm, "value"))
    link((obj, "gamma"), (gamma, "value"))
    link((obj, "linthresh"), (linthresh, "value"))
    link((obj, "linscale"), (linscale, "value"))
    link((obj, "auto"), (auto, "value"))

    def on_percentile_change(change):
        obj.vmin_percentile = change.new[0]
        obj.vmax_percentile = change.new[1]

    percentile.observe(on_percentile_change, names="value")

    def on_vmin_change(change):
        percentile.value = [change.new, percentile.value[1]]

    obj.observe(on_vmin_change, "vmin_percentile")

    def on_vmax_change(change):
        percentile.value = [percentile.value[0], change.new]

    obj.observe(on_vmax_change, "vmax_percentile")

    def on_apply_clicked(change):
        obj.apply()

    apply.observe(on_apply_clicked, names="clicks")

    def on_reset_clicked(change):
        obj.reset()

    reset.observe(on_reset_clicked, names="clicks")

    box = ContainerWidget(
        children=[
            left,
            right,
            auto,
            percentile,
            bins,
            norm,
            gamma,
            linthresh,
            linscale,
            help,
            ContainerWidget(children=[apply, reset, close], layout="horizontal"),
        ],
        layout="vertical",
    )

    def on_close_clicked(change):
        obj.close()

    close.observe(on_close_clicked, names="clicks")

    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def spikes_removal_aw(obj, **kwargs):
    wdict = {}
    threshold = FloatTextWidget(description="Threshold")
    add_noise = CheckboxWidget(description="Add noise")
    default_spike_width = IntTextWidget(description="Default spike width")
    spline_order = IntSliderWidget(min=1, max=10, description="Spline order")
    progress_bar = IntProgressWidget(max=len(obj.coordinates) - 1, description="Progress")
    help_text = HTMLWidget(value=SPIKES_REMOVAL_INSTRUCTIONS.replace('\n', '<br/>'))
    help = ContainerWidget(children=[help_text], layout="vertical")
    set_title_container(help, ["Help"])

    show_diff = ButtonWidget(
        description="Show derivative histogram",
        tooltip="This figure is useful to estimate the threshold.",
    )
    close = ButtonWidget(
        description="Close",
        tooltip="Close widget and remove span selector from the signal figure.",
    )
    next_btn = ButtonWidget(description="Find next", tooltip="Find next spike")
    previous = ButtonWidget(description="Find previous", tooltip="Find previous spike")
    remove = ButtonWidget(description="Remove spike", tooltip="Remove spike and find next one.")
    wdict["threshold"] = threshold
    wdict["add_noise"] = add_noise
    wdict["default_spike_width"] = default_spike_width
    wdict["spline_order"] = spline_order
    wdict["progress_bar"] = progress_bar
    wdict["show_diff_button"] = show_diff
    wdict["close_button"] = close
    wdict["next_button"] = next_btn
    wdict["previous_button"] = previous
    wdict["remove_button"] = remove

    def on_show_diff_clicked(change):
        obj._show_derivative_histogram_fired()

    show_diff.observe(on_show_diff_clicked, names="clicks")

    def on_next_clicked(change):
        obj.find()

    next_btn.observe(on_next_clicked, names="clicks")

    def on_previous_clicked(change):
        obj.find(back=True)

    previous.observe(on_previous_clicked, names="clicks")

    def on_remove_clicked(change):
        obj.apply()

    remove.observe(on_remove_clicked, names="clicks")

    link((obj, "threshold"), (threshold, "value"))
    link((obj, "add_noise"), (add_noise, "value"))
    link((obj, "default_spike_width"), (default_spike_width, "value"))
    link((obj, "spline_order"), (spline_order, "value"))
    link((obj, "index"), (progress_bar, "value"))

    advanced = ContainerWidget(
        children=[
            labelme("Add noise", add_noise),
            labelme("Default spike width", default_spike_width),
            labelme("Spline order", spline_order),
        ],
        layout="vertical",
    )
    set_title_container(advanced, ["Advanced settings"])

    box = ContainerWidget(
        children=[
            ContainerWidget(
                children=[
                    show_diff,
                    labelme("Threshold", threshold),
                    labelme("Progress", progress_bar),
                ],
                layout="vertical",
            ),
            advanced,
            help,
            ContainerWidget(children=[previous, next_btn, remove, close], layout="horizontal"),
        ],
        layout="vertical",
    )

    def on_close_clicked(change):
        obj.span_selector_switch(False)

    close.observe(on_close_clicked, names="clicks")

    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def remove_baseline_aw(obj, **kwargs):
    wdict = {}
    algorithm = enum2dropdown(obj.traits()["algorithm"], description="Method")
    _time_per_pixel = FloatTextWidget(disabled=True, description="Time per pixel (ms)")
    lam = FloatTextWidget(description="lam")
    diff_order = IntSliderWidget(min=1, max=3, description="diff_order")
    p = FloatSliderWidget(min=0.0, max=1.0, description="p")
    lam_1 = FloatSliderWidget(min=-10, max=0, description="lam_1")
    eta = FloatSliderWidget(min=0.0, max=1.0, description="eta")
    penalized_spline = CheckboxWidget(description="penalized_spline")
    poly_order = IntSliderWidget(min=1, max=10, description="poly_order")
    peak_ratio = FloatSliderWidget(min=0.0, max=1.0, description="peak_ratio")
    num_knots = IntSliderWidget(min=10, max=10000, description="num_knots")
    spline_degree = IntSliderWidget(min=1, max=5, description="spline_degree")
    symmetric = CheckboxWidget(description="symmetric")
    quantile = FloatSliderWidget(min=0.001, max=0.5, description="quantile")
    smooth_half_window = IntSliderWidget(min=1, max=100, description="smooth_half_window")
    num_std = IntSliderWidget(min=1, max=100, description="num_std")
    interp_half_window = IntSliderWidget(min=1, max=100, description="interp_half_window")
    half_window = IntSliderWidget(min=1, max=100, description="half_window")
    section = IntSliderWidget(min=1, max=100, description="section")
    segments = IntSliderWidget(min=1, max=100, description="segments")
    link((obj, "lam"), (lam, "value"))
    link((obj, "_time_per_pixel"), (_time_per_pixel, "value"))
    link((obj, "algorithm"), (algorithm, "value"))
    link((obj, "diff_order"), (diff_order, "value"))
    link((obj, "p"), (p, "value"))
    link((obj, "lam_1"), (lam_1, "value"))
    link((obj, "eta"), (eta, "value"))
    link((obj, "penalized_spline"), (penalized_spline, "value"))
    link((obj, "poly_order"), (poly_order, "value"))
    link((obj, "peak_ratio"), (peak_ratio, "value"))
    link((obj, "num_knots"), (num_knots, "value"))
    link((obj, "spline_degree"), (spline_degree, "value"))
    link((obj, "symmetric"), (symmetric, "value"))
    link((obj, "quantile"), (quantile, "value"))
    link((obj, "smooth_half_window"), (smooth_half_window, "value"))
    link((obj, "num_std"), (num_std, "value"))
    link((obj, "interp_half_window"), (interp_half_window, "value"))
    link((obj, "half_window"), (half_window, "value"))
    link((obj, "section"), (section, "value"))
    link((obj, "segments"), (segments, "value"))

    parameters_widget_dict = {
        "lam": lam,
        "diff_order": diff_order,
        "p": p,
        "lam_1": lam_1,
        "eta": eta,
        "penalized_spline": penalized_spline,
        "poly_order": poly_order,
        "peak_ratio": peak_ratio,
        "num_knots": num_knots,
        "spline_degree": spline_degree,
        "symmetric": symmetric,
        "quantile": quantile,
        "smooth_half_window": smooth_half_window,
        "num_std": num_std,
        "interp_half_window": interp_half_window,
        "half_window": half_window,
        "section": section,
        "segments": segments,
    }

    def update_algorithm_parameters(change):
        for parameter_name, parameter_widget in parameters_widget_dict.items():
            if getattr(obj, f"_enable_{parameter_name}"):
                parameter_widget.disabled = False
            else:
                parameter_widget.disabled = True

    algorithm.observe(update_algorithm_parameters, names="value")

    class Dummy:
        new = algorithm.value

    update_algorithm_parameters(change=Dummy())

    close = ButtonWidget(
        description="Close",
        tooltip="Close widget and remove baseline from the signal figure.",
    )
    apply = ButtonWidget(
        description="Apply",
        tooltip="Remove the baseline in the whole dataset.",
    )

    method_parameters = ContainerWidget(
        children=[value for value in parameters_widget_dict.values()],
        layout="vertical",
    )
    set_title_container(method_parameters, ["Method parameters"])

    wdict["algorithm"] = algorithm
    wdict["_time_per_pixel"] = _time_per_pixel
    wdict["lam"] = lam
    wdict["diff_order"] = diff_order
    wdict["p"] = p
    wdict["lam_1"] = lam_1
    wdict["eta"] = eta
    wdict["penalized_spline"] = penalized_spline
    wdict["poly_order"] = poly_order
    wdict["peak_ratio"] = peak_ratio
    wdict["num_knots"] = num_knots
    wdict["spline_degree"] = spline_degree
    wdict["symmetric"] = symmetric
    wdict["quantile"] = quantile
    wdict["smooth_half_window"] = smooth_half_window
    wdict["num_std"] = num_std
    wdict["interp_half_window"] = interp_half_window
    wdict["half_window"] = half_window
    wdict["section"] = section
    wdict["segments"] = segments
    wdict["apply"] = apply

    box = ContainerWidget(
        children=[
            algorithm,
            _time_per_pixel,
            method_parameters,
            ContainerWidget(children=[apply, close], layout="horizontal"),
        ],
        layout="vertical",
    )

    def on_apply_clicked(change):
        obj.apply()

    apply.observe(on_apply_clicked, names="clicks")

    def on_close_clicked(change):
        obj.close()

    close.observe(on_close_clicked, names="clicks")

    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def smooth_butterworth_aw(obj, **kwargs):
    wdict = {}
    cutoff = FloatSliderWidget(min=0.01, max=1., description="Cutoff")
    order = IntTextWidget(description="Order")
    type_ = _Dropdown(options=["low", "high"], value="low", description="Type")
    color = TextWidget(description="Color")
    close = ButtonWidget(
        description="Close",
        tooltip="Close widget and remove the smoothed line from the signal figure.",
    )
    apply = ButtonWidget(
        description="Apply",
        tooltip="Perform the operation using the selected range.",
    )
    link((obj, "cutoff_frequency_ratio"), (cutoff, "value"))
    link((obj, "type"), (type_, "value"))
    link((obj, "order"), (order, "value"))
    wdict["cutoff"] = cutoff
    wdict["order"] = order
    wdict["type"] = type_
    wdict["color"] = color
    wdict["close_button"] = close
    wdict["apply_button"] = apply

    box = ContainerWidget(
        children=[
            labelme("Cutoff frequency ration", cutoff),
            labelme("Type", type_),
            labelme("Order", order),
            ContainerWidget(children=[apply, close], layout="horizontal"),
        ],
        layout="vertical",
    )

    def on_apply_clicked(change):
        obj.apply()

    apply.observe(on_apply_clicked, names="clicks")

    def on_close_clicked(change):
        obj.close()

    close.observe(on_close_clicked, names="clicks")

    return {
        "widget": box,
        "wdict": wdict,
    }


@add_display_arg
def find_peaks2D_aw(obj, **kwargs):
    wdict = {}
    local_max_distance = IntSliderWidget(min=1, max=20, value=3, description="Distance")
    local_max_threshold = FloatSliderWidget(min=0, max=20, value=10, description="Threshold")
    max_alpha = FloatSliderWidget(min=0, max=6, value=3, description="Alpha")
    max_distance = IntSliderWidget(min=1, max=20, value=10, description="Distance")
    minmax_distance = FloatSliderWidget(min=0, max=6, value=3, description="Distance")
    minmax_threshold = FloatSliderWidget(min=0, max=20, value=10, description="Threshold")
    zaefferer_grad_threshold = FloatSliderWidget(min=0, max=0.2, value=0.1, step=0.2 * 1E-1, description="Gradient threshold")
    zaefferer_window_size = IntSliderWidget(min=2, max=80, value=40, description="Window size")
    zaefferer_distance_cutoff = FloatSliderWidget(min=0, max=100, value=50, description="Distance cutoff")
    stat_alpha = FloatSliderWidget(min=0, max=2, value=1, description="Alpha")
    stat_window_radius = IntSliderWidget(min=5, max=20, value=10, description="Radius")
    stat_convergence_ratio = FloatSliderWidget(min=0, max=0.1, value=0.05, description="Convergence ratio")
    log_min_sigma = FloatSliderWidget(min=0, max=2, value=1, description="Min sigma")
    log_max_sigma = FloatSliderWidget(min=0, max=100, value=50, description="Max sigma")
    log_num_sigma = FloatSliderWidget(min=0, max=20, value=10, description="Num sigma")
    log_threshold = FloatSliderWidget(min=0, max=0.4, value=0.2, description="Threshold")
    log_overlap = FloatSliderWidget(min=0, max=1, value=0.5, description="Overlap")
    log_log_scale = CheckboxWidget(value=False, description="Log scale")
    dog_min_sigma = FloatSliderWidget(min=0, max=2, value=1, description="Min sigma")
    dog_max_sigma = FloatSliderWidget(min=0, max=100, value=50, description="Max sigma")
    dog_sigma_ratio = FloatSliderWidget(min=0, max=3.2, value=1.6, description="Sigma ratio")
    dog_threshold = FloatSliderWidget(min=0, max=0.4, value=0.2, description="Threshold")
    dog_overlap = FloatSliderWidget(min=0, max=1, value=0.5, description="Overlap")
    xc_distance = FloatSliderWidget(min=0, max=10., value=5., description="Distance")
    xc_threshold = FloatSliderWidget(min=0, max=2., value=0.5, description="Threshold")

    wdict["local_max_distance"] = local_max_distance
    wdict["local_max_threshold"] = local_max_threshold
    wdict["max_alpha"] = max_alpha
    wdict["max_distance"] = max_distance
    wdict["minmax_distance"] = minmax_distance
    wdict["minmax_threshold"] = minmax_threshold
    wdict["zaefferer_grad_threshold"] = zaefferer_grad_threshold
    wdict["zaefferer_window_size"] = zaefferer_window_size
    wdict["zaefferer_distance_cutoff"] = zaefferer_distance_cutoff
    wdict["stat_alpha"] = stat_alpha
    wdict["stat_window_radius"] = stat_window_radius
    wdict["stat_convergence_ratio"] = stat_convergence_ratio
    wdict["log_min_sigma"] = log_min_sigma
    wdict["log_max_sigma"] = log_max_sigma
    wdict["log_num_sigma"] = log_num_sigma
    wdict["log_threshold"] = log_threshold
    wdict["log_overlap"] = log_overlap
    wdict["log_log_scale"] = log_log_scale
    wdict["dog_min_sigma"] = dog_min_sigma
    wdict["dog_max_sigma"] = dog_max_sigma
    wdict["dog_sigma_ratio"] = dog_sigma_ratio
    wdict["dog_threshold"] = dog_threshold
    wdict["dog_overlap"] = dog_overlap
    wdict["xc_distance"] = xc_distance
    wdict["xc_threshold"] = xc_threshold

    link((obj, "local_max_distance"), (local_max_distance, "value"))
    link((obj, "local_max_threshold"), (local_max_threshold, "value"))
    link((obj, "max_alpha"), (max_alpha, "value"))
    link((obj, "max_distance"), (max_distance, "value"))
    link((obj, "minmax_distance"), (minmax_distance, "value"))
    link((obj, "minmax_threshold"), (minmax_threshold, "value"))
    link((obj, "zaefferer_grad_threshold"), (zaefferer_grad_threshold, "value"))
    link((obj, "zaefferer_window_size"), (zaefferer_window_size, "value"))
    link((obj, "zaefferer_distance_cutoff"), (zaefferer_distance_cutoff, "value"))
    link((obj, "stat_alpha"), (stat_alpha, "value"))
    link((obj, "stat_window_radius"), (stat_window_radius, "value"))
    link((obj, "stat_convergence_ratio"), (stat_convergence_ratio, "value"))
    link((obj, "log_min_sigma"), (log_min_sigma, "value"))
    link((obj, "log_max_sigma"), (log_max_sigma, "value"))
    link((obj, "log_num_sigma"), (log_num_sigma, "value"))
    link((obj, "log_threshold"), (log_threshold, "value"))
    link((obj, "log_overlap"), (log_overlap, "value"))
    link((obj, "log_log_scale"), (log_log_scale, "value"))
    link((obj, "dog_min_sigma"), (dog_min_sigma, "value"))
    link((obj, "dog_max_sigma"), (dog_max_sigma, "value"))
    link((obj, "dog_sigma_ratio"), (dog_sigma_ratio, "value"))
    link((obj, "dog_threshold"), (dog_threshold, "value"))
    link((obj, "dog_overlap"), (dog_overlap, "value"))
    link((obj, "xc_distance"), (xc_distance, "value"))
    link((obj, "xc_threshold"), (xc_threshold, "value"))

    method = enum2dropdown(obj.traits()["method"])
    link((obj, "method"), (method, "value"))

    close = ButtonWidget(
        description="Close",
        tooltip="Close widget and close figure.",
    )
    compute = ButtonWidget(
        description="Compute over navigation axes.",
        tooltip="Find the peaks by iterating over the navigation axes.",
    )

    box_local_max = ContainerWidget(
        children=[labelme("Distance", local_max_distance), labelme("Threshold", local_max_threshold)],
        layout="vertical",
    )
    box_max = ContainerWidget(
        children=[labelme("Alpha", max_alpha), labelme("Distance", max_distance)],
        layout="vertical",
    )
    box_minmax = ContainerWidget(
        children=[labelme("Distance", minmax_distance), labelme("Threshold", minmax_threshold)],
        layout="vertical",
    )
    box_zaefferer = ContainerWidget(
        children=[
            labelme("Gradient threshold", zaefferer_grad_threshold),
            labelme("Window size", zaefferer_window_size),
            labelme("Distance cutoff", zaefferer_distance_cutoff),
        ],
        layout="vertical",
    )
    box_stat = ContainerWidget(
        children=[
            labelme("Alpha", stat_alpha),
            labelme("Radius", stat_window_radius),
            labelme("Convergence ratio", stat_convergence_ratio),
        ],
        layout="vertical",
    )
    box_log = ContainerWidget(
        children=[
            labelme("Min sigma", log_min_sigma),
            labelme("Max sigma", log_max_sigma),
            labelme("Num sigma", log_num_sigma),
            labelme("Threshold", log_threshold),
            labelme("Overlap", log_overlap),
            labelme("Log scale", log_log_scale),
        ],
        layout="vertical",
    )
    box_dog = ContainerWidget(
        children=[
            labelme("Min sigma", dog_min_sigma),
            labelme("Max sigma", dog_max_sigma),
            labelme("Sigma ratio", dog_sigma_ratio),
            labelme("Threshold", dog_threshold),
            labelme("Overlap", dog_overlap),
        ],
        layout="vertical",
    )
    box_xc = ContainerWidget(
        children=[labelme("Distance", xc_distance), labelme("Threshold", xc_threshold)],
        layout="vertical",
    )

    method_parameters = ContainerWidget(
        children=[
            box_local_max,
            box_max,
            box_minmax,
            box_zaefferer,
            box_stat,
            box_log,
            box_dog,
            box_xc,
        ],
        layout="vertical",
    )
    set_title_container(method_parameters, ["Method parameters"])

    widgets_list = [
        labelme("Method", method),
        method_parameters,
        ContainerWidget(children=[compute, close], layout="horizontal"),
    ]

    box = ContainerWidget(children=widgets_list, layout="vertical")

    def on_compute_clicked(change):
        obj.compute_navigation()

    compute.observe(on_compute_clicked, names="clicks")

    def on_close_clicked(change):
        obj.close()

    close.observe(on_close_clicked, names="clicks")

    return {
        "widget": box,
        "wdict": wdict,
    }
