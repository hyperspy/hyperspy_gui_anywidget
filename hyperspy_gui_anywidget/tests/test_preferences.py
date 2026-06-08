# -*- coding: utf-8 -*-

import hyperspy.api as hs
import pytest
from traits.api import TraitError

from hyperspy_gui_anywidget.tests.utils import KWARGS

module_list = [hs]
try:
    import exspy

    module_list.append(exspy)
except Exception:
    pass


@pytest.mark.parametrize("module", module_list)
def test_preferences_widget(module):
    kwargs = KWARGS.copy()
    kwargs["toolkit"] = "anywidget"

    result = module.preferences.gui(**kwargs)
    wd = result["anywidget"]["wdict"]

    assert "save_button" in wd
    assert "close_button" in wd

    tab_keys = [k for k in wd.keys() if k.startswith("tab_")]
    assert len(tab_keys) > 0

    for tabkey in tab_keys:
        tabvalue = wd[tabkey]
        tabname = tabkey[4:]
        tab_obj = getattr(module.preferences, tabname)

        for key, value_widget in tabvalue.items():
            trait_value = getattr(tab_obj, key)
            assert value_widget.value == trait_value

            original_value = trait_value
            set_ok = False

            if isinstance(trait_value, bool):
                value_widget.value = not original_value
                assert getattr(tab_obj, key) == value_widget.value
            elif isinstance(trait_value, float):
                value_widget.value = original_value + 1.0
                set_ok = getattr(tab_obj, key) == value_widget.value
            elif isinstance(trait_value, str):
                try:
                    value_widget.value = "test_value"
                    set_ok = getattr(tab_obj, key) == value_widget.value
                except (ValueError, TypeError, TraitError):
                    pass
            elif hasattr(trait_value, "__iter__") and not isinstance(trait_value, str):
                continue

            if not isinstance(trait_value, bool) and set_ok:
                assert getattr(tab_obj, key) == value_widget.value


@pytest.mark.parametrize("module", module_list)
def test_preferences_widget_returns_correct_traits(module):
    kwargs = KWARGS.copy()
    kwargs["toolkit"] = "anywidget"

    result = module.preferences.gui(**kwargs)
    wd = result["anywidget"]["wdict"]

    for tabkey, tabvalue in wd.items():
        if tabkey.startswith("tab_"):
            tabname = tabkey[4:]
            tab_obj = getattr(module.preferences, tabname)

            for trait_name in tab_obj.editable_traits():
                assert trait_name in tabvalue
