"""Reusable anywidget widget classes for hyperspy_gui_anywidget.

Each class is an ``anywidget.AnyWidget`` subclass with an inline ``_esm``
JavaScript string. No build step is required.
"""

import traitlets
from anywidget.widget import AnyWidget


class FloatTextWidget(AnyWidget):
    """A float input widget with a label."""
    _esm = """
    function render({ model, el }) {
      const description = model.get("description");
      const value = model.get("value");

      el.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
          <label style="min-width: 120px;">${description}</label>
          <input type="number" step="any" value="${value}" style="flex: 1;">
        </div>
      `;
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
    }
    export default { render };
    """
    value = traitlets.Float(0.0).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)


class TextWidget(AnyWidget):
    """A text input widget with a label."""
    _esm = """
    function render({ model, el }) {
      const description = model.get("description");
      const value = model.get("value");
      const disabled = model.get("disabled");

      el.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
          <label style="min-width: 120px;">${description}</label>
          <input type="text" value="${value}" ${disabled ? "disabled" : ""} style="flex: 1;">
        </div>
      `;
      const input = el.querySelector("input");
      const label = el.querySelector("label");

      input.addEventListener("change", () => {
        model.set("value", input.value);
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
    }
    export default { render };
    """
    value = traitlets.Unicode("").tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)
    disabled = traitlets.Bool(False).tag(sync=True)


class IntTextWidget(AnyWidget):
    """An integer input widget with a label."""
    _esm = """
    function render({ model, el }) {
      const description = model.get("description");
      const value = model.get("value");
      const disabled = model.get("disabled");

      el.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
          <label style="min-width: 120px;">${description}</label>
          <input type="number" value="${value}" ${disabled ? "disabled" : ""} style="flex: 1;">
        </div>
      `;
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
    }
    export default { render };
    """
    value = traitlets.Int(0).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)
    disabled = traitlets.Bool(False).tag(sync=True)


