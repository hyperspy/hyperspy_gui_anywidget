"""Reusable anywidget widget classes for hyperspy_gui_anywidget.

Each class is an ``anywidget.AnyWidget`` subclass with an inline ``_esm``
JavaScript string. No build step is required.
"""

import sys

import traitlets
from anywidget.widget import AnyWidget
from ipywidgets import Accordion, HBox, Tab, VBox


class FloatTextWidget(AnyWidget):
    """A float input widget with a label."""

    _esm = """
    function render({ model, el }) {
      const description = model.get("description");
      const value = model.get("value");
      const disabled = model.get("disabled");
      const visible = model.get("visible");

      el.innerHTML = `
        <div style="display: ${visible ? "flex" : "none"}; align-items: center; gap: 10px; margin-bottom: 5px;">
          <label style="min-width: 120px; text-align: right; margin-right: 5px;">${description}</label>
          <input type="number" step="any" value="${value}" ${disabled ? "disabled" : ""} style="flex: 0 0 160px; width: 160px; max-width: 160px;">
        </div>
      `;
      const row = el.querySelector("div");
      const input = el.querySelector("input");
      const label = el.querySelector("label");

      input.addEventListener("change", () => {
        model.set("value", parseFloat(input.value));
        model.save_changes();
      });

      model.on("change:value", () => {
        input.value = model.get("value");
      });

      model.on("change:description", () => {
        label.textContent = model.get("description");
      });

      model.on("change:disabled", () => {
        input.disabled = model.get("disabled");
      });

      model.on("change:visible", () => {
        row.style.display = model.get("visible") ? "flex" : "none";
      });
    }
    export default { render };
    """
    value = traitlets.Float(0.0).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)
    disabled = traitlets.Bool(False).tag(sync=True)
    visible = traitlets.Bool(True).tag(sync=True)


class TextWidget(AnyWidget):
    """A text input widget with a label."""

    _esm = """
    function render({ model, el }) {
      const description = model.get("description");
      const value = model.get("value");
      const disabled = model.get("disabled");
      const visible = model.get("visible");
      const showColor = model.get("is_color");

      function normalizeColor(inputValue) {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        if (!ctx) return null;
        try {
          ctx.fillStyle = inputValue || "#000000";
          const normalized = ctx.fillStyle;
          return /^#[0-9a-f]{6}$/i.test(normalized) ? normalized : null;
        } catch {
          return null;
        }
      }

      function colorPickerValue(inputValue) {
        return normalizeColor(inputValue) || "#000000";
      }

      if (showColor) {
        el.innerHTML = `
          <div style="display: ${visible ? "flex" : "none"}; align-items: center; gap: 10px; margin-bottom: 5px;">
            <label style="min-width: 120px; text-align: right; margin-right: 5px;">${description}</label>
            <div style="display: flex; align-items: center; gap: 8px;">
              <input class="text-input" type="text" value="${value}" ${disabled ? "disabled" : ""} style="flex: 0 0 160px; width: 160px; max-width: 160px;">
              <input class="picker-input" type="color" value="${colorPickerValue(value)}" ${disabled ? "disabled" : ""} style="flex: 0 0 32px; width: 32px; height: 32px; padding: 0; border: none; background: transparent;">
            </div>
          </div>
        `;
      } else {
        el.innerHTML = `
          <div style="display: ${visible ? "flex" : "none"}; align-items: center; gap: 10px; margin-bottom: 5px;">
            <label style="min-width: 120px; text-align: right; margin-right: 5px;">${description}</label>
            <input class="text-input" type="text" value="${value}" ${disabled ? "disabled" : ""} style="flex: 0 0 160px; width: 160px; max-width: 160px;">
          </div>
        `;
      }
      const row = el.querySelector("div");
      const input = el.querySelector(".text-input");
      const colorInput = el.querySelector(".picker-input");
      const label = el.querySelector("label");

      input.addEventListener("change", () => {
        model.set("value", input.value);
        model.save_changes();
        if (colorInput) {
          colorInput.value = colorPickerValue(input.value);
        }
      });

      if (colorInput) {
        colorInput.addEventListener("change", () => {
          input.value = colorInput.value;
          model.set("value", colorInput.value);
          model.save_changes();
        });
      }

      model.on("change:value", () => {
        const newValue = model.get("value");
        input.value = newValue;
        if (colorInput) {
          colorInput.value = colorPickerValue(newValue);
        }
      });

      model.on("change:description", () => {
        label.textContent = model.get("description");
      });

      model.on("change:disabled", () => {
        input.disabled = model.get("disabled");
        if (colorInput) {
          colorInput.disabled = model.get("disabled");
        }
      });

      model.on("change:visible", () => {
        row.style.display = model.get("visible") ? "flex" : "none";
      });
    }
    export default { render };
    """
    value = traitlets.Unicode("").tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)
    disabled = traitlets.Bool(False).tag(sync=True)
    visible = traitlets.Bool(True).tag(sync=True)
    is_color = traitlets.Bool(False).tag(sync=True)


class IntTextWidget(AnyWidget):
    """An integer input widget with a label."""

    _esm = """
    function render({ model, el }) {
      const description = model.get("description");
      const value = model.get("value");
      const disabled = model.get("disabled");
      const visible = model.get("visible");

      el.innerHTML = `
        <div style="display: ${visible ? "flex" : "none"}; align-items: center; gap: 10px; margin-bottom: 5px;">
          <label style="min-width: 120px; text-align: right; margin-right: 5px;">${description}</label>
          <input type="number" value="${value}" ${disabled ? "disabled" : ""} style="flex: 0 0 160px; width: 160px; max-width: 160px;">
        </div>
      `;
      const row = el.querySelector("div");
      const input = el.querySelector("input");
      const label = el.querySelector("label");

      input.addEventListener("change", () => {
        model.set("value", parseInt(input.value));
        model.save_changes();
      });

      model.on("change:value", () => {
        input.value = model.get("value");
      });

      model.on("change:description", () => {
        label.textContent = model.get("description");
      });

      model.on("change:disabled", () => {
        input.disabled = model.get("disabled");
      });

      model.on("change:visible", () => {
        row.style.display = model.get("visible") ? "flex" : "none";
      });
    }
    export default { render };
    """
    value = traitlets.Int(0).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)
    disabled = traitlets.Bool(False).tag(sync=True)
    visible = traitlets.Bool(True).tag(sync=True)


