# HyperSpy GUI AnyWidget — Full Implementation Plan

## TL;DR

> **Quick Summary**: Build `hyperspy_gui_anywidget`, a 1:1 replacement for `hyperspy_gui_ipywidgets` using anywidget, targeting Marimo notebooks and environments where ipywidgets doesn't work well. Each widget function returns a single self-contained `AnyWidget` subclass with layout handled entirely in JavaScript via `_esm` and `_css`, eliminating dependency on ipywidgets container widgets (VBox/HBox/Accordion/Tab).
>
> **Deliverables**:
> - Complete Python package `hyperspy_gui_anywidget` with all 33 widget functions across 7 modules
> - `hyperspy_extension.yaml` registration for all HyperSpy toolkeys
> - TDD test suite with pytest
> - CI pipeline via GitHub Actions
> - Documentation (README, docstrings)
>
> **Estimated Effort**: Large
> **Parallel Execution**: YES - 4 waves
> **Critical Path**: Task 1 → Task 2 → Task 3 → Tasks 4-8 → Tasks 9-11 → Task 12 → Task 13 → F1-F4

---

## Context

### Original Request
Create a Python package `hyperspy_gui_anywidget` as a 1:1 replacement for `hyperspy_gui_ipywidgets` using anywidget, for environments where ipywidgets isn't supported (primarily Marimo notebooks).

### Interview Summary
**Key Discussions**:
- Scope: Full 1:1 replacement of all 33 widget functions from `hyperspy_gui_ipywidgets`
- Target: Marimo notebooks as priority, any anywidget-compatible environment
- API compatibility: Keep similar public API, deviate only for clear advantage
- JS approach: Inline ESM strings via `_esm` (no build step)
- Testing: TDD approach with pytest

**Research Findings**:
- `hyperspy_gui_ipywidgets` has 33 widget functions across 7 modules (axes, model, roi, preferences, microscope_parameters, tools, custom_widgets) plus utils
- Registration is via `hyperspy_extension.yaml` with entry point in `pyproject.toml`
- Widget functions follow pattern: `@add_display_arg` decorator → returns `{"widget": ..., "wdict": {...}}`
- anywidget is a thin layer OVER ipywidgets using ESM + traitlets — works in Marimo natively
- `link_traits` bridges Enthought traits ↔ traitlets — keep as dependency
- ipywidgets containers (VBox/HBox/Accordion/Tab) DON'T work in Marimo — layout must be handled in JS

### Metis Review
**Identified Gaps (addressed)**:
- **Container Widget Problem**: ipywidgets VBox/HBox don't work in Marimo → Each widget returns a SINGLE AnyWidget with layout in JS (resolved)
- **link_traits bridging**: Keep `link_traits` as dependency for traits↔traitlets sync (resolved)
- **add_display_arg in Marimo**: `IPython.display.display()` doesn't work in Marimo → Make decorator environment-aware (resolved)
- **Shadow DOM CSS**: Marimo places anywidget in shadow DOM → Use `_css` property for all styles (resolved)
- **ipympl dependency**: Defer matplotlib integration to v1.1 — not in scope (resolved)
- **Python version**: Match ≥3.10 (modern practice, HyperSpy 2.0 supports ≥3.9)

---

## Work Objectives

### Core Objective
Create a fully functional `hyperspy_gui_anywidget` package that replaces `hyperspy_gui_ipywidgets` for use in Marimo notebooks and any anywidget-compatible environment.

### Environment & Workflow Constraints
- **Conda environment**: All work must be done in the `hyperspy-dev` conda environment. Activate it before any work: `conda activate hyperspy-dev`
- **Package installation**: Install packages in the `hyperspy-dev` environment using `conda` (preferred) or `pip` (if not available via conda)
- **HyperSpy modifications**: If changes to HyperSpy itself are required, branch from `RELEASE_next_minor` or `RELEASE_next_patch` as appropriate, following HyperSpy's contribution guidelines
- **Git branching**: For this package itself, use feature branches with conventional commit messages

### Concrete Deliverables
- `pyproject.toml` with entry point and dependencies
- `hyperspy_extension.yaml` with all 33 toolkey mappings under toolkit `anywidget:`
- 7 source modules: `axes.py`, `model.py`, `roi.py`, `preferences.py`, `microscope_parameters.py`, `tools.py`, `custom_widgets.py`
- `utils.py` with environment-aware `add_display_arg` and anywidget-specific helpers
- `__init__.py` with lazy loading (matching ipywidgets pattern)
- `conftest.py` with test fixtures
- Test suite: 7 test modules matching source modules, TDD approach
- `README.md` with installation and usage instructions
- `.github/workflows/ci.yml` for CI
- `LICENSE` file (GPLv3, matching HyperSpy ecosystem)

### Definition of Done
- [ ] `pip install -e .` succeeds
- [ ] `import hyperspy_gui_anywidget` succeeds
- [ ] `hs.signals.Signal1D([1,2,3]).gui(toolkit="anywidget", display=False)` works
- [ ] All 33 widget functions return `{"widget": AnyWidget, "wdict": {...}}`
- [ ] ROI widget tests pass: modify widget → HyperSpy object updates, modify HyperSpy → widget updates
- [ ] Works in both Jupyter and Marimo (manually verified with Marimo notebook)

### Must Have
- All 33 widget functions registered in `hyperspy_extension.yaml`
- Every widget works with `display=False` (returns wdict dict)
- `link_traits` used for traits↔traitlets synchronization
- `add_display_arg` works in both Jupyter and Marimo
- Each widget is a single `AnyWidget` subclass with self-contained layout
- All tests pass with pytest
- Inline `_esm` JS for all widgets (no build step)

### Must NOT Have (Guardrails)
- NO ipywidgets container widgets (VBox, HBox, Accordion, Tab, Layout) — they don't work in Marimo
- NO unconditional `IPython.display.display()` — doesn't work in Marimo
- NO ipympl dependency — deferred to v1.1
- NO JavaScript build step (no esbuild, no vite, no npm) — inline `_esm` only
- NO unnecessary abstraction — keep it simple, follow ipywidgets patterns where sensible
- NO AI-generated code bloat: excessive comments, unnecessary abstractions, generic variable names
- NO placeholder/stub implementations — every widget must be functional

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.
> Acceptance criteria requiring "user manually tests/confirms" are FORBIDDEN.

### Test Decision
- **Infrastructure exists**: NO (greenfield project)
- **Automated tests**: YES (TDD)
- **Framework**: pytest
- **TDD workflow**: Each task follows RED (failing test) → GREEN (minimal impl) → REFACTOR

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Python package**: Use `pytest` — run tests, assert pass count, check coverage
- **Widget behavior**: Use `pytest` — create HyperSpy objects, call `.gui(toolkit="anywidget", display=False)`, assert wdict structure
- **Registration**: Use Bash (Python) — `import hyperspy.api as hs`, verify toolkit appears
- **Marimo**: Agent creates temporary notebook, validates widget rendering

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately - foundation):
├── Task 1: Project scaffolding + config [quick]
└── Task 2: Utils module with TDD [unspecified-high]

Wave 2 (After Wave 1 - POC + simple modules):
├── Task 3: Proof-of-concept widget + Marimo validation [deep]
├── Task 4: ROI widgets (6 functions) with TDD [unspecified-high]
├── Task 5: Axes widgets (3 functions) with TDD [unspecified-high]
├── Task 6: Preferences widgets (2 functions) with TDD [quick]
└── Task 7: Microscope parameters widgets (3 functions) with TDD [unspecified-high]

Wave 3 (After Wave 2 - complex modules, MAX PARALLEL):
├── Task 8: Model widgets (7 functions) with TDD [deep]
├── Task 9: Tools Part 1 — Calibration & range widgets (6 functions) with TDD [unspecified-high]
├── Task 10: Tools Part 2 — Smoothing & processing widgets (7 functions) with TDD [unspecified-high]
└── Task 11: Tools Part 3 — Complex tool widgets (4 functions) with TDD [deep]

Wave 4 (After Wave 3 - integration & docs):
├── Task 12: Integration tests + CI pipeline [unspecified-high]
└── Task 13: Documentation — README, docstrings, usage examples [writing]

