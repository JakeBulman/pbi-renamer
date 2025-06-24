import json, os, stat, shutil, re
from pathlib import Path


output_folder = Path(Path(__file__).parent / '../powerbi-files/output-pbi')
target_folder = Path(Path(__file__).parent / '../powerbi-files/target-pbi')
test_folder = Path(Path(__file__).parent / '../powerbi-files/test-pbi')

output_folder.mkdir(exist_ok=True)
target_folder.mkdir(exist_ok=True)

def clear_folder(top_folder: Path) -> None:
    """
    Takes a directory folder and removes all files and permissions from it recursively so that it can be emptied.
    """

    def recursive_ro_strip(current_dir) -> None:
        dirs = current_dir.glob('*')
        item_count = len(list(dirs))
        #Reset glob as it is "consumed" by the counter
        dirs = current_dir.glob('*')
        #Check if anything is in the folder
        if item_count > 0:
            for dir in dirs:
                #If item is a folder, strip it's read-only. If it's a file, delete it.
                if Path(dir).is_dir():
                    os.chmod(dir.absolute() ,stat.S_IWRITE)
                    recursive_ro_strip(dir)
                else:
                    dir.unlink()
            #Run through everything 
            dirs = current_dir.glob('*')
            for dir in dirs:
                os.chmod(dir.absolute() ,stat.S_IWRITE)
                recursive_ro_strip(dir)
        else:
            #Once all files and read_only removed from within, delete the folder, unless it's top folder
            if current_dir.resolve() != top_folder.resolve():
                shutil.rmtree(current_dir)

    #Begin the recursion
    recursive_ro_strip(top_folder)


clear_folder(output_folder)
