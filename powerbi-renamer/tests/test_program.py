import os, stat, pytest, shutil
from pathlib import Path

from src.program import clear_folder, check_target_folder

def test_clear_folder():
    # Setup: create a temp folder and populate it
    test_folder = Path('./test-clear-folder')
    if test_folder.exists():
        pytest.skip("Please remove existing './test-clear-folder' before running tests")
    test_folder.mkdir()

    # Normal files
    (test_folder / 'file1.txt').write_text('hello')
    (test_folder / 'file2.txt').write_text('world')

    # Nested subdir with a file
    subdir = test_folder / 'subdir'
    subdir.mkdir()
    (subdir / 'file3.txt').write_text('foo')

    # Read-only subdir + file
    ro_subdir = test_folder / 'readonly_subdir'
    ro_subdir.mkdir()
    ro_file = ro_subdir / 'secret.txt'
    ro_file.write_text('top secret')
    # Make both the file and the folder read-only
    os.chmod(ro_file, stat.S_IREAD)
    os.chmod(ro_subdir, stat.S_IREAD)

    # Exercise
    clear_folder(test_folder)

    # Verify: nothing left inside
    assert not any(test_folder.iterdir()), "Folder must be empty regardless of read-only flags"

    # Teardown: remove the (now empty) folder
    test_folder.rmdir()

def test_check_target_folder():
    # Setup: create a temp folder and populate it with sample files
    test_sample_folder = Path(Path(__file__).parent / '../powerbi-files/sample-pbi/')

    # Check that the sample folder exists, as it is required for testing
    try:
        assert test_sample_folder.exists()
    except AssertionError:
        raise FileNotFoundError(f"Sample folder ../powerbi-files/sample-pbi/ does not exist. Please ensure it is present before running tests.")

    # Create the target folder for testing
    test_target_folder = Path(Path(__file__).parent / '../powerbi-files/test-target-pbi/')
    if test_target_folder.exists():
        test_target_folder.rmdir()  # Remove existing folder if it exists
    test_target_folder.mkdir()


    ###Excercise 1###
    # Exercise1: check if the target folder has no .pbip file
    with pytest.raises(FileNotFoundError) as excinfo:
        check_target_folder(test_target_folder)
    # Verify1: check that the exception message is correct
    assert str(excinfo.value) == f".pbip file does not exist in {test_target_folder}."
    

    ###Excercise 2###
    # Copy sample files to the target folder
    shutil.copytree(test_sample_folder, test_target_folder, dirs_exist_ok=True)

    # Exercise2: check if the target folder contains exactly one .pbip file
    test_report_name = check_target_folder(test_target_folder)
    # Verify2: check if the target folder exists and contains exactly one .pbip file
    assert test_report_name == "Test PBI.pbip", f"Expected exactly one .pbip file in {test_target_folder}, found {test_report_name}."


    ###Excercise 3###
    # Copy extra sample file to the target folder
    shutil.copy(Path(test_sample_folder / "Test PBI.pbip") , test_target_folder, dirs_exist_ok=True)

    # Exercise3: check if the target folder has multiple .pbip files. 
    # This test could be extended to cover multiple folders, but as the process runs off of the .pbip file's name it shouldn't be an issue.
    with pytest.raises(RuntimeError) as excinfo:
        check_target_folder(test_target_folder)  
    # Verify3: check that the exception message is correct
    assert str(excinfo.value) == f"Too many .pbip files in {test_target_folder}."


    ###Excercise 4###
    # Delete target-pbi folder and check for errors
    target_folder = Path(Path(__file__).parent / '../powerbi-files/target-pbi/')
    target_folder.rmdir()
    # Exercise4: check if an error is raised when the target folder doesn'ty exist. 
    with pytest.raises(RuntimeError) as excinfo:
        check_target_folder(test_target_folder)  
    # Verify3: check that the exception message is correct
    assert str(excinfo.value) == f"Too many .pbip files in {test_target_folder}."  


    # Teardown: remove all test folders, create removed folders if they don't exist
    test_target_folder.rmdir()
    target_folder.mkdir(exist_ok=True)