class IntSliderWidget(AnyWidget):
    """An integer range slider widget with a label and readout."""

    _esm = """
    function render({ model, el }) {
      const min = model.get("min");
      const max = model.get("max");
      const step = model.get("step");
      const value = model.get("value");
      const description = model.get("description");
      const visible = model.get("visible");
      const sliderWidth = model.get("slider_width");
      const sliderStyle = sliderWidth
        ? `flex: 0 0 ${sliderWidth}; width: ${sliderWidth}; max-width: ${sliderWidth};`
        : "flex: 1;";

      el.innerHTML = `
        <div style="display: ${visible ? "flex" : "none"}; align-items: center; gap: 10px; margin-bottom: 5px;">
          <label style="min-width: 120px; text-align: right; margin-right: 5px;">${description}</label>
          <input type="range" min="${min}" max="${max}" step="${step}" value="${value}" style="${sliderStyle}">
          <span class="readout" style="min-width: 40px; text-align: right;">${value}</span>
        </div>
      `;
      const row = el.querySelector("div");
      const input = el.querySelector("input");
      const readout = el.querySelector(".readout");
      const label = el.querySelector("label");

      // _dragging guards against change:value events fired while the user is
      // actively holding the slider.  _pendingSent tracks every value sent to
      // Python so that round-trip confirmations (echo_update / update) for
      // those values are suppressed — otherwise delayed confirmations for
      // intermediate drag positions reset the slider after the user releases.
      let _dragging = false;
      const _pendingSent = [];

      function commitValue() {
        _dragging = false;
        const val = parseInt(input.value);
        model.set("value", val);
        model.save_changes();
        readout.textContent = val;
      }

      function clearDragging() {
        _dragging = false;
      }
      window.addEventListener("mouseup", clearDragging);
      window.addEventListener("touchend", clearDragging);

      input.addEventListener("input", () => {
        _dragging = true;
        const val = parseInt(input.value);
        readout.textContent = val;
        if (model.get("continuous_update") !== false) {
          _pendingSent.push(val);
          model.set("value", val);
          model.save_changes();
        }
      });
      input.addEventListener("change", commitValue);

      model.on("change:value", () => {
        if (_dragging) return;
        const val = model.get("value");
        const idx = _pendingSent.indexOf(val);
        if (idx !== -1) {
          _pendingSent.splice(idx, 1);
          return;
        }
        input.value = val;
        readout.textContent = val;
      });

      model.on("change:min", () => {
        input.min = model.get("min");
      });

      model.on("change:max", () => {
        input.max = model.get("max");
      });

      model.on("change:step", () => {
        input.step = model.get("step");
      });

      model.on("change:description", () => {
        label.textContent = model.get("description");
      });

      model.on("change:visible", () => {
        row.style.display = model.get("visible") ? "flex" : "none";
      });
      return () => {
        window.removeEventListener("mouseup", clearDragging);
        window.removeEventListener("touchend", clearDragging);
      };
    }
    export default { render };
    """
    value = traitlets.Int(0).tag(sync=True)
    min = traitlets.Int(0).tag(sync=True)
    max = traitlets.Int(100).tag(sync=True)
    step = traitlets.Int(1).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)
    continuous_update = traitlets.Bool(True).tag(sync=True)
    slider_width = traitlets.Unicode("").tag(sync=True)
    visible = traitlets.Bool(True).tag(sync=True)

    @traitlets.validate("value")
    def _validate_value(self, proposal):
        value = proposal["value"]
        return min(max(value, self.min), self.max)


class FloatSliderWidget(AnyWidget):
    """A float range slider widget with a label and readout."""

    _esm = """
    function render({ model, el }) {
      const min = model.get("min");
      const max = model.get("max");
      const step = model.get("step");
      const value = model.get("value");
      const description = model.get("description");
      const visible = model.get("visible");
      const sliderWidth = model.get("slider_width");
      const sliderStyle = sliderWidth
        ? `flex: 0 0 ${sliderWidth}; width: ${sliderWidth}; max-width: ${sliderWidth};`
        : "flex: 1;";

      function formatFloat(v, format) {
        if (typeof v !== "number") return v;
        if (format) {
          const match = String(format).match(new RegExp("^\\.(\\d+)f$"));
          if (match) {
            return v.toFixed(parseInt(match[1]));
          }
        }
        if (Number.isInteger(v)) return v;
        const a = Math.abs(v);
        if (a === 0) return "0";
        if (a >= 1000) return v.toFixed(1);
        if (a >= 100) return v.toFixed(2);
        if (a >= 10) return v.toFixed(3);
        if (a >= 1) return v.toFixed(4);
        if (a >= 0.1) return v.toFixed(5);
        if (a >= 0.01) return v.toFixed(6);
        return v.toPrecision(6);
      }

      el.innerHTML = `
        <div style="display: ${visible ? "flex" : "none"}; align-items: center; gap: 10px; margin-bottom: 5px;">
          <label style="min-width: 120px; text-align: right; margin-right: 5px;">${description}</label>
          <input type="range" min="${min}" max="${max}" step="${step}" value="${value}" style="${sliderStyle}">
          <span class="readout" style="min-width: 60px; text-align: right;">${formatFloat(value, model.get("readout_format"))}</span>
        </div>
      `;
      const row = el.querySelector("div");
      const input = el.querySelector("input");
      const readout = el.querySelector(".readout");
      const label = el.querySelector("label");

      let _dragging = false;
      const _pendingSent = [];

      function commitValue() {
        _dragging = false;
        const val = parseFloat(input.value);
        model.set("value", val);
        model.save_changes();
        readout.textContent = formatFloat(val, model.get("readout_format"));
      }

      function clearDragging() {
        _dragging = false;
      }
      window.addEventListener("mouseup", clearDragging);
      window.addEventListener("touchend", clearDragging);

      input.addEventListener("input", () => {
        _dragging = true;
        const val = parseFloat(input.value);
        readout.textContent = formatFloat(val, model.get("readout_format"));
        if (model.get("continuous_update") !== false) {
          _pendingSent.push(val);
          model.set("value", val);
          model.save_changes();
        }
      });
      input.addEventListener("change", commitValue);

      model.on("change:value", () => {
        if (_dragging) return;
        const val = model.get("value");
        const idx = _pendingSent.indexOf(val);
        if (idx !== -1) {
          _pendingSent.splice(idx, 1);
          return;
        }
        input.value = val;
        readout.textContent = formatFloat(val, model.get("readout_format"));
      });

      model.on("change:min", () => {
        input.min = model.get("min");
      });

      model.on("change:max", () => {
        input.max = model.get("max");
      });

      model.on("change:step", () => {
        input.step = model.get("step");
      });

      model.on("change:description", () => {
        label.textContent = model.get("description");
      });

      model.on("change:visible", () => {
        row.style.display = model.get("visible") ? "flex" : "none";
      });
      return () => {
        window.removeEventListener("mouseup", clearDragging);
        window.removeEventListener("touchend", clearDragging);
      };
    }
    export default { render };
    """
    value = traitlets.Float(0.0).tag(sync=True)
    min = traitlets.Float(0.0).tag(sync=True)
    max = traitlets.Float(100.0).tag(sync=True)
    step = traitlets.Float(1.0).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)
    continuous_update = traitlets.Bool(True).tag(sync=True)
    readout_format = traitlets.Unicode("").tag(sync=True)
    slider_width = traitlets.Unicode("").tag(sync=True)
    visible = traitlets.Bool(True).tag(sync=True)

    @traitlets.validate("value")
    def _validate_value(self, proposal):
        value = proposal["value"]
        return min(max(value, self.min), self.max)


