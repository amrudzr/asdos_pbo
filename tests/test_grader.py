import unittest
from datetime import datetime, timedelta
from src.grader import calculate_base_score, calculate_late_penalty, calculate_final_score

class TestGrader(unittest.TestCase):
    def test_calculate_base_score(self):
        # Format: is_plagiarized, is_compiled, has_good_explanation
        
        # Original and good explanation
        score, flag = calculate_base_score(False, True, True)
        self.assertEqual(score, 90)
        self.assertEqual(flag, "")
        
        # Original and bad explanation
        score, flag = calculate_base_score(False, True, False)
        self.assertEqual(score, 80)
        self.assertEqual(flag, "REVIEW MANUAL")
        
        # Plagiarized (explanation doesn't matter)
        score, flag = calculate_base_score(True, True, True)
        self.assertEqual(score, 69)
        self.assertEqual(flag, "")
        
        score, flag = calculate_base_score(True, True, False)
        self.assertEqual(score, 69)
        self.assertEqual(flag, "")
        
        # Not compiled (plagiarism or explanation doesn't matter)
        score, flag = calculate_base_score(False, False, True)
        self.assertEqual(score, 0)
        self.assertEqual(flag, "")

    def test_calculate_late_penalty(self):
        deadline = datetime(2026, 4, 20, 23, 59, 59)
        
        # On time
        submitted = datetime(2026, 4, 20, 23, 59, 59)
        self.assertEqual(calculate_late_penalty(deadline, submitted), 0)
        
        submitted = datetime(2026, 4, 20, 10, 0, 0)
        self.assertEqual(calculate_late_penalty(deadline, submitted), 0)
        
        # 1 day late (counts as 1 week penalty)
        submitted = deadline + timedelta(days=1)
        self.assertEqual(calculate_late_penalty(deadline, submitted), 1)
        
        # 7 days late (exactly 1 week)
        submitted = deadline + timedelta(days=7)
        self.assertEqual(calculate_late_penalty(deadline, submitted), 1)
        
        # 8 days late (counts as 2 weeks penalty)
        submitted = deadline + timedelta(days=8)
        self.assertEqual(calculate_late_penalty(deadline, submitted), 2)

    def test_calculate_final_score(self):
        deadline = datetime(2026, 4, 20, 23, 59, 59)
        submitted = deadline + timedelta(days=8) # 2 penalty points
        
        base_score, flag = calculate_base_score(False, True, True) # 90
        final_score = calculate_final_score(base_score, calculate_late_penalty(deadline, submitted))
        
        self.assertEqual(final_score, 88)

if __name__ == '__main__':
    unittest.main()