Wave FINAL (After ALL tasks — 4 parallel reviews, then user okay):
├── F1: Plan compliance audit (oracle)
├── F2: Code quality review (unspecified-high)
├── F3: Real manual QA in Jupyter + Marimo (unspecified-high)
└── F4: Scope fidelity check (deep)
-> Present results -> Get explicit user okay

Critical Path: Task 1 → Task 2 → Task 3 → Tasks 4-7 → Tasks 8-11 → Task 12 → Task 13 → F1-F4 → user okay
Parallel Speedup: ~60% faster than sequential
Max Concurrent: 5 (Wave 2)
```

### Dependency Matrix

| Task | Depends On | Blocks |
|------|-----------|--------|
| 1 | — | 2-13 |
| 2 | 1 | 3-11 |
| 3 | 2 | 4-13 (validates architecture) |
| 4 | 2, 3 | 12, 13 |
| 5 | 2, 3 | 12, 13 |
| 6 | 2, 3 | 12, 13 |
| 7 | 2, 3 | 12, 13 |
| 8 | 2, 3 | 12, 13 |
| 9 | 2, 3 | 12, 13 |
| 10 | 2, 3 | 12, 13 |
| 11 | 2, 3 | 12, 13 |
| 12 | 4-11 | 13 |
| 13 | 12 | F1-F4 |
| F1 | 13 | — |
| F2 | 13 | — |
| F3 | 13 | — |
| F4 | 13 | — |

### Agent Dispatch Summary

- **Wave 1**: 2 tasks — T1 `quick`, T2 `unspecified-high`
- **Wave 2**: 5 tasks — T3 `deep`, T4 `unspecified-high`, T5 `unspecified-high`, T6 `quick`, T7 `unspecified-high`
- **Wave 3**: 4 tasks — T8 `deep`, T9 `unspecified-high`, T10 `unspecified-high`, T11 `deep`
- **Wave 4**: 2 tasks — T12 `unspecified-high`, T13 `writing`
- **FINAL**: 4 tasks — F1 `oracle`, F2 `unspecified-high`, F3 `unspecified-high`, F4 `deep`

---

## TODOs

- [ ] 1. Project Scaffolding + Configuration

  **What to do**:
  - Activate the `hyperspy-dev` conda environment: `conda activate hyperspy-dev`
  - Verify the environment has hyperspy, anywidget, link_traits, and pytest installed: `conda list | grep -E "hyperspy|anywidget|link-traits|pytest"`; install any missing packages via `conda install` or `pip install`
  - Initialize git repo with `git init`
  - Create `pyproject.toml` modeled after hyperspy_gui_ipywidgets but with these differences:
    - `name = "hyperspy_gui_anywidget"`
    - `dependencies = ["hyperspy>=2.3.0", "anywidget>=0.9.0", "link_traits", "traitlets>=5.0"]`
    - No `ipympl` dependency (deferred)
    - Entry point: `[project.entry-points."hyperspy.extensions"] hyperspy_gui_anywidget = "hyperspy_gui_anywidget"`
    - Build system: `hatchling` (modern, used by anywidget)
    - Python ≥3.10
    - Optional dev deps: `pytest`, `pytest-cov`, `ruff`, `marimo`
  - Create package structure:
    ```
    hyperspy_gui_anywidget/
    ├── __init__.py          (lazy loading pattern from ipywidgets ref)
    ├── conftest.py           (disable traitsui, enable anywidget)
    ├── hyperspy_extension.yaml  (all 33 mappings, toolkit: anywidget)
    ├── utils.py              (placeholder, filled in Task 2)
    ├── axes.py               (placeholder)
    ├── model.py              (placeholder)
    ├── roi.py                (placeholder)
    ├── preferences.py        (placeholder)
    ├── microscope_parameters.py (placeholder)
    ├── tools.py              (placeholder)
    ├── custom_widgets.py     (placeholder)
    └── tests/
        ├── __init__.py
        └── utils.py          (KWARGS dict with toolkit="anywidget", display=False)
    ```
  - Create `.gitignore` (Python, pytest, ruff cache, .egg-info, __pycache__)
  - Create `LICENSE` file (GPLv3, matching HyperSpy ecosystem)
  - Create empty README.md (placeholder, filled in Task 13)
  - Write TDD test first: `tests/test_import.py` that verifies `import hyperspy_gui_anywidget` and checks `__version__` exists
  - Implement `__init__.py` with lazy loading pattern (matching ipywidgets ref: `__getattr__` + `importlib.import_module`)
  - Implement `hyperspy_extension.yaml` with ALL 33 toolkey→function mappings (change toolkit name from `ipywidgets:` to `anywidget:`, change function name suffixes from `_ipy` to `_aw`, change module from `hyperspy_gui_ipywidgets` to `hyperspy_gui_anywidget`)
  - Run `pip install -e .` and verify it succeeds
  - Run `python -c "import hyperspy_gui_anywidget"` and verify no errors

  **Must NOT do**:
  - Do NOT include `ipympl` in dependencies
  - Do NOT include `ipywidgets` in dependencies (it comes transitively via anywidget, but we don't import it directly)
  - Do NOT create any npm/JS build configuration
  - Do NOT use `setuptools` build backend — use `hatchling`

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Scaffolding task, well-defined structure, reference implementation available
  - **Skills**: `[]`
  - **Skills Evaluated but Omitted**:
    - `git-master`: Not needed for scaffolding, will commit later

  **Parallelization**:
  - **Can Run In Parallel**: NO (foundation for all other tasks)
  - **Parallel Group**: Wave 1 (with Task 2)
  - **Blocks**: Tasks 2-13, F1-F4
  - **Blocked By**: None (can start immediately)

  **References (CRITICAL - Be Exhaustive)**:

  **Pattern References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/pyproject.toml` — Copy structure, adapt package name, dependencies, entry point
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/__init__.py` — Lazy loading pattern using `__getattr__` + `importlib.import_module`
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/hyperspy_extension.yaml` — Copy ALL 33 toolkey mappings, change toolkit name to `anywidget:`, function suffixes to `_aw`, module to `hyperspy_gui_anywidget`

  **API/Type References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/conftest.py` — Test fixture pattern: disable traitsui, enable toolkit
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/tests/utils.py` — `KWARGS` dict pattern for tests

  **External References**:
  - Hatchling build system: https://hatch.pypa.io/latest/
  - anywidget pyproject.toml pattern: see production examples in research findings

  **WHY Each Reference Matters**:
  - ipywidgets `pyproject.toml`: Exact dependencies format, classifier list, optional-dependencies structure to copy
  - ipywidgets `__init__.py`: Lazy module loading pattern that HyperSpy relies on
  - ipywidgets `hyperspy_extension.yaml`: Complete list of 33 toolkeys — must map ALL of them
  - ipywidgets `conftest.py`: Pattern for test fixture that enables/disables GUI toolkits
  - ipywidgets `tests/utils.py`: `KWARGS = {"toolkit": "ipywidgets", "display": False}` — change to `"anywidget"`

  **Acceptance Criteria**:

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Package installs and imports correctly
    Tool: Bash
    Preconditions: `hyperspy-dev` conda environment activated
    Steps:
      1. Run `conda activate hyperspy-dev && pip install -e /Users/francisco/Git/hyperspy_gui_anywidget/`
      2. Run `python -c "import hyperspy_gui_anywidget; print(hyperspy_gui_anywidget.__version__)"`
    Expected Result: Version string printed, no import errors
    Failure Indicators: ImportError, ModuleNotFoundError
    Evidence: .sisyphus/evidence/task-1-install-import.txt

  Scenario: hyperspy_extension.yaml has all 33 toolkey mappings
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `python -c "import yaml; data = yaml.safe_load(open('hyperspy_gui_anywidget/hyperspy_extension.yaml')); assert len(data['GUI']['widgets']['anywidget']) == 33, f'Expected 33, got {len(data[\"GUI\"][\"widgets\"][\"anywidget\"])}'; print('OK: 33 mappings')"`
    Expected Result: "OK: 33 mappings" printed
    Failure Indicators: AssertionError with count mismatch
    Evidence: .sisyphus/evidence/task-1-yaml-mappings.txt

  Scenario: Entry point is discoverable by HyperSpy
    Tool: Bash
    Preconditions: Package installed, hyperspy installed
    Steps:
      1. Run `python -c "from importlib.metadata import entry_points; eps = entry_points(); gui_eps = [ep for ep in eps.get('hyperspy.extensions', []) if ep.name == 'hyperspy_gui_anywidget']; assert len(gui_eps) == 1, 'Entry point not found'; print('OK: entry point found')"`
    Expected Result: "OK: entry point found" printed
    Failure Indicators: AssertionError
    Evidence: .sisyphus/evidence/task-1-entry-point.txt
  ```

  **Commit**: YES (groups with Task 2)
  - Message: `feat(init): scaffold project structure and configuration`
  - Files: `pyproject.toml`, `__init__.py`, `hyperspy_extension.yaml`, `conftest.py`, `tests/__init__.py`, `tests/utils.py`, `.gitignore`, `LICENSE`, `README.md`, all placeholder source modules
  - Pre-commit: `pip install -e . && python -c "import hyperspy_gui_anywidget"`

- [ ] 2. Utils Module with TDD

  **What to do**:
  - Write tests first in `tests/test_utils.py`:
    - `test_add_display_arg_returns_wdict_when_display_false` — decorator wraps function that returns dict with "widget" and "wdict" keys, call with `display=False`, assert wdict returned
    - `test_add_display_arg_displays_widget_in_jupyter` — mock `IPython.display.display`, call with `display=True`, verify mock called with widget
    - `test_add_display_arg_does_not_display_in_marimo` — mock environment detection, verify display not called in Marimo context
    - `test_labelme_creates_labeled_widget` — verify labelme returns a widget with label and input
    - `test_enum2dropdown_creates_dropdown` — verify dropdown options match trait values
  - Implement `utils.py`:
    - `add_display_arg(f)` — decorator that:
      - Pops `display` kwarg (default True)
      - If `display=True` AND running in Jupyter (not Marimo): calls `IPython.display.display(wdict["widget"])`
      - If `display=True` AND running in Marimo: just returns wdict (Marimo handles display)
      - If `display=False`: returns wdict
      - Environment detection: check for `marimo` in `sys.modules` or use a simpler heuristic
    - `labelme(label, widget)` — anywidget version: creates an AnyWidget with label and input field in a flex row layout
    - `labelme_sandwich(label1, widget, label2)` — similar but with labels on both sides
    - `get_label(trait, label)` — generates label text from trait metadata (same logic as ipywidgets version)
    - `enum2dropdown(trait, **kwargs)` — creates an AnyWidget dropdown with trait's enum values
    - `float2floattext(trait, label)` — creates labeled FloatText AnyWidget
    - `str2text(trait, label)` — creates labeled Text AnyWidget
    - `set_title_container(container, titles)` — handles tab/accordion titles (adapted for anywidget approach)
  - Each helper creates a small AnyWidget subclass with inline `_esm` for the layout
  - Run tests: `pytest tests/test_utils.py -v`

  **Must NOT do**:
  - Do NOT import ipywidgets directly (VBox, HBox, Label, etc.) — use AnyWidget with inline JS layout
  - Do NOT use `IPython.display.display()` unconditionally — must be environment-aware
  - Do NOT create separate container widget classes (AnyVBox etc.) — layout is embedded in each widget's _esm

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Requires understanding of both anywidget patterns and HyperSpy's trait system; multiple small widgets to implement
  - **Skills**: `[]`
  - **Skills Evaluated but Omitted**:
    - None needed — utils implementation is straightforward with reference

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1, though ideally after)
  - **Parallel Group**: Wave 1 (with Task 1)
  - **Blocks**: Tasks 3-11
  - **Blocked By**: Task 1 (needs pyproject.toml for install)

  **References (CRITICAL - Be Exhaustive)**:

  **Pattern References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/utils.py` — Complete utils implementation to adapt; `add_display_arg` decorator, `labelme`, `labelme_sandwich`, `get_label`, `enum2dropdown`, `float2floattext`, `str2text`, `set_title_container`
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/roi.py` — Usage of `labelme`, `labelme_sandwich`, `add_display_arg`, `link` from link_traits; this is the primary consumer of utils

  **API/Type References**:
  - anywidget.AnyWidget class with `_esm` and `_css` attributes + traitlets with `.tag(sync=True)`
  - `link_traits.link()` API: `link((obj, "trait_name"), (widget, "traitlet_name"))` for bidirectional sync

  **Test References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/tests/test_roi.py` — Pattern: create object → `obj.gui(toolkit="ipywidgets", display=False)` → assert wdict values → modify widget → assert object updated

  **External References**:
  - anywidget docs: https://anywidget.dev/en/ — AnyWidget class API, _esm pattern, _css pattern, traitlets sync

  **WHY Each Reference Matters**:
  - ipywidgets `utils.py`: Direct blueprint for every utility function — must adapt each one from ipywidgets to anywidget
  - ipywidgets `roi.py`: Shows how utils are consumed in real widgets — validates the API design
  - ipywidgets `test_roi.py`: Shows the test pattern for testing widget behavior via HyperSpy's `.gui()` method
  - anywidget docs: Needed for correct AnyWidget class definition and traitlets usage

  **Acceptance Criteria**:

  **If TDD (tests enabled)**:
  - [ ] Test file created: `hyperspy_gui_anywidget/tests/test_utils.py`
  - [ ] `pytest tests/test_utils.py -v` → PASS (all tests)

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: add_display_arg decorator works with display=False
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `python -c "from hyperspy_gui_anywidget.utils import add_display_arg; @add_display_arg
def test_func(obj, **kwargs): return {'widget': 'mock_widget', 'wdict': {}}
result = test_func(None, display=False); assert result == {'widget': 'mock_widget', 'wdict': {}}, f'Expected wdict, got {result}'"`
    Expected Result: wdict returned when display=False
    Failure Indicators: AssertionError, different return type
    Evidence: .sisyphus/evidence/task-2-display-false.txt

  Scenario: add_display_arg works in Marimo context
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `python -c "import sys; sys.modules['marimo'] = type(sys)('marimo'); from hyperspy_gui_anywidget.utils import add_display_arg; @add_display_arg
def test_func(obj, **kwargs): return {'widget': 'mock_widget', 'wdict': {}}
result = test_func(None, display=True); assert result == {'widget': 'mock_widget', 'wdict': {}}, 'Marimo should return wdict, not call IPython.display'"`
    Expected Result: wdict returned when in Marimo context (no IPython.display call)
    Failure Indicators: IPython.display.display was called, or wdict not returned
    Evidence: .sisyphus/evidence/task-2-marimo-context.txt

  Scenario: labelme creates AnyWidget with label and input
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `python -c "from hyperspy_gui_anywidget.utils import labelme; from traits.api import Undefined; widget = labelme('test_label', None); print(type(widget)); assert hasattr(widget, '_esm'), 'Should be AnyWidget with _esm'"`
    Expected Result: AnyWidget instance with _esm property
    Failure Indicators: TypeError, AttributeError
    Evidence: .sisyphus/evidence/task-2-labelme.txt
  ```

  **Commit**: YES (groups with Task 1)
  - Message: `feat(utils): add utils module with add_display_arg and helpers`
  - Files: `utils.py`, `tests/test_utils.py`
  - Pre-commit: `pytest tests/test_utils.py -v`

- [ ] 3. Proof-of-Concept Widget + Marimo Validation

  **What to do**:
  - This is the ARCHITECTURE VALIDATION task — prove the AnyWidget approach works in Marimo before building all 33 widgets
  - Implement SpanROI widget as proof-of-concept (simplest widget with bidirectional sync):
    - Write test first in `tests/test_roi.py` (partial, just SpanROI for now):
      ```python
      def test_span_roi_anywidget():
          roi = hs.roi.SpanROI(left=0, right=10)
          wd = roi.gui(toolkit="anywidget", display=False)["anywidget"]["wdict"]
          assert wd["left"].value == 0
          assert wd["right"].value == 10
          wd["left"].value = -10
          wd["right"].value = 0
          assert roi.left == -10
          assert roi.right == 0
      ```
    - Implement `roi.py` with `span_roi_aw` function:
      - Create `SpanROIWidget(anywidget.AnyWidget)` class with `_esm` inline JS
      - Traitlets: `left = traitlets.Float(0).tag(sync=True)`, `right = traitlets.Float(10).tag(sync=True)`
      - `_esm`: Two labeled FloatText inputs in a flex row
      - `_css`: Styling for layout (compatible with shadow DOM)
      - Use `link_traits.link()` to sync HyperSpy ROI → widget and widget → HyperSpy ROI
      - Return `{"widget": widget_instance, "wdict": {"left": left_widget, "right": right_widget}}`
    - **CRITICAL DECISION**: The widget function must be a single AnyWidget that renders ALL UI elements. For SpanROI, this means the `_esm` renders both "Left" and "Right" FloatText inputs in a horizontal layout. Each synced trait becomes an AnyWidget with its own `_esm`. The container function wraps them.
    - Actually, reconsidering: For simplicity, each FloatText can be a separate small AnyWidget (like `FloatTextWidget`), and the container function returns a dict with `"widget"` being a `HBox`-equivalent layout. BUT since VBox/HBox don't work in Marimo, the container itself must be an AnyWidget that knows about its children.
    - **Final approach**: Create simple base widgets (`FloatTextWidget`, `DropdownWidget`) as AnyWidget subclasses. The `span_roi_aw` function creates instances of these, links them with `link_traits`, and returns them in wdict. The `"widget"` key points to a container AnyWidget that renders child widgets.
    - **Actually simpler approach**: Since each small widget is its own AnyWidget with its own DOM, we can return the first/primary widget and put others in wdict. Or we can compose them into a single rendering AnyWidget. Let the proof-of-concept validate which approach works in Marimo.
    - Run test: `pytest tests/test_roi.py::test_span_roi_anywidget -v`
  - Create a minimal Marimo notebook that validates rendering:
    - Create `examples/test_marimo.py` (can be run as `marimo run examples/test_marimo.py`)
    - Import hyperspy, create SpanROI, call `.gui(toolkit="anywidget")`
    - Verify widget renders and syncs
  - Create a minimal Jupyter validation script:
    - Create `examples/test_jupyter.py` that validates same in Jupyter context
  - If proof-of-concept FAILS (container approach doesn't work in Marimo):
    - Pivot to monolithic approach (each widget function creates ONE AnyWidget with all UI in its _esm)
    - Document the pivot decision in code comments
  - If proof-of-concept SUCCEEDS:
    - Lock in the architecture pattern
    - Document the pattern in a docstring in `utils.py` or `custom_widgets.py`

  **Must NOT do**:
  - Do NOT use ipywidgets containers (VBox, HBox, Accordion, Tab, Layout)
  - Do NOT import ipywidgets directly
  - Do NOT implement all 33 widgets in this task — ONLY SpanROI as proof-of-concept
  - Do NOT skip the Marimo validation step

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Architecture validation task — requires experimentation, debugging, and design decisions that affect all subsequent tasks
  - **Skills**: `[]`
  - **Skills Evaluated but Omitted**:
    - None needed — this is core implementation work

  **Parallelization**:
  - **Can Run In Parallel**: NO (validates architecture for all subsequent widget tasks)
  - **Parallel Group**: Wave 2 (starts after Task 2)
  - **Blocks**: Tasks 4-11 (architecture must be validated before volume implementation)
  - **Blocked By**: Tasks 1, 2

  **References (CRITICAL - Be Exhaustive)**:

  **Pattern References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/roi.py` — Complete ROI implementations, especially `span_roi_ipy` (lines 9-22) as the direct reference for SpanROI
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/utils.py` — `add_display_arg` decorator, `labelme` helper, `link` usage from link_traits

  **API/Type References**:
  - anywidget.AnyWidget class — `_esm` for JS render function, `_css` for styles, traitlets with `.tag(sync=True)` for state
  - `link_traits.link()` — `link((obj, "left"), (widget, "value"))` for bidirectional trait sync
  - HyperSpy ROI classes: `hs.roi.SpanROI(left=0, right=10)` — has traits `left` and `right`

  **Test References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/tests/test_roi.py` — Exact test pattern to replicate: create ROI → call `.gui()` → assert wdict values → modify widget → assert HyperSpy object updates

  **External References**:
  - anywidget docs: https://anywidget.dev/en/ — Render function signature, CSS in shadow DOM, traitlets sync
  - Marimo anywidget docs: https://docs.marimo.io/guides/3rdparty/anywidget.html — How Marimo renders anywidget

  **WHY Each Reference Matters**:
  - ipywidgets `roi.py`: Direct reference implementation — shows exactly what `span_roi_aw` must replicate
  - ipywidgets `test_roi.py`: Exact test assertions to replicate — validates bidirectional sync
  - anywidget docs: Must understand `_esm` render function, `_css` shadow DOM styling, and `.tag(sync=True)` pattern
  - Marimo anywidget docs: Must understand how Marimo renders anywidget — validates the container approach

  **Acceptance Criteria**:

  **If TDD (tests enabled)**:
  - [ ] Test file created: `hyperspy_gui_anywidget/tests/test_roi.py`
  - [ ] `pytest tests/test_roi.py::test_span_roi_anywidget -v` → PASS

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: SpanROI widget creates and synchronizes correctly
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `python -c "import hyperspy.api as hs; from hyperspy_gui_anywidget.tests.utils import KWARGS; roi = hs.roi.SpanROI(left=0, right=10); result = roi.gui(**KWARGS); wd = result['anywidget']['wdict']; assert 'left' in wd, 'left key missing'; assert 'right' in wd, 'right key missing'; assert wd['left'].value == 0; assert wd['right'].value == 10; wd['left'].value = -10; assert roi.left == -10, f'Expected -10, got {roi.left}'"`
    Expected Result: Widget created, values initialized, bidirectional sync works
    Failure Indicators: KeyError, AssertionError, ImportError
    Evidence: .sisyphus/evidence/task-3-spanroi-sync.txt

  Scenario: SpanROI widget is type AnyWidget (not ipywidgets)
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `python -c "import anywidget; import hyperspy.api as hs; from hyperspy_gui_anywidget.tests.utils import KWARGS; roi = hs.roi.SpanROI(left=0, right=10); result = roi.gui(**KWARGS); widget = result['anywidget']['widget']; assert isinstance(widget, anywidget.AnyWidget), f'Expected AnyWidget, got {type(widget)}'"`
    Expected Result: Widget is an AnyWidget instance
    Failure Indicators: TypeError, not AnyWidget
    Evidence: .sisyphus/evidence/task-3-anywidget-type.txt

  Scenario: Marimo environment doesn't crash on import
    Tool: Bash
    Preconditions: Package installed, marimo installed
    Steps:
      1. Run `python -c "import marimo; import hyperspy.api as hs; from hyperspy_gui_anywidget.tests.utils import KWARGS; roi = hs.roi.SpanROI(left=0, right=10); result = roi.gui(**KWARGS); print('Marimo context OK')"`
    Expected Result: No crash when Marimo is in sys.modules
    Failure Indicators: ImportError, RuntimeError, display-related errors
    Evidence: .sisyphus/evidence/task-3-marimo-import.txt
  ```

  **Commit**: YES
  - Message: `feat(roi): add SpanROI proof-of-concept with Marimo validation`
  - Files: `roi.py` (partial), `custom_widgets.py` (partial), `tests/test_roi.py` (partial), `examples/test_marimo.py`, `examples/test_jupyter.py`
  - Pre-commit: `pytest tests/test_roi.py::test_span_roi_anywidget -v`

- [ ] 4. ROI Widgets — Complete All 6 Functions with TDD

  **What to do**:
  - Write tests first in `tests/test_roi.py` (SpanROI test already exists from Task 3, add remaining 5):
    - `test_point1d_roi_anywidget` — Point1DROI, test value sync
    - `test_point2d_roi_anywidget` — Point2DROI, test x/y sync
    - `test_rectangular_roi_anywidget` — RectangularROI, test left/right/top/bottom sync
    - `test_circle_roi_anywidget` — CircleROI, test cx/cy/r/r_inner sync
    - `test_line2d_roi_anywidget` — Line2DROI, test x1/y1/x2/y2/linewidth sync
  - Follow the SAME pattern as ipywidgets `roi.py` but using the architecture validated in Task 3:
    - Each ROI function creates AnyWidget instances for each parameter
    - Uses `link_traits.link()` for bidirectional trait sync
    - Returns `{"widget": container_widget, "wdict": {...}}`
  - Implement all 6 widget functions in `roi.py`:
    - `span_roi_aw(obj, **kwargs)` — SpanROI (already done in Task 3, verify it still works)
    - `point1d_roi_aw(obj, **kwargs)` — Point1DROI with single FloatText
    - `point_2d_aw(obj, **kwargs)` — Point2DROI with x/y FloatText pair
    - `rectangular_roi_aw(obj, **kwargs)` — RectangularROI with 4 FloatText in 2 rows
    - `circle_roi_aw(obj, **kwargs)` — CircleROI with cx/cy/r/r_inner
    - `line2d_roi_aw(obj, **kwargs)` — Line2DROI with x1/y1/x2/y2/linewidth
  - Create `custom_widgets.py` with reusable AnyWidget base widgets:
    - `FloatTextWidget(anywidget.AnyWidget)` — labeled FloatText with value synced via traitlets
    - `ContainerWidget(anywidget.AnyWidget)` — horizontal/vertical layout container for multiple child widgets
    - These are used across ALL widget modules, not just ROI
  - Run all tests: `pytest tests/test_roi.py -v`

  **Must NOT do**:
  - Do NOT use ipywidgets containers (VBox, HBox, etc.)
  - Do NOT copy ipywidgets implementation verbatim — adapt to anywidget pattern validated in Task 3
  - Do NOT skip any of the 6 ROI widget functions

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Repetitive implementation following established pattern from Task 3
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 5, 6, 7)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 12
  - **Blocked By**: Tasks 1, 2, 3

  **References (CRITICAL)**:

  **Pattern References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/roi.py` — ALL 6 ROI implementations to adapt (span_roi, point1d_roi, point_2d, rectangular_roi, circle_roi, line2d_roi)
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/custom_widgets.py` — `OddIntSlider` pattern for custom widget creation

  **Test References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/tests/test_roi.py` — ALL 6 ROI tests with exact assertions for bidirectional trait sync

  **WHY Each Reference Matters**:
  - ipywidgets `roi.py`: Direct blueprint for each of the 6 widget functions — shows exactly which traits to link and what wdict keys to return
  - ipywidgets `test_roi.py`: Exact test assertions for each ROI type — validates that modifying widget updates HyperSpy and vice versa

  **Acceptance Criteria**:

  **If TDD**:
  - [ ] Test file exists: `tests/test_roi.py` with all 6 ROI tests
  - [ ] `pytest tests/test_roi.py -v` → PASS (6 tests, 0 failures)

  **QA Scenarios**:

  ```
  Scenario: All 6 ROI widgets create correctly and sync bidirectionally
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `python -c "
import hyperspy.api as hs
from hyperspy_gui_anywidget.tests.utils import KWARGS
# Test each ROI type
roi_types = [
    ('SpanROI', hs.roi.SpanROI(left=0, right=10), ['left', 'right']),
    ('Point1DROI', hs.roi.Point1DROI(value=5.5), ['value']),
    ('Point2DROI', hs.roi.Point2DROI(x=0, y=10), ['x', 'y']),
    ('RectangularROI', hs.roi.RectangularROI(left=0, right=10, top=-10, bottom=0), ['left', 'right', 'top', 'bottom']),
    ('CircleROI', hs.roi.CircleROI(cx=0, cy=0, r=1, r_inner=0.5), ['cx', 'cy', 'radius', 'inner_radius']),
    ('Line2DROI', hs.roi.Line2DROI(x1=0, x2=10, y1=0, y2=10), ['x1', 'x2', 'y1', 'y2', 'linewidth']),
]
for name, roi, keys in roi_types:
    result = roi.gui(**KWARGS)
    wd = result['anywidget']['wdict']
    assert all(k in wd for k in keys), f'{name} missing keys: {set(keys) - set(wd.keys())}'
    print(f'{name}: OK')
