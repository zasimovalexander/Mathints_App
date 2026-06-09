"""
Build and manage a single active window of a math unit.

Responsibilities:
    • Create and configure the interactive interface for a math unit.
    • Route internal actions (buttons, menus, entry operations) to handlers.
    • Maintain consistent UI state across interactions and input sessions.
    • Provide contextual help and alternative input options through the main menu.
    • Ensure controlled initialization and termination of calculations.
    • Return to the selection menu of math units.
    • Handle safe application exit, ensuring that any active worker threads
      are properly stopped.

Notes:
    • Returning to the selection UI hides the current window while preserving all last actions and states;
      the input-related info window is closed to avoid confusion in other modules.
    • The native window widget [x] repeats the return behavior.
    • Behavior-driven settings by the last session.
"""


import tkinter as tk
from re import findall as re__findall, search as re__search
from typing import Callable

import values as vls
from modules.calcs_math import gen_rand, primality
from modules.commons import ensure_dir, save_pkl


def make_ui(
        win_parent: tk.Tk,
        settings: dict[str, str
                            | int
                            | tuple[str | int, ...]],
        specific: dict[str, str],
        i_munit: int
) -> tk.Toplevel:
    """
    Build and return the UI window for a math unit. And loop all widgets on the internal dict for context exchange.
    """
    cfg: dict[str, str
                   | int
                   | tk.Tk | tk.Toplevel | tk.Label | tk.Entry | tk.Text | tk.Canvas | tk.Button
                   | list[str]
                   | dict[str | bool, str | tk.Toplevel]] = {
        "max_rank": settings["Max_rank"],                                                    # : int
        "max_nums": settings["Max_numbers"],                                                 # : int
        "min_nums": settings["Min_numbers"] - 1,                                             # : int
        "numbers": [],                                                                       # : list[str]
        "sep_nums": vls.TEXTS_MU["Menu"]["0_9"]["next_items"][-1],                           # : str
        "patt_nums": r"[1-9][0-9]*",                                                         # : str
        "last_text": "",                                                                     # : str
        "win_parent": win_parent,                                                            # : tk.Tk
        "wins_help": {},                                                                     # : dict[str, tk.Toplevel]
        "states_wgt": {True: "disable", False: "normal"},                                    # : dict[bool, str]
        "rand_name": vls.SET_CUST["RAND"]["name"].format(imu=i_munit),                       # : str
    }
    cust = win_parent.ui_pick__cust
    i_lang = cust[vls.SET_CUST["LANG"]["name"]]
    cfg.update({"munit": settings["Name"][i_lang][2:],                                       # : str
                "pref_ranks": vls.TEXTS_MU["Label"][i_lang],                                 # : str
                "delta_rank": 10 - cfg["max_rank"],                                          # : int
                "patt_final_sep": fr"{cfg["patt_nums"]}{cfg["sep_nums"]}+(?:0|\D)*$"})       # : str

    # Make widgets
    win = tk.Toplevel(win_parent)
    win._make_ui__last_state = ""
    win._make_ui__calculations = lambda nums, _: nums
    win.title(cfg["munit"])
    cfg["win"] = win                                                                         # : tk.Toplevel

    cfg["label_ranks"] = tk.Label(win, text=cfg["pref_ranks"])                               # : tk.Label

    cfg["entry"] = tk.Entry(win, width=53, bd=3)                                             # : tk.Entry

    cfg["butt_clean"] = make_button(cfg,
                                    vls.TEXTS_MU["Button"]["clean"][i_lang],
                                    lambda: (_clean_entry(cfg), _control_input(cfg)),
                                    "disabled")                                              # : tk.Button

    frame_display = tk.Frame(win)
    scroll_x = tk.Scrollbar(frame_display, orient="horizontal")
    scroll_y = tk.Scrollbar(frame_display)
    cfg["display"] = (_make_text, _make_canvas)[i_munit](frame_display, scroll_x, scroll_y)  # : tk.Text | tk.Canvas
    scroll_x.config(command=cfg["display"].xview)
    scroll_y.config(command=cfg["display"].yview)
    scroll_x.pack(side="bottom", fill="x")
    scroll_y.pack(side="right", fill="y")
    cfg["display"].pack(side="left", fill="both", expand=True)

    buttons = [make_button(cfg,
                           vls.TEXTS_MU["Button"][k][i_lang],
                           lambda f=fnc: f(cfg)
                           ) for k, fnc in zip(("back", "exit"),
                                               (_revert, confirm_end))]
    cfg["butt_equal"] = make_button(cfg,
                                    vls.TEXTS_MU["Button"]["equal"][i_lang],
                                    lambda: _to_calcs(cfg),
                                    "disabled")                                              # : tk.Button

    # Place widgets
    if cust.get(cfg["rand_name"]) not in vls.SET_CUST["RAND"]["valid"]:
        cust[cfg["rand_name"]] = 0
    _make_menu(cfg, specific, i_lang, cust[cfg["rand_name"]])
    cfg["label_ranks"].grid(row=0, sticky="w", padx=5)
    cfg["entry"].grid(row=1, sticky="w", padx=5, pady=5)
    cfg["butt_clean"].grid(row=1, column=1, sticky="nw", pady=5)
    frame_display.grid(row=2, columnspan=2, sticky="nsew", padx=5)  # occupy all grid columns for independent widening
    win.columnconfigure(1, weight=1)
    win.rowconfigure(2, weight=1)
    for btn, sd in zip((*buttons, cfg["butt_equal"]),
                       ("w", "e", "")):
        btn.grid(row=3, sticky=sd, padx=10, pady=10)

    # Make binds
    cfg["entry"].bind(
        "<KeyRelease>",
        lambda event: _control_input(cfg)
    )
    cfg["entry"].bind(
        vls.TEXTS_MU["Event_kb"]["equal"],
        lambda event: _to_calcs(cfg)
    )
    win.bind(
        vls.TEXTS_MU["Event_kb"]["back"],
        lambda event: _revert(cfg)
    )
    win.bind(
        vls.TEXTS_MU["Event_kb"]["exit"],
        lambda event: confirm_end(cfg)
    )
    win.protocol(
        "WM_DELETE_WINDOW",
        lambda: _revert(cfg)
    )

    # The setup section
    w, h = settings["Geometry_win"]
    win.geometry(f"{w}x{h}+{win_parent.winfo_rootx()}+{win_parent.winfo_rooty()}")
    win.minsize(*settings["Minsize_win"])
    cfg["entry"].focus_force()

    return win


