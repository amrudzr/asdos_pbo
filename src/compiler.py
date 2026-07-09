import os
import subprocess
from typing import List, Tuple

def check_compilation(source_dir: str, classpaths: List[str] = None) -> Tuple[bool, str]:
    """
    Checks the compilation of Java source files in the specified directory.
    
    Args:
        source_dir: Path to the directory containing .java files.
        classpaths: List of paths to external .jar files.
        
    Returns:
        Tuple containing a boolean (True if successful, False otherwise) and a message.
    """
    java_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.java'):
                java_files.append(os.path.join(root, file))
                
    if not java_files:
        return False, "Tidak ditemukan file .java di direktori."
        
    # Auto-detect greenfoot standard libraries for compilation
    if classpaths is None:
        classpaths = []
        
    default_greenfoot_jars = [
        r"C:\Program Files\Greenfoot\lib\greenfoot.jar",
        r"C:\Program Files\Greenfoot\lib\bluejcore.jar",
        r"C:\Program Files (x86)\Greenfoot\lib\greenfoot.jar",
        r"C:\Program Files (x86)\Greenfoot\lib\bluejcore.jar"
    ]
    
    for jar in default_greenfoot_jars:
        if os.path.exists(jar) and jar not in classpaths:
            classpaths.append(jar)
        
    cp_separator = ';' if os.name == 'nt' else ':'
    cp_arg = cp_separator.join(classpaths)
    
    cmd = ['javac']
    if cp_arg:
        cmd.extend(['-cp', cp_arg])
    cmd.extend(java_files)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return True, "Kompilasi berhasil."
        else:
            return False, f"Gagal kompilasi:\n{result.stderr}"
    except FileNotFoundError:
        return False, "Kompilator Java (javac) tidak ditemukan pada sistem."
    except Exception as e:
        return False, f"Terjadi kesalahan saat kompilasi: {str(e)}"
