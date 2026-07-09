import math
from datetime import datetime
from typing import Tuple
import os
import re

def check_for_explanations(source_dir: str) -> bool:
    """
    Check if the Java files in the source directory contain meaningful explanations in comments.
    """
    total_comment_words = 0
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.java'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Find block comments and line comments
                        block_comments = re.findall(r'/\*.*?\*/', content, re.DOTALL)
                        line_comments = re.findall(r'//.*', content)
                        
                        for comment in block_comments + line_comments:
                            # Clean comment markers and split into words
                            text = re.sub(r'^/\*+|\*+/$|^//+', '', comment)
                            words = [w for w in text.split() if w.isalnum()]
                            total_comment_words += len(words)
                except Exception:
                    pass
                    
    # Heuristic: > 15 words in comments across the project indicates they added explanations
    return total_comment_words > 15

def calculate_base_score(is_plagiarized: bool, is_compiled: bool, has_good_explanation: bool, file_format: str = "") -> Tuple[int, str]:
    """
    Calculate the base score for a project submission.
    
    Returns:
        Tuple[int, str]: A tuple containing the base score and a manual review flag if needed.
    """
    if not is_compiled:
        # Default to 0 for compilation failure, up to policy (0-50).
        return 0, ""
    
    if is_plagiarized:
        return 69, ""
        
    if file_format == ".greenfoot":
        return 78, ""
        
    if has_good_explanation:
        return 95, ""
    else:
        return 80, "REVIEW MANUAL"

def calculate_late_penalty(deadline: datetime, submitted_at: datetime) -> int:
    """
    Calculate late penalty points. Deducts 1 point per week of delay.
    """
    if submitted_at <= deadline:
        return 0
        
    delta = submitted_at - deadline
    weeks_late = math.ceil(delta.total_seconds() / (7 * 24 * 3600))
    return weeks_late

def calculate_final_score(base_score: int, late_penalty: int) -> int:
    """
    Calculate the final score after applying late penalty.
    """
    return max(0, base_score - late_penalty)
