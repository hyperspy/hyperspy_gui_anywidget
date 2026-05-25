<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-05-25 | Updated: 2026-05-25 -->

# hyperspy_gui_anywidget package

## Purpose
This package contains the live HyperSpy anywidget integration: widget primitives, GUI builders, registry metadata, and compatibility helpers for Jupyter and Marimo. The modules here define the 33 registered GUI entry points exposed through `hyperspy_extension.yaml`.

## Key Files

| File | Description |
|------|-------------|
| `__init__.py` | Lazy-import package entry point and runtime version resolution. |
| `custom_widgets.py` | Core anywidget primitives, `ContainerWidget`, `FlatContainer`, and layout/serialization logic shared across the package. |
| `utils.py` | Helper widgets, trait-to-widget converters, labeling helpers, and `add_display_arg()` environment-aware display wrapper. |
| `tools.py` | GUI builders for interactive signal tools such as smoothing, calibration, background removal, and peak finding. |
| `axes.py` | AxesManager and navigation-slider widgets, including numbered Jupyter titles and continuous-update wiring. |
| `model.py` | Parameter/component/model widget builders and fitting-related UI helpers. |
| `preferences.py` | Preferences GUI construction for Jupyter tabs and Marimo flattened tabs. |
| `roi.py` | ROI widget builders for span, point, rectangular, circle, and line ROIs. |
| `microscope_parameters.py` | Microscope-parameter GUI entry points for supported exspy workflows. |
| `hyperspy_extension.yaml` | HyperSpy extension registry mapping GUI keys to module/function pairs; CI verifies the entry count. |
| `conftest.py` | Shared pytest configuration for package tests. |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `tests/` | Regression and integration tests for widget sync, layout behavior, and registry coverage (see `tests/AGENTS.md`). |

## For AI Agents

### Working In This Directory
- Preserve the Jupyter/Marimo split: Jupyter uses real `ipywidgets` containers, Marimo uses flattened `FlatContainer` configs.
- Match existing widget-return conventions and avoid introducing alternate shapes for `display=False` results.
- Keep `hyperspy_extension.yaml` in sync when adding or removing registered GUI builders.
- Prefer targeted fixes and regression tests close to the affected module.

### Testing Requirements
- Run the closest module tests first (`test_tools.py`, `test_model.py`, `test_axes.py`, etc.).
- Re-run `pytest --pyargs hyperspy_gui_anywidget` after touching shared infrastructure such as `custom_widgets.py`, `utils.py`, or registry files.
- For display-path changes, also rebuild docs because usage guidance references these semantics.

### Common Patterns
- Widgets rely on `link_traits.link()` for bidirectional HyperSpy↔traitlets sync.
- `ContainerWidget` is the abstraction boundary for layout containers across environments.
- Shared helper metadata (`visible`, `continuous_update`, `slider_width`, `readout_format`, `is_color`) flows through `_widget_config()` into `FlatContainer` rendering.
- Public GUI functions are generally decorated with `@add_display_arg`.

## Dependencies

### Internal
- `tests/` mirrors module behavior and should be updated whenever widget behavior changes.
- `docs/api.rst` exposes API reference for the main modules in this directory.
- `README.md` and `docs/user-guide.md` describe the supported Jupyter/Marimo workflows these modules must preserve.

### External
- HyperSpy / exspy objects and traits drive the GUI inputs and outputs.
- anywidget and traitlets power the browser-side widgets.
- ipywidgets provides notebook container primitives such as `VBox`, `HBox`, `Tab`, and `Accordion`.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