class CheckboxWidget(AnyWidget):
    """A checkbox widget with a label."""

    _esm = """
    function render({ model, el }) {
      const value = model.get("value");
      const description = model.get("description");

      el.innerHTML = `
        <label style="display: flex; align-items: center; gap: 5px; cursor: pointer; margin-bottom: 5px;">
          <input type="checkbox" ${value ? "checked" : ""}>
          <span>${description}</span>
        </label>
      `;
      const input = el.querySelector("input");
      const span = el.querySelector("span");

      input.addEventListener("change", () => {
        model.set("value", input.checked);
        model.save_changes();
      });

      model.on("change:value", () => {
        input.checked = model.get("value");
      });

      model.on("change:description", () => {
        span.textContent = model.get("description");
      });
    }
    export default { render };
    """
    value = traitlets.Bool(True).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)


class LabelWidget(AnyWidget):
    """A simple text label widget."""

    _esm = """
    function render({ model, el }) {
      const value = model.get("value");
      el.innerHTML = `<span>${value}</span>`;
      model.on("change:value", () => {
        el.querySelector("span").textContent = model.get("value");
      });
    }
    export default { render };
    """
    value = traitlets.Unicode("").tag(sync=True)


class BoundedFloatTextWidget(AnyWidget):
    """A bounded float input widget with min/max validation."""

    _esm = """
    function render({ model, el }) {
      const value = model.get("value");
      const min = model.get("min");
      const max = model.get("max");
      const step = model.get("step");
      const description = model.get("description");
      const disabled = model.get("disabled");
      const visible = model.get("visible");

      el.innerHTML = `
        <div style="display: ${visible ? "flex" : "none"}; align-items: center; gap: 10px; margin-bottom: 5px;">
          <label style="min-width: 120px; text-align: right; margin-right: 5px;">${description}</label>
          <input type="number" min="${min}" max="${max}" step="${step}" value="${value}" ${disabled ? "disabled" : ""} style="flex: 0 0 160px; width: 160px; max-width: 160px;">
        </div>
      `;
      const row = el.querySelector("div");
      const input = el.querySelector("input");
      const label = el.querySelector("label");

      function commitValue() {
        let val = parseFloat(input.value);
        if (val < model.get("min")) val = model.get("min");
        if (val > model.get("max")) val = model.get("max");
        model.set("value", val);
        model.save_changes();
      }

      input.addEventListener("input", () => {
        if (model.get("continuous_update")) {
          commitValue();
        }
      });
      input.addEventListener("change", commitValue);

      model.on("change:value", () => {
        input.value = model.get("value");
      });

      model.on("change:min", () => {
        input.min = model.get("min");
      });

      model.on("change:max", () => {
        input.max = model.get("max");
      });

      model.on("change:step", () => {
        input.step = model.get("step");
      });

      model.on("change:description", () => {
        label.textContent = model.get("description");
      });

      model.on("change:disabled", () => {
        input.disabled = model.get("disabled");
      });

      model.on("change:visible", () => {
        row.style.display = model.get("visible") ? "flex" : "none";
      });
    }
    export default { render };
    """
    value = traitlets.Float(0.0).tag(sync=True)
    min = traitlets.Float(0.0).tag(sync=True)
    max = traitlets.Float(100.0).tag(sync=True)
    step = traitlets.Float(1.0).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)
    disabled = traitlets.Bool(False).tag(sync=True)
    continuous_update = traitlets.Bool(True).tag(sync=True)
    visible = traitlets.Bool(True).tag(sync=True)

    @traitlets.validate("value")
    def _validate_value(self, proposal):
        value = proposal["value"]
        return min(max(value, self.min), self.max)


def _widget_to_json(x, obj):
    if isinstance(x, dict):
        return {k: _widget_to_json(v, obj) for k, v in x.items()}
    elif isinstance(x, (list, tuple)):
        return [_widget_to_json(v, obj) for v in x]
    elif hasattr(x, "model_id"):
        return "IPY_MODEL_" + x.model_id
    else:
        return x


widget_serialization = {"to_json": _widget_to_json, "from_json": None}


class ButtonWidget(AnyWidget):
    """A button widget that increments a ``clicks`` trait on press."""

    _esm = """
    function render({ model, el }) {
      const description = model.get("description");
      const tooltip = model.get("tooltip");
      el.innerHTML = `<button title="${tooltip}">${description}</button>`;
      const button = el.querySelector("button");
      button.addEventListener("click", () => {
        model.set("clicks", model.get("clicks") + 1);
        model.save_changes();
      });
    }
    export default { render };
    """
    description = traitlets.Unicode("Button").tag(sync=True)
    tooltip = traitlets.Unicode("").tag(sync=True)
    clicks = traitlets.Int(0).tag(sync=True)


class HTMLWidget(AnyWidget):
    """A widget that renders HTML content."""

    _esm = """
    function render({ model, el }) {
      const value = model.get("value");
      el.innerHTML = `<div>${value}</div>`;
      model.on("change:value", () => {
        el.querySelector("div").innerHTML = model.get("value");
      });
    }
    export default { render };
    """
    value = traitlets.Unicode("").tag(sync=True)


class IntProgressWidget(AnyWidget):
    """A progress bar widget with a label and readout."""

    _esm = """
    function render({ model, el }) {
      const value = model.get("value");
      const max = model.get("max");
      const description = model.get("description");
      el.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
          <label style="min-width: 120px; text-align: right; margin-right: 5px;">${description}</label>
          <progress value="${value}" max="${max}" style="flex: 1;"></progress>
          <span class="readout" style="min-width: 40px; text-align: right;">${value}/${max}</span>
        </div>
      `;
      const progress = el.querySelector("progress");
      const readout = el.querySelector(".readout");
      model.on("change:value", () => {
        progress.value = model.get("value");
        readout.textContent = model.get("value") + "/" + model.get("max");
      });
      model.on("change:max", () => {
        progress.max = model.get("max");
        readout.textContent = model.get("value") + "/" + model.get("max");
      });
    }
    export default { render };
    """
    value = traitlets.Int(0).tag(sync=True)
    max = traitlets.Int(100).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)