"`
    Expected Result: All 6 ROI types create successfully with expected wdict keys
    Failure Indicators: KeyError, AssertionError, ImportError
    Evidence: .sisyphus/evidence/task-4-all-roi.txt
  ```

  **Commit**: YES
  - Message: `feat(roi): complete all ROI widgets with TDD`
  - Files: `roi.py`, `custom_widgets.py`, `tests/test_roi.py`
  - Pre-commit: `pytest tests/test_roi.py -v`

- [ ] 5. Axes Widgets (3 Functions) with TDD

  **What to do**:
  - Write tests first in `tests/test_axes.py`:
    - `test_navigation_sliders` — Create Signal2D, call `s.axes_manager.gui(toolkit="anywidget", display=False)`, verify wdict structure
    - `test_data_axis_gui` — Create a DataAxis, verify axis widget
    - `test_axes_manager_gui` — Create AxesManager, verify full axes GUI
  - Implement `axes.py` with 3 widget functions:
    - `ipy_navigation_sliders` (keep naming close to ipywidgets version but consider `_aw` suffix) → `aw_navigation_sliders`
    - `_get_axis_widgets` (private helper)
    - `aw_axes_gui` (was `ipy_axes_gui`)
  - Axes widgets involve sliders (IntSlider, FloatSlider), dropdowns, and label layouts
  - Create `IntSliderWidget`, `FloatSliderWidget` in `custom_widgets.py` if not already present from Task 4
  - Follow the architecture pattern validated in Task 3 — each slider is an AnyWidget with inline _esm
  - Navigation sliders need special handling: they control navigation through signal dimensions
  - Run tests: `pytest tests/test_axes.py -v`

  **Must NOT do**:
  - Do NOT use ipywidgets IntSlider, FloatSlider — create AnyWidget equivalents
  - Do NOT import ipywidgets directly

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Moderate complexity, follows established pattern from Tasks 3-4
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 4, 6, 7)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 12
  - **Blocked By**: Tasks 1, 2, 3

  **References**:

  **Pattern References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/axes.py` — Full axes implementation with navigation sliders, axis widgets, axes manager GUI

  **Test References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/tests/test_axes.py` — Test patterns for axes GUI

  **WHY Each Reference Matters**:
  - ipywidgets `axes.py`: Shows navigation slider implementation, DataAxis widget structure, AxesManager GUI composition
  - ipywidgets `test_axes.py`: Test assertions for slider behavior and axis interaction

  **Acceptance Criteria**:

  **If TDD**:
  - [ ] `pytest tests/test_axes.py -v` → PASS (all tests)

  **QA Scenarios**:

  ```
  Scenario: Navigation sliders create and function correctly
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `python -c "import hyperspy.api as hs; from hyperspy_gui_anywidget.tests.utils import KWARGS; s = hs.signals.Signal2D([[1,2],[3,4]]); result = s.axes_manager.gui(**KWARGS); assert 'anywidget' in result; print('Navigation sliders OK')"`
    Expected Result: Signal2D axes manager GUI created successfully
    Failure Indicators: KeyError, TypeError
    Evidence: .sisyphus/evidence/task-5-axes.txt
  ```

  **Commit**: YES
  - Message: `feat(axes): add axes widgets with TDD`
  - Files: `axes.py`, `custom_widgets.py` (if updated), `tests/test_axes.py`
  - Pre-commit: `pytest tests/test_axes.py -v`

- [ ] 6. Preferences Widgets (2 Functions) with TDD

  **What to do**:
  - Write tests first in `tests/test_preferences.py`:
    - `test_preferences_widget` — Verify `hs.preferences.gui(toolkit="anywidget", display=False)` works
    - `test_exspy_preferences_widget` — Verify exspy preferences widget
  - Implement `preferences.py` with 2 widget functions:
    - `show_preferences_widget` — HyperSpy general preferences
    - `show_exspy_preferences_widget` — exSpy-specific preferences
  - Preferences widgets typically display nested dictionaries as interactive forms
  - May need accordion/tab-like layout in JS for preference categories
  - Run tests: `pytest tests/test_preferences.py -v`

  **Must NOT do**:
  - Do NOT use ipywidgets Accordion/Tab — implement in JS via _esm

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Only 2 functions, moderate complexity, follows established pattern
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 4, 5, 7)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 12
  - **Blocked By**: Tasks 1, 2, 3

  **References**:

  **Pattern References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/preferences.py` — Preferences widget implementation with accordion style layout
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/tests/test_preferences.py` — Test patterns for preferences

  **Acceptance Criteria**:

  **If TDD**:
  - [ ] `pytest tests/test_preferences.py -v` → PASS

  **QA Scenarios**:

  ```
  Scenario: Preferences widget creates and displays correctly
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `python -c "import hyperspy.api as hs; from hyperspy_gui_anywidget.tests.utils import KWARGS; result = hs.preferences.gui(**KWARGS); assert 'anywidget' in result; print('Preferences OK')"`
    Expected Result: Preferences GUI created with anywidget toolkit
    Failure Indicators: KeyError, AttributeError
    Evidence: .sisyphus/evidence/task-6-preferences.txt
  ```

  **Commit**: YES
  - Message: `feat(preferences): add preferences widgets with TDD`
  - Files: `preferences.py`, `tests/test_preferences.py`
  - Pre-commit: `pytest tests/test_preferences.py -v`

- [ ] 7. Microscope Parameters Widgets (3 Functions) with TDD

  **What to do**:
  - Write tests first in `tests/test_microscope_parameters.py`:
    - `test_eels_microscope_parameters` — EELS microscope parameters widget
    - `test_eds_sem_microscope_parameters` — EDS SEM parameters widget
    - `test_eds_tem_microscope_parameters` — EDS TEM parameters widget
  - Implement `microscope_parameters.py` with 3 widget functions:
    - `eels_microscope_parameter_aw`
    - `eds_sem_microscope_parameter_aw`
    - `eds_tem_microscope_parameter_aw`
  - These display microscope parameters (convergence angle, collection angle, etc.) as FloatText widgets
  - Follow the same pattern as ipywidgets but with AnyWidget equivalents
  - Run tests: `pytest tests/test_microscope_parameters.py -v`

  **Must NOT do**:
  - Do NOT use ipywidgets FloatText — use AnyWidget FloatTextWidget from custom_widgets

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 3 functions, similar pattern to other modules, requires understanding of exspy/HyperSpy microscope parameters
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 4, 5, 6)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 12
  - **Blocked By**: Tasks 1, 2, 3

  **References**:

  **Pattern References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/microscope_parameters.py` — All 3 microscope parameter widget implementations
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/tests/test_microscope_parameters.py` — Test patterns

  **Acceptance Criteria**:

  **If TDD**:
  - [ ] `pytest tests/test_microscope_parameters.py -v` → PASS (3 tests)

  **QA Scenarios**:

  ```
  Scenario: EELS microscope parameters widget creates correctly
    Tool: Bash
    Preconditions: Package installed, exspy installed
    Steps:
      1. Run `python -c "import exspy.api as exs; from hyperspy_gui_anywidget.tests.utils import KWARGS; s = exs.signals.EELSSpectrum([1,2,3]); result = s.microscope_parameters.gui(**KWARGS); assert 'anywidget' in result; print('EELS params OK')"` (if exspy import works; skip gracefully if not)
    Expected Result: Microscope parameters GUI created
    Failure Indicators: ImportError if exspy not available, KeyError
    Evidence: .sisyphus/evidence/task-7-microscope-params.txt
  ```

  **Commit**: YES
  - Message: `feat(microscope): add microscope parameters widgets with TDD`
  - Files: `microscope_parameters.py`, `tests/test_microscope_parameters.py`
  - Pre-commit: `pytest tests/test_microscope_parameters.py -v`

- [ ] 8. Model Widgets (7 Functions) with TDD

  **What to do**:
  - Write tests first in `tests/test_model.py`:
    - `test_parameter_widget` — Create a Parameter, test get_parameter_widget
    - `test_component_widget` — Create a Component, test get_component_widget
    - `test_model_widget` — Create a Model, test get_model_widget
    - `test_eelscl_widget` — Create EELSCLEdge Component, test get_eelscl_widget
    - `test_scalable_fixed_pattern_widget` — Create ScalableFixedPattern, test get_scalable_fixed_pattern_widget
    - `test_fit_component` — Test model.fit_component GUI
    - `test_interactive_slider_bounds` — Test slider bounds helper
  - Implement `model.py` with 7 widget functions:
    - `get_parameter_widget` — Parameter adjustment widget (sliders/floattext for each parameter trait)
    - `get_component_widget` — Component widget wrapping parameter widgets
    - `get_model_widget` — Model widget with component list and parameter controls
    - `get_eelscl_widget` — EELS edge component widget (special component type)
    - `get_scalable_fixed_pattern_widget` — Scalable fixed pattern component widget
    - `fit_component_aw` — Interactive component fitting widget with slider for position
    - `_interactive_slider_bounds` — Private helper for slider bounds
  - Model widgets are the most complex — they involve nested structures (Model → Component → Parameter), interactive sliders, and dynamic trait observation
  - Focus on making parameter ↔ widget sync work correctly with `link_traits`
  - Run tests: `pytest tests/test_model.py -v`

  **Must NOT do**:
  - Do NOT use ipywidgets containers — implement layout in _esm
  - Do NOT simplify the model widgets beyond what ipywidgets version provides — must be 1:1

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Most complex module — nested structures, many traits to sync, interactive sliders
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 9, 10, 11)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 12
  - **Blocked By**: Tasks 1, 2, 3

  **References**:

  **Pattern References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/model.py` — Complete model widget implementation (7 functions, most complex module)
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/tests/test_model.py` — Test patterns for model widgets

  **Acceptance Criteria**:

  **If TDD**:
  - [ ] `pytest tests/test_model.py -v` → PASS (7+ tests)

  **QA Scenarios**:

  ```
  Scenario: Model parameter widget creates and syncs
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `python -c "import hyperspy.api as hs; from hyperspy_gui_anywidget.tests.utils import KWARGS; s = hs.signals.Signal1D([1,2,3,4,5]); m = s.create_model(); m.append(hs.model.components1D.Gaussian()); result = m.gui(**KWARGS); assert 'anywidget' in result; print('Model widget OK')"`
    Expected Result: Model widget created with parameter controls
    Failure Indicators: ImportError, TypeError, trait sync errors
    Evidence: .sisyphus/evidence/task-8-model.txt

  Scenario: Parameter widget bidirectional sync
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `python -c "import hyperspy.api as hs; from hyperspy_gui_anywidget.tests.utils import KWARGS; g = hs.model.components1D.Gaussian(); result = g.parameters.A.gui(**KWARGS); wd = result['anywidget']['wdict']; wd['value'].value = 5.0; assert abs(g.parameters.A.value - 5.0) < 0.01, 'Parameter sync failed'"`
    Expected Result: Modifying widget value updates HyperSpy parameter
    Failure Indicators: AssertionError — sync not working
    Evidence: .sisyphus/evidence/task-8-parameter-sync.txt
  ```

  **Commit**: YES
  - Message: `feat(model): add model widgets with TDD`
  - Files: `model.py`, `tests/test_model.py`
  - Pre-commit: `pytest tests/test_model.py -v`

- [ ] 9. Tools Part 1 — Calibration & Range Widgets (6 Functions) with TDD

  **What to do**:
  - Write tests first (add to `tests/test_tools.py`):
    - `test_interactive_range_selector` — Navigation range selector widget
    - `test_calibrate` — Signal1D calibration widget
    - `test_calibrate2d` — Signal2D calibration widget
    - `test_print_edges_table` — EELS edge table display widget
  - Implement in `tools.py` (first 4+ functions, will be expanded in Tasks 10-11):
    - `interactive_range_aw` — Interactive range selector (used for selecting signal range)
    - `calibrate_aw` — Signal1D calibration GUI
    - `calibrate2d_aw` — Signal2D calibration GUI
    - `print_edges_table_aw` — EELS edge table display
  - These tools involve interactive sliders and range selection
  - Run tests: `pytest tests/test_tools.py -v -k "calibrate or range or print_edges"`

  **Must NOT do**:
  - Do NOT implement smoothing/processing widgets — those are Tasks 10-11

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Moderate complexity, follows established pattern
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 8, 10, 11)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 12
  - **Blocked By**: Tasks 1, 2, 3

  **References**:

  **Pattern References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/tools.py` — Full tools implementation, reference for calibration and range functions

  **Test References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/tests/test_tools.py` — Test patterns for tool widgets

  **Acceptance Criteria**:

  **If TDD**:
  - [ ] `pytest tests/test_tools.py -v -k "calibrate or range or print_edges"` → PASS

  **QA Scenarios**:

  ```
  Scenario: Interactive range selector creates widget
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `python -c "import hyperspy.api as hs; from hyperspy_gui_anywidget.tests.utils import KWARGS; s = hs.signals.Signal1D([1,2,3,4,5]); result = s.gui(**KWARGS); assert 'anywidget' in result; print('Range selector OK')"`
    Expected Result: Interactive range widget created
    Evidence: .sisyphus/evidence/task-9-tools-calibration.txt
  ```

  **Commit**: YES
  - Message: `feat(tools): add calibration and range tool widgets with TDD`
  - Files: `tools.py` (partial), `tests/test_tools.py` (partial)
  - Pre-commit: `pytest tests/test_tools.py -v -k "calibrate or range or print_edges"`

- [ ] 10. Tools Part 2 — Smoothing & Processing Widgets (7 Functions) with TDD

  **What to do**:
  - Write tests first (add to `tests/test_tools.py`):
    - `test_smooth_savitzky_golay` — Savitzky-Golay smoothing widget
    - `test_smooth_lowess` — LOWESS smoothing widget
    - `test_smooth_total_variation` — Total variation smoothing widget
    - `test_smooth_butterworth` — Butterworth smoothing widget
    - `test_remove_background` — Background removal widget
    - `test_remove_baseline` — Baseline removal widget
    - `test_image_contrast_editor` — Image contrast editor widget
  - Implement in `tools.py` (add to existing functions from Task 9):
    - `smooth_savitzky_golay_aw` — Savitzky-Golay filter parameters (window_length, polyorder)
    - `smooth_lowess_aw` — LOWESS smoothing parameters
    - `smooth_tv_aw` — Total variation smoothing parameters
    - `smooth_butterworth` — Butterworth filter (note: no _ipy suffix in original!)
    - `remove_background_aw` — Background removal with ROI selection
    - `remove_baseline_aw` — Baseline removal widget
    - `image_constast_editor_aw` — Note: typo in original ipywidgets function name preserved
  - These widgets involve sliders for parameters and often ROI selection
  - Run tests: `pytest tests/test_tools.py -v -k "smooth or background or baseline or contrast"`

  **Must NOT do**:
  - Do NOT implement spikes_removal or find_peaks — those are Task 11

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Moderate complexity, many similar slider-based widgets
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 8, 9, 11)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 12
  - **Blocked By**: Tasks 1, 2, 3

  **References**:

  **Pattern References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/tools.py` — Reference for smoothing and processing widgets

  **Acceptance Criteria**:

  **If TDD**:
  - [ ] `pytest tests/test_tools.py -v -k "smooth or background or baseline or contrast"` → PASS

  **QA Scenarios**:

  ```
  Scenario: Smoothing widgets create and sync parameters
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `python -c "import hyperspy.api as hs; from hyperspy_gui_anywidget.tests.utils import KWARGS; s = hs.signals.Signal1D([1,2,3,4,5,4,3,2,1]); result = s.gui(**KWARGS); assert 'anywidget' in result; print('Smoothing OK')"`
    Expected Result: Smoothing widget created
    Evidence: .sisyphus/evidence/task-10-tools-smoothing.txt
  ```

  **Commit**: YES
  - Message: `feat(tools): add smoothing and processing widgets with TDD`
  - Files: `tools.py` (partial), `tests/test_tools.py` (partial)
  - Pre-commit: `pytest tests/test_tools.py -v -k "smooth or background or baseline or contrast"`

