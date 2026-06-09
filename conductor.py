"""
Application entry point.

Requirements:
    Python 3.12+

High-Level Control Structure (optional runtime side-effects: (1), (2)):
    conductor.py ───┬──────────────────────┬─► docs/spec_mu*.pkl
     ║     └─(0)    │                      │
     ║           ┌─►├─► common_ui.py ───┬─►└─► values.py ◄──┐
     ║           │  │          └─(1)    │                   │
     ╠═► mu0.py ─┼─►└───► commons.py ◄──┴─► calcs_math.py ◄─┤   (0) artfs/
     ║    └─(2)  │                                          │   (1) artfs/cust_set.pkl
     ╚═► mu1.py ─┴──────────────────────────────────────────┘   (2) artfs/Factoring.txt

Responsibilities:
    • Create the root window.
    • Build the selection UI (labels, radio buttons, control buttons, language menu).
    • Bind navigation and control (as add options) keys.
    • Route control to the chosen math unit.
    • Handle safe application exit.

Workflow:
    • User selects a math unit in the root window.
    • Language change is then disabled for the current session.
    • The root window is hidden (restored upon return).
    • The selected module is called with:
        - parent root window
        - settings and texts dictionaries
        - identifier of a math unit.

Scalability:
    Core processing logic (loops, sampling, generation, constants) relating to:
        - thematic module quantity
        - UI language localizations
        - additional features (e.g., randomizer types)
    is designed for easy future expansion or reduction with minimal code changes.

Notes:
    • Only one interactive window (selection or math unit UI) is active at a time.
    • The runtime parameter dict (root window attribute):
        - serves as the application's runtime source of truth for user settings
        - stores validated values and allows modules to access current configuration without duplicating state
        - provides application-wide language localization settings
        - supports behavior-driven preferences that enhance UX
        - is persisted on application exit.
    • Runtime workspace integrity is ensured by recreating missing directories.
    • Non-critical module data (description, custom settings) may be absent; defaults are used.
"""


import tkinter as tk
from importlib import import_module as importlib__import_module

import values as vls
from modules.common_ui import make_button, confirm_end
from modules.commons import load_pkl


def ui_pick() -> None:
    """
    Create the root window for math unit selection and the external dict for user settings. Also loop all widgets on
    the internal dict for context exchange.
    """
    def sync_munit(*_) -> None: cust[munit_name] = clue_mu.get()

    cfg: dict[str, int
                   | tk.Tk | tk.Menu | tk.Label | tk.Button
                   | None] = {
        "qty_units": len(vls.SET_MUS),                                                   # : int
    }

    win_pick = tk.Tk()
    cust = win_pick.ui_pick__cust = load_pkl(vls.SET_CUST["Path"])
    lang_name = vls.SET_CUST["LANG"]["name"]
    if cust.get(lang_name) not in vls.SET_CUST["LANG"]["valid"]:
        cust[lang_name] = 0
    i_lang = cust[lang_name]
    win_pick.title(vls.TEXTS_PICK["Title"][i_lang])
    cfg["win_pick"] = win_pick                                                           # : tk.Tk

    # The choice section
    menu = tk.Menu(win_pick)
    win_pick.config(menu=menu)
    menu_lang = tk.Menu(menu, tearoff=False)
    menu.add_cascade(
        label=vls.TEXTS_PICK["Menu"]["name"][i_lang],
        menu=menu_lang
    )
    for idx, itm in enumerate(vls.TEXTS_PICK["Menu"]["languages"]):
        menu_lang.add_command(
            label=itm,
            command=lambda i=idx: _chose_lang(cfg, i),
            state = "normal" if idx != i_lang else "disabled"
        )
    cfg.update({"menu": menu, "menu_lang": menu_lang})                                   # : tk.Menu

    munit_name = vls.SET_CUST["MUNIT"]["name"]
    if cust.get(munit_name) not in vls.SET_CUST["MUNIT"]["valid"]:
        cust[munit_name] = 0
    clue_mu = tk.IntVar(win_pick,
                        value=cust[munit_name])
    clue_mu.trace_add("write", sync_munit)
    for idx in range(cfg["qty_units"]):
        ident = f"label_radbut{idx}"
        cfg[ident] = tk.Label(win_pick,
                              text=vls.SET_MUS[idx]["Name"][i_lang],
                              font=("", 10))                                             # : tk.Label
        cfg[ident].grid(row=idx, column=0, sticky="w", padx=30)
        tk.Radiobutton(
            win_pick,
            cursor="hand2",
            variable=clue_mu,
            value=idx  # assign current idx immediately
        ).grid(row=idx, column=1, sticky="w")

    # The control section
    cfg["button"] = make_button({"win": win_pick},
                                vls.TEXTS_PICK["Button"][i_lang],
                                lambda: _open_munit(cfg))                                # : tk.Button
    cfg["button"].grid(columnspan=2, pady=5)
    cfg["label"] = tk.Label(win_pick,
                            text=vls.TEXTS_PICK["Label"][i_lang])                        # : tk.Label
    cfg["label"].grid(columnspan=2, padx=5, pady=5)

    for ent, dlt in vls.TEXTS_PICK["Event_kb"]["directions"].items():
        win_pick.bind(
            ent,
            lambda event, d=dlt: clue_mu.set((clue_mu.get() + d) % cfg["qty_units"])
        )
    win_pick.bind(
        vls.TEXTS_PICK["Event_kb"]["begin"],
        lambda event: _open_munit(cfg, clue_mu.get())
    )
    qty_langs = len(vls.TEXTS_PICK["Menu"]["languages"])
    win_pick.bind(
        vls.TEXTS_PICK["Event_kb"]["lang"],
        lambda event: _chose_lang(cfg, (cust[lang_name] + 1) % qty_langs)
    )
    concord = {"win": win_pick, "win_parent": win_pick}  # to match the call interface
    win_pick.bind(
        vls.TEXTS_PICK["Event_kb"]["exit"],
        lambda event: confirm_end(concord)
    )
    win_pick.protocol(
        "WM_DELETE_WINDOW",
        lambda: confirm_end(concord)
    )

    # The setup section
    win_pick.resizable(False, False)
    win_pick.focus_set()
    win_pick.mainloop()


