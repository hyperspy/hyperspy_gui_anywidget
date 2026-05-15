# -*- coding: utf-8 -*-
# Copyright 2007-2025 The HyperSpy developers
#
# Test that the package can be imported and has a version attribute

def test_import():
    """Test that the package can be imported."""
    import hyperspy_gui_anywidget  # noqa: F401


def test_version():
    """Test that the package has a __version__ attribute."""
    from hyperspy_gui_anywidget import __version__
    assert __version__ is not None
    assert isinstance(__version__, str)


def test_lazy_modules():
    from hyperspy_gui_anywidget import axes, model, roi, tools, preferences, microscope_parameters
    assert axes is not None
    assert model is not None
    assert roi is not None
    assert tools is not None
    assert preferences is not None
    assert microscope_parameters is not None