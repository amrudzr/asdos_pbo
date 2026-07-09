import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from src.compiler import check_compilation

@pytest.fixture
def temp_java_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@patch('subprocess.run')
def test_check_compilation_success(mock_run, temp_java_dir):
    mock_run.return_value = MagicMock(returncode=0)
    java_code = "public class Main { public static void main(String[] args) {} }"
    with open(os.path.join(temp_java_dir, "Main.java"), "w") as f:
        f.write(java_code)
        
    success, msg = check_compilation(temp_java_dir)
    assert success is True
    assert msg == "Kompilasi berhasil."

@patch('subprocess.run')
def test_check_compilation_failure(mock_run, temp_java_dir):
    mock_run.return_value = MagicMock(returncode=1, stderr="syntax error")
    java_code = "public class Main { public static void main(String[] args) { syntax error } }"
    with open(os.path.join(temp_java_dir, "Main.java"), "w") as f:
        f.write(java_code)
        
    success, msg = check_compilation(temp_java_dir)
    assert success is False
    assert "Gagal kompilasi" in msg

def test_check_compilation_no_java_files(temp_java_dir):
    success, msg = check_compilation(temp_java_dir)
    assert success is False
    assert msg == "Tidak ditemukan file .java di direktori."
@patch('subprocess.run')
def test_check_compilation_not_found(mock_run, temp_java_dir):
    mock_run.side_effect = FileNotFoundError()
    java_code = "public class Main { public static void main(String[] args) {} }"
    with open(os.path.join(temp_java_dir, "Main.java"), "w") as f:
        f.write(java_code)
        
    success, msg = check_compilation(temp_java_dir)
    assert success is False
    assert "tidak ditemukan" in msg