def _chose_lang(
        cfg: dict,
        i_lang: int  # new value
) -> None:
    """
    Switch UI language, refresh the root window, and rewrite its default value. A current widget item is blocked.
    """
    cfg["win_pick"].title(vls.TEXTS_PICK["Title"][i_lang])
    cust = cfg["win_pick"].ui_pick__cust
    lang_name = vls.SET_CUST["LANG"]["name"]
    cfg["menu"].entryconfig(
        vls.TEXTS_PICK["Menu"]["name"][cust[lang_name]],  # current value
        label=vls.TEXTS_PICK["Menu"]["name"][i_lang]
    )
    for idx in range(cfg["qty_units"]):
        cfg[f"label_radbut{idx}"].config(text=vls.SET_MUS[idx]["Name"][i_lang])
    cfg["button"].config(text=vls.TEXTS_PICK["Button"][i_lang])
    cfg["label"].config(text=vls.TEXTS_PICK["Label"][i_lang])
    cfg["menu_lang"].entryconfig(i_lang, state="disabled")
    cfg["menu_lang"].entryconfig(cust[lang_name], state="normal")
    cust[lang_name] = i_lang


def _open_munit(cfg: dict) -> None:
    """
    Open the selected math unit window and control user's settings.

    Workflow:
        • On the first run, the function disables the language switching option.
        • Hide the root window.
        • Load module settings from the root-level file.
        • Restore its specification from a store (pickle), or use default stub if not available.
        • Dynamically import a module by a path.
        • Call its UI entry point with parent window, settings, and specification.
    """
    cfg["win_pick"].withdraw()
    i_lang = cfg["win_pick"].ui_pick__cust[vls.SET_CUST["LANG"]["name"]]
    if cfg["menu"]:
        cfg["menu"].entryconfig(
            vls.TEXTS_PICK["Menu"]["name"][i_lang],
            state="disabled"
        )
        cfg["menu"] = None                                                               # : None
        cfg["win_pick"].unbind(vls.TEXTS_PICK["Event_kb"]["lang"])
    i_munit = cfg["win_pick"].ui_pick__cust[vls.SET_CUST["MUNIT"]["name"]]
    set_mu = vls.SET_MUS[i_munit]
    spec_mu = load_pkl(set_mu["Path_help"].format(lng=i_lang))
    if not spec_mu:
        spec_mu = dict.fromkeys(vls.TEXTS_MU["Menu"]["Help"]["blocks"],
                                "[data not found]")
    munit = importlib__import_module(set_mu["Path"])
    munit.ui(cfg["win_pick"], set_mu, spec_mu, i_munit)


if __name__ == "__main__":
    ui_pick()
