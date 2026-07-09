import unittest
from datetime import datetime
from src.parser import extract_nim, parse_timestamp

class TestParser(unittest.TestCase):
    def test_extract_nim_standard(self):
        filename = "Tugas_PBO_1234567890_Rizky"
        self.assertEqual(extract_nim(filename), "1234567890")
        
    def test_extract_nim_custom_format(self):
        filename = "12.3456.7.89012_Tugas"
        self.assertEqual(extract_nim(filename), "12.3456.7.89012")
        
    def test_extract_nim_not_found(self):
        filename = "Tugas_PBO_Tanpa_NIM"
        self.assertIsNone(extract_nim(filename))
        
    def test_parse_timestamp_valid(self):
        # Format: [Hari], [DD] [Bulan] [YYYY], [H]:[MM] [AM/PM]
        ts_str = "Monday, 20 April 2026, 7:43 PM"
        dt = parse_timestamp(ts_str)
        self.assertIsNotNone(dt)
        self.assertEqual(dt.year, 2026)
        self.assertEqual(dt.month, 4)
        self.assertEqual(dt.day, 20)
        self.assertEqual(dt.hour, 19)
        self.assertEqual(dt.minute, 43)
        
    def test_parse_timestamp_invalid(self):
        ts_str = "2026-04-20 19:43:00"
        dt = parse_timestamp(ts_str)
        self.assertIsNone(dt)

if __name__ == '__main__':
    unittest.main()
