import re
from datetime import datetime
from rich.console import Console

console = Console()

def extract_nim(text: str) -> str:
    """
    Mengekstrak NIM mahasiswa dari teks.
    NIM bisa berupa:
    1. Deretan angka 8-15 digit.
    2. Format kustom dengan titik, misal XX.XXXX.X.XXXXX (opsional)
    """
    # 1. Coba format XX.XXXX.X.XXXXX
    match_custom = re.search(r'\d{2}\.\d{4}\.\d\.\d{5}', text)
    if match_custom:
        return match_custom.group(0)
        
    # 2. Coba format deretan angka 8-15 digit
    match = re.search(r'(?<!\d)\d{8,15}(?!\d)', text)
    if match:
        return match.group(0)
        
    return None

def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parsing string timestamp sesuai format spesifik:
    [Hari], [DD] [Bulan] [YYYY], [H]:[MM] [AM/PM]
    Contoh: Monday, 20 April 2026, 7:43 PM
    """
    try:
        timestamp_str = timestamp_str.strip()
        dt = datetime.strptime(timestamp_str, "%A, %d %B %Y, %I:%M %p")
        return dt
    except ValueError as e:
        console.print(f"[bold red]Error Parsing Waktu:[/bold red] Format '{timestamp_str}' tidak sesuai. Gunakan format seperti 'Monday, 20 April 2026, 7:43 PM'.")
        return None
