# Learnings - hyperspy-gui-anywidget

## 2025-05-15: utils.py implementation

- AnyWidget subclasses work fine with inline `_esm` JS strings; no build step needed.
- Creating composite layouts in anywidget is done by embedding HTML/CSS directly in each widget's `_esm`, not by nesting widget instances like ipywidgets VBox/HBox.
- `labelme` and `labelme_sandwich` extract `value` and `description_tooltip` from the inner widget and return a new labeled AnyWidget instance. The inner widget is not rendered as a child; its traits are copied into the wrapper.
- `add_display_arg` decorator:
  - `display=True` in Jupyter calls `IPython.display.display(wdict["widget"])` and returns None.
  - `display=True` in Marimo (detected via `"marimo" in sys.modules`) returns `wdict` so Marimo handles rendering.
  - `display=False` always returns `wdict`.
- `_Labeled` and `_LabeledSandwich` use `traitlets.Any()` for `value` so they can wrap both floats and strings. The JS render function switches `<input type="number">` vs `<input type="text">` based on `typeof value`.
- `set_title_container` keeps the same logic as the ipywidgets reference because anywidget container subclasses can implement `set_title` or expose a `titles` trait.
- Tests must avoid creating new `MagicMock()` instances in assertions; reuse the same mock object to prevent identity mismatches.

### SpanROI POC Implementation Notes
- **AnyWidget Child Rendering**: Rendering child widgets via `traitlets.List()` and JS serialization (`widget_manager.create_view`) works natively in Jupyter. We defined `_widget_to_json` manually to avoid importing `ipywidgets` directly, fulfilling the strict constraint while correctly passing `IPY_MODEL_xxx` references.
- **Marimo Limitation**: Marimo currently does not support passing AnyWidget children into `_esm` via `widget_manager` APIs. We added a fallback inside `ContainerWidget`'s ESM so it gracefully falls back when `model.widget_manager` is missing.
- **Architecture**: The pattern of wrapping values in standard JS HTML (for native AnyWidgets) and linking them to python attributes via `link_traits` is viable. We're splitting inputs out into `wdict` via separate `FloatTextWidget` instances, but placing them inside a unified `ContainerWidget`.