- [ ] 11. Tools Part 3 — Complex Tool Widgets (4 Functions) with TDD

  **What to do**:
  - Write tests first (add to `tests/test_tools.py`):
    - `test_spikes_removal` — Spikes removal tool (interactive spectrum viewer)
    - `test_find_peaks2d` — 2D peak finding widget
  - Implement in `tools.py` (add remaining functions):
    - `spikes_removal_aw` — Interactive spike detection and removal (most complex tool — needs matplotlib viewer)
    - `find_peaks2D_aw` — 2D peak finding widget with threshold slider
  - These are the most complex tool widgets — `spikes_removal_ipy` involves matplotlib integration and interactive spectrum display, which may need special handling
  - For `spikes_removal_aw`: May need to create a matplotlib-display AnyWidget or defer matplotlib-dependent features
  - Run ALL tools tests: `pytest tests/test_tools.py -v`

  **Must NOT do**:
  - Do NOT depend on ipympl — matplotlib integration for spikes_removal may need to be simplified or work differently in anywidget
  - Do NOT skip the complex tool widgets because they're hard — they must be implemented

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Most complex tools — interactive visualization, matplotlib integration, multi-step UI
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 8, 9, 10)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 12
  - **Blocked By**: Tasks 1, 2, 3

  **References**:

  **Pattern References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/tools.py` — Reference for spikes_removal_ipy and find_peaks2D_ipy

  **Acceptance Criteria**:

  **If TDD**:
  - [ ] `pytest tests/test_tools.py -v` → PASS (ALL tools tests)

  **QA Scenarios**:

  ```
  Scenario: All tools widgets create without errors
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `pytest tests/test_tools.py -v --tb=short`
    Expected Result: All tools tests pass
    Failure Indicators: Any test failure
    Evidence: .sisyphus/evidence/task-11-tools-complex.txt
  ```

  **Commit**: YES
  - Message: `feat(tools): add complex tool widgets with TDD`
  - Files: `tools.py` (complete), `tests/test_tools.py` (complete)
  - Pre-commit: `pytest tests/test_tools.py -v`

- [ ] 12. Integration Tests + CI Pipeline

  **What to do**:
  - Create comprehensive integration test suite in `tests/test_integration.py`:
    - `test_all_toolkeys_registered` — Verify `hyperspy_extension.yaml` has exactly 33 entries under `anywidget:` toolkit
    - `test_gui_method_with_anywidget_toolkit` — Test `obj.gui(toolkit="anywidget", display=False)` for each widget type
    - `test_entry_point_discovery` — Verify HyperSpy discovers the anywidget extension
    - `test_bidirectional_sync_all_widgets` — Create each type of object, test that widget → HyperSpy and HyperSpy → widget sync works
    - `test_display_false_returns_wdict` — Verify `display=False` returns dict with "widget" and "wdict" keys for every registered function
    - `test_display_true_in_jupyter` — Mock Jupyter environment, verify IPython.display called
    - `test_display_true_in_marimo` — Mock Marimo environment, verify wdict returned without IPython.display call
  - Create `.github/workflows/ci.yml`:
    - Lint: `ruff check .`
    - Test: `pytest tests/ -v` on Python 3.10, 3.11, 3.12, 3.13
    - Coverage: `pytest --cov=hyperspy_gui_anywidget tests/`
  - Ensure all existing tests pass as a complete suite (not just individually)
  - Run full test suite: `pytest hyperspy_gui_anywidget/tests/ -v`

  **Must NOT do**:
  - Do NOT add new widget implementations — only add integration testing infrastructure
  - Do NOT skip any widget type in integration tests

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Integration testing requires understanding of all modules and edge cases
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 13)
  - **Parallel Group**: Wave 4
  - **Blocks**: F1-F4
  - **Blocked By**: Tasks 4-11

  **References**:

  **Pattern References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/tests/` — Test structure and patterns
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/hyperspy_gui_ipywidgets/conftest.py` — Test fixture setup

  **Acceptance Criteria**:

  **QA Scenarios**:

  ```
  Scenario: Full test suite passes
    Tool: Bash
    Preconditions: All widget modules implemented
    Steps:
      1. Run `pytest hyperspy_gui_anywidget/tests/ -v --tb=short`
    Expected Result: All tests pass, 0 failures
    Failure Indicators: Any test failure or error
    Evidence: .sisyphus/evidence/task-12-full-test-suite.txt

  Scenario: CI pipeline runs successfully
    Tool: Bash
    Preconditions: All tests passing locally
    Steps:
      1. Run `ruff check hyperspy_gui_anywidget/ && pytest hyperspy_gui_anywidget/tests/ -v`
    Expected Result: No lint errors, all tests pass
    Failure Indicators: Lint errors or test failures
    Evidence: .sisyphus/evidence/task-12-ci-pipeline.txt

  Scenario: All 33 toolkeys registered in YAML
    Tool: Bash
    Preconditions: Package installed
    Steps:
      1. Run `python -c "import yaml; data = yaml.safe_load(open('hyperspy_gui_anywidget/hyperspy_extension.yaml')); assert len(data['GUI']['widgets']['anywidget']) == 33; print('All 33 toolkeys registered')"`
    Expected Result: "All 33 toolkeys registered" printed
    Evidence: .sisyphus/evidence/task-12-yaml-count.txt
  ```

  **Commit**: YES
  - Message: `test(integration): add integration tests and CI pipeline`
  - Files: `tests/test_integration.py`, `.github/workflows/ci.yml`
  - Pre-commit: `pytest hyperspy_gui_anywidget/tests/ -v`

- [ ] 13. Documentation — README, Docstrings, Usage Examples

  **What to do**:
  - Write `README.md` with:
    - Project description: "anywidget-based GUI elements for HyperSpy"
    - Installation instructions: `pip install hyperspy_gui_anywidget`
    - Quick start: How to use with HyperSpy (`import hyperspy.api as hs; hs.preferences.GUIs.enable_anywidget_gui = True`)
    - Usage in Jupyter notebook example
    - Usage in Marimo notebook example
    - Comparison with hyperspy_gui_ipywidgets
    - Development instructions: `pip install -e ".[dev]"`, `pytest`, `ruff check`
    - License notice (GPLv3)
  - Add comprehensive docstrings to all public modules and functions:
    - Each module: brief description, list of widget functions
    - Each widget function: docstring matching ipywidgets style (Args, Returns)
    - `utils.py`: Docstrings for add_display_arg, labelme, etc.
    - `custom_widgets.py`: Docstrings for FloatTextWidget, DropdownWidget, etc.
  - Add usage examples directory:
    - `examples/basic_usage.py` — Simple Signal1D with navigation sliders
    - `examples/roi_usage.py` — ROI widgets example
    - `examples/model_usage.py` — Model fitting example
  - Ensure `hyperspy_extension.yaml` has comments explaining each section

  **Must NOT do**:
  - Do NOT add excessive or obvious comments (avoid AI slop)
  - Do NOT add comments that just restate what the code does
  - Do NOT create separate docs/ directory or Sphinx docs — just README and docstrings

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Documentation task requiring clear, concise writing
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 12)
  - **Parallel Group**: Wave 4
  - **Blocks**: F1-F4
  - **Blocked By**: Tasks 4-11

  **References**:

  **Pattern References**:
  - `/Users/francisco/Git/hyperspy_gui_ipywidgets/README.md` — README structure and content to adapt

  **Acceptance Criteria**:

  **QA Scenarios**:

  ```
  Scenario: README contains all required sections
    Tool: Bash
    Preconditions: README.md exists
    Steps:
      1. Run `python -c "
sections = ['Installation', 'Quick Start', 'Usage', 'Marimo', 'Development', 'License']
with open('README.md') as f:
    content = f.read()
for s in sections:
    assert s in content, f'Missing section: {s}'
    print(f'{s}: found')
"`
    Expected Result: All required sections present
    Failure Indicators: Missing section
    Evidence: .sisyphus/evidence/task-13-readme.txt

  Scenario: All public functions have docstrings
    Tool: Bash
    Preconditions: All modules implemented
    Steps:
      1. Run `python -c "
import hyperspy_gui_anywidget as pkg
for module_name in pkg.__all__:
    if module_name == '__version__':
        continue
    module = getattr(pkg, module_name)
    for name in dir(module):
        obj = getattr(module, name)
        if callable(obj) and not name.startswith('_'):
            assert obj.__doc__, f'{module_name}.{name} missing docstring'
            print(f'{module_name}.{name}: OK')
"`
    Expected Result: All public functions have docstrings
    Failure Indicators: AssertionError with function name
    Evidence: .sisyphus/evidence/task-13-docstrings.txt
  ```

  **Commit**: YES
  - Message: `docs: add README, docstrings, and usage examples`
  - Files: `README.md`, all source modules (docstrings), `examples/basic_usage.py`, `examples/roi_usage.py`, `examples/model_usage.py`
  - Pre-commit: None (documentation only)

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.
>
> **Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.**
> **Never mark F1-F4 as checked before getting user's okay.** Rejection or user feedback -> fix -> re-run -> present again -> wait for okay.

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, import module, run test). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run `ruff check` + `pytest`. Review all source files for: `as any`/type ignores, empty catches, print statements in prod, commented-out code, unused imports. Check AI slop: excessive comments, over-abstraction, generic names. Verify `hyperspy_extension.yaml` has all 33 entries. Verify all widget functions follow `@add_display_arg` + return `{"widget": ..., "wdict": {...}}` pattern.
  Output: `Lint [PASS/FAIL] | Tests [N pass/N fail] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high` (+ `playwright` skill if UI)
  Start from clean environment. Run `pip install -e .`. Create a Python script that: (1) imports hyperspy and hyperspy_gui_anywidget, (2) creates each type of object (Signal1D, Signal2D, ROI, etc.), (3) calls `.gui(toolkit="anywidget", display=False)` on each, (4) verifies wdict keys match expected, (5) tests bidirectional sync with link_traits. Create a Marimo notebook that imports and renders a SpanROI widget.
  Output: `Widgets [N/33 working] | Sync [N/N bidirectional] | Marimo [PASS/FAIL] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff. Verify 1:1 — everything in spec was built (no missing), nothing beyond spec was built (no creep). Check "Must NOT do" compliance: no ipywidgets containers, no IPython.display.display unconditional, no build step, no ipympl. Detect cross-task contamination. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- **Task 1**: `feat(init): scaffold project structure and pyproject.toml` — pyproject.toml, __init__.py, hyperspy_extension.yaml, conftest.py, LICENSE, .gitignore
