import hyperspy.api as hs

from hyperspy_gui_anywidget.tests.utils import KWARGS


def test_span_roi_anywidget():
    roi = hs.roi.SpanROI(left=0, right=10)

    kwargs = KWARGS.copy()
    kwargs["toolkit"] = "anywidget"
    kwargs["display"] = False

    result = roi.gui(**kwargs)

    wd = result["anywidget"]["wdict"]

    assert wd["left"].value == 0
    assert wd["right"].value == 10

    wd["left"].value = -10
    wd["right"].value = 0

    assert roi.left == -10
    assert roi.right == 0

    roi.left = -5
    roi.right = 5

    assert wd["left"].value == -5
    assert wd["right"].value == 5


def test_point1d_roi_anywidget_syncs_value():
    roi = hs.roi.Point1DROI(value=2)
    result = roi.gui(**KWARGS)
    wd = result["anywidget"]["wdict"]

    assert wd["value"].value == 2
    wd["value"].value = 4
    assert roi.value == 4


def test_point2d_roi_anywidget_syncs_values():
    roi = hs.roi.Point2DROI(x=1, y=2)
    result = roi.gui(**KWARGS)
    wd = result["anywidget"]["wdict"]

    assert wd["x"].value == 1
    assert wd["y"].value == 2
    wd["x"].value = 3
    wd["y"].value = 4
    assert roi.x == 3
    assert roi.y == 4


def test_rectangular_roi_anywidget_syncs_values():
    roi = hs.roi.RectangularROI(left=0, right=5, top=1, bottom=6)
    result = roi.gui(**KWARGS)
    wd = result["anywidget"]["wdict"]

    wd["left"].value = -1
    wd["right"].value = 7
    wd["top"].value = 2
    wd["bottom"].value = 8

    assert roi.left == -1
    assert roi.right == 7
    assert roi.top == 2
    assert roi.bottom == 8


def test_circle_roi_anywidget_syncs_values():
    roi = hs.roi.CircleROI(cx=1, cy=2, r=3, r_inner=1)
    result = roi.gui(**KWARGS)
    wd = result["anywidget"]["wdict"]

    wd["cx"].value = 4
    wd["cy"].value = 5
    wd["radius"].value = 6
    wd["inner_radius"].value = 2

    assert roi.cx == 4
    assert roi.cy == 5
    assert roi.r == 6
    assert roi.r_inner == 2


def test_line2d_roi_linewidth_widget_exists():
    roi = hs.roi.Line2DROI(x1=0, y1=1, x2=2, y2=3, linewidth=4)
    result = roi.gui(**KWARGS)
    wd = result["anywidget"]["wdict"]
    assert wd["linewidth"].value == 4
    wd["x1"].value = 10
    wd["y2"].value = 30
    wd["linewidth"].value = 5
    assert roi.x1 == 10
    assert roi.y2 == 30
    assert roi.linewidth == 5
