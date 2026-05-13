"""
A collection of common patterns for controlling.
"""


from pickle import load as pickle__load, dump as pickle__dump, UnpicklingError as pickle__UnpicklingError
from typing import Callable


def load_pkl(path: str) -> dict[str, str | int]:
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


def factory_funcs(
        _make_ui: Callable,
        _calcs: Callable,
        i_extra: int =None
) -> Callable:
    """
    Build a function-controller for the math unit UI.
    """
    def _ui(*args) -> None:
        """
        Call the common window constructor or return existing one. Create and update the objects attributes for
        inter module interaction.
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
