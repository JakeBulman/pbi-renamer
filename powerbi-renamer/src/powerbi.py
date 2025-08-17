from pathlib import Path
from typing import Union
import json, re

class Page(object):
    """
    A class to represent a page in a Power BI report.
    It can be used to manipulate the page's properties.
    """

    def __init__(self, page_name : str, root: Union[str, Path]):
        self.name = page_name #get this from pages.json
        self.display_name = self.set_displayname(self, root)
        self.required_name = "B"
        
    def __repr__(self):
        return f"Page(name={self.name})"
    
    def set_displayname(self,root : Union[str, Path]) -> None:
        """
        Sets the name of the page.
        """
        page_json = (root / self.name / "page.json")

        # Here you would add logic to update the page's name in the actual Power BI file.
    

class PowerBI(object):
    """
    A class to represent a Power BI report.
    It can be used to load and manipulate Power BI report files.
    """
        
    def __init__(self, object_folder: Union[str, Path]):
        self.name = self.load_target_folder(object_folder)
        self.location = object_folder
        self.report_pages_folder = Path(object_folder) / f"{self.name}.Report" / "definition/pages"
        self.pages = [] # List to hold Page objects
        self.load_pages()
        print(self.pages[1].name)

    def slugify(s: str) -> str:
        """
        Convert a string into a slug ("Page 1" -> "page-1").
        """
        s = s.lower().strip()
        s = re.sub(r'[^\w\s-]', '', s)
        s = re.sub(r'[\s_-]+', '-', s)
        s = re.sub(r'^-+|-+$', '', s)
        return s

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

        return report_name
    
    def load_pages(self) -> list:
        """
        Loads the pages from the Power BI report.
        This method reads pages.json file and populates self.pages.
        """
        pages_file = self.report_pages_folder / "pages.json"
        if not pages_file.is_file():
            raise FileNotFoundError(f"Pages file '{pages_file}' does not exist.")
        

        # Here you would add logic to read the JSON file and populate self.pages.
        with open(pages_file, 'r') as j:
            json_pages = json.loads(j.read())
            json_pages_list = json_pages.get('pageOrder')
            print(json_pages_list)
            for page in json_pages_list:
                self.pages.append(Page(page, self.report_pages_folder))




