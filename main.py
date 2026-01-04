import yt_dlp
import os
import platform
import subprocess
import shutil
import sys

# --- CONFIGURATION ---
# Dapatkan lokasi sebenar folder projek ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cipta "Bunker" khas untuk download supaya tak bersepah
SAFE_ZONE = os.path.join(BASE_DIR, 'MP3_Downloads')

# Pastikan bunker ni wujud
if not os.path.exists(SAFE_ZONE):
    os.makedirs(SAFE_ZONE)

# --- HELPER FUNCTIONS ---
def open_folder_window(path):
    try:
        if platform.system() == "Windows": os.startfile(path)
        else: subprocess.call(["open" if platform.system() == "Darwin" else "xdg-open", path])
        print(f"📂 Folder opened: '{path}'")
    except Exception as e: print(f"❌ Error: {e}")

def get_ffmpeg_path():
    return os.path.join(BASE_DIR, 'ffmpeg.exe')

# --- UPDATE MENU (FIXED LOCATION) ---
def update_menu():
    while True:
        print("\n" + "="*40)
        print("      SYSTEM UPDATE CENTER")
        print("="*40)
        print("1. Update PROGRAM (Fix bugs/Path issue)")
        print("2. Update LIBRARY (yt-dlp)")
        print("0. < BACK")
        
        choice = input("\nSelect Option (0-2): ").strip()
        if choice == '0': return

        if choice == '1':
            print("\n[INFO] Updating Program...")
            print(f"[TARGET] {BASE_DIR}") # Tunjuk user kita update kat mana
            
            # --- THE FIX IS HERE ---
            # Kita tambah 'cd /d {BASE_DIR}' supaya dia masuk folder betul dulu
            update_cmd = (
                f'start "MP3 Turbo Updater" cmd /c '
                f'"cd /d "{BASE_DIR}" ' 
                f'&& timeout /t 3 >nul && echo [Downloading]... '
                f'&& curl -k -L -o update.zip https://github.com/abdurrafiqz0304/mp4tomp3/archive/refs/heads/main.zip '
                f'&& echo [Extracting]... && tar -xf update.zip '
                f'&& echo [Updating]... && xcopy mp4tomp3-main\\* . /E /Y /Q '
                f'&& rmdir /s /q mp4tomp3-main && del update.zip '
                f'&& echo [Done] Restarting... && install.bat"'
            )
            os.system(update_cmd)
            sys.exit()

        if choice == '2':
            print("\n[INFO] Updating yt-dlp...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])
                print("\n✅ Library updated!")
                input("\n[ENTER] to continue...")
                return
            except Exception as e:
                print(f"\n❌ Failed: {e}")
                input("[ENTER] to return...")

# --- FILE MANAGER ---
def delete_files_bulk(path):
    while True:
        try: files = [f for f in os.listdir(path) if f.endswith('.mp3')]
        except: return
        
        if not files:
            print(f"\n⚠️ No MP3 files in this folder.")
            return
        
        print(f"\n--- DELETE FILES ({os.path.basename(path)}) ---")
        for idx, f in enumerate(files, 1): print(f"{idx}. {f}")
        print("0. < BACK")
        
        choice = input("\nSelect files (e.g. 1,3): ").strip()
        if choice == '0': return
        try:
            indices = [int(x) for x in choice.split(',') if x.strip().isdigit()]
            to_delete = [files[n-1] for n in indices if 0 <= n-1 < len(files)]
            if not to_delete: continue
            
            if input(f"Delete {len(to_delete)} files? (y/n): ").lower() == 'y':
                for f in to_delete:
                    os.remove(os.path.join(path, f))
                    print(f"Deleted: {f}")
        except: print("❌ Invalid input.")

def delete_entire_folder(path):
    folder_name = os.path.basename(path)
    if folder_name.lower() == 'mp3_downloads':
        print("\n❌ Cannot delete the main Root folder.")
        return False
    
    if input(f"\n⚠️ DELETE FOLDER '{folder_name}'? Type 'DELETE': ") == 'DELETE':
        try:
            shutil.rmtree(path)
            print("✅ Folder deleted.")
            return True
        except Exception as e: print(f"❌ Error: {e}")
    return False

# --- DOWNLOADER ---
def download_audio(sources, quality_choice, download_mode, target_folder):
    if not os.path.exists(target_folder): os.makedirs(target_folder)
    kbps = '320' if quality_choice == '1' else '128'
    
    ffmpeg_loc = get_ffmpeg_path()
    if not os.path.exists(ffmpeg_loc):
        print(f"\n❌ FFmpeg missing at {ffmpeg_loc}. Run install.bat.")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': kbps}],
        'ffmpeg_location': ffmpeg_loc,
        'quiet': False, 'no_warnings': False,
        'noplaylist': True if download_mode == '1' else False,
        'outtmpl': f'{target_folder}/%(title)s.%(ext)s',
        'force_ipv4': True, 'socket_timeout': 15, 'nocheckcertificate': True,
    }

    print("\n[INFO] Connecting to YouTube...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in sources:
            try: ydl.download([url.strip()])
            except Exception as e: print(f"\n❌ FAILED: {e}")

# --- ISOLATED FOLDER MENU ---
def folder_menu():
    while True:
        print(f"\n--- FOLDER SELECTION ---")
        print(f"[Root: .../{os.path.basename(SAFE_ZONE)}/]") 
        print("1. Default Folder (Main)")
        print("2. Create New Sub-Folder")
        print("3. Select Existing Sub-Folder")
        print("0. < BACK")
        
        choice = input("Option: ").strip()
        if choice == '0': return None
        
        if choice == '1': 
            return SAFE_ZONE
        
        if choice == '2': 
            name = input("Enter sub-folder name: ").strip()
            return os.path.join(SAFE_ZONE, name if name else 'General')
        
        if choice == '3':
            all_items = os.listdir(SAFE_ZONE)
            folders = [f for f in all_items if os.path.isdir(os.path.join(SAFE_ZONE, f))]
            
            if not folders:
                print("⚠️ No sub-folders found inside MP3_Downloads.")
                continue

            for i, f in enumerate(folders, 1): print(f"{i}. {f}")
            
            try: 
                idx = int(input("Select number: ")) - 1
                if 0 <= idx < len(folders):
                    return os.path.join(SAFE_ZONE, folders[idx])
            except: pass

def main_menu():
    while True:
        print("\n" + "="*40)
        print("   MP3 TURBO V2.7 (PATH FIXED)   ")
        print("="*40)
        print("1. Single Video")
        print("2. Playlist")
        print("3. Bulk (.txt)")
        print("4. File Manager")
        print("5. UPDATE CENTER")
        print("6. Exit")
        
        mode = input("\nSelect (1-6): ").strip()
        if mode == '6': break
        if mode == '5': update_menu(); continue

        if mode == '4': 
            print(f"\n[Scanning: {SAFE_ZONE}]")
            f = folder_menu()
            if f:
                while os.path.exists(f):
                    folder_name = os.path.basename(f)
                    print(f"\nManage '{folder_name}': 1.Open 2.Del Files 3.Del Folder 0.Back")
                    c = input("Op: ")
                    if c=='0': break
                    if c=='1': open_folder_window(f)
                    if c=='2': delete_files_bulk(f)
                    if c=='3': 
                        if delete_entire_folder(f): break
            continue

        if mode in ['1','2','3']:
            folder = folder_menu()
            if not folder: continue
            q = input("\nQuality (1=320k, 2=128k): ").strip()
            
            while True:
                if mode == '3':
                    tf = input("Txt filename (0 to cancel): ").strip()
                    if tf == '0': break
                    if os.path.exists(tf):
                        with open(tf) as f: download_audio(f.readlines(), q, '1', folder)
                    else: print("File not found.")
                else:
                    lnk = input("Link (0 to stop): ").strip()
                    if lnk == '0': break
                    download_audio([lnk], q, mode, folder)
                
                print("\nDone. Next? (Y=Again, N=Menu, O=Open Folder)")
                act = input(">> ").lower()
                if act == 'o': 
                    open_folder_window(folder)
                    act = input("Continue? (y/n): ").lower()
                if act != 'y': break

if __name__ == "__main__":
    main_menu()