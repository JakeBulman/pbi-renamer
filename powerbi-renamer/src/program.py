import json, os, stat, shutil, re
from pathlib import Path
from typing import Union

output_folder = Path(Path(__file__).parent / '../powerbi-files/output-pbi')
target_folder = Path(Path(__file__).parent / '../powerbi-files/target-pbi')
test_folder = Path(Path(__file__).parent / '../powerbi-files/test-pbi')

output_folder.mkdir(exist_ok=True)
target_folder.mkdir(exist_ok=True)

def clear_folder(root: Union[str, Path],*,keep_root: bool = True) -> None:
    """
    Recursively clear read-only flags and delete all files/dirs under `root`.
    If keep_root is False, the root folder itself is also removed.
    """
    root = Path(root)

    def _on_rm_error(func, path, exc_info):
        # Called by shutil.rmtree on failure (e.g. read-only). Clear flag and retry.
        p = Path(path)
        p.chmod(stat.S_IWRITE)
        func(path)

    # Iterate direct children of root
    for child in root.iterdir():
        if child.is_dir():
            # Recursively delete entire subdir, handling read-only via onerror
            shutil.rmtree(child, onerror=_on_rm_error)
        else:
            # File: clear RO flag then unlink
            child.chmod(stat.S_IWRITE)
            child.unlink()

    # Finally, remove the root folder itself if desired
    if not keep_root:
        shutil.rmtree(root, onerror=_on_rm_error)
        
#Begin the recursion
clear_folder(output_folder, keep_root=True)