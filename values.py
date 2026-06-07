"""
Constant definitions for module settings, windows texts, and keyboard events used throughout the application.

Format specifiers:
    • {lng} for language ID: 0=EN, 1=UA, 2=RU; other textual values are localized by selecting from tuples.
    • {imu} associate a custom default value of the randomizer with its module.
"""


sm1 = "• "
sm2 = 406       # px min width
sm3 = 14        # px cell
sm4 = sm3 // 2  # px half cell
SET_MUS = {
    0: {
        "Name": (f"{sm1}GCD and LCM Computation", f"{sm1}Обчислення НСД і НСК", f"{sm1}Вычисление НОД и НОК"),
        "Path": "modules.mu0",
        "Path_help": "docs/spec_mu0_{lng}.pkl",
        "Path_result": "artfs/Factoring.txt",
        "Geometry_win": (400, 300),
        "Minsize_win": (400, 200),
        "Max_numbers": 6,
        "Min_numbers": 1,
        "Max_rank": 8,
    },
    1: {
        "Name": (f"{sm1}Common Fractions", f"{sm1}Звичайні дроби", f"{sm1}Обыкновенные дроби"),
        "Path": "modules.mu1",
        "Path_help": "docs/spec_mu1_{lng}.pkl",
        "Geometry_win": (450, 360),
        "Minsize_win": (sm2, 200),
        "Widths_cell": (sm3, sm4),
        "Min_cells": (sm2 - sm3 * 3) // sm4,
        "Max_numbers": 4,
        "Min_numbers": 4,
        "Max_rank": 3,
    },
}

SET_CUST = {
    "Path": "artfs/cust_set.pkl",
    "LANG": {
        "name": "default_lang",
        "valid": (0, 1, 2),
    },
    "MUNIT": {
        "name": "default_munit",
        "valid": (0, 1),
    },
    "RAND": {
        "name": "default_rand_mu{imu}",
        "valid": (0, 1, 2),
    },
}

tp1 = "\n[Enter]"
tp2 = (" [Ctrl]+[L]", " [Up]/[Down]", " [Ctrl]+[Q]")
kb_exit = "<Control-q>"
TEXTS_PICK = {
    "Title": ("Units", "Модулі", "Модули"),
    "Menu": {
        "name": ("Language", "Мова", "Язык"),
        "languages": ("eng", "укр", "рус"),
    },
    "Button": (f"Begin{tp1}", f"Почати{tp1}", f"Начать{tp1}"),
    "Label": ("language{0}, unit{1}, exit{2}".format(*tp2), "мова{0}, модуль{1}, вихід{2}".format(*tp2),
              "язык{0}, модуль{1}, выход{2}".format(*tp2)),
    "Event_kb": {
        "directions": {"<Up>": -1, "<Down>": 1},
        "begin": "<Return>",
        "lang": "<Control-l>",
        "exit": kb_exit,
    },
}

tm11, TM12 = "RULES", "UI"
tm2 = " [Ctrl]+[N]:"
tm3 = ("R-", " [Ctrl]+[R]  ")
tm4, tm5, tm6 = "\n[Ctrl]+[B]", "\n[Ctrl]+[E]", "\n[Ctrl]+[Q]"
TEXTS_MU = {
    "Menu": {
        "Help": {
            "name": ("Info", "Довідка", "Справка"),
            "blocks": (tm11, TM12),
            tm11: ("Rules", "Правила", "Правила"),
            TM12: ("Interface", "Інтерфейс", "Интерфейс"),
        },
        "0_9": {
            "name": "0÷9",
            "first_spec": ("Layout:", "Розкладка:", "Раскладка:"),
            "next_items": ("<del", "<-", "->", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ";"),
        },
        "Rand": {
            "name": ("Generator", "Генератор", "Генератор"),
            "first_iter": ((f"Natural{tm2}", f"Even{tm2}", f"Prime{tm2}"),
                           (f"Натуральне{tm2}", f"Парне{tm2}", f"Просте{tm2}"),
                           (f"Натуральное{tm2}", f"Четное{tm2}", f"Простое{tm2}")),
            "next_suffix": ("-digit", "-значне", "-значное"),
            "last_series": ("{0}digit{1}".format(*tm3), "{0}значні{1}".format(*tm3), "{0}значные{1}".format(*tm3)),
        },
    },
    "Label": ("digits: ", "розряди: ", "разряды: "),
    "Button": {
        "back": (f"Units{tm4}", f"Модулі{tm4}", f"Модули{tm4}"),
        "equal": (f"Execute{tm5}", f"Виконати{tm5}", f"Выполнить{tm5}"),
        "exit": (f"Exit{tm6}", f"Вихід{tm6}", f"Выход{tm6}"),
        "clean": (f"Clean", f"Очистити", f"Очистить"),
    },
    "Event_kb": {
        "back": "<Control-b>",
        "equal": "<Control-e>",
        "exit": kb_exit,
        "rand_nums": "<Control-n>",
        "rand": "<Control-r>",
    },
}

tc1 = "? / ->"
tc2 = "\n[Ctrl]+[Q]"
TEXTS_CONFIRM = {
    "Title": (f"Really{tc1}", f"Точно{tc1}", f"Точно{tc1}"),
    "Button": (f"Finish work{tc2}", f"Завершити роботу{tc2}", f"Завершить работу{tc2}"),
    "Event_kb": kb_exit,
}

MAP_RANKS = {"1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "0":"⁰"}

DMAP = {"clr0": "blue", "clr1": "black", "clr2": "darkblue", "clr3": "grey", "clr4": "darkred",
        "font": ('Comic Sans MS', 9, 'bold'), "font_ops": ('Comic Sans MS', 11, 'bold'),
        "equal": "=", "larger": ">", "less": "<", "adt": "+", "sub": "−", "mul": "•", "div": ":"}
