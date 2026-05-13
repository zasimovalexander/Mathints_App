"""
Use only as a dev helper for preparing and filling the specification repository from strictly formatted TXT sources.
"""


from os import chdir as os__chdir
from pathlib import Path as pathlib__Path
from pickle import dump as pickle__dump, load as pickle__load

import values as vls


ITEMS = (vls.tm11, vls.TM12)  # sourced from the constants module to preserve a single source of truth


def save_pkl(
        dir_saving: str,
        dir_files: str,
        suf_files: str
) -> None:
    """
    Parse helper TXT files and save each module's data as a separate pickle.
    """
    path = pathlib__Path(dir_saving)
    path.mkdir(parents=True, exist_ok=True)
    for path_file in pathlib__Path(dir_files).glob(f"{suf_files}*.txt"):
        specific = _read_txt(path_file)
        for k in specific.keys():
            path_pkl = path / f"{suf_files}_{k}_{path_file.stem[-1]}.pkl"
            with path_pkl.open("wb") as f_pkl:
                pickle__dump(specific[k], f_pkl)


def _read_txt(path_content: pathlib__Path) -> dict[str, dict[str, str]]:
    """
    Parse a helper TXT file and prepare data structure.

    Returns:
        dict: Data from the TXT file, as a result like {"key_munit": {"item0": "text0", "item1": "text1"}, ...}

    Notes:
        • The TXT file must have a strict format:
            - each unit's description is a 6-line block
            - the 1st line of each block is ignored and used only as a loop condition
            - the last line of the file must be empty.
        • During execution, the two format specifiers are also populated with values from the app's constants file.
    """
    with open(path_content, "r", encoding="utf-8") as f_txt:
        spec = {}
        while f_txt.readline().strip():
            key_munit, item0, text0, item1, text1 = [f_txt.readline().strip() for _ in range(5)]
            text0, text1 = [txt.replace("|", "\n") for txt in (text0, text1)]
            constants = vls.SET_MUS[int(key_munit[-1])]
            text1 = text1.format(**{"qty": constants["Max_numbers"], "rng": constants["Max_rank"]})
            spec[key_munit] = {item0.format(rules=ITEMS[0]): text0, item1.format(ui=ITEMS[1]): text1}
    return spec


def load_pkl(path_store: str) -> dict[str, str] | str:
    """
    Test loading data from a pickle file.

    Returns:
        dict: Data from the PKL file like {"item0": "text0", "item1": "text1"}, or warning if the file does not exist.
    """
    path = pathlib__Path(path_store)
    if path.exists():
        with path.open("rb") as f:
            return pickle__load(f)
    return "[data not found]"


if __name__ == "__main__":
    os__chdir('..')
    save_pkl("docs", "_helpDev", "spec")
    #print(load_pkl("docs/spec_mu1_0.pkl"))
