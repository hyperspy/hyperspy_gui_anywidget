"""
Architecture pattern for HyperSpy AnyWidget ROI widgets:
1. Use `@add_display_arg` decorator from utils to handle environments (Jupyter, Marimo, etc)
2. Instantiate individual input widgets (e.g. FloatTextWidget) for `wdict`
3. Link the HyperSpy object's attributes to the input widgets using `link_traits.link`
4. Instantiate a ContainerWidget to hold the input widgets
5. Return {"widget": container_widget, "wdict": wdict_dict}
"""

from hyperspy_gui_anywidget.utils import add_display_arg
from hyperspy_gui_anywidget.custom_widgets import FloatTextWidget, ContainerWidget
from link_traits import link

@add_display_arg
def span_roi_aw(obj, **kwargs):
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
