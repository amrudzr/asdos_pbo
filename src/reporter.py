import csv
import os
import shutil
from typing import List, Dict, Any
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()

def generate_report_table(data: List[Dict[str, Any]]) -> None:
    """
    Generate and print an interactive console table using rich.
    """
    table = Table(title="Laporan Hasil Penilaian Tugas PBO", show_header=True, header_style="bold magenta")
    table.add_column("No.", justify="right", style="dim", width=4)
    table.add_column("NIM", style="dim", width=15)
    table.add_column("Format File", style="cyan")
    table.add_column("Nilai Dasar", justify="right")
    table.add_column("Penalti (Poin)", justify="right", style="red")
    table.add_column("Nilai Akhir", justify="right", style="green")
    table.add_column("Keterangan", justify="left")
    table.add_column("Waktu Pengumpulan", justify="center")

    sorted_data = sorted(
        data,
        key=lambda x: x.get("submitted_at").timestamp() if x.get("submitted_at") else float('inf')
    )

    for idx, row in enumerate(sorted_data, start=1):
        submit_time = row.get("submitted_at")
        time_str = submit_time.strftime("%d %B %Y %H:%M") if submit_time else "-"
        table.add_row(
            str(idx),
            str(row.get("nim", "")),
            str(row.get("file_format", "Manual")),
            str(row.get("base_score", 0)),
            f"-{row.get('penalty', 0)}",
            str(row.get("final_score", 0)),
            str(row.get("notes", "")),
            time_str
        )
    
    console.print(table)
    console.print("=====")
    
    total = len(data)
    plagiat = sum(1 for d in data if d.get("is_plagiarized"))
    orisinal = total - plagiat
    
    console.print(f"\n[bold cyan]Total Data yang Dicek:[/bold cyan] {total}")
    console.print(f"[bold green]Total Data Orisinal:[/bold green] {orisinal}")
    console.print(f"[bold red]Total Data Plagiasi:[/bold red] {plagiat}\n")


def export_to_csv(data: List[Dict[str, Any]], filename: str = "report_nilai.csv") -> bool:
    """
    Export the evaluation data to a CSV file.
    """
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["NIM", "Format File", "Nilai Dasar", "Penalti", "Nilai Akhir", "Keterangan"])
            
            # Write rows
            for row in data:
                writer.writerow([
                    row.get("nim", ""),
                    row.get("file_format", "Manual"),
                    row.get("base_score", 0),
                    row.get("penalty", 0),
                    row.get("final_score", 0),
                    row.get("notes", "")
                ])
        console.print(f"[bold green]Berhasil mengekspor data ke {filename}[/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Gagal mengekspor data ke CSV: {e}[/bold red]")
        return False

def export_to_excel(data: List[Dict[str, Any]], filename: str = "report_nilai.xlsx") -> bool:
    """
    Export the evaluation data to an Excel file using openpyxl.
    """
    try:
        from openpyxl import Workbook
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Rekapitulasi Nilai"
        
        # Write header
        headers = ["NIM", "Format File", "Nilai Dasar", "Penalti", "Nilai Akhir", "Keterangan"]
        ws.append(headers)
        
        # Write rows
        for row in data:
            ws.append([
                row.get("nim", ""),
                row.get("file_format", "Manual"),
                row.get("base_score", 0),
                row.get("penalty", 0),
                row.get("final_score", 0),
                row.get("notes", "")
            ])
            
        wb.save(filename)
        console.print(f"[bold green]Berhasil mengekspor data ke {filename}[/bold green]")
        return True
    except ImportError:
        console.print("[bold yellow]Library 'openpyxl' tidak ditemukan. Gagal mengekspor ke Excel. Pastikan sudah diinstal.[/bold yellow]")
        return False
    except Exception as e:
        console.print(f"[bold red]Gagal mengekspor data ke Excel: {e}[/bold red]")
        return False

def cleanup_temp_dir(temp_path: str = "temp") -> None:
    """
    Delete the temporary directory and all its contents.
    """
    try:
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
            console.print(f"[bold green]Direktori sementara '{temp_path}' berhasil dibersihkan.[/bold green]")
        else:
            console.print(f"[bold yellow]Direktori '{temp_path}' tidak ditemukan, tidak ada yang perlu dibersihkan.[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Gagal membersihkan direktori '{temp_path}': {e}[/bold red]")

def generate_plagiarism_report(data: List[Dict[str, Any]]) -> None:
    """
    Generate and print a table detailing who plagiarized whom based on submission timestamps.
    """
    plagiarized_pairs = set()
    table_rows = []
    recap_data = {}

    for s1 in data:
        if s1.get("is_plagiarized") and s1.get("plagiarized_with"):
            # Find the other student
            s2 = next((s for s in data if s.get("folder_name") == s1.get("plagiarized_with")), None)
            if not s2:
                continue
                
            pair_key = tuple(sorted([str(s1.get("nim", "")), str(s2.get("nim", ""))]))
            if pair_key in plagiarized_pairs:
                continue
                
            plagiarized_pairs.add(pair_key)
            
            # Compare timestamps
            t1 = s1.get("submitted_at")
            t2 = s2.get("submitted_at")
            
            if t1 and t2:
                if t1 <= t2:
                    asli = s1
                    plagiat = s2
                else:
                    asli = s2
                    plagiat = s1
                    
                table_rows.append({
                    "asli_nim": asli.get("nim", ""),
                    "asli_time": asli.get("submitted_at").strftime("%d %B %Y %H:%M"),
                    "plagiat_nim": plagiat.get("nim", ""),
                    "plagiat_folder": plagiat.get("folder_name", ""),
                    "plagiat_time": plagiat.get("submitted_at").strftime("%d %B %Y %H:%M")
                })
                
                asli_nim = asli.get("nim", "")
                plagiat_info = f"{plagiat.get('nim', '')} ({plagiat.get('folder_name', '')})"
                if asli_nim not in recap_data:
                    recap_data[asli_nim] = []
                recap_data[asli_nim].append(plagiat_info)
                
    if table_rows:
        table = Table(title="Laporan Detail Plagiarisme", show_header=True, header_style="bold red")
        table.add_column("No.", justify="right", style="dim", width=4)
        table.add_column("Mahasiswa (Plagiat)", style="yellow")
        table.add_column("Waktu Pengumpulan (Plagiat)", justify="center")
        table.add_column("Sumber Asli", style="green")
        table.add_column("Waktu Pengumpulan (Asli)", justify="center")
        
        for idx, row in enumerate(table_rows, start=1):
            table.add_row(
                str(idx),
                str(row["plagiat_nim"]),
                str(row["plagiat_time"]),
                str(row["asli_nim"]),
                str(row["asli_time"])
            )
            
        console.print(table)
        console.print("=====")
        
        if recap_data:
            recap_table = Table(title="Rekap Data Asli & Plagiasi", show_header=True, header_style="bold blue")
            recap_table.add_column("No.", justify="right", style="dim", width=4)
            recap_table.add_column("Sumber Asli (NIM)", style="green")
            recap_table.add_column("Jumlah Plagiasi", justify="center")
            recap_table.add_column("Daftar File Plagiat", style="yellow")
            
            for idx, (asli_nim, plagiat_list) in enumerate(recap_data.items(), start=1):
                recap_table.add_row(
                    str(idx),
                    str(asli_nim),
                    str(len(plagiat_list)),
                    ", ".join(plagiat_list)
                )
                
            console.print(recap_table)
            console.print("=====")

