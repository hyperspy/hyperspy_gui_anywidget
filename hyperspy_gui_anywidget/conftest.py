import matplotlib

matplotlib.use("agg")

import hyperspy.api as hs

hs.preferences.GUIs.enable_traitsui_gui = False
hs.preferences.GUIs.enable_anywidget_gui = True

# Use matplotlib fixture to clean up figure, setup backend, etc.
# Import at bottom to avoid matplotlib backend issues - must set Agg before importing pyplot
from matplotlib.testing.conftest import mpl_test_settings  # noqa: E402, F401
