import yt_dlp
import os
import platform
import subprocess
import shutil
import sys

# --- FUNGSI BANTUAN (UTILITIES) ---
def open_folder_window(path):
    try:
        if platform.system() == "Windows": os.startfile(path)
        else: subprocess.call(["open" if platform.system() == "Darwin" else "xdg-open", path])
        print(f"📂 Folder '{path}' dibuka.")
    except Exception as e: print(f"❌ Error buka folder: {e}")

def get_ffmpeg_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'ffmpeg.exe')

def update_system():
    print("\n[SYSTEM UPDATE] Mengemaskini yt-dlp...")
    print("Sila tunggu sekejap...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
        print("\n✅ Update BERJAYA! Sila restart program.")
        input("[Tekan ENTER untuk keluar]")
        sys.exit()
    except Exception as e:
        print(f"❌ Update Gagal: {e}")

# --- FUNGSI DOWNLOAD UTAMA ---
def download_audio(sources, quality_choice, download_mode, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    kbps = '320' if quality_choice == '1' else '128'
    is_noplaylist = True if download_mode == '1' else False
    
    ffmpeg_loc = get_ffmpeg_path()
    if not os.path.exists(ffmpeg_loc):
        print(f"\n❌ ERROR: FFmpeg tak jumpa di: {ffmpeg_loc}")
        print("   Sila run 'install.bat' semula.")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': kbps,
        }],
        'ffmpeg_location': ffmpeg_loc,
        'quiet': False,       # Tunjuk bar loading (Live UI)
        'no_warnings': True,
        'noplaylist': is_noplaylist,
        'outtmpl': f'{target_folder}/%(title)s.%(ext)s',
        'noprogress': False,  # Pastikan bar loading keluar
    }

    print("\n" + "="*50)
    print(f"   MEMPROSES DOWNLOAD ({len(sources)} Item)   ")
    print("="*50)
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in sources:
            try:
                print(f"\nTarget: {url}")
                ydl.download([url.strip()])
            except Exception as e:
                print(f"\n❌ GAGAL: {e}")

# --- MENU NAVIGATION (USER INTERFACE) ---

def folder_menu():
    while True:
        print("\n--- PILIH FOLDER ---")
        print("1. Guna folder 'downloads' (Default)")
        print("2. Buat Folder BARU")
        print("3. Pilih Folder SEDIA ADA")
        print("0. < KEMBALI")
        
        c = input("Pilihan: ").strip()
        
        if c == '0': return None # Signal untuk Back
        if c == '1': return 'downloads'
        if c == '2':
            name = input("Nama folder baru: ").strip()
            return name if name else 'downloads'
        if c == '3':
            # List folder semasa
            folders = [f for f in os.listdir('.') if os.path.isdir(f) and not f.startswith('.')]
            if not folders: 
                print("⚠️ Tiada folder lain.")
                continue
            for i, f in enumerate(folders, 1): print(f"{i}. {f}")
            
            try:
                sel = input("Pilih nombor: ")
                return folders[int(sel)-1]
            except: print("❌ Input salah.")

def quality_menu():
    while True:
        print("\n--- PILIH KUALITI AUDIO ---")
        print("1. High Quality (320kbps) - Padu")
        print("2. Standard (128kbps) - Jimat Data")
        print("0. < KEMBALI")
        
        c = input("Pilihan: ").strip()
        if c == '0': return None
        if c in ['1', '2']: return c
        print("❌ Pilihan tak sah.")

def file_manager_menu():
    # Logic file manager (simplified)
    folder = folder_menu()
    if not folder: return # Kalau user tekan back kat folder menu

    if not os.path.exists(folder): 
        print("⚠️ Folder tiada.")
        return
    
    while True:
        print(f"\n--- MANAGER: {folder} ---")
        print("1. Buka Folder (Explorer)")
        print("2. Padam Fail")
        print("3. Padam Folder Ini")
        print("0. < KEMBALI MENU UTAMA")
        c = input("Pilihan: ").strip()
        
        if c == '0': break
        elif c == '1': open_folder_window(folder)
        elif c == '2':
            files = [f for f in os.listdir(folder) if f.endswith('.mp3')]
            if not files: print("Tiada lagu."); continue
            for i, f in enumerate(files, 1): print(f"{i}. {f}")
            sel = input("Nombor fail nak padam (0 cancel): ")
            if sel.isdigit() and 0 < int(sel) <= len(files):
                os.remove(os.path.join(folder, files[int(sel)-1]))
                print("✅ Terpadam.")
        elif c == '3':
            if input("Taip 'PADAM' untuk sahkan: ") == 'PADAM':
                shutil.rmtree(folder)
                print("✅ Folder dipadam.")
                break

def main_menu():
    while True:
        print("\n" + "="*50)
        print("   MP3 TURBO V2.0 (NAVIGATION FIXED)   ")
        print("="*50)
        print("1. Download Single Link")
        print("2. Download Playlist")
        print("3. Bulk Download (.txt)")
        print("4. File Manager")
        print("5. UPDATE SYSTEM (Fix Slow)")
        print("6. Keluar")
        
        mode = input("\nPilih Menu (1-6): ").strip()

        if mode == '6': break
        if mode == '5': update_system(); continue
        if mode == '4': file_manager_menu(); continue
        
        if mode not in ['1', '2', '3']:
            print("❌ Pilihan tak sah.")
            continue

        # --- LANGKAH 1: PILIH FOLDER ---
        folder_target = folder_menu()
        if folder_target is None: continue # User tekan 0, balik ke menu utama

        # --- LANGKAH 2: PILIH KUALITI ---
        quality = quality_menu()
        if quality is None: continue # User tekan 0, balik ke menu utama

        # --- LANGKAH 3: INPUT LINK ---
        links = []
        if mode == '3':
            print("\n(Taip '0' untuk kembali)")
            fname = input("Nama fail .txt: ").strip()
            if fname == '0': continue
            
            if os.path.exists(fname): 
                with open(fname) as f: links = f.readlines()
            else:
                print("❌ Fail tak jumpa!")
                continue
        else:
            print("\n(Taip '0' untuk kembali)")
            l = input("Paste Link YouTube: ").strip()
            if l == '0': continue
            if l: links = [l]
        
        # --- EXECUTE ---
        if links:
            download_audio(links, quality, mode, folder_target)
            
            print("\n----------------------------------")
            ask = input("Buka folder sekarang? (y/n): ").lower()
            if ask == 'y': open_folder_window(folder_target)

if __name__ == "__main__":
    main_menu()
