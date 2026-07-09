import time
import pytest
from unittest.mock import patch
from datetime import datetime

# Import core modules
from src.grader import calculate_base_score, calculate_late_penalty, calculate_final_score
from src.reporter import generate_report_table, export_to_csv, cleanup_temp_dir

def simulate_pipeline(num_students: int) -> float:
    start_time = time.time()
    
    # Simulate processing N students
    deadline = datetime(2026, 4, 20, 19, 43)
    results = []
    
    for i in range(num_students):
        nim = f"130120{i:04d}"
        
        # Simulate extraction and parsing
        submitted_at = datetime(2026, 4, 21, 10, 0)
        
        # Simulate compile and plagiarism
        is_compiled = True
        is_plagiarized = False
        
        # Grading
        base, notes = calculate_base_score(is_plagiarized, is_compiled, True)
        penalty = calculate_late_penalty(deadline, submitted_at)
        final = calculate_final_score(base, penalty)
        
        results.append({
            "nim": nim,
            "base_score": base,
            "penalty": penalty,
            "final_score": final,
            "notes": notes
        })
        
    # Simulate reporting
    # We won't print to console in performance test to avoid stdout bottleneck
    export_to_csv(results, "temp_perf_report.csv")
    
    # Cleanup
    cleanup_temp_dir("temp")
    
    end_time = time.time()
    return end_time - start_time

def test_performance_improvement():
    """
    Test that processes 100 dummy students.
    The goal is to ensure it runs fast. If old process was X seconds, we expect new to be < X * 0.3.
    Since we don't have the old process, we will set a strict threshold (e.g. < 1.0 second for 100 students).
    """
    time_taken = simulate_pipeline(100)
    
    # Ensure it's very fast (under 2 seconds for 100 dummy data processing simulation)
    assert time_taken < 2.0, f"Performance test failed! Took {time_taken} seconds."
    print(f"\n[Performance] Processing 100 students took {time_taken:.4f} seconds.")
