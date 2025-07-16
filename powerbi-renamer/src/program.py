import json
import os
import stat
import shutil
import re

from pathlib import Path
from typing import Union

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

def check_target_folder(root: Union[str, Path]) -> str:
    """
    Validates that a sample folder and the given target folder exist,
    checks for exactly one .pbip file, and ensures its definition folder exists.
    """
    target_folder = Path(root)
    sample_folder = target_folder.parent / "sample-pbi"



    if not sample_folder.is_dir():
        raise FileNotFoundError(
            f"Sample folder '{sample_folder}' does not exist. Please ensure it is present."
        )

    if not target_folder.is_dir():
        raise FileNotFoundError(
            f"Target folder '{target_folder}' does not exist. Please ensure it is present."
        )

    pbip_files = list(target_folder.glob("*.pbip"))
    if len(pbip_files) == 0:
        raise FileNotFoundError(f".pbip file does not exist in {target_folder}.")
    if len(pbip_files) > 1:
        raise RuntimeError(f"Too many .pbip files in {target_folder}.")

    pbip_file = pbip_files[0]
    report_name = pbip_file.stem
    report_definition_folder = (
        target_folder.parent / f"{report_name}.Report" / "definition"
    )

    if not report_definition_folder.is_dir():
        raise FileNotFoundError(
            f"Expected report folder '{report_definition_folder}' not found."
        )

    return pbip_file.name

def main():
    clear_folder(output_folder, keep_root=True)
    result = check_target_folder(target_folder)
    print(f"Found report: {result}")

if __name__ == "__main__":
    main()