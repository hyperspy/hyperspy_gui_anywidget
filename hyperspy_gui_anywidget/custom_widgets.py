import traitlets
from anywidget.widget import AnyWidget

class FloatTextWidget(AnyWidget):
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

class ContainerWidget(AnyWidget):
    """
    Reusable container widget that renders child widgets in its _esm.
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
