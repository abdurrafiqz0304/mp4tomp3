import yt_dlp
import os
import platform
import subprocess
import shutil
import sys

# --- HELPER FUNCTIONS ---
def get_base_dir():
    """Dapatkan lokasi folder di mana script ini berada (mp4tomp3-main)."""
    return os.path.dirname(os.path.abspath(__file__))

def open_folder_window(path):
    try:
        if platform.system() == "Windows": os.startfile(path)
        else: subprocess.call(["open" if platform.system() == "Darwin" else "xdg-open", path])
        print(f"📂 Folder opened: '{path}'")
    except Exception as e: print(f"❌ Error: {e}")

def get_ffmpeg_path():
    return os.path.join(get_base_dir(), 'ffmpeg.exe')

# --- UPDATE MENU ---
def update_menu():
    while True:
        print("\n" + "="*40)
        print("      SYSTEM UPDATE CENTER")
        print("="*40)
        print("1. Update PROGRAM (Fix bugs/Features)")
        print("2. Update LIBRARY (yt-dlp fix)")
        print("0. < BACK")
        
        choice = input("\nSelect Option (0-2): ").strip()
        if choice == '0': return

        if choice == '1':
            print("\n[INFO] Updating Program... (App will restart)")
            update_cmd = (
                'start "MP3 Turbo Updater" cmd /c '
                '"timeout /t 3 >nul && echo [INFO] Downloading... '
                '&& curl -k -L -o update.zip https://github.com/abdurrafiqz0304/mp4tomp3/archive/refs/heads/main.zip '
                '&& echo [INFO] Extracting... && tar -xf update.zip '
                '&& echo [INFO] Overwriting... && xcopy mp4tomp3-main\\* . /E /Y /Q '
                '&& rmdir /s /q mp4tomp3-main && del update.zip '
                '&& echo [SUCCESS] Restarting... && install.bat"'
            )
            os.system(update_cmd)
            sys.exit()

        if choice == '2':
            print("\n[INFO] Updating yt-dlp library...")
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
        try:
            files = [f for f in os.listdir(path) if f.endswith('.mp3')]
        except FileNotFoundError:
            print("❌ Folder not found.")
            return

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
            
            print(f"Deleting {len(to_delete)} files...")
            if input("Confirm? (y/n): ").lower() == 'y':
                for f in to_delete:
                    os.remove(os.path.join(path, f))
                    print(f"Deleted: {f}")
        except: print("❌ Invalid input.")

def delete_entire_folder(path):
    folder_name = os.path.basename(path)
    if folder_name == 'downloads':
        print("\n❌ Cannot delete default 'downloads' folder.")
        return False
    
    if input(f"\n⚠️ DELETE FOLDER '{folder_name}'? Type 'DELETE': ") == 'DELETE':
        try:
            shutil.rmtree(path)
            print("✅ Folder deleted.")
            return True
        except Exception as e:
            print(f"❌ Error deleting folder: {e}")
    return False

# --- DOWNLOADER ---
def download_audio(sources, quality_choice, download_mode, target_folder):
    # Pastikan target_folder wujud
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

# --- FOLDER MENU (KAU MINTA TU) ---
def folder_menu():
    # Ini kunci utama: Kita ambil path folder program ni
    base_dir = get_base_dir()
    
    while True:
        print(f"\n--- FOLDER SELECTION ---")
        print(f"[Location: {base_dir}]") # Tunjuk user kita cari kat mana
        print("1. Use default 'downloads' folder")
        print("2. Create a NEW folder")
        print("3. Select EXISTING folder (from this project)")
        print("0. < BACK")
        
        choice = input("Option: ").strip()
        if choice == '0': return None
        
        if choice == '1': 
            return os.path.join(base_dir, 'downloads')
        
        if choice == '2': 
            name = input("Enter new folder name: ").strip()
            return os.path.join(base_dir, name if name else 'downloads')
        
        if choice == '3':
            # List folder hanya dalam base_dir
            all_items = os.listdir(base_dir)
            folders = [f for f in all_items if os.path.isdir(os.path.join(base_dir, f)) and not f.startswith('.')]
            
            if not folders:
                print("⚠️ No folders found in project directory.")
                continue

            for i, f in enumerate(folders, 1): print(f"{i}. {f}")
            
            try: 
                idx = int(input("Select number: ")) - 1
                if 0 <= idx < len(folders):
                    # Return Full Path supaya tak sesat
                    return os.path.join(base_dir, folders[idx])
            except: pass

def main_menu():
    while True:
        print("\n" + "="*40)
        print("   MP3 TURBO V2.5 (FIXED PATH)   ")
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