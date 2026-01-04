import yt_dlp
import os
import platform
import subprocess
import shutil
import sys

# --- FUNGSI BANTUAN ---
def open_folder_window(path):
    try:
        if platform.system() == "Windows": os.startfile(path)
        else: subprocess.call(["open" if platform.system() == "Darwin" else "xdg-open", path])
        print(f"📂 Folder '{path}' dibuka.")
    except Exception as e: print(f"❌ Error buka folder: {e}")

def get_ffmpeg_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'ffmpeg.exe')

# --- FUNGSI UPDATE ---
def update_engine():
    """Update library yt-dlp (Untuk fix speed/error)"""
    print("\n[SYSTEM] Mengemaskini enjin yt-dlp...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
        print("✅ Enjin berjaya dikemaskini!")
        input("[Tekan ENTER]")
    except Exception as e:
        print(f"❌ Gagal: {e}")
        input("[Tekan ENTER]")

def update_app_code():
    """Update kod main.py dari GitHub (git pull)"""
    print("\n[APP UPDATE] Memeriksa versi terbaru dari GitHub...")
    
    # 1. Check kalau folder ni valid Git Repo
    if not os.path.exists(".git"):
        print("❌ ERROR: Folder ini bukan 'Git Repository'.")
        print("   Anda mungkin download guna ZIP.")
        print("   Sila delete folder ini dan install semula guna command 'git clone'.")
        input("[Tekan ENTER]")
        return

    # 2. Cuba tarik update
    try:
        # Jalankan git pull
        process = subprocess.run(["git", "pull"], capture_output=True, text=True)
        
        if "Already up to date" in process.stdout:
            print("✅ Aplikasi anda sudah TERKINI (V2.1).")
        else:
            print(process.stdout)
            print("✅ UPDATE BERJAYA! Kod baru telah dimuat turun.")
            print("⚠️ Sila TUTUP window ini dan BUKA SEMULA 'mp3' untuk apply changes.")
            sys.exit() # Matikan program supaya user restart
            
    except Exception as e:
        print(f"❌ Gagal update: {e}")
        print("Pastikan anda ada internet dan Git installed.")
    
    input("[Tekan ENTER]")

# --- DOWNLOADER ---
def download_audio(sources, quality_choice, download_mode, target_folder):
    if not os.path.exists(target_folder): os.makedirs(target_folder)
    
    ffmpeg_loc = get_ffmpeg_path()
    if not os.path.exists(ffmpeg_loc):
        print(f"\n❌ ERROR: FFmpeg tak jumpa. Run install.bat balik.")
        return

    kbps = '320' if quality_choice == '1' else '128'
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': kbps}],
        'ffmpeg_location': ffmpeg_loc,
        'quiet': False,
        'no_warnings': True,
        'noplaylist': True if download_mode == '1' else False,
        'outtmpl': f'{target_folder}/%(title)s.%(ext)s',
        'noprogress': False,
    }

    print("\n" + "="*40)
    print(f"   MEMPROSES... ({len(sources)} Fail)   ")
    print("="*40)
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in sources:
            try:
                print(f"\nTarget: {url}")
                ydl.download([url.strip()])
            except Exception as e: print(f"\n❌ GAGAL: {e}")

# --- MENUS ---
def folder_menu():
    while True:
        print("\n--- PILIH FOLDER ---")
        print("1. 'downloads' (Default)")
        print("2. Folder Baru")
        print("3. Folder Sedia Ada")
        print("0. < KEMBALI")
        c = input("Pilihan: ").strip()
        if c == '0': return None
        if c == '1': return 'downloads'
        if c == '2': return input("Nama folder: ").strip() or 'downloads'
        if c == '3':
            fs = [f for f in os.listdir('.') if os.path.isdir(f) and not f.startswith('.')]
            for i,f in enumerate(fs,1): print(f"{i}. {f}")
            try: return fs[int(input("Pilih: "))-1]
            except: pass

def main_menu():
    while True:
        print("\n" + "="*50)
        print("   MP3 TURBO V2.1 (SELF-UPDATER)   ")
        print("="*50)
        print("1. Download Single Link")
        print("2. Download Playlist")
        print("3. Bulk (.txt)")
        print("4. File Manager")
        print("5. UPDATE ENGINE (Fix Slow Speed)")
        print("6. UPDATE APP CODE (Dapatkan Feature Baru)")
        print("7. Keluar")
        
        mode = input("\nPilih (1-7): ").strip()

        if mode == '7': break
        if mode == '5': update_engine(); continue
        if mode == '6': update_app_code(); continue # MENU BARU
        if mode == '4': 
            # (Ringkasan File Manager untuk jimat space)
            f = folder_menu()
            if f: open_folder_window(f)
            continue
        
        if mode in ['1','2','3']:
            folder = folder_menu()
            if not folder: continue
            
            print("\nKualiti:\n1. 320kbps (HQ)\n2. 128kbps (Std)\n0. Back")
            q = input("Pilih: ").strip()
            if q == '0': continue
            
            links = []
            if mode == '3':
                fn = input("Nama file .txt: ")
                if os.path.exists(fn): 
                    with open(fn) as f: links = f.readlines()
            else:
                l = input("Link YouTube: ")
                if l != '0': links = [l]
            
            if links:
                download_audio(links, q, mode, folder)
                if input("\nBuka folder? (y/n): ").lower() == 'y': open_folder_window(folder)

if __name__ == "__main__":
    main_menu()
