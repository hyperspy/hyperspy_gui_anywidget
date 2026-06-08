import hyperspy.api as hs
import pytest
from numpy.random import random

from hyperspy_gui_anywidget.tests.utils import KWARGS

exspy = pytest.importorskip("exspy")


class TestSetMicroscopeParameters:
    def setup_method(self, method):
        self.s = hs.signals.Signal1D((2, 3, 4))

    def _perform_t(self, signal_type):
        s = self.s
        s.set_signal_type(signal_type)
        md = s.metadata
        wd = s.set_microscope_parameters(**KWARGS)["anywidget"]["wdict"]
        if signal_type == "EELS":
            try:
                # exspy <= 0.3.2
                mapping = exspy.signals.eels.EELSTEMParametersUI.mapping
            except AttributeError:
                mapping = exspy.signals._eels.EELSTEMParametersUI.mapping
        elif signal_type == "EDS_SEM":
            try:
                # exspy <= 0.3.2
                mapping = exspy.signals.eds_sem.EDSSEMParametersUI.mapping
            except AttributeError:
                mapping = exspy.signals._eds_sem.EDSSEMParametersUI.mapping
        elif signal_type == "EDS_TEM":
            try:
                # exspy <= 0.3.2
                mapping = exspy.signals.eds_tem.EDSTEMParametersUI.mapping
            except AttributeError:
                mapping = exspy.signals._eds_tem.EDSTEMParametersUI.mapping
        for key, widget in wd.items():
            if "button" not in key:
                widget.value = random()
        button = wd["store_button"]
        # Trigger store by simulating a button click for anywidget
        button.clicks += 1
        for item, name in mapping.items():
            assert md.get_item(item) == wd[name].value

    def test_eels(self):
        self._perform_t(signal_type="EELS")

    def test_eds_tem(self):
        self._perform_t(signal_type="EDS_TEM")

    def test_eds_sem(self):
        self._perform_t(signal_type="EDS_SEM")
