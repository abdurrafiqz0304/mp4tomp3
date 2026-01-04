import yt_dlp
import os
import platform
import subprocess
import shutil
import sys  # Tambah library ini untuk fungsi exit

# --- HELPER FUNCTIONS ---
def open_folder_window(path):
    """Opens the target folder in the system's file explorer."""
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        else:
            opener = "open" if platform.system() == "Darwin" else "xdg-open"
            subprocess.call([opener, path])
        print(f"📂 Folder '{path}' opened successfully.")
    except Exception as e:
        print(f"❌ Failed to open folder: {e}")

def get_ffmpeg_path():
    """Locates ffmpeg.exe relative to the script location."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_path = os.path.join(script_dir, 'ffmpeg.exe')
    return ffmpeg_path

# --- NEW UPDATE FUNCTION ---
def update_software():
    print("\n" + "="*40)
    print("      SYSTEM UPDATE INITIATED")
    print("="*40)
    print("[INFO] The application will close and start the updater.")
    print("[INFO] A new window will appear. Please wait...")
    
    # Command panjang yang kau minta tadi
    update_cmd = (
        'start "MP3 Turbo Updater" cmd /c '
        '"curl -k -L -o projek.zip https://github.com/abdurrafiqz0304/mp4tomp3/archive/refs/heads/main.zip '
        '&& tar -xf projek.zip '
        '&& cd mp4tomp3-main '
        '&& install.bat"'
    )
    
    # Jalankan command dalam window CMD baru
    os.system(update_cmd)
    
    print("👋 Closing application to allow update...")
    sys.exit() # Tutup program ini serta-merta

def delete_files_bulk(path):
    """Menu to delete single or multiple files."""
    while True:
        files = [f for f in os.listdir(path) if f.endswith('.mp3')]
        if not files:
            print(f"\n⚠️ No MP3 files found in '{path}'.")
            return

        print(f"\n--- DELETE FILES (Folder: {path}) ---")
        for idx, f in enumerate(files, 1):
            print(f"{idx}. {f}")
        print("0. < BACK")

        choice = input("\nSelect file number(s) to delete (e.g. 1,3,5): ").strip()
        if choice == '0': return

        try:
            indices = [int(x.strip()) for x in choice.split(',') if x.strip().isdigit()]
            files_to_delete = []
            for n in indices:
                idx = n - 1
                if 0 <= idx < len(files):
                    files_to_delete.append(files[idx])

            if not files_to_delete:
                print("❌ No valid files selected.")
                continue

            print(f"\nYou are about to DELETE {len(files_to_delete)} file(s).")
            confirm = input("⚠️ Are you sure? (y/n): ").lower()
            if confirm == 'y':
                for f in files_to_delete:
                    os.remove(os.path.join(path, f))
                    print(f"✅ Deleted: {f}")
            else:
                print("❌ Cancelled.")
        except ValueError:
            print("❌ Invalid input.")

def delete_entire_folder(path):
    """Deletes the entire folder."""
    if os.path.basename(path) == 'downloads':
        print("\n❌ The default 'downloads' folder cannot be deleted.")
        return False
    
    print(f"\n⚠️ DANGER: You are about to DELETE '{path}' and all its contents!")
    confirm = input("Type 'DELETE' to confirm: ").strip()
    if confirm == 'DELETE':
        shutil.rmtree(path)
        print(f"✅ Folder '{path}' deleted.")
        return True
    return False

# --- CORE DOWNLOADER ---
def download_audio(sources, quality_choice, download_mode, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    kbps = '320' if quality_choice == '1' else '128'
    is_noplaylist = True if download_mode == '1' else False
    
    ffmpeg_loc = get_ffmpeg_path()
    if not os.path.exists(ffmpeg_loc):
        print(f"\n❌ CRITICAL ERROR: FFmpeg not found at {ffmpeg_loc}")
        print("   Please run 'install.bat' again to fix this.")
        return

    def progress_hook(d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%')
            print(f"\r[DOWNLOADING] {p}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\n[DONE] Processing Audio...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': kbps,
        }],
        'ffmpeg_location': ffmpeg_loc,
        'progress_hooks': [progress_hook],
        'quiet': False,
        'no_warnings': False,
        'noplaylist': is_noplaylist,
        'outtmpl': f'{target_folder}/%(title)s.%(ext)s',
        
        # Stability Settings
        'force_ipv4': True,
        'socket_timeout': 15,
        'nocheckcertificate': True,
    }

    print("\n[INFO] connecting to YouTube...")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in sources:
            try:
                ydl.download([url.strip()])
            except Exception as e:
                print(f"\n❌ FAILED: {e}")

# --- MENUS ---
def folder_menu():
    while True:
        print("\n--- FOLDER SELECTION ---")
        print("1. Use default 'downloads' folder")
        print("2. Create a NEW folder")
        print("3. Select EXISTING folder")
        print("0. < BACK")
        
        choice = input("Option: ").strip()
        if choice == '0': return None
        if choice == '1': return 'downloads'
        if choice == '2':
            name = input("Enter new folder name: ").strip()
            return name if name else 'downloads'
        if choice == '3':
            folders = [f for f in os.listdir('.') if os.path.isdir(f) and not f.startswith('.')]
            if not folders:
                print("⚠️ No folders found.")
                continue
            for idx, f in enumerate(folders, 1): print(f"{idx}. {f}")
            try:
                idx = int(input("Select number: ")) - 1
                if 0 <= idx < len(folders): return folders[idx]
            except: pass
        else: print("❌ Invalid option.")

def file_manager_menu():
    folder = folder_menu()
    if not folder: return
    while os.path.exists(folder):
        print(f"\n--- MANAGING: {folder} ---")
        print("1. Open Folder")
        print("2. Delete Files")
        print("3. Delete Entire Folder")
        print("0. < BACK")
        c = input("Option: ").strip()
        if c == '0': break
        if c == '1': open_folder_window(folder)
        if c == '2': delete_files_bulk(folder)
        if c == '3': 
            if delete_entire_folder(folder): break

def main_menu():
    while True:
        print("\n" + "="*50)
        print("   MP3 TURBO V2.1 (AUTO-UPDATER)   ")
        print("="*50)
        print("1. Download Single Video")
        print("2. Download Playlist / Album")
        print("3. Bulk Download (from .txt)")
        print("4. File Manager")
        print("5. UPDATE SOFTWARE (New!)")
        print("6. Exit")
        
        mode = input("\nSelect Menu (1-6): ").strip()

        if mode == '6':
            print("Goodbye!")
            break

        if mode == '5':
            update_software()
            continue
            
        if mode == '4':
            file_manager_menu()
            continue

        if mode in ['1', '2', '3']:
            folder = folder_menu()
            if not folder: continue

            print("\n--- AUDIO QUALITY ---")
            print("1. High Quality (320kbps)")
            print("2. Standard (128kbps)")
            q = input("Select Option: ").strip()
            if q not in ['1', '2']: continue

            while True:
                if mode == '3':
                    txt_file = input("\nEnter .txt filename (or '0' to cancel): ").strip()
                    if txt_file == '0': break
                    
                    if os.path.exists(txt_file):
                        with open(txt_file, 'r') as f: links = f.readlines()
                        download_audio(links, q, '1', folder)
                    else:
                        print("❌ File not found.")
                else:
                    print(f"\n[Current Settings: Folder='{folder}' | Mode={'Single' if mode=='1' else 'Playlist'}]")
                    link = input("Paste YouTube Link (or '0' to stop): ").strip()
                    
                    if link == '0': break
                    
                    download_audio([link], q, mode, folder)

                print("\n" + "-"*40)
                print("Job Done! What next?")
                print("Y = Download another video (Same Settings)")
                print("N = Back to Main Menu")
                print("O = Open Folder")
                
                next_action = input("Choice (y/n/o): ").strip().lower()

                if next_action == 'o':
                    open_folder_window(folder)
                    next_action = input("Continue downloading? (y/n): ").strip().lower()

                if next_action != 'y':
                    break 

if __name__ == "__main__":
    main_menu()