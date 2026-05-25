<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-05-25 | Updated: 2026-05-25 -->

# examples

## Purpose
This directory contains the user-facing notebook examples for the extension. The examples demonstrate the supported Jupyter and Marimo workflows without the older debug/QA scripts that were removed during cleanup.

## Key Files

| File | Description |
|------|-------------|
| `comparison_notebook.ipynb` | Clean side-by-side comparison of representative `ipywidgets` and `anywidget` HyperSpy GUIs using `display=False` for paired display. |
| `jupyter_anywidget_example.ipynb` | Practical Jupyter Notebook / JupyterLab walkthrough showing the default `display=True` workflow and when `display=False` is useful. |
| `marimo_anywidget_example.py` | Marimo app example showing explicit `mo.ui.anywidget(...)` embedding from `display=False` results. |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| *(none)* | The examples directory is intentionally flat and currently contains only the three maintained examples. |

## For AI Agents

### Working In This Directory
- Keep examples user-facing and minimal; do not reintroduce debug or QA utility scripts here.
- Prefer examples that match documented supported environments and current runtime behavior.
- Jupyter notebooks should be stored without bulky saved outputs unless there is a strong reason otherwise.

### Testing Requirements
- Validate notebook JSON structure after editing `.ipynb` files.
- For Marimo example changes, run at least a lint/LSP pass and, when possible, a focused regression test set covering the related widgets.
- Update `README.md` example links if filenames or supported launch paths change.

### Common Patterns
- Jupyter examples treat `display=True` as the normal path.
- Marimo examples use `display=False` plus `mo.ui.anywidget(...)` for explicit layout control.
- Comparison flows often use `toolkit="ipywidgets"` and `toolkit="anywidget"` side by side to demonstrate parity.

## Dependencies

### Internal
- Reflects the public workflows described in `README.md` and `docs/user-guide.md`.
- Exercises GUI builders from the core package modules.

### External
- HyperSpy, anywidget, and ipywidgets for the Jupyter examples.
- Marimo for the app-style example.

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
