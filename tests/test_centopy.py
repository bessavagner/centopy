import os
import shutil
import unittest
import tempfile

from centopy.base import BaseFilesManager
from centopy.core import FilesManager


class TestBaseFilesManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.file_manager = BaseFilesManager(self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_file_creation(self):
        # Test creating a new file
        file_name = "test_file.txt"
        file_path = self.file_manager.file_path(file_name)
        self.assertFalse(file_path.exists())
        with open(file_path, "w", encoding='utf-8') as f:
            f.write("Test content")
        self.assertTrue(file_path.exists())
        self.assertEqual(
            self.file_manager.get_file_state(file_name), "unknown"
        )

    def test_list_files(self):
        # Test listing files in the directory
        files = ["file1.txt", "file2.txt", "file3.txt"]
        for file_name in files:
            file_path = self.file_manager.file_path(file_name)
            with open(file_path, "w", encoding='utf-8') as f:
                f.write("Test content")
        listed_files = self.file_manager.list_files()
        self.assertEqual(set(files), set(listed_files))

    def test_delete_file(self):
        # Test deleting a file
        file_name = "test_file.txt"
        file_path = self.file_manager.file_path(file_name)
        with open(file_path, "w", encoding='utf-8') as f:
            f.write("Test content")
        self.assertTrue(file_path.exists())
        self.file_manager.delete_file(file_name)
        self.assertFalse(file_path.exists())
        self.assertEqual(self.file_manager.get_file_state(file_name), "deleted")

    def test_invalid_folder_path(self):
        # Test invalid folder path raises ValueError
        with self.assertRaises(ValueError):
            BaseFilesManager("/path/does/not/exist")

    def test_nonexistent_file_deletion(self):
        # Test deleting a nonexistent file
        file_name = "nonexistent_file.txt"
        expected_log_message = (
            f"WARNING:standard:File not found: {file_name}. "
            "Nothing to delete"
        )
        with self.assertLogs('standard', level="WARNING") as cm:
            self.file_manager.delete_file(file_name)
            print(cm.output)
        self.assertIn(expected_log_message, cm.output)

    def test_str_representation(self):
        # Test __str__ representation of the object
        file_name = "test_file.txt"
        file_path = self.file_manager.file_path(file_name)
        with open(file_path, "w", encoding='utf-8') as f:
            f.write("Test content")
        expected_str = f"Working dir: {self.temp_dir}\n{file_name}: unknown"
        self.assertEqual(str(self.file_manager), expected_str)

class TestFilesManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.file_manager = FilesManager(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_save_and_load_file(self):
        # Test saving and loading a file
        file_name = "test_file.txt"
        file_contents = "Test content"
        self.file_manager.write(file_name, file_contents)
        loaded_contents = self.file_manager.read(file_name)
        self.assertEqual(loaded_contents, file_contents)
        self.assertEqual(self.file_manager.get_file_state(file_name), "loaded")

    def test_load_nonexistent_file(self):
        # Test loading a nonexistent file
        file_name = "nonexistent_file.txt"
        loaded_contents = self.file_manager.read(file_name)
        self.assertIsNone(loaded_contents)
        self.assertEqual(self.file_manager.get_file_state(file_name), "failed")

    def test_read_and_write_file(self):
        # Test reading and writing a file
        file_name = "test_file.txt"
        file_contents = "Test content"
        self.file_manager.write(file_name, file_contents)
        read_contents = self.file_manager.read(file_name)
        self.assertEqual(read_contents, file_contents)

    def test_invalid_folder_path(self):
        # Test invalid folder path raises ValueError
        with self.assertRaises(ValueError):
            FilesManager("/path/does/not/exist")

    def test_list_files(self):
        # Test listing files in the directory
        files = ["file1.txt", "file2.txt", "file3.txt"]
        for file_name in files:
            file_path = self.file_manager.file_path(file_name)
            with open(file_path, "w", encoding='utf-8') as f:
                f.write("Test content")
        listed_files = self.file_manager.list_files()
        self.assertEqual(set(files), set(listed_files))


if __name__ == "__main__":
    unittest.main()