- **Task 2**: `feat(utils): add utils module with add_display_arg and helpers` — utils.py, tests/test_utils.py
- **Task 3**: `feat(roi): add SpanROI proof-of-concept with Marimo validation` — roi.py (partial), custom_widgets.py (partial), tests, POC notebook
- **Task 4**: `feat(roi): complete all ROI widgets with TDD` — roi.py, tests/test_roi.py
- **Task 5**: `feat(axes): add axes widgets with TDD` — axes.py, tests/test_axes.py
- **Task 6**: `feat(preferences): add preferences widgets with TDD` — preferences.py, tests/test_preferences.py
- **Task 7**: `feat(microscope): add microscope parameters widgets with TDD` — microscope_parameters.py, tests/test_microscope_parameters.py
- **Task 8**: `feat(model): add model widgets with TDD` — model.py, tests/test_model.py
- **Task 9**: `feat(tools): add calibration and range tool widgets with TDD` — tools.py (partial), tests/test_tools.py (partial)
- **Task 10**: `feat(tools): add smoothing and processing widgets with TDD` — tools.py (partial), tests/test_tools.py (partial)
- **Task 11**: `feat(tools): add complex tool widgets with TDD` — tools.py (complete), tests/test_tools.py (complete)
- **Task 12**: `test(integration): add integration tests and CI pipeline` — tests, .github/workflows/ci.yml
- **Task 13**: `docs: add README, docstrings, and usage examples` — README.md, docstrings

---

## Success Criteria

### Verification Commands
```bash
pip install -e .                                    # Expected: Successfully installed
python -c "import hyperspy_gui_anywidget"            # Expected: no error
python -c "import hyperspy.api as hs; hs.roi.SpanROI(left=0, right=10).gui(toolkit='anywidget', display=False)"  # Expected: returns dict with "widget" and "wdict"
pytest hyperspy_gui_anywidget/tests/ -v              # Expected: all tests pass
ruff check hyperspy_gui_anywidget/                  # Expected: no errors
```

### Final Checklist
- [ ] All "Must Have" items present
- [ ] All "Must NOT Have" items absent
- [ ] All tests pass
- [ ] Works in Marimo (verified via notebook)
- [ ] All 33 widget functions registered in hyperspy_extension.yaml