def _make_text(
        frame: tk.Frame,
        srl_x: tk.Scrollbar,
        srl_y: tk.Scrollbar
) -> tk.Text:
    """
    Build and return a Text widget for result demonstrating.
    """
    text = tk.Text(frame,
                   wrap="none",
                   font=("Consolas", 11),
                   bg="#e6f2ff",
                   relief="flat",
                   padx = 10, pady = 10,
                   xscrollcommand=srl_x.set, yscrollcommand=srl_y.set,
                   state="disabled")
    return text


def _make_canvas(
        frame: tk.Frame,
        srl_x: tk.Scrollbar,
        srl_y: tk.Scrollbar
) -> tk.Canvas:
    """
    Build and return a Canvas widget for result demonstrating.
    """
    return tk.Canvas(frame,
                     bg="white",
                     relief="flat",
                     xscrollcommand=srl_x.set, yscrollcommand=srl_y.set)


def _revert(cfg: dict) -> None:
    """
    Return to math unit selection, saving the current window state.
    """
    win_help_unique = cfg["wins_help"].pop(vls.TM12, None)
    if win_help_unique:
        win_help_unique.destroy()
    cfg["win"]._make_ui__last_state = cfg["win"].state()
    cfg["win"].withdraw()
    cfg["win_parent"].deiconify()
    cfg["win_parent"].focus_force()


def _to_calcs(cfg: dict) -> None:
    """
    Feedback to the calling module: initialization of math calculations with an additional layer of input control.
    """
    _relay_lock(cfg, True)
    numbers = cfg["win"]._make_ui__calculations(cfg["numbers"], cfg["display"])
    if numbers == cfg["numbers"]:
        _relay_lock(cfg)
    else:
        _update_and_unlock(cfg, numbers)


def _relay_lock(
        cfg: dict,
        frozen: bool =False
) -> None:
    """
    Disable or enable user interaction with the main input controls.

    Args:
        • If frozen == True: Disable.
        • If frozen == False: Enable, but some widgets are unavailable if additional conditions are not met.

    Call Cases:
        • Directly if updating the user input data context is not required.
        • Through the helper function that updates that context beforehand.
    """
    cfg["entry"].config(state=cfg["states_wgt"][frozen])
    if cfg["last_text"]:
        cfg["butt_clean"].config(state=cfg["states_wgt"][frozen])
    if len(cfg["numbers"]) > cfg["min_nums"]:
        cfg["butt_equal"].config(state=cfg["states_wgt"][frozen])


