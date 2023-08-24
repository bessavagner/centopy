import os
import shutil
import unittest
import tempfile
import zipfile

from unittest.mock import patch

from centopy.base import BaseFilesManager
from centopy.core import FilesManager
from centopy.core import Compressor


class TestBaseFilesManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.manager = BaseFilesManager(self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_file_creation(self):
        # Test creating a new file
        file_name = "test_file.txt"
        file_path = self.manager.file_path(file_name)
        self.assertFalse(file_path.exists())
        with open(file_path, "w", encoding='utf-8') as f:
            f.write("Test content")
        self.assertTrue(file_path.exists())
        self.assertEqual(
            self.manager.get_file_state(file_name), "unknown"
        )

    def test_list_files(self):
        # Test listing files in the directory
        files = ["file1.txt", "file2.txt", "file3.txt"]
        for file_name in files:
            file_path = self.manager.file_path(file_name)
            with open(file_path, "w", encoding='utf-8') as f:
                f.write("Test content")
        listed_files = self.manager.list_files()
        self.assertEqual(set(files), set(listed_files))

    def test_delete_file(self):
        # Test deleting a file
        file_name = "test_file.txt"
        file_path = self.manager.file_path(file_name)
        with open(file_path, "w", encoding='utf-8') as f:
            f.write("Test content")
        self.assertTrue(file_path.exists())
        self.manager.delete_file(file_name)
        self.assertFalse(file_path.exists())
        self.assertEqual(self.manager.get_file_state(file_name), "deleted")

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
            self.manager.delete_file(file_name)
            print(cm.output)
        self.assertIn(expected_log_message, cm.output)

    def test_str_representation(self):
        # Test __str__ representation of the object
        file_name = "test_file.txt"
        file_path = self.manager.file_path(file_name)
        with open(file_path, "w", encoding='utf-8') as f:
            f.write("Test content")
        expected_str = f"Working dir: {self.temp_dir}\n{file_name}: unknown"
        self.assertEqual(str(self.manager), expected_str)

class TestFilesManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.manager = FilesManager(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_write_and_read(self):
        file_name = 'test_write.txt'
        content = "Test content"
        
        self.manager.write(file_name, content)
        read_content = self.manager.read(file_name)
        
        self.assertEqual(read_content, content)

    def test_writeb_and_readb(self):
        file_name = 'test_writeb.txt'
        content = b'Test content'
        
        self.manager.writeb(file_name, content)
        read_content = self.manager.readb(file_name)
        
        self.assertEqual(read_content, content)

    def test_append_and_read(self):
        file_name = 'test_append.txt'
        content1 = "First line\n"
        content2 = "Second line\n"
        
        self.manager.write(file_name, content1)
        self.manager.append(file_name, content2)
        
        read_content = self.manager.read(file_name)
        
        expected_content = content1 + content2
        self.assertEqual(read_content, expected_content)

    def test_appendb_and_readb(self):
        file_name = 'test_appendb.txt'
        content1 = b'First line\n'
        content2 = b'Second line\n'
        
        self.manager.writeb(file_name, content1)
        self.manager.appendb(file_name, content2)
        
        read_content = self.manager.readb(file_name)
        
        expected_content = content1 + content2
        self.assertEqual(read_content, expected_content)

    def test_delete_file(self):
        file_name = 'test_delete.txt'
        content = "Test content"
        
        self.manager.write(file_name, content)
        self.manager.delete_file(file_name)
        
        self.assertFalse(os.path.exists(self.manager.file_path(file_name)))

    def test_get_file_state(self):
        file_name = 'test_state.txt'
        content = "Test content"
        
        self.manager.write(file_name, content)
        state = self.manager.get_file_state(file_name)
        
        self.assertEqual(state, "saved")

    def test_read_nonexistent_file(self):
        # Test loading a nonexistent file
        file_name = "nonexistent_file.txt"
        loaded_contents = self.manager.read(file_name)
        self.assertIsNone(loaded_contents)
        self.assertEqual(self.manager.get_file_state(file_name), "failed")

    def test_invalid_folder_path(self):
        # Test invalid folder path raises ValueError
        with self.assertRaises(ValueError):
            FilesManager("/path/does/not/exist")

    def test_list_files(self):
        # Test listing files in the directory
        files = ["file1.txt", "file2.txt", "file3.txt"]
        for file_name in files:
            file_path = self.manager.file_path(file_name)
            with open(file_path, "w", encoding='utf-8') as f:
                f.write("Test content")
        listed_files = self.manager.list_files()
        self.assertEqual(set(files), set(listed_files))


class TestCompressor(unittest.TestCase):

    def setUp(self):
        self.temp_dir =  tempfile.mkdtemp()
        self.compressor = Compressor('test', wdir=self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_init(self):
        self.assertTrue(self.compressor.path().exists())

    def test_namelist_non_existing_file(self):
        names = self.compressor.namelist()
        self.assertEqual(names, [])

    def test_namelist_existing_file(self):
        file_name = "file.txt"
        file_path = self.compressor.manager.file_path(file_name)
        self.assertFalse(file_path.exists())
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('Test data')
        self.compressor.add(file_name, delete_source=False)
        names = self.compressor.namelist()
        self.assertIn(file_name, names)
        self.assertIn(file_name, self.compressor.manager.list_files())

    def test_add_non_existing_file(self):
        with patch('centopy.core.logger') as mock_logger:
            self.compressor.add('non_existent_file.txt')
            mock_logger.warning.assert_called_once()

    def test_write_and_read_text_file(self):
        self.compressor.write('test.txt', 'Hello, World!')
        content = self.compressor.read('test.txt')
        self.assertEqual(content, 'Hello, World!')

    def test_write_and_read_binary_file(self):
        content = b'Test binary data'
        file_name = "test.bin"
        file_path = self.compressor.manager.file_path(file_name)
        with open(file_path, 'wb') as bin_file:
            bin_file.write(content)
        self.compressor.add(file_name, delete_source=False)
        read_content = self.compressor.read('test.bin', as_text=False)
        self.assertEqual(read_content, content)

    def test_extract_file(self):
        content = 'Extract me'
        file_name = 'test.txt'
        file_path = self.compressor.manager.file_path(file_name)
        self.compressor.write(file_name, content)
        extracted_path = self.compressor.extract(file_name)
        self.assertEqual(extracted_path, str(file_path))
        with open(file_path, 'r', encoding='utf-8') as file_:
            extracted_content = file_.read()
            self.assertEqual(extracted_content, 'Extract me')
    
    def test_writeb_and_readb(self):
        file_name = 'test_writeb.txt'
        content = b'Test binary content'
        
        self.compressor.writeb(file_name, content)
                
        read_content = self.compressor.read(file_name, as_text=False)
        self.assertEqual(read_content, content)

    def test_append(self):
        
        file_name1 = 'test_keep.txt'
        file_name2 = 'test_append.txt'
        content1 = 'This line should remain\n'
        content2_1 = 'First binary line\n'
        content2_2 = 'Second binary line\n'
        
        self.compressor.write(file_name1, content1)
        self.compressor.write(file_name2, content2_1)
        
        name_list_before = self.compressor.namelist()
        
        self.compressor.append(file_name2, content2_2)
                
        read_content = self.compressor.read(file_name2, as_text=True)
        expected_content = content2_1 + content2_2
        
        name_list_after = self.compressor.namelist()
        
        self.assertEqual(read_content, expected_content)
        for member in name_list_before:
            self.assertIn(member, name_list_after)

    def test_appendb(self):
        
        file_name1 = 'test_keep.bin'
        file_name2 = 'test_append.bin'
        content1 = b'This line should remain\n'
        content2_1 = b'First binary line\n'
        content2_2 = b'Second binary line\n'
        
        self.compressor.writeb(file_name1, content1)
        self.compressor.writeb(file_name2, content2_1)
        
        name_list_before = self.compressor.namelist()
        
        self.compressor.appendb(file_name2, content2_2)
                
        read_content = self.compressor.readb(file_name2)
        expected_content = content2_1 + content2_2
        
        name_list_after = self.compressor.namelist()
        
        self.assertEqual(read_content, expected_content)
        for member in name_list_before:
            self.assertIn(member, name_list_after)

    def test_update(self,):

        file_name = 'text_to_update.txt'
        path = self.compressor.manager.folder_path / file_name
        content = "This will be overwritten"
        updated_content = "\nUpdated content"

        self.compressor.write(file_name, content)
        
        with open(path, 'w', encoding='utf-8') as file_:
            file_.write(updated_content)
        
        self.compressor.update(file_name, delete_source=True)
        
        updated_content_read = self.compressor.read(file_name)
        
        self.assertEqual(updated_content_read, updated_content)
        self.assertNotIn(content, updated_content_read)
        self.assertNotIn(file_name, self.compressor.manager.list_files())

if __name__ == "__main__":
    unittest.main()
