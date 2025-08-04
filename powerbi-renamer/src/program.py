import stat
import shutil

from pathlib import Path
from typing import Union

try:
    from src.powerbi import PowerBI
except:
    from powerbi import PowerBI

output_folder = Path(__file__).parent / '../powerbi-files/output-pbi'
target_folder = Path(__file__).parent / '../powerbi-files/target-pbi'
test_folder   = Path(__file__).parent / '../powerbi-files/test-pbi'

# Ensure these exist when you run as a script
output_folder.mkdir(exist_ok=True)
target_folder.mkdir(exist_ok=True)

def clear_folder(root: Union[str, Path], *, keep_root: bool = True) -> None:
    """
    Recursively clear read-only flags and delete all files/dirs under `root`.
    If keep_root is False, the root folder itself is also removed.
    """
    root = Path(root)
    if not root.is_dir():
        raise FileNotFoundError(f"The following folder does not exist: {root}.")

    def _on_rm_error(func, path, exc_info):
        p = Path(path)
        p.chmod(stat.S_IWRITE)
        func(path)

    for child in root.iterdir():
        if child.is_dir():
            shutil.rmtree(child, onerror=_on_rm_error)
        else:
            child.chmod(stat.S_IWRITE)
            child.unlink()

    if not keep_root:
        shutil.rmtree(root, onerror=_on_rm_error)


def main():
    clear_folder(output_folder, keep_root=True)
    powerbi = PowerBI(target_folder)
    print(f"Found report: {powerbi.name}")

if __name__ == "__main__":
    main()