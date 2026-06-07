"""
A collection of common patterns for controlling.
"""


from pickle import load as pickle__load, dump as pickle__dump, UnpicklingError as pickle__UnpicklingError
from pathlib import Path as pathlib__Path
from typing import Callable


def load_pkl(path: str) -> dict[str, int]:
    """
    Read the parameters.
    """
    try:
        with open(path, "rb") as f_rd:
            obj = pickle__load(f_rd)
        if not isinstance(obj, dict):
            raise TypeError
    except (OSError, EOFError, pickle__UnpicklingError, TypeError):
        obj = {}
    return obj


def ensure_dir(path: str) -> None:
    """
    Restore the parent directory tree.
    """
    try:
        pathlib__Path(path).parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        return


def save_pkl(
        obj: dict[str, int],
        path: str
) -> None:
    """
    Write the parameters.
    """
    try:
        with open(path, "wb") as f_wt:
            pickle__dump(obj, f_wt)
    except OSError:
        return


def save_txt(
        texts: list[str],
        path: str
) -> None:
    """
    Write a text.
    """
    try:
        with open(path, "w", encoding="utf-8") as f_wt:
            f_wt.writelines(texts)
    except OSError:
        return


def factory_funcs(
        _make_ui: Callable,
        _calcs: Callable,
        i_extra: int =None
) -> Callable:
    """
    Build a function-controller for a math unit. It acts as a window lifecycle manager and runtime state holder.
    """
    def _ui(*args) -> None:
        """
        Create a reusable UI entry-point controller.

        Responsibilities:
            • Call the UI constructor or reuse an existing window.
            • Preserve module-local UI state between calls.
            • Bind calculation handlers to UI objects.
            • Attach shared runtime attributes for intermodule interaction.
            • Forward runtime arguments and optionally interception desired values.

        Low-level Control Structure (topology of the import/runtime stages):
            conductor.py
             ├─ Import Stage
             │   └─ mu*.py dynamic loading
             │       ├─ import commons.factory_funcs
             │       ├─ import common_ui.make_ui
             │       └─ ui = factory_funcs(make_ui, calcs[, extra])
             │                ├─ closure creation
             │                └─ _ui(*args) controller binding
             └─ Runtime Stage
                 └─ mu*.ui(...) execution
                     └─ _ui(*args)
        """
        if hasattr(_ui, "_ui__win"):
            _ui._ui__win.deiconify()
            st = "zoomed"
            if _ui._ui__win._make_ui__last_state == st:
                _ui._ui__win.state(st)
        else:
            _ui._ui__win = _make_ui(*args)
            _ui._ui__win._make_ui__calculations = _calcs
            _calcs._ui__last_numbers = ()
            if i_extra is not None:
                _calcs._ui__extra = args[i_extra]

    return _ui
