"""ROI widgets for HyperSpy using anywidget.

Each function follows the same pattern:

1. Apply ``@add_display_arg`` for environment-aware display.
2. Create input widgets (e.g. ``FloatTextWidget``) and populate ``wdict``.
3. Link HyperSpy object attributes to widgets via ``link_traits.link``.
4. Wrap everything in a ``ContainerWidget``.
5. Return ``{"widget": container, "wdict": wdict}``.
"""

from hyperspy_gui_anywidget.utils import add_display_arg
from hyperspy_gui_anywidget.custom_widgets import FloatTextWidget, ContainerWidget
from link_traits import link


@add_display_arg
def span_roi_aw(obj, **kwargs):
    """Build a widget for ``SpanROI``.

    Parameters
    ----------
    obj : hyperspy.roi.SpanROI
        The ROI instance to link against.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    wdict = {}

    left = FloatTextWidget(description="Left")
    right = FloatTextWidget(description="Right")

    link((obj, "left"), (left, "value"))
    link((obj, "right"), (right, "value"))

    wdict["left"] = left
    wdict["right"] = right

    container = ContainerWidget(children=[left, right], layout="horizontal")

    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def point1d_roi_aw(obj, **kwargs):
    """Build a widget for ``Point1DROI``.

    Parameters
    ----------
    obj : hyperspy.roi.Point1DROI
        The ROI instance to link against.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    wdict = {}

    value = FloatTextWidget(description="value")
    link((obj, "value"), (value, "value"))

    wdict["value"] = value

    container = ContainerWidget(children=[value], layout="horizontal")

    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def point_2d_aw(obj, **kwargs):
    """Build a widget for ``Point2DROI``.

    Parameters
    ----------
    obj : hyperspy.roi.Point2DROI
        The ROI instance to link against.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    wdict = {}

    x = FloatTextWidget(description="x")
    y = FloatTextWidget(description="y")
    link((obj, "x"), (x, "value"))
    link((obj, "y"), (y, "value"))

    wdict["x"] = x
    wdict["y"] = y

    container = ContainerWidget(children=[x, y], layout="horizontal")

    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def rectangular_roi_aw(obj, **kwargs):
    """Build a widget for ``RectangularROI``.

    Parameters
    ----------
    obj : hyperspy.roi.RectangularROI
        The ROI instance to link against.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    wdict = {}

    left = FloatTextWidget(description="left")
    right = FloatTextWidget(description="right")
    link((obj, "left"), (left, "value"))
    link((obj, "right"), (right, "value"))
    container1 = ContainerWidget(children=[left, right], layout="horizontal")

    top = FloatTextWidget(description="top")
    bottom = FloatTextWidget(description="bottom")
    link((obj, "top"), (top, "value"))
    link((obj, "bottom"), (bottom, "value"))
    container2 = ContainerWidget(children=[top, bottom], layout="horizontal")

    container = ContainerWidget(children=[container1, container2], layout="vertical")

    wdict["left"] = left
    wdict["right"] = right
    wdict["top"] = top
    wdict["bottom"] = bottom

    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def circle_roi_aw(obj, **kwargs):
    """Build a widget for ``CircleROI``.

    Parameters
    ----------
    obj : hyperspy.roi.CircleROI
        The ROI instance to link against.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    wdict = {}

    cx = FloatTextWidget(description="x")
    cy = FloatTextWidget(description="y")
    link((obj, "cx"), (cx, "value"))
    link((obj, "cy"), (cy, "value"))
    container1 = ContainerWidget(children=[cx, cy], layout="horizontal")

    radius = FloatTextWidget(description="radius")
    inner_radius = FloatTextWidget(description="inner_radius")
    link((obj, "r"), (radius, "value"))
    link((obj, "r_inner"), (inner_radius, "value"))
    container2 = ContainerWidget(children=[radius, inner_radius], layout="horizontal")

    container = ContainerWidget(children=[container1, container2], layout="vertical")

    wdict["cx"] = cx
    wdict["cy"] = cy
    wdict["radius"] = radius
    wdict["inner_radius"] = inner_radius

    return {
        "widget": container,
        "wdict": wdict,
    }


@add_display_arg
def line2d_roi_aw(obj, **kwargs):
    """Build a widget for ``Line2DROI``.

    Parameters
    ----------
    obj : hyperspy.roi.Line2DROI
        The ROI instance to link against.
    **kwargs
        Passed through to the widget builder.

    Returns
    -------
    dict or None
        ``{"widget": ContainerWidget, "wdict": {...}}`` when
        ``display=False``, otherwise ``None`` (widget displayed inline).
    """
    wdict = {}

    x1 = FloatTextWidget(description="x1")
    y1 = FloatTextWidget(description="y1")
    link((obj, "x1"), (x1, "value"))
    link((obj, "y1"), (y1, "value"))
    container1 = ContainerWidget(children=[x1, y1], layout="horizontal")

    x2 = FloatTextWidget(description="x2")
    y2 = FloatTextWidget(description="y2")
    link((obj, "x2"), (x2, "value"))
    link((obj, "y2"), (y2, "value"))
    container2 = ContainerWidget(children=[x2, y2], layout="horizontal")

    linewidth = FloatTextWidget(description="linewidth")
    link((obj, "linewidth"), (linewidth, "value"))

    container = ContainerWidget(children=[container1, container2, linewidth], layout="vertical")

    wdict["x1"] = x1
    wdict["y1"] = y1
    wdict["x2"] = x2
    wdict["y2"] = y2
    wdict["linewidth"] = linewidth

    return {
        "widget": container,
        "wdict": wdict,
    }