class ToggleButtonWidget(AnyWidget):
    """A toggle button widget with a boolean ``value`` trait."""

    _esm = """
    function render({ model, el }) {
      const value = model.get("value");
      const description = model.get("description");
      el.innerHTML = `<button style="background: ${value ? '#2196F3' : '#e0e0e0'}; color: ${value ? 'white' : 'black'};">${description}</button>`;
      const button = el.querySelector("button");
      button.addEventListener("click", () => {
        model.set("value", !model.get("value"));
        model.save_changes();
      });
      model.on("change:value", () => {
        const v = model.get("value");
        button.style.background = v ? '#2196F3' : '#e0e0e0';
        button.style.color = v ? 'white' : 'black';
      });
    }
    export default { render };
    """
    value = traitlets.Bool(False).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)


class FloatRangeSliderWidget(AnyWidget):
    """A two-number input widget for low/high range values."""

    _esm = """
    function render({ model, el }) {
      const min = model.get("min");
      const max = model.get("max");
      const step = model.get("step");
      const value = model.get("value") || [0, 0];
      const description = model.get("description");
      el.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
          <label style="min-width: 120px; text-align: right; margin-right: 5px;">${description}</label>
          <input type="number" step="${step}" value="${value[0]}" class="low" style="flex: 1;">
          <span>-</span>
          <input type="number" step="${step}" value="${value[1]}" class="high" style="flex: 1;">
        </div>
      `;
      const low = el.querySelector(".low");
      const high = el.querySelector(".high");
      const label = el.querySelector("label");

      function updateValues() {
        const vlow = parseFloat(low.value);
        const vhigh = parseFloat(high.value);
        model.set("value", [vlow, vhigh]);
        model.save_changes();
      }

      low.addEventListener("change", updateValues);
      high.addEventListener("change", updateValues);

      model.on("change:value", () => {
        const val = model.get("value");
        low.value = val[0];
        high.value = val[1];
      });

      model.on("change:min", () => {
        low.min = model.get("min");
        high.min = model.get("min");
      });

      model.on("change:max", () => {
        low.max = model.get("max");
        high.max = model.get("max");
      });

      model.on("change:step", () => {
        low.step = model.get("step");
        high.step = model.get("step");
      });

      model.on("change:description", () => {
        label.textContent = model.get("description");
      });
    }
    export default { render };
    """
    value = traitlets.List(trait=traitlets.Float(), default_value=[0.0, 100.0]).tag(sync=True)
    min = traitlets.Float(0.0).tag(sync=True)
    max = traitlets.Float(100.0).tag(sync=True)
    step = traitlets.Float(0.1).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)


class OddIntSliderWidget(IntSliderWidget):
    """An integer slider that only accepts odd values."""

    step = traitlets.Int(2).tag(sync=True)

    @traitlets.validate("value")
    def _validate_value(self, proposal):
        value = proposal["value"]
        if value % 2 == 0:
            value += 1
        return min(max(value, self.min), self.max)


class ContainerWidget:
    def __new__(cls, children=None, layout="vertical", **kwargs):
        children = children or []
        if "marimo" in sys.modules:
            return _make_flat_container(children, layout, **kwargs)
        if layout == "horizontal":
            return HBox(children=children, **kwargs)
        elif layout == "tabs":
            titles = kwargs.pop("titles", None)
            tab = Tab(children=children, **kwargs)
            if titles:
                for i, title in enumerate(titles):
                    tab.set_title(i, str(title))
            return tab
        elif layout == "accordion":
            titles = kwargs.pop("titles", None)
            acc = Accordion(children=children, **kwargs)
            if titles:
                for i, title in enumerate(titles):
                    acc.set_title(i, str(title))
            return acc
        else:
            return VBox(children=children, **kwargs)


def _widget_config(w):
    from hyperspy_gui_anywidget.utils import _Dropdown, _Labeled, _LabeledSandwich

    cfg = {"id": str(id(w))}
    if isinstance(w, (FloatTextWidget, IntTextWidget, BoundedFloatTextWidget)):
        cfg["type"] = "number"
        cfg["value"] = w.value
        cfg["label"] = w.description
        cfg["disabled"] = getattr(w, "disabled", False)
        cfg["visible"] = getattr(w, "visible", True)
        cfg["step"] = str(getattr(w, "step", "any"))
        cfg["min"] = getattr(w, "min", None)
        cfg["max"] = getattr(w, "max", None)
        cfg["continuous_update"] = getattr(w, "continuous_update", True)
    elif isinstance(w, TextWidget):
        cfg["type"] = "text"
        cfg["value"] = w.value
        cfg["label"] = w.description
        cfg["disabled"] = w.disabled
        cfg["visible"] = getattr(w, "visible", True)
        cfg["is_color"] = w.is_color
    elif isinstance(w, LabelWidget):
        cfg["type"] = "label"
        cfg["value"] = w.value
    elif isinstance(w, CheckboxWidget):
        cfg["type"] = "checkbox"
        cfg["value"] = w.value
        cfg["label"] = w.description
    elif isinstance(w, ButtonWidget):
        cfg["type"] = "button"
        cfg["label"] = w.description
        cfg["tooltip"] = w.tooltip
        cfg["value"] = w.clicks
    elif isinstance(w, ToggleButtonWidget):
        cfg["type"] = "toggle"
        cfg["value"] = w.value
        cfg["label"] = w.description
    elif isinstance(w, (IntSliderWidget, FloatSliderWidget, OddIntSliderWidget)):
        cfg["type"] = "slider"
        cfg["value"] = w.value
        cfg["label"] = w.description
        cfg["min"] = w.min
        cfg["max"] = w.max
        cfg["step"] = w.step
        cfg["continuous_update"] = getattr(w, "continuous_update", True)
        cfg["continuous_update_key"] = str(id(w)) + "_cu"
        cfg["readout_format"] = getattr(w, "readout_format", "")
        cfg["slider_width"] = getattr(w, "slider_width", "")
        cfg["visible"] = getattr(w, "visible", True)
    elif isinstance(w, HTMLWidget):
        cfg["type"] = "html"
        cfg["value"] = w.value
    elif isinstance(w, IntProgressWidget):
        cfg["type"] = "progress"
        cfg["value"] = w.value
        cfg["label"] = w.description
        cfg["max"] = w.max
    elif isinstance(w, FloatRangeSliderWidget):
        cfg["type"] = "range_slider"
        cfg["value"] = list(w.value) if w.value else [0.0, 100.0]
        cfg["label"] = w.description
        cfg["min"] = w.min
        cfg["max"] = w.max
        cfg["step"] = w.step
    elif isinstance(w, _Dropdown):
        cfg["type"] = "dropdown"
        cfg["value"] = w.value
        cfg["label"] = getattr(w, "description", "")
        cfg["options"] = w.options
    elif isinstance(w, _Labeled):
        cfg["type"] = "labeled"
        cfg["value"] = w.value
        cfg["label"] = w.label
    elif isinstance(w, _LabeledSandwich):
        cfg["type"] = "sandwich"
        cfg["value"] = w.value
        cfg["label1"] = w.label1
        cfg["label2"] = w.label2
    elif isinstance(w, AnyWidget):
        # Generic anywidget fallback — detect widget type from traits.
        # Handles widgets from other modules (e.g. preferences._RangeSlider)
        # that are not explicitly listed above.
        wval = getattr(w, "value", None)
        wdesc = getattr(w, "description", None)
        wmin = getattr(w, "min", None)
        wmax = getattr(w, "max", None)
        wstep = getattr(w, "step", None)
        if isinstance(wval, (int, float)) and wmin is not None and wmax is not None:
            cfg["type"] = "slider"
            cfg["value"] = wval
            cfg["label"] = wdesc or ""
            cfg["min"] = wmin
            cfg["max"] = wmax
            cfg["step"] = str(wstep) if wstep is not None else "any"
        elif isinstance(wval, (int, float)):
            cfg["type"] = "number"
            cfg["value"] = wval
            cfg["label"] = wdesc or ""
            cfg["step"] = "any"
        elif isinstance(wval, str):
            cfg["type"] = "text"
            cfg["value"] = wval
            cfg["label"] = wdesc or ""
        else:
            cfg["type"] = "unknown"
            cfg["value"] = str(w)
    else:
        cfg["type"] = "unknown"
        cfg["value"] = str(w)
    return cfg