def _update_and_unlock(
        cfg: dict,
        numbers: list[str],
        position: str | int =tk.END,
        ending: bool =False
) -> None:
    """
    Update numeric context, Entry content, and cursor position. Redraw ranks for the normalized numbers and unlock
    input control.

    Notes:
        Normalized text insertion is deferred via after_idle() to avoid race conditions with user input, preventing
        ghost characters during correction.
    """
    cfg["numbers"] = numbers
    cfg["last_text"] = cfg["sep_nums"].join(numbers)
    if ending:
        cfg["last_text"] += cfg["sep_nums"]
    suite_ranks = f"{cfg["sep_nums"]} ".join([str(len(n)) for n in numbers])
    cfg["label_ranks"].config(text=f"{cfg["pref_ranks"]}{suite_ranks}")
    cfg["entry"].after_idle(lambda: (_relay_lock(cfg),
                                     _clean_entry(cfg),
                                     cfg["entry"].insert(0, cfg["last_text"]),
                                     cfg["entry"].icursor(position)))


def _clean_entry(cfg: dict) -> None:
    """
    Clear the Entry widget.
    """
    if cfg["entry"].get():
        cfg["entry"].delete(0, tk.END)


def confirm_end(cfg: dict) -> None:
    """
    Confirm to exit the application. The modal Tk window is composed of three independent layers (OS/Tk/Python
    flow control), which are not strictly synchronized across platforms. Design rationale:
        • transient(): binds dialog to parent window (OS-level hint).
        • grab_set(): redirects all Tk events to this window (Tk-level modal lock).
        • focus_set(): best-effort request to move keyboard input to dialog (not guaranteed by OS).
        • wait_window(): blocks Python execution until Tk receives a window destroy event.
    """
    win_confirm = tk.Toplevel(cfg["win"])
    win_confirm.transient(cfg["win"])
    win_confirm.grab_set()
    i_lang = cfg["win_parent"].ui_pick__cust[vls.SET_CUST["LANG"]["name"]]
    win_confirm.title(vls.TEXTS_CONFIRM["Title"][i_lang])

    button = make_button({"win": win_confirm},
                         vls.TEXTS_CONFIRM["Button"][i_lang],
                         lambda: _end(cfg))
    button.config(width=0)
    button.pack(pady=5)
    win_confirm.bind(
        vls.TEXTS_CONFIRM["Event_kb"],
        lambda event: _end(cfg)
    )

    win_confirm.geometry(f"140x40+{cfg["win"].winfo_rootx()}+{cfg["win"].winfo_rooty()}")
    win_confirm.resizable(False, False)
    win_confirm.focus_set()
    win_confirm.wait_window()


def _end(cfg: dict) -> None:
    """
    Save custom settings, stop any worker threads if present, and close the root window.
    """
    ensure_dir(vls.SET_CUST["Path"])
    save_pkl(cfg["win_parent"].ui_pick__cust, vls.SET_CUST["Path"])
    if hasattr(cfg["win_parent"], "worker_threads"):
        for trd in list(getattr(cfg["win_parent"], "worker_threads", [])):
            if hasattr(trd, "stop"):
                trd.stop()
            if trd.is_alive():
                trd.join(timeout=1)
        cfg["win_parent"].worker_threads.clear()
    cfg["win_parent"].destroy()


def make_button(
        cfg: dict,
        info: str,
        func: Callable,
        st: str ="normal"
) -> tk.Button:
    """
    Build and return a Button widget.
    """
    return tk.Button(cfg["win"],
                     text=info,
                     justify="center",
                     font="Helvetica 7",
                     width=8,
                     bg="grey",
                     activebackground="white",
                     cursor="hand2",
                     command=func,
                     state=st)


