import os
import javalang  # type: ignore
from typing import List, Dict, Set

class PlagiarismChecker:
    def __init__(self, exclude_files: List[str] = None):
        """
        Initializes the PlagiarismChecker.
        
        Args:
            exclude_files: List of file names to be ignored (e.g., standard template files).
        """
        self.exclude_files = set(exclude_files) if exclude_files else set()
        self.similarity_threshold = 80.0
        self.ignore_ngrams = set()
        
    def get_ngrams(self, tokens: List[str], n: int = 3) -> Set[tuple]:
        if len(tokens) < n:
            return set([tuple(tokens)]) if tokens else set()
        return set(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))
        
    def build_corpus(self, directories: List[str], base_dir: str = ""):
        """
        Analyzes all projects to find common n-grams (boilerplate) and ignores them.
        """
        ngram_doc_counts = {}
        total_docs = len(directories)
        
        for d in directories:
            path = os.path.join(base_dir, d) if base_dir else d
            files = self._read_java_files(path)
            code = "\n".join(files.values())
            tokens = self._get_ast_tokens(code)
            ngrams = self.get_ngrams(tokens)
            
            for ng in ngrams:
                ngram_doc_counts[ng] = ngram_doc_counts.get(ng, 0) + 1
                
        # If an ngram appears in > 50% of students, it's lecturer's boilerplate
        threshold = total_docs * 0.5
        for ng, count in ngram_doc_counts.items():
            if count > threshold:
                self.ignore_ngrams.add(ng)
        
    def _read_java_files(self, directory: str) -> Dict[str, str]:
        """
        Reads all .java files in the given directory except those in the exclude_files.
        """
        java_contents = {}
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.java') and file not in self.exclude_files:
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            java_contents[path] = f.read()
                    except Exception:
                        pass
        return java_contents

    def _get_ast_tokens(self, source_code: str) -> List[str]:
        """
        Extracts token types and specific values from source code using javalang for comparison.
        This helps differentiate between generic boilerplate and actual copied logic.
        """
        try:
            tokens = list(javalang.tokenizer.tokenize(source_code))
            result = []
            for tok in tokens:
                tok_type = type(tok).__name__
                # Sertakan nilai untuk variabel, teks, dan angka agar unik
                if tok_type in ('Identifier', 'String', 'Decimal', 'Integer', 'Boolean', 'Character'):
                    result.append(f"{tok_type}:{tok.value}")
                else:
                    result.append(tok_type)
            return result
        except Exception:
            return []
            
    def _calculate_similarity(self, tokens1: List[str], tokens2: List[str]) -> float:
        """
        Calculates the similarity percentage between two lists of tokens using Tri-grams.
        """
        if not tokens1 and not tokens2:
            return 100.0
        if not tokens1 or not tokens2:
            return 0.0
            
        ngrams1 = self.get_ngrams(tokens1)
        ngrams2 = self.get_ngrams(tokens2)
        
        if not ngrams1 and not ngrams2:
            return 100.0
        if not ngrams1 or not ngrams2:
            return 0.0
            
        # Hapus boilerplate dari perhitungan
        ngrams1 = ngrams1 - self.ignore_ngrams
        ngrams2 = ngrams2 - self.ignore_ngrams
        
        intersection = ngrams1.intersection(ngrams2)
        union = ngrams1.union(ngrams2)
        
        if len(union) == 0:
            # Jika semua kode adalah boilerplate, berarti custom logic 0%, similarity 0%
            return 0.0
            
        return (len(intersection) / len(union)) * 100.0

    def check_project_similarity(self, project1_dir: str, project2_dir: str) -> tuple[float, str]:
        """
        Checks the similarity between two project directories.
        Returns a tuple of (percentage value, recap string).
        """
        files1 = self._read_java_files(project1_dir)
        files2 = self._read_java_files(project2_dir)
        
        if not files1 or not files2:
            return 0.0, ""
            
        # Combine all code in the project for overall similarity
        code1 = "\n".join(files1.values())
        code2 = "\n".join(files2.values())
        
        tokens1 = self._get_ast_tokens(code1)
        tokens2 = self._get_ast_tokens(code2)
        
        overall_sim = self._calculate_similarity(tokens1, tokens2)
        
        # Calculate file-by-file highlights
        highlights = []
        for f1_path, code_f1 in files1.items():
            f1_name = os.path.basename(f1_path)
            t1 = self._get_ast_tokens(code_f1)
            if not t1:
                continue
                
            best_sim = 0.0
            best_f2 = ""
            for f2_path, code_f2 in files2.items():
                f2_name = os.path.basename(f2_path)
                t2 = self._get_ast_tokens(code_f2)
                if not t2:
                    continue
                sim = self._calculate_similarity(t1, t2)
                if sim > best_sim:
                    best_sim = sim
                    best_f2 = f2_name
                    
            if best_sim > 70.0:  # Threshold for reporting a file match highlight
                highlights.append(f"  - {f1_name} mirip {best_sim:.2f}% dengan {best_f2}")
                
        recap = "\n".join(highlights)
        
        return overall_sim, recap

    def is_plagiarized(self, similarity: float) -> bool:
        """
        Determines whether the similarity exceeds the threshold (> 80%).
        """
        return similarity > self.similarity_threshold