def _flatten_widget_tree(children):
    configs = []
    for child in children:
        if isinstance(child, (VBox, HBox)):
            configs.append(
                {
                    "type": "layout_start",
                    "direction": "column" if isinstance(child, VBox) else "row",
                }
            )
            configs.extend(_flatten_widget_tree(child.children))
            configs.append({"type": "layout_end"})
        elif isinstance(child, Tab):
            for i, tab_child in enumerate(child.children):
                title = child.get_title(i)
                configs.append({"type": "tab_start", "title": title})
                configs.extend(_flatten_widget_tree([tab_child]))
                configs.append({"type": "tab_end"})
        elif isinstance(child, Accordion):
            titles = [child.get_title(i) for i in range(len(child.children))]
            configs.append({"type": "accordion_start", "titles": titles})
            configs.extend(_flatten_widget_tree(child.children))
            configs.append({"type": "accordion_end"})
        elif isinstance(child, FlatContainer):
            configs.append({"type": "layout_start", "direction": child._layout})
            configs.extend(child._children_config)
            configs.append({"type": "layout_end"})
        else:
            configs.append(_widget_config(child))
    return configs


def _make_flat_container(children, layout, **kwargs):
    if layout == "accordion":
        titles = kwargs.get("titles", [])
        configs = _flatten_widget_tree(children)
        configs = (
            [{"type": "accordion_start", "titles": list(titles)}]
            + configs
            + [{"type": "accordion_end"}]
        )
        layout = "vertical"
    elif layout == "tabs":
        titles = kwargs.get("titles", [])
        configs = []
        for i, child in enumerate(children):
            title = titles[i] if i < len(titles) else "Tab {}".format(i + 1)
            configs.append({"type": "tab_start", "title": title})
            configs.extend(_flatten_widget_tree([child]))
            configs.append({"type": "tab_end"})
        layout = "vertical"
    else:
        configs = _flatten_widget_tree(children)
    container = FlatContainer(_children_config=configs, _layout=layout)
    container._source_children = children
    _wire_flat_sync(container, children)
    return container


def _wire_flat_sync(container, children):
    """Wire bidirectional sync between FlatContainer and child widgets."""
    idx_map = {}
    leaf_idx = 0
    _applying = False  # re-entrancy guard

    def _map_children(kids):
        nonlocal leaf_idx
        for child in kids:
            if isinstance(child, (VBox, HBox)):
                _map_children(child.children)
            elif isinstance(child, FlatContainer) and hasattr(child, "_source_children"):
                # Recurse into nested FlatContainers so the outer sync can reach
                # leaf widgets that are embedded by _flatten_widget_tree.
                _map_children(child._source_children)
            else:
                idx_map[str(id(child))] = (leaf_idx, child)
                leaf_idx += 1

    _map_children(children)

    def _frontend_to_python(change):
        nonlocal _applying
        if _applying:
            return
        _applying = True
        try:
            old_vals = change.get("old", {})
            for cfg_id, new_value in change["new"].items():
                if cfg_id in idx_map and old_vals.get(cfg_id) != new_value:
                    _, widget = idx_map[cfg_id]
                    _apply_value(widget, new_value)
        finally:
            _applying = False

    container.observe(_frontend_to_python, names="_children_values")

    for cfg_id, (_, widget) in idx_map.items():

        def _make_observer(cid, w):
            def _python_to_frontend(change):
                current = dict(container._children_values)
                current[cid] = _extract_value(w)
                container._children_values = current

            return _python_to_frontend

        trait_name = "clicks" if isinstance(widget, ButtonWidget) else "value"
        widget.observe(_make_observer(cfg_id, widget), names=trait_name)

        if hasattr(type(widget), "continuous_update"):
            cu_key = cfg_id + "_cu"

            def _make_cu_observer(cu_k, w):
                def _cu_to_frontend(change):
                    current = dict(container._children_values)
                    current[cu_k] = w.continuous_update
                    container._children_values = current

                return _cu_to_frontend

            widget.observe(_make_cu_observer(cu_key, widget), names="continuous_update")


def _extract_value(widget):
    if isinstance(widget, FloatRangeSliderWidget):
        return list(widget.value)
    if isinstance(widget, ButtonWidget):
        return widget.clicks
    return widget.value


def _apply_value(widget, value):
    if isinstance(widget, FloatRangeSliderWidget):
        widget.value = list(value)
    elif isinstance(widget, ButtonWidget):
        widget.clicks = int(value)
    elif isinstance(widget, CheckboxWidget):
        widget.value = bool(value)
    elif isinstance(widget, (FloatTextWidget, FloatSliderWidget, BoundedFloatTextWidget)):
        widget.value = float(value)
    elif isinstance(
        widget, (IntTextWidget, IntSliderWidget, IntProgressWidget, OddIntSliderWidget)
    ):
        widget.value = int(value)
    else:
        widget.value = value


