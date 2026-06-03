"""
Application entry point.

Requirements:
    Python 3.12+

High-Level Control Structure (optional runtime side-effects: (1), (2)):
    conductor.py ───┬──────────────────────┬─► docs/spec_mu*.pkl
     ║     └─(1)    │                      │
     ║           ┌─►├─► common_ui.py ───┬─►└─► values.py ◄──┐
     ║           │  │          └─(1)    │                   │
     ╠═► mu0.py ─┼─►└───► commons.py ◄──┴─► calcs_math.py ◄─┤
     ║    └─(2)  │                                          │   (1) artfs/cust_set.pkl
     ╚═► mu1.py ─┴──────────────────────────────────────────┘   (2)       Factoring.txt

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
        - identifiers of a math unit and a UI language.

Scalability:
    Core processing logic (loops, sampling, generation, constants) relating to:
        - thematic module quantity
        - UI language localizations
        - additional features (e.g., randomizer types)
    is designed for easy future expansion or reduction with minimal code changes.

Notes:
    • Only one interactive window (selection or math unit UI) is active at a time.
    • Non-critical module data (description) may be absent; defaults are used.
    • Behavior-driven settings: persistence follows user actions.
"""


import tkinter as tk
from importlib import import_module as importlib__import_module

import values as vls
from modules.common_ui import make_button, confirm_end
from modules.commons import load_pkl, save_pkl


def ui_pick() -> None:
    """
    Create the root window for math unit selection. And loop all widgets on the internal dict for context exchange.
    """
    cfg: dict[str, int
                   | tk.Tk | tk.Menu | tk.Label | tk.Button
                   | None] = {
        "qty_units": len(vls.SET_MUS),                                                   # : int
    }
    v = load_pkl(vls.SET_CUST["Path"]).get(vls.SET_CUST["LANG"]["name"])
    i_lang = v if v in vls.SET_CUST["LANG"]["valid"] else 0
    cfg["i_lang"] = i_lang                                                               # : int

    win_pick = tk.Tk()
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
            command=lambda i=idx: _chose_lang(cfg, i)
        )
    menu_lang.entryconfig(i_lang, state="disabled")
    cfg.update({"menu": menu, "menu_lang": menu_lang})                                   # : tk.Menu

    v = load_pkl(vls.SET_CUST["Path"]).get(vls.SET_CUST["MUNIT"]["name"])
    clue_mu = tk.IntVar(win_pick,
                        value=v if v in vls.SET_CUST["MUNIT"]["valid"] else 0)
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
                                lambda: _open_munit(cfg, clue_mu.get()))                 # : tk.Button
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
        lambda event: _chose_lang(cfg, (cfg["i_lang"] + 1) % qty_langs)
    )
    concord = {"win": win_pick, "win_parent": win_pick}  # to match the call interface
    win_pick.bind(
        vls.TEXTS_PICK["Event_kb"]["exit"],
        lambda event: confirm_end(concord, cfg["i_lang"])
    )
    win_pick.protocol(
        "WM_DELETE_WINDOW",
        lambda: confirm_end(concord, cfg["i_lang"])
    )

    # The setup section
    win_pick.resizable(False, False)
    win_pick.focus_set()
    win_pick.mainloop()


def _chose_lang(
        cfg: dict,
        ilg: int  # new value
) -> None:
    """
    Switch UI language, refresh the root window, and rewrite its default value. A current widget item is blocked.
    """
    cfg["win_pick"].title(vls.TEXTS_PICK["Title"][ilg])
    cfg["menu"].entryconfig(
        vls.TEXTS_PICK["Menu"]["name"][cfg["i_lang"]],
        label=vls.TEXTS_PICK["Menu"]["name"][ilg]
    )
    for idx in range(cfg["qty_units"]):
        cfg[f"label_radbut{idx}"].config(text=vls.SET_MUS[idx]["Name"][ilg])
    cfg["button"].config(text=vls.TEXTS_PICK["Button"][ilg])
    cfg["label"].config(text=vls.TEXTS_PICK["Label"][ilg])
    cfg["menu_lang"].entryconfig(ilg, state="disabled")
    cfg["menu_lang"].entryconfig(cfg["i_lang"], state="normal")
    cfg["i_lang"] = ilg
    obj = load_pkl(vls.SET_CUST["Path"])
    obj[vls.SET_CUST["LANG"]["name"]] = ilg
    save_pkl(obj, vls.SET_CUST["Path"])


def _open_munit(
        cfg: dict,
        i_munit: int
) -> None:
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
    if cfg["menu"]:
        cfg["menu"].entryconfig(
            vls.TEXTS_PICK["Menu"]["name"][cfg["i_lang"]],
            state="disabled"
        )
        cfg["menu"] = None                                                               # : None
        cfg["win_pick"].unbind(vls.TEXTS_PICK["Event_kb"]["lang"])
    obj = load_pkl(vls.SET_CUST["Path"])
    v = obj.get(vls.SET_CUST["MUNIT"]["name"])
    if v not in vls.SET_CUST["MUNIT"]["valid"] or v != i_munit:
        obj[vls.SET_CUST["MUNIT"]["name"]] = i_munit
        save_pkl(obj, vls.SET_CUST["Path"])
    cfg["win_pick"].withdraw()
    set_mu = vls.SET_MUS[i_munit]
    spec_mu = load_pkl(set_mu["Path_help"].format(lng=cfg["i_lang"]))
    if not spec_mu:
        spec_mu = dict.fromkeys(vls.TEXTS_MU["Menu"]["Help"]["blocks"],
                                "[data not found]")
    munit = importlib__import_module(set_mu["Path"])
    munit.ui(cfg["win_pick"], set_mu, spec_mu, i_munit, cfg["i_lang"])


if __name__ == "__main__":
    ui_pick()
