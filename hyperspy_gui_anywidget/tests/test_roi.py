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
