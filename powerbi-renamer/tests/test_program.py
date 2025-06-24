def test_clear_folder():
    from src.program import clear_folder
    from pathlib import Path

    # Define a temporary folder for testing
    test_folder = Path('./test-clear-folder')
    test_folder.mkdir(exist_ok=True)

    # Create some files and directories in the test folder
    (test_folder / 'file1.txt').touch()
    (test_folder / 'file2.txt').touch()
    (test_folder / 'subdir').mkdir(exist_ok=True)
    (test_folder / 'subdir' / 'file3.txt').touch()

    # Call the clear_folder function
    clear_folder(test_folder)

    # Check if the folder is empty
    assert not any(test_folder.iterdir()), "The folder should be empty after clearing."

    # Clean up the test folder
    test_folder.rmdir()  # Remove the test folder itself