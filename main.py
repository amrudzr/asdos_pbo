from rich.console import Console
from rich.prompt import Prompt, Confirm
from src.parser import parse_timestamp
from src.grader import calculate_late_penalty, calculate_base_score, calculate_final_score, check_for_explanations
from src.reporter import generate_report_table, export_to_csv, cleanup_temp_dir, generate_plagiarism_report
console = Console()

def get_valid_timestamp(prompt_msg: str):
    while True:
        ts_input = Prompt.ask(f"[bold blue]{prompt_msg}[/bold blue] (Contoh: Monday, 20 April 2026, 7:43 PM)")
        if ts_input.lower() in ('q', 'quit', 'exit'):
            return None
        dt = parse_timestamp(ts_input)
        if dt:
            return dt

def main():
    console.print("[bold green]Sistem Automasi Penilaian Tugas PBO Siap![/bold green]")
    
    # 3.1 Input Parameter Deadline
    console.print("\n[bold cyan]--- Pengaturan Deadline ---[/bold cyan]")
    deadline = get_valid_timestamp("Masukkan waktu deadline tugas")
    if not deadline:
        return
        
    console.print(f"[bold green]Deadline berhasil diset ke:[/bold green] {deadline}\n")
    
    # Ekstraksi File
    console.print("\n[bold cyan]--- Ekstraksi Tugas ---[/bold cyan]")
    archives_dir = Prompt.ask("Masukkan path folder berisi file .zip/.gfar/.greenfoot (kosongkan jika ingin input manual per NIM)", default="")
    
    import os
    extracted_dirs = []
    if archives_dir and os.path.exists(archives_dir):
        from src.extractor import extract_archives
        extract_archives(archives_dir, "temp")
        if os.path.exists("temp"):
            for item in os.listdir("temp"):
                if os.path.isdir(os.path.join("temp", item)):
                    extracted_dirs.append(item)
                    
    console.print("\n[bold cyan]--- Penilaian Tugas ---[/bold cyan]")
    
    global_checker = None
    if extracted_dirs:
        from src.plagiarism import PlagiarismChecker
        console.print("[bold cyan]Membangun corpus dari semua tugas untuk mendeteksi boilerplate dosen...[/bold cyan]")
        global_checker = PlagiarismChecker()
        global_checker.build_corpus(extracted_dirs, base_dir="temp")
        
    results = []
    
    def process_student(nim: str, source_dir: str = None, file_format: str = "Manual"):
        submitted_at = get_valid_timestamp(f"Masukkan waktu pengumpulan untuk {nim} (atau 'q' untuk lewati/selesai)")
        if not submitted_at:
            return False
            
        penalty_weeks = calculate_late_penalty(deadline, submitted_at)
        
        if penalty_weeks > 4:
            console.print(f"[bold yellow]Peringatan: Keterlambatan terdeteksi sangat lama ({penalty_weeks} minggu)![/bold yellow]")
            confirm = Confirm.ask("Apakah Anda yakin ingin melanjutkan dengan penalti ini?")
            if not confirm:
                console.print("[bold red]Operasi dibatalkan untuk input ini.[/bold red]\n")
                return True
                
        if not source_dir:
            source_dir = Prompt.ask(f"Masukkan path folder tugas {nim}", default=f"submissions/{nim}")
            
        if not os.path.exists(source_dir):
            console.print(f"[bold red]Folder {source_dir} tidak ditemukan! Menganggap gagal compile.[/bold red]")
            is_compiled = False
        else:
            console.print(f"[bold cyan]Melakukan auto-compile pada {source_dir}...[/bold cyan]")
            from src.compiler import check_compilation
            is_compiled, msg = check_compilation(source_dir)
            if is_compiled:
                console.print(f"[bold green]✓ {msg}[/bold green]")
            else:
                console.print(f"[bold red]✗ {msg}[/bold red]")

        asset_notes = ""
        if is_compiled and source_dir:
            from src.asset_validator import validate_assets
            console.print("[bold cyan]Memvalidasi aset gambar dan suara...[/bold cyan]")
            img_c, snd_c, missing = validate_assets(source_dir)
            console.print(f"[bold green]✓ Ditemukan {img_c} gambar dan {snd_c} suara.[/bold green]")
            if missing:
                missing_str = ", ".join(missing)
                console.print(f"[bold yellow]⚠ Peringatan: Aset berikut dipanggil di kode tapi tidak ditemukan: {missing_str}[/bold yellow]")
                asset_notes = f"Aset: {img_c} gbr, {snd_c} sra | Hilang: {missing_str}"
            else:
                asset_notes = f"Aset: {img_c} gbr, {snd_c} sra"

        is_plagiarized = False
        plagiarized_with = None
        if is_compiled:
            if extracted_dirs and source_dir and os.path.normpath(source_dir).startswith("temp"):
                console.print("[bold cyan]Memeriksa indikasi plagiarisme dengan tugas lain...[/bold cyan]")
                max_sim = 0.0
                plagiarized_with_temp = ""
                
                best_recap = ""
                for other_folder in extracted_dirs:
                    other_dir = os.path.join("temp", other_folder)
                    if os.path.abspath(other_dir) != os.path.abspath(source_dir):
                        sim, recap = global_checker.check_project_similarity(source_dir, other_dir)
                        if sim > max_sim:
                            max_sim = sim
                            plagiarized_with_temp = other_folder
                            best_recap = recap
                            
                if global_checker.is_plagiarized(max_sim):
                    is_plagiarized = True
                    plagiarized_with = plagiarized_with_temp
                    console.print(f"[bold red]⚠ Terdeteksi Plagiat! Kemiripan {max_sim:.2f}% dengan {plagiarized_with}[/bold red]")
                    if best_recap:
                        console.print(f"[bold yellow]Highlight Kemiripan per File:[/bold yellow]\n[yellow]{best_recap}[/yellow]")
                else:
                    console.print(f"[bold green]✓ Aman dari plagiat (Kemiripan tertinggi: {max_sim:.2f}%)[/bold green]")
            else:
                is_plagiarized = Confirm.ask("Apakah terdeteksi plagiat (kemiripan > 80%)?")
            
        has_good_explanation = False
        if is_compiled and not is_plagiarized and file_format != ".greenfoot":
            console.print("[bold cyan]Mengecek improvisasi dan penjelasan pada komentar kode...[/bold cyan]")
            has_good_explanation = check_for_explanations(source_dir)
            if has_good_explanation:
                console.print("[bold green]✓ Ditemukan improvisasi/penjelasan (Skor += 15)[/bold green]")
            else:
                console.print("[bold yellow]✗ Tidak ada/kurang improvisasi atau penjelasan.[/bold yellow]")
            
        base_score, notes = calculate_base_score(is_plagiarized, is_compiled, has_good_explanation, file_format)
        
        if asset_notes:
            notes = f"{notes} | {asset_notes}" if notes else asset_notes
            
        final_score = calculate_final_score(base_score, penalty_weeks)
        
        results.append({
            "nim": nim,
            "folder_name": os.path.basename(source_dir) if source_dir else None,
            "base_score": base_score,
            "penalty": penalty_weeks,
            "final_score": final_score,
            "notes": notes,
            "submitted_at": submitted_at,
            "is_plagiarized": is_plagiarized,
            "plagiarized_with": plagiarized_with,
            "file_format": file_format
        })
        console.print(f"[bold green]Data ditambahkan![/bold green]\n")
        return True

    if extracted_dirs:
        from src.parser import extract_nim
        for folder_name in extracted_dirs:
            nim = extract_nim(folder_name) or folder_name
            console.print(f"\n[bold magenta]Menilai tugas:[/bold magenta] {nim}")
            source_dir = os.path.join("temp", folder_name)
            
            file_format = "Manual"
            if archives_dir and os.path.exists(archives_dir):
                moodle_folder = os.path.join(archives_dir, folder_name)
                if os.path.isdir(moodle_folder):
                    for sub_item in os.listdir(moodle_folder):
                        if sub_item.endswith(".zip"): file_format = ".zip"; break
                        elif sub_item.endswith(".gfar"): file_format = ".gfar"; break
                        elif sub_item.endswith(".greenfoot"): file_format = ".greenfoot"; break
                else:
                    for ext in [".zip", ".gfar", ".greenfoot"]:
                        if os.path.exists(os.path.join(archives_dir, folder_name + ext)):
                            file_format = ext
                            break
                        
            if not process_student(nim, source_dir, file_format):
                break
    else:
        while True:
            nim = Prompt.ask("Masukkan NIM mahasiswa (atau 'q' untuk selesai)")
            if nim.lower() in ('q', 'quit', 'exit'):
                break
            if not process_student(nim):
                break

    if results:
        # Phase 4: Pelaporan
        console.print("\n[bold cyan]--- Hasil Rekapitulasi ---[/bold cyan]")
        generate_plagiarism_report(results)
        generate_report_table(results)
        
        export = Confirm.ask("Apakah Anda ingin mengekspor data ke CSV?")
        if export:
            export_to_csv(results)
            
        update_excel = Confirm.ask("Apakah Anda ingin mengupdate file Excel Master?")
        if update_excel:
            from src.reporter import update_master_excel
            col_name = Prompt.ask("Masukkan nama kolom tugas di Excel (misal: 'nama tugas 1')")
            update_master_excel(results, col_name)

            
    # Cleanup dummy temp dir
    cleanup_temp_dir("temp")

if __name__ == "__main__":
    main()
