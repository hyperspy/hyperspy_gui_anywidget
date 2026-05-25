<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-05-25 | Updated: 2026-05-25 -->

# hyperspy_gui_anywidget tests

## Purpose
This directory contains the package regression suite. The tests verify registry imports, widget serialization, bidirectional trait sync, Jupyter/Marimo layout behavior, and the parity fixes that keep the anywidget implementation aligned with the sibling ipywidgets toolkit where intended.

## Key Files

| File | Description |
|------|-------------|
| `test_import.py` | Smoke tests for package importability and lazy module exposure. |
| `test_axes.py` | AxesManager, navigation slider, and axis-title behavior checks. |
| `test_custom_widgets.py` | Focused tests for widget config metadata, flattening, and `FlatContainer` sync helpers. |
| `test_model.py` | Parameter/component/model GUI behavior and fit-component regressions. |
| `test_preferences.py` | Preferences GUI trait mapping and returned widget structure. |
| `test_roi.py` | ROI widget sync tests for span, point, rectangle, circle, and line builders. |
| `test_tools.py` | Tool-widget regressions for smoothing, calibration, background removal, and contrast editors. |
| `test_utils.py` | Helper-level tests for display wrapping, converter fallbacks, and labeling utilities. |
| `test_integration.py` | End-to-end registry and GUI flow checks spanning multiple modules. |
| `test_microscope_parameters.py` | exspy microscope-parameter widget tests when optional dependencies are available. |
| `utils.py` | Shared test constants (for example the default `KWARGS` dict). |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `__pycache__/` | Python bytecode cache; ignore for edits and documentation. |

## For AI Agents

### Working In This Directory
- Add or update focused regression tests when widget behavior, trait sync, serialization, or layout logic changes.
- Keep test names scenario-oriented so failures point to specific GUI regressions.
- Reuse `KWARGS` and existing helper patterns instead of inventing new test harnesses unless the scenario truly requires it.

### Testing Requirements
- Run the affected test module(s) first, then `pytest --pyargs hyperspy_gui_anywidget` for full confidence.
- When touching optional exspy behavior, ensure tests degrade gracefully with `pytest.importorskip` or equivalent patterns already used here.
- For docs/CI-only changes, this directory may not need edits, but package behavior changes almost always do.

### Common Patterns
- Most tests call `.gui(toolkit="anywidget", display=False)` and assert against the returned `widget` / `wdict` structure.
- Widget-to-object and object-to-widget synchronization should be checked in both directions where practical.
- Jupyter-vs-Marimo compatibility is often exercised by mocking or flattening behavior rather than requiring a live frontend runtime.

## Dependencies

### Internal
- Mirrors the runtime modules in `../` one-for-one where practical.
- Uses `../conftest.py` for shared pytest configuration.

### External
- pytest and pytest-cov for execution and coverage.
- HyperSpy / exspy objects for realistic GUI builders and model objects.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