class FlatContainer(AnyWidget):
    _esm = """
    function render({ model, el }) {
      const configs = model.get("_children_config");
      const values = model.get("_children_values") || {};
      const layout = model.get("_layout") || "vertical";

      function fmt(v, format) {
        if (typeof v !== "number") return v;
        if (format) {
          const match = String(format).match(new RegExp("^\\.(\\d+)f$"));
          if (match) {
            return v.toFixed(parseInt(match[1]));
          }
        }
        if (Number.isInteger(v)) return v;
        const a = Math.abs(v);
        if (a === 0) return "0";
        if (a >= 1000) return v.toFixed(1);
        if (a >= 100) return v.toFixed(2);
        if (a >= 10) return v.toFixed(3);
        if (a >= 1) return v.toFixed(4);
        if (a >= 0.1) return v.toFixed(5);
        if (a >= 0.01) return v.toFixed(6);
        if (a >= 0.001) return v.toFixed(7);
        return v.toPrecision(6);
      }

      function normalizeColor(inputValue) {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        if (!ctx) return null;
        try {
          ctx.fillStyle = inputValue || "#000000";
          const normalized = ctx.fillStyle;
          return /^#[0-9a-f]{6}$/i.test(normalized) ? normalized : null;
        } catch {
          return null;
        }
      }

      function colorPickerValue(inputValue) {
        return normalizeColor(inputValue) || "#000000";
      }

      if (model.get("_closed")) { el.style.display = "none"; return; }
      model.on("change:_closed", () => {
        if (model.get("_closed")) el.style.display = "none";
      });

      el.style.display = "flex";
      el.style.flexDirection = layout === "horizontal" ? "row" : "column";
      el.style.gap = "10px";
      el.style.flexWrap = "wrap";

      const idToEl = {};
      const draggingSliders = new Set();
      const _pendingSentBySlider = new Map();
      const _cuState = new Map();  // slider cfg.id → live continuous_update boolean
      const _onMouseUp = () => draggingSliders.clear();
      window.addEventListener("mouseup", _onMouseUp);
      window.addEventListener("touchend", _onMouseUp);
      const stack = [{ parent: el, layout: layout }];

      function makeRow(cfg) {
        const row = document.createElement("div");
        row.style.display = "flex";
        row.style.flexDirection = "row";
        row.style.gap = "8px";
        row.style.alignItems = "center";
        return row;
      }

      function updateValues(newValues) {
        for (const [id, val] of Object.entries(newValues)) {
          if (id.endsWith("_cu")) { _cuState.set(id, !!val); continue; }
          const el_info = idToEl[id];
          if (!el_info) continue;
          const { el: target, colorEl, cfg } = el_info;
          if (cfg.type === "number" || cfg.type === "text") {
            target.value = val;
            if (cfg.is_color && colorEl) {
              colorEl.value = colorPickerValue(val);
            }
          } else if (cfg.type === "slider") {
            if (!draggingSliders.has(id)) {
              const pending = _pendingSentBySlider.get(id);
              const pidx = pending ? pending.indexOf(val) : -1;
              if (pidx !== -1) {
                pending.splice(pidx, 1);
              } else {
                target.value = val;
                const readout = target.parentElement.querySelector(".flat-readout");
                if (readout) readout.textContent = fmt(val, cfg.readout_format);
              }
            }
          } else if (cfg.type === "checkbox") {
            target.checked = val;
          } else if (cfg.type === "label") {
            target.textContent = val;
          } else if (cfg.type === "toggle") {
            target.textContent = cfg.label;
            target.style.background = val ? "#2196F3" : "#e0e0e0";
            target.style.color = val ? "white" : "black";
          }
        }
      }

      model.on("change:_children_values", () => {
        updateValues(model.get("_children_values"));
      });

      let tabState = null;

      for (const cfg of configs) {
        if (cfg.type === "tab_start") {
          const tabContentEl = document.createElement("div");
          const parent = stack[stack.length - 1].parent;

          stack.push({ parent: tabContentEl, layout: "vertical", _tabData: { parent: parent, title: cfg.title, tabEl: tabContentEl } });
          continue;
        }
        if (cfg.type === "tab_end") {
          const entry = stack.pop();
          if (!entry._tabData) continue;
          const { parent, title, tabEl } = entry._tabData;
          if (!parent._tabGroup) {
            parent._tabGroup = {
              headers: document.createElement("div"),
              content: document.createElement("div"),
              tabs: [],
              activeIdx: 0,
            };
            parent._tabGroup.headers.style.display = "flex";
            parent._tabGroup.headers.style.borderBottom = "1px solid #ccc";
            parent._tabGroup.content.style.padding = "10px 0";
            parent.appendChild(parent._tabGroup.headers);
            parent.appendChild(parent._tabGroup.content);
          }
          const group = parent._tabGroup;
          const idx = group.tabs.length;
          group.tabs.push({ title: title, el: tabEl });

          const btn = document.createElement("button");
          btn.textContent = title;
          btn.style.padding = "8px 16px";
          btn.style.border = "none";
          btn.style.background = "transparent";
          btn.style.cursor = "pointer";
          btn.addEventListener("click", () => {
            group.activeIdx = idx;
            group.content.innerHTML = "";
            group.content.appendChild(group.tabs[idx].el);
            group.headers.querySelectorAll("button").forEach((b, i) => {
              b.style.background = i === idx ? "#e0e0e0" : "transparent";
              b.style.borderBottom = i === idx ? "2px solid #3366cc" : "none";
            });
          });
          group.headers.appendChild(btn);
          if (idx === 0) {
            group.content.appendChild(tabEl);
            btn.style.background = "#e0e0e0";
            btn.style.borderBottom = "2px solid #3366cc";
          }
          continue;
        }
        if (cfg.type === "accordion_start") {
          const titles = cfg.titles || [];
          const accordionEl = document.createElement("div");
          accordionEl.style.display = "flex";
          accordionEl.style.flexDirection = "column";
          accordionEl.style.gap = "2px";
          accordionEl.style.width = "100%";

          const parent = stack[stack.length - 1].parent;
          parent.appendChild(accordionEl);

          stack.push({ parent: accordionEl, layout: "vertical", _accordion: { titles, sections: [] } });
          continue;
        }
        if (cfg.type === "accordion_end") {
          const entry = stack.pop();
          if (!entry._accordion) continue;
          const { titles } = entry._accordion;
          const accordionEl = entry.parent;

          const childNodes = Array.from(accordionEl.children);
          accordionEl.innerHTML = "";

          childNodes.forEach((childEl, i) => {
            const header = document.createElement("button");
            header.textContent = (titles[i] !== undefined ? String(titles[i]) : "Section " + (i + 1));
            header.style.width = "100%";
            header.style.textAlign = "left";
            header.style.padding = "8px 12px";
            header.style.border = "1px solid #ccc";
            header.style.background = "#f5f5f5";
            header.style.cursor = "pointer";
            header.style.fontSize = "13px";
            header.style.fontWeight = "500";

            const content = document.createElement("div");
            content.style.display = "none";
            content.style.padding = "8px";
            content.style.border = "1px solid #ccc";
            content.style.borderTop = "none";
            content.style.background = "#fff";
            content.appendChild(childEl);

            header.addEventListener("click", () => {
              const isOpen = content.style.display !== "none";
              content.style.display = isOpen ? "none" : "block";
              header.style.background = isOpen ? "#f5f5f5" : "#e8e8e8";
            });

            accordionEl.appendChild(header);
            accordionEl.appendChild(content);

            if (i === 0) {
              content.style.display = "block";
              header.style.background = "#e8e8e8";
            }
          });
          continue;
        }
        if (cfg.type === "layout_start") {
          const container = document.createElement("div");
          container.style.display = "flex";
          container.style.flexDirection = cfg.direction;
          container.style.gap = "10px";
          container.style.flexWrap = "wrap";
          const current = stack[stack.length - 1];
          current.parent.appendChild(container);
          stack.push({ parent: container, layout: cfg.direction });
          continue;
        }
        if (cfg.type === "layout_end") {
          stack.pop();
          continue;
        }

        const current = stack[stack.length - 1];
        const parent = current.parent;

        if (cfg.type === "label") {
          const span = document.createElement("span");
          span.textContent = cfg.value;
          parent.appendChild(span);
          idToEl[cfg.id] = { el: span, cfg };
          continue;
        }

        if (cfg.type === "html") {
          const div = document.createElement("div");
          div.innerHTML = cfg.value;
          parent.appendChild(div);
          idToEl[cfg.id] = { el: div, cfg };
          continue;
        }

        if (cfg.type === "button") {
          const btn = document.createElement("button");
          btn.textContent = cfg.label;
          btn.title = cfg.tooltip || "";
          btn.addEventListener("click", () => {
            const prev = (model.get("_children_values") || {})[cfg.id] || 0;
            model.set("_children_values", { [cfg.id]: prev + 1 });
            model.save_changes();
          });
          parent.appendChild(btn);
          idToEl[cfg.id] = { el: btn, cfg };
          continue;
        }

        if (cfg.type === "toggle") {
          const btn = document.createElement("button");
          btn.textContent = cfg.label;
          btn.style.background = cfg.value ? "#2196F3" : "#e0e0e0";
          btn.style.color = cfg.value ? "white" : "black";
          btn.addEventListener("click", () => {
            const cur = (model.get("_children_values") || {})[cfg.id] ?? cfg.value;
            model.set("_children_values", { [cfg.id]: !cur });
            model.save_changes();
          });
          parent.appendChild(btn);
          idToEl[cfg.id] = { el: btn, cfg };
          continue;
        }

        if (cfg.type === "progress") {
          const row = makeRow(cfg);
          const label = document.createElement("label");
          label.textContent = cfg.label;
          label.style.minWidth = "120px";
          label.style.textAlign = "right";
          label.style.marginRight = "5px";
          row.appendChild(label);
          const prog = document.createElement("progress");
          prog.value = cfg.value;
          prog.max = cfg.max;
          prog.style.flex = "1";
          row.appendChild(prog);
          const span = document.createElement("span");
          span.textContent = cfg.value + "/" + cfg.max;
          span.className = "flat-readout";
          span.style.minWidth = "40px";
          span.style.textAlign = "right";
          row.appendChild(span);
          parent.appendChild(row);
          idToEl[cfg.id] = { el: prog, cfg };
          continue;
        }

        if (cfg.type === "dropdown") {
          const row = makeRow(cfg);
          if (cfg.label) {
            const label = document.createElement("label");
            label.textContent = cfg.label;
            label.style.minWidth = "120px";
          label.style.textAlign = "right";
          label.style.marginRight = "5px";
            row.appendChild(label);
          }
          if (cfg.visible === false) {
            row.style.display = "none";
          }
          const select = document.createElement("select");
          select.style.flex = "0 0 160px";
          select.style.width = "160px";
          select.style.maxWidth = "160px";
          for (const opt of (cfg.options || [])) {
            const option = document.createElement("option");
            option.value = opt;
            option.textContent = opt;
            if (opt === cfg.value) option.selected = true;
            select.appendChild(option);
          }
          select.addEventListener("change", () => {
            model.set("_children_values", { [cfg.id]: select.value });
            model.save_changes();
          });
          row.appendChild(select);
          parent.appendChild(row);
          idToEl[cfg.id] = { el: select, cfg };
          continue;
        }

        if (cfg.type === "sandwich") {
          const row = makeRow(cfg);
          const l1 = document.createElement("span");
          l1.textContent = cfg.label1;
          l1.style.whiteSpace = "nowrap";
          l1.style.minWidth = "120px";
          l1.style.textAlign = "right";
          l1.style.marginRight = "5px";
          row.appendChild(l1);
          const input = document.createElement("input");
          input.type = typeof cfg.value === "number" ? "number" : "text";
          input.value = cfg.value;
          input.style.flex = "0 0 160px";
          input.style.width = "160px";
          input.style.maxWidth = "160px";
          row.appendChild(input);
          const l2 = document.createElement("span");
          l2.textContent = cfg.label2;
          l2.style.whiteSpace = "nowrap";
          l2.style.minWidth = "120px";
          l2.style.textAlign = "left";
          l2.style.marginLeft = "5px";
          row.appendChild(l2);
          parent.appendChild(row);

          input.addEventListener("change", () => {
            const val = typeof cfg.value === "number" ? parseFloat(input.value) : input.value;
            model.set("_children_values", { [cfg.id]: val });
            model.save_changes();
          });
          idToEl[cfg.id] = { el: input, cfg };
          continue;
        }

        if (cfg.type === "labeled") {
          const row = makeRow(cfg);
          const label = document.createElement("span");
          label.textContent = cfg.label;
          label.style.whiteSpace = "nowrap";
          row.appendChild(label);
          const input = document.createElement("input");
          input.type = typeof cfg.value === "number" ? "number" : "text";
          input.value = cfg.value;
          input.style.flex = "0 0 160px";
          input.style.width = "160px";
          input.style.maxWidth = "160px";
          row.appendChild(input);
          parent.appendChild(row);

          input.addEventListener("change", () => {
            const val = typeof cfg.value === "number" ? parseFloat(input.value) : input.value;
            model.set("_children_values", { [cfg.id]: val });
            model.save_changes();
          });
          idToEl[cfg.id] = { el: input, cfg };
          continue;
        }

        if (cfg.type === "range_slider") {
          const row = makeRow(cfg);
          const label = document.createElement("label");
          label.textContent = cfg.label;
          label.style.minWidth = "120px";
          label.style.textAlign = "right";
          label.style.marginRight = "5px";
          row.appendChild(label);
          const rangeVal = cfg.value || [0, 0];
          const low = document.createElement("input");
          low.type = "number";
          low.value = rangeVal[0];
          low.step = cfg.step;
          low.style.flex = "1";
          row.appendChild(low);
          const dash = document.createElement("span");
          dash.textContent = "-";
          row.appendChild(dash);
          const high = document.createElement("input");
          high.type = "number";
          high.value = rangeVal[1];
          high.step = cfg.step;
          high.style.flex = "1";
          row.appendChild(high);
          parent.appendChild(row);

          function updateRange() {
            model.set("_children_values", { [cfg.id]: [parseFloat(low.value), parseFloat(high.value)] });
            model.save_changes();
          }
          low.addEventListener("change", updateRange);
          high.addEventListener("change", updateRange);
          idToEl[cfg.id] = { el: low, cfg };
          continue;
        }

        const row = makeRow(cfg);
        if (cfg.label !== undefined && cfg.label !== "") {
          const label = document.createElement("label");
          label.textContent = cfg.label;
          label.style.minWidth = "120px";
          label.style.textAlign = "right";
          label.style.marginRight = "5px";
          row.appendChild(label);
        }
        if (cfg.visible === false) {
          row.style.display = "none";
        }

        let input;
        if (cfg.type === "number") {
          input = document.createElement("input");
          input.type = "number";
          input.step = cfg.step || "any";
          input.value = cfg.value;
          if (cfg.min !== null && cfg.min !== undefined) input.min = cfg.min;
          if (cfg.max !== null && cfg.max !== undefined) input.max = cfg.max;
          input.disabled = cfg.disabled;
        } else if (cfg.type === "checkbox") {
          input = document.createElement("input");
          input.type = "checkbox";
          input.checked = cfg.value;
        } else if (cfg.type === "slider") {
          input = document.createElement("input");
          input.type = "range";
          input.min = cfg.min;
          input.max = cfg.max;
          input.step = cfg.step;
          input.value = cfg.value;
          if (cfg.disabled) input.disabled = true;
          const readout = document.createElement("span");
          readout.textContent = fmt(cfg.value, cfg.readout_format);
          readout.className = "flat-readout";
          readout.style.minWidth = "40px";
          readout.style.textAlign = "right";
          row.appendChild(readout);

          function sliderUpdate() {
            const val = cfg.type === "slider" && Number.isInteger(cfg.step) && Number.isInteger(cfg.value)
              ? parseInt(input.value) : parseFloat(input.value);
            const newValues = { ...model.get("_children_values") };
            newValues[cfg.id] = val;
            model.set("_children_values", newValues);
            model.save_changes();
            readout.textContent = fmt(val, cfg.readout_format);
          }
          input.addEventListener("input", () => {
            draggingSliders.add(cfg.id);
            const val = cfg.type === "slider" && Number.isInteger(cfg.step) && Number.isInteger(cfg.value)
              ? parseInt(input.value) : parseFloat(input.value);
            readout.textContent = fmt(val, cfg.readout_format);
            const _cu = _cuState.has(cfg.continuous_update_key)
              ? _cuState.get(cfg.continuous_update_key)
              : cfg.continuous_update;
            if (_cu !== false) {
              if (!_pendingSentBySlider.has(cfg.id)) _pendingSentBySlider.set(cfg.id, []);
              _pendingSentBySlider.get(cfg.id).push(val);
              // Send only this slider's value, not the full dict.  Spreading
              // model.get("_children_values") would include stale sibling-widget
              // values (e.g. vwidget) whose Python echo hasn't arrived yet.
              // Python would then apply that stale value, reverting axis.index.
              model.set("_children_values", { [cfg.id]: val });
              model.save_changes();
            }
          });
          input.addEventListener("change", () => {
            draggingSliders.delete(cfg.id);
            if (cfg.continuous_update === false) {
              sliderUpdate();
            } else {
              // With continuous_update=true the input event already sent the
              // final value to Python.  Calling sliderUpdate here would spread
              // stale sibling-widget values (e.g. vwidget) whose Python echo
              // has not yet arrived, causing Python to revert axis.index.
              const val = Number.isInteger(cfg.step) && Number.isInteger(cfg.value)
                ? parseInt(input.value) : parseFloat(input.value);
              readout.textContent = fmt(val, cfg.readout_format);
            }
          });
        } else {
          input = document.createElement("input");
          input.type = "text";
          input.value = cfg.value;
          if (cfg.disabled) input.disabled = true;
        }

        if (cfg.type === "slider") {
          if (cfg.slider_width) {
            input.style.flex = `0 0 ${cfg.slider_width}`;
            input.style.width = cfg.slider_width;
            input.style.maxWidth = cfg.slider_width;
          } else {
            input.style.flex = "1";
          }
        } else {
          input.style.flex = "0 0 160px";
          input.style.width = "160px";
          input.style.maxWidth = "160px";
        }
        let colorInput = null;
        if (cfg.is_color) {
          colorInput = document.createElement("input");
          colorInput.type = "color";
          colorInput.value = colorPickerValue(cfg.value);
          if (cfg.disabled) colorInput.disabled = true;
          colorInput.style.flex = "0 0 32px";
          colorInput.style.width = "32px";
          colorInput.style.height = "32px";
          colorInput.style.padding = "0";
          colorInput.style.border = "none";
          colorInput.style.background = "transparent";
        }
        row.appendChild(input);
        if (colorInput) {
          row.appendChild(colorInput);
        }
        parent.appendChild(row);

        if (cfg.type !== "slider") {
          input.addEventListener("change", () => {
            let val;
            if (cfg.type === "number") val = parseFloat(input.value);
            else if (cfg.type === "checkbox") val = input.checked;
            else val = input.value;
            model.set("_children_values", { [cfg.id]: val });
            model.save_changes();
            if (colorInput) {
              colorInput.value = colorPickerValue(input.value);
            }
          });
          if (colorInput) {
            colorInput.addEventListener("change", () => {
              input.value = colorInput.value;
              model.set("_children_values", { [cfg.id]: colorInput.value });
              model.save_changes();
            });
          }
        }

        idToEl[cfg.id] = { el: input, colorEl: colorInput, cfg };
      }
      return () => {
        window.removeEventListener("mouseup", _onMouseUp);
        window.removeEventListener("touchend", _onMouseUp);
      };
    }
    export default { render };
    """
    _children_config = traitlets.List().tag(sync=True)
    _children_values = traitlets.Dict(default_value={}).tag(sync=True)
    _layout = traitlets.Unicode("vertical").tag(sync=True)
    _closed = traitlets.Bool(False).tag(sync=True)

    def close(self):
        self._closed = True
        super().close()
