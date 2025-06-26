import os, stat, pytest
from pathlib import Path

from src.program import clear_folder

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
