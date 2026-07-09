import zipfile
import os
import shutil
from rich.console import Console

console = Console()

def extract_archives(source_dir: str, temp_dir: str = "temp"):
    """
    Ekstrak semua file .zip, .gfar, dan .greenfoot di direktori sumber ke direktori temp.
    Mendukung format folder submission Moodle (Nama_ID_assignsubmission_file_/file.zip).
    Melakukan Try-Catch agar program tidak berhenti jika ada file yang bermasalah.
    """
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        
    if not os.path.exists(source_dir):
        console.print(f"[bold red]Error:[/bold red] Direktori sumber '{source_dir}' tidak ditemukan.")
        return
        
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        
        # Process Moodle format (folders) or direct files
        archives_to_process = []
        if os.path.isdir(item_path):
            dest_path = os.path.join(temp_dir, item)
            for sub_item in os.listdir(item_path):
                archives_to_process.append((os.path.join(item_path, sub_item), sub_item, dest_path))
        else:
            dest_path = os.path.join(temp_dir, os.path.splitext(item)[0])
            archives_to_process.append((item_path, item, dest_path))
            
        for filepath, filename, dest_path in archives_to_process:
            if filename.endswith(".greenfoot"):
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)
                try:
                    shutil.copy2(filepath, os.path.join(dest_path, filename))
                    console.print(f"[green]Sukses:[/green] Berhasil menyalin {filename}")
                except Exception as e:
                    console.print(f"[bold red]Error:[/bold red] Gagal menyalin {filename} - {str(e)}")
                continue

            if filename.endswith(".zip") or filename.endswith(".gfar"):
                try:
                    with zipfile.ZipFile(filepath, 'r') as zip_ref:
                        zip_ref.extractall(dest_path)
                    console.print(f"[green]Sukses:[/green] Berhasil mengekstrak {filename}")
                except zipfile.BadZipFile:
                    console.print(f"[bold yellow]Peringatan:[/bold yellow] File {filename} rusak (corrupt) dan diabaikan.")
                except RuntimeError as e:
                    if 'password' in str(e).lower() or 'encrypted' in str(e).lower():
                        console.print(f"[bold yellow]Peringatan:[/bold yellow] File {filename} terproteksi password dan diabaikan.")
                    else:
                        console.print(f"[bold red]Error:[/bold red] Gagal mengekstrak {filename} - {str(e)}")
                except Exception as e:
                    console.print(f"[bold red]Error Tidak Terduga:[/bold red] Gagal mengekstrak {filename} - {str(e)}")