class IntSliderWidget(AnyWidget):
    """An integer range slider widget with a label and readout."""
    _esm = """
    function render({ model, el }) {
      const min = model.get("min");
      const max = model.get("max");
      const value = model.get("value");
      const description = model.get("description");
      const continuous_update = model.get("continuous_update");

      el.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
          <label style="min-width: 120px;">${description}</label>
          <input type="range" min="${min}" max="${max}" value="${value}" style="flex: 1;">
          <span class="readout" style="min-width: 40px; text-align: right;">${value}</span>
        </div>
      `;
      const input = el.querySelector("input");
      const readout = el.querySelector(".readout");
      const label = el.querySelector("label");

      function updateValue() {
        const val = parseInt(input.value);
        model.set("value", val);
        model.save_changes();
        readout.textContent = val;
      }

      if (continuous_update) {
        input.addEventListener("input", updateValue);
      } else {
        input.addEventListener("change", updateValue);
      }

      model.on("change:value", () => {
        const val = model.get("value");
        input.value = val;
        readout.textContent = val;
      });

      model.on("change:min", () => {
        input.min = model.get("min");
      });

      model.on("change:max", () => {
        input.max = model.get("max");
      });

      model.on("change:description", () => {
        label.textContent = model.get("description");
      });
    }
    export default { render };
    """
    value = traitlets.Int(0).tag(sync=True)
    min = traitlets.Int(0).tag(sync=True)
    max = traitlets.Int(100).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)
    continuous_update = traitlets.Bool(True).tag(sync=True)

    @traitlets.validate('value')
    def _validate_value(self, proposal):
        value = proposal['value']
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
      const continuous_update = model.get("continuous_update");

      el.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
          <label style="min-width: 120px;">${description}</label>
          <input type="range" min="${min}" max="${max}" step="${step}" value="${value}" style="flex: 1;">
          <span class="readout" style="min-width: 60px; text-align: right;">${value}</span>
        </div>
      `;
      const input = el.querySelector("input");
      const readout = el.querySelector(".readout");
      const label = el.querySelector("label");

      function updateValue() {
        const val = parseFloat(input.value);
        model.set("value", val);
        model.save_changes();
        readout.textContent = val;
      }

      if (continuous_update) {
        input.addEventListener("input", updateValue);
      } else {
        input.addEventListener("change", updateValue);
      }

      model.on("change:value", () => {
        const val = model.get("value");
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
    }
    export default { render };
    """
    value = traitlets.Float(0.0).tag(sync=True)
    min = traitlets.Float(0.0).tag(sync=True)
    max = traitlets.Float(100.0).tag(sync=True)
    step = traitlets.Float(1.0).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)
    continuous_update = traitlets.Bool(True).tag(sync=True)

    @traitlets.validate('value')
    def _validate_value(self, proposal):
        value = proposal['value']
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

      el.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
          <label style="min-width: 120px;">${description}</label>
          <input type="number" step="${step}" value="${value}" ${disabled ? "disabled" : ""} style="flex: 1;">
        </div>
      `;
      const input = el.querySelector("input");
      const label = el.querySelector("label");

      input.addEventListener("change", () => {
        let val = parseFloat(input.value);
        if (val < min) val = min;
        if (val > max) val = max;
        model.set("value", val);
        model.save_changes();
      });

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
    }
    export default { render };
    """
    value = traitlets.Float(0.0).tag(sync=True)
    min = traitlets.Float(0.0).tag(sync=True)
    max = traitlets.Float(100.0).tag(sync=True)
    step = traitlets.Float(1.0).tag(sync=True)
    description = traitlets.Unicode("").tag(sync=True)
    disabled = traitlets.Bool(False).tag(sync=True)

    @traitlets.validate('value')
    def _validate_value(self, proposal):
        value = proposal['value']
        return min(max(value, self.min), self.max)


def _widget_to_json(x, obj):
    if isinstance(x, dict):
        return {k: _widget_to_json(v, obj) for k, v in x.items()}
    elif isinstance(x, (list, tuple)):
        return [_widget_to_json(v, obj) for v in x]
    elif hasattr(x, 'model_id'):
        return "IPY_MODEL_" + x.model_id
    else:
        return x

widget_serialization = {
    'to_json': _widget_to_json,
    'from_json': None
}

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
          <label style="min-width: 120px;">${description}</label>
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
      const value = model.get("value");
      const description = model.get("description");
      el.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
          <label style="min-width: 120px;">${description}</label>
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
    @traitlets.validate('value')
    def _validate_value(self, proposal):
        value = proposal['value']
        if value % 2 == 0:
            value += 1
        return min(max(value, self.min), self.max)


class ContainerWidget(AnyWidget):
    """A layout container for child widgets.

    Renders children horizontally or vertically based on the ``layout`` trait.
    In Jupyter, child widgets are resolved via ``widget_manager.create_view``.
    In Marimo, a fallback message is shown when ``widget_manager`` is absent.
    """
    _esm = """
    function render({ model, el }) {
      const container = document.createElement("div");
      const layout = model.get("layout");

      container.style.display = "flex";
      container.style.flexDirection = layout === "horizontal" ? "row" : "column";
      container.style.gap = "10px";
      el.appendChild(container);

      const children = model.get("children");

      if (model.widget_manager) {
        Promise.all(children.map(child => model.widget_manager.create_view(child)))
          .then(views => {
            views.forEach(view => {
              container.appendChild(view.el);
              // Not all views have render, but Jupyter widget views usually handle rendering upon attachment or it's already done
            });
          });
      } else {
        container.innerHTML = "<span style='color:red;'>Child widgets rendering requires widget_manager.</span>";
      }
    }
    export default { render };
    """
    children = traitlets.List().tag(sync=True, **widget_serialization)
    layout = traitlets.Unicode("horizontal").tag(sync=True)
