import pytest
import os
import tempfile
import shutil
from src.plagiarism import PlagiarismChecker

@pytest.fixture
def workspace():
    temp_dir = tempfile.mkdtemp()
    
    proj1 = os.path.join(temp_dir, "proj1")
    proj2 = os.path.join(temp_dir, "proj2")
    proj3 = os.path.join(temp_dir, "proj3")
    
    os.makedirs(proj1)
    os.makedirs(proj2)
    os.makedirs(proj3)
    
    yield temp_dir, proj1, proj2, proj3
    shutil.rmtree(temp_dir)

def test_identical_projects(workspace):
    _, proj1, proj2, _ = workspace
    
    code = "public class Main { public static void main(String[] args) { System.out.println(\"Hello\"); } }"
    
    with open(os.path.join(proj1, "Main.java"), "w") as f:
        f.write(code)
    with open(os.path.join(proj2, "Main.java"), "w") as f:
        f.write(code)
        
    checker = PlagiarismChecker()
    similarity = checker.check_project_similarity(proj1, proj2)
    
    assert similarity == 100.0
    assert checker.is_plagiarized(similarity) is True

def test_different_projects(workspace):
    _, proj1, proj2, _ = workspace
    
    code1 = "public class Main { public static void main(String[] args) { System.out.println(\"Hello\"); } }"
    code2 = "public class Utils { public int add(int a, int b) { return a + b; } }"
    
    with open(os.path.join(proj1, "Main.java"), "w") as f:
        f.write(code1)
    with open(os.path.join(proj2, "Utils.java"), "w") as f:
        f.write(code2)
        
    checker = PlagiarismChecker()
    similarity = checker.check_project_similarity(proj1, proj2)
    
    assert similarity < 30.0
    assert checker.is_plagiarized(similarity) is False

def test_plagiarism_with_different_spacing_and_variables(workspace):
    _, proj1, proj2, _ = workspace
    
    code1 = "public class Main { public void test() { int x = 10; return x; } }"
    # Changed variable names and spacing, but tokens type structure should be very similar
    code2 = "public \nclass\n Main { public void test( ) \n { int myVar = 10;\n return myVar; } }"
    
    with open(os.path.join(proj1, "Main.java"), "w") as f:
        f.write(code1)
    with open(os.path.join(proj2, "Main.java"), "w") as f:
        f.write(code2)
        
    checker = PlagiarismChecker()
    similarity = checker.check_project_similarity(proj1, proj2)
    
    assert similarity > 80.0
    assert checker.is_plagiarized(similarity) is True

def test_excluded_files(workspace):
    _, proj1, proj2, _ = workspace
    
    code = "public class Template { public void setup() {} }"
    student_code = "public class Student { private String name; public void greet() { System.out.println(\"Hi\"); } }"
    
    with open(os.path.join(proj1, "Template.java"), "w") as f:
        f.write(code)
    with open(os.path.join(proj1, "Student1.java"), "w") as f:
        f.write(student_code)
        
    with open(os.path.join(proj2, "Template.java"), "w") as f:
        f.write(code)
    with open(os.path.join(proj2, "Student2.java"), "w") as f:
        f.write("public class Different { public void logic() { int x = 0; for(int i=0; i<10; i++) x+=i; } }")
        
    # Test without exclusion, template might boost similarity
    checker_no_exclude = PlagiarismChecker()
    sim_no_exclude = checker_no_exclude.check_project_similarity(proj1, proj2)
    
    # Test with exclusion
    checker_exclude = PlagiarismChecker(exclude_files=["Template.java"])
    sim_exclude = checker_exclude.check_project_similarity(proj1, proj2)
    
    assert sim_exclude < sim_no_exclude
    
    # Actually without template, Student1 and Student2 are completely different
    assert sim_exclude < 30.0
