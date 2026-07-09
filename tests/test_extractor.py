import os
import unittest
import zipfile
import shutil
from src.extractor import extract_archives

class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_data"
        self.temp_dir = "test_temp"
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Create a dummy zip file
        self.valid_zip_path = os.path.join(self.test_dir, "valid.zip")
        with zipfile.ZipFile(self.valid_zip_path, 'w') as zf:
            zf.writestr('dummy.txt', 'Hello World')
            
        # Create a corrupt zip file
        self.corrupt_zip_path = os.path.join(self.test_dir, "corrupt.zip")
        with open(self.corrupt_zip_path, 'w') as f:
            f.write("This is not a real zip file.")
            
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            
    def test_extract_valid_zip(self):
        extract_archives(self.test_dir, self.temp_dir)
        
        # Verify that 'valid' directory is created inside test_temp
        extracted_dir = os.path.join(self.temp_dir, "valid")
        self.assertTrue(os.path.exists(extracted_dir))
        self.assertTrue(os.path.exists(os.path.join(extracted_dir, "dummy.txt")))
        
    def test_extract_corrupt_zip_no_crash(self):
        # Even with a corrupt zip, extract_archives should not raise an exception
        try:
            extract_archives(self.test_dir, self.temp_dir)
        except Exception as e:
            self.fail(f"extract_archives raised an exception unexpectedly: {e}")
            
if __name__ == '__main__':
    unittest.main()