def _make_menu(
        cfg: dict,
        spec: dict[str, str],
        i_lang: int,
        i_rand: int
) -> None:
    """
    Build the main menu containing help and input options.
    """
    menu = tk.Menu(cfg["win"])
    cfg["win"].config(menu=menu)

    # The help submenu
    menu_help = tk.Menu(menu, tearoff=False)
    menu.add_cascade(
        label=vls.TEXTS_MU["Menu"]["Help"]["name"][i_lang],
        menu=menu_help
    )
    for itm in vls.TEXTS_MU["Menu"]["Help"]["blocks"]:
        menu_help.add_command(
            label=vls.TEXTS_MU["Menu"]["Help"][itm][i_lang],
            command=lambda k=itm: _show_help(cfg, k, vls.TEXTS_MU["Menu"]["Help"][k][i_lang], spec[k])
        )

    # The additional input submenu
    menu_0_9 = tk.Menu(menu)
    menu.add_cascade(
        label=vls.TEXTS_MU["Menu"]["0_9"]["name"],
        menu=menu_0_9
    )
    menu_0_9.add_cascade(
        label=vls.TEXTS_MU["Menu"]["0_9"]["first_spec"][i_lang],
        state="disabled",
        activebackground="#f0f0f0"
    )
    menu_0_9.add_command(
        label=vls.TEXTS_MU["Menu"]["0_9"]["next_items"][0],
        command=lambda: _calls_in_menu(cfg, _backspace)
    )
    for idx, lbl in enumerate(vls.TEXTS_MU["Menu"]["0_9"]["next_items"][1:3]):
        menu_0_9.add_command(
            label=lbl,
            command=lambda i=idx: _calls_in_menu(cfg, _move_cursor, i)
        )
    for ch in vls.TEXTS_MU["Menu"]["0_9"]["next_items"][3:]:
        menu_0_9.add_command(
            label=ch,
            command=lambda c=ch: _calls_in_menu(cfg, _add_entry, c)
        )

    # The random numbers generation submenu
    menu_rand = tk.Menu(menu)
    menu.add_cascade(
        label=vls.TEXTS_MU["Menu"]["Rand"]["name"][i_lang],
        menu=menu_rand
    )
    tops_rand = vls.TEXTS_MU["Menu"]["Rand"]["first_iter"][i_lang]
    qty = len(tops_rand)
    menu_rand.add_command(
        label=tops_rand[i_rand],
        command=lambda: _calls_in_menu(cfg, _looping_item, tops_rand, menu_rand, qty)
    )
    cfg["entry"].bind(
        vls.TEXTS_MU["Event_kb"]["rand_nums"],
        lambda event: _calls_in_menu(cfg, _looping_item, tops_rand, menu_rand, qty)
    )
    suf = vls.TEXTS_MU["Menu"]["Rand"]["next_suffix"][i_lang]
    for idx in range(1, cfg["max_rank"] + 1):
        menu_rand.add_command(
            label=f"{idx}{suf}",
            command=lambda rank_rand=idx: _calls_in_menu(cfg, _rand_numbers, rank_rand)
        )
    menu_rand.add_command(
        label=vls.TEXTS_MU["Menu"]["Rand"]["last_series"][i_lang],
        command=lambda: _calls_in_menu(cfg, _rand_numbers)
    )
    cfg["entry"].bind(
        vls.TEXTS_MU["Event_kb"]["rand"],
        lambda event: _calls_in_menu(cfg, _rand_numbers)
    )


def _show_help(
        cfg: dict,
        key_win: str,
        part_title: str,
        content: str
) -> None:
    """
    Show a single copy of read-only popup with the Scrollbars.
    """
    if key_win in cfg["wins_help"]:
        cfg["wins_help"][key_win].deiconify()
        return

    win_help = tk.Toplevel(cfg["win"], bg="#f0f0f0")
    win_help.title(f"{cfg["munit"]}: {part_title}")
    cfg["wins_help"][key_win] = win_help

    scroll = tk.Scrollbar(win_help)
    text = tk.Text(win_help,
                   wrap="word",
                   font=("Consolas", 11),
                   bg="#f0f0f0",
                   relief="flat",
                   yscrollcommand=scroll.set)
    scroll.config(command=text.yview)
    scroll.pack(side="right", fill="y")
    text.insert("1.0", content)
    text.config(state="disabled")
    text.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    win_help.protocol(
        "WM_DELETE_WINDOW",
        lambda: (cfg["wins_help"].pop(key_win), win_help.destroy())
    )

    win_help.minsize(300, 150)
    win_help.geometry(f"500x250+{cfg["win"].winfo_rootx()}+{cfg["win"].winfo_rooty()}")
    win_help.focus_set()


def _calls_in_menu(
        cfg: dict,
        func: Callable,
        *args: int | str | tuple[str, ...] | tk.Menu
) -> None:
    """
    Transfer focus to the Entry widget, then call the specified function. Provide consistent focus behavior for input
    with tear-off menus.
    """
    cfg["entry"].focus_set()
    func(cfg, *args)


