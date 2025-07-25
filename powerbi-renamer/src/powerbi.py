from pathlib import Path
from typing import Union

class PowerBI(object):
    """
    A class to represent a Power BI report.
    It can be used to load and manipulate Power BI report files.
    """

    def __init__(self, object_folder: Union[str, Path]):
        self.name = self.load_target_folder(object_folder)
        self.location = object_folder

    def load_target_folder(self, root: Union[str, Path]) -> str:
        """
        Validates that a sample folder and the given target folder exist,
        checks for exactly one .pbip file, and ensures its definition folder exists.
        """
        target_folder = Path(root)
        sample_folder = target_folder.parent / "sample-pbi"

        if not sample_folder.is_dir():
            raise FileNotFoundError(f"Sample folder '{sample_folder}' does not exist. Please ensure it is present.")

        if not target_folder.is_dir():
            raise FileNotFoundError(f"The following folder does not exist: {target_folder}.")

        pbip_files = list(target_folder.glob("*.pbip"))
        if len(pbip_files) == 0:
            raise FileNotFoundError(f".pbip file does not exist in {target_folder}.")
        if len(pbip_files) > 1:
            raise RuntimeError(f"Too many .pbip files in {target_folder}.")

        pbip_file = pbip_files[0]
        report_name = pbip_file.stem
        report_definition_folder = (target_folder / f"{report_name}.Report" / "definition")

        if not report_definition_folder.is_dir():
            raise FileNotFoundError(f"Expected report folder '{report_definition_folder}' not found.")

        return pbip_file.name