def _backspace(cfg: dict) -> None:
    """
    Delete the symbol on the Entry cursor right and normalize content.
    """
    idx_insert = cfg["entry"].index("insert")
    if idx_insert > 0:
        cfg["entry"].delete(idx_insert - 1)
        _control_input(cfg)


def _move_cursor(
        cfg: dict,
        idx_move: int
) -> None:
    """
    Move the cursor within the Entry widget.
    """
    cfg["entry"].icursor(cfg["entry"].index("insert") - [1, -1][idx_move])


def _add_entry(
        cfg: dict,
        line: str
) -> None:
    """
    Insert a string into the Entry widget at the cursor and normalize it (like the keyboard pipeline).
    """
    cfg["entry"].insert("insert", line)
    _control_input(cfg)


def _looping_item(
        cfg: dict,
        tops: tuple[str, ...],
        submenu: tk.Menu,
        qty_tops: int
) -> None:
    """
    Switch a menu item's label and globally store the current state.
    """
    idx_item = 1  # index 0 is tearoff item in this menu
    i_rand = (tops.index(submenu.entrycget(idx_item, "label")) + 1) % qty_tops
    submenu.entryconfig(idx_item, label=tops[i_rand])
    cfg["win_parent"].ui_pick__cust[cfg["rand_name"]] = i_rand


def _rand_numbers(
        cfg: dict,
        rank: int =0
) -> None:
    """
    Random search of natural numbers and apply them to the Entry widget.

    Args:
        • If rank > 0: Single random number of that digit length, if the max amount of numbers has not been reached.
        • If rank == 0: Sequence of random numbers with random digit lengths (input control is not required).
    """
    _relay_lock(cfg, True)
    if rank > 0:
        if len(cfg["numbers"]) < cfg["max_nums"]:
            number_rand = _make_rand(cfg, rank)
            _relay_lock(cfg)
            _add_entry(cfg, f"{cfg["sep_nums"]}{number_rand}")
        else:
            _relay_lock(cfg)
    elif rank == 0:
        numbers_rand = []
        for _ in range(cfg["max_nums"]):
            numbers_rand.append(str(_make_rand(cfg, gen_rand(1, cfg["delta_rank"]))))
        _update_and_unlock(
            cfg,
            numbers_rand
        )


def _make_rand(
        cfg: dict,
        r: int
) -> int:
    """
    Generate a random natural number of the r-digits, optionally as an even (1), or a prime (2).
    """
    roundup = lambda n: n + 1 if n != 2 and n % 2 == 0 else n

    num = gen_rand(r)
    i_rand = cfg["win_parent"].ui_pick__cust[cfg["rand_name"]]
    if i_rand == 1:
        while num % 2:
            num = gen_rand(r)
    elif i_rand == 2:
        num = roundup(num)
        while not primality(num):
            num = roundup(gen_rand(r))
    return num


def _control_input(cfg: dict) -> None:
    """
    Session-based user input control for the Entry widget.

    Responsibilities:
        • Treat each valid keystroke sequence as a single input session.
        • Lock the UI during processing and unlock afterwards.
        • Ignore non-text-modifying events or skip checks when Entry is empty.
        • Normalize or ignore repeated delimiters, leading zeros, and other invalid pasted content.
        • Extract numbers and truncate them to configured limits.
        • Update the content widgets, also preserve the cursor position and the last number separator.
        • The last user action or system update takes precedence in case of concurrent calls.
    """
    _relay_lock(cfg, True)
    raw_text = cfg["entry"].get()
    if raw_text == cfg["last_text"]:
        _relay_lock(cfg)
        return
    if not raw_text:
        _update_and_unlock(cfg, [])
        return

    numbers_norm = _truncate_numbers(cfg, re__findall(cfg["patt_nums"], raw_text))
    pos_cursor = cfg["entry"].index("insert")

    _update_and_unlock(
        cfg,
        numbers_norm,
        position= pos_cursor,
        ending= re__search(cfg["patt_final_sep"], raw_text) and len(numbers_norm) < cfg["max_nums"]
    )


def _truncate_numbers(
        cfg: dict,
        nums: list[str]
) -> list[str]:
    """
    Enforce limits on item numbers (priority to the left data side) and max digit length.
    """
    nums = nums[:cfg["max_nums"]]
    for idx in range(len(nums)):
        nums[idx] = nums[idx][:cfg["max_rank"]]
    return nums
