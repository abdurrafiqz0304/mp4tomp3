import yt_dlp
import os
import platform
import subprocess
import shutil
import sys

# --- HELPER FUNCTIONS ---
def open_folder_window(path):
    try:
        if platform.system() == "Windows": os.startfile(path)
        else: subprocess.call(["open" if platform.system() == "Darwin" else "xdg-open", path])
        print(f"📂 Folder '{path}' opened.")
    except Exception as e: print(f"❌ Error: {e}")

def get_ffmpeg_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'ffmpeg.exe')

# --- UPDATE FUNCTION (FIXED: SAME FOLDER UPDATE) ---
def update_software():
    print("\n" + "="*40)
    print("      SYSTEM UPDATE INITIATED")
    print("="*40)
    print("[INFO] Updating inside CURRENT folder...")
    print("[INFO] The app will close, update files, and restart.")
    
    # 1. timeout 3: Tunggu Python tutup supaya file tak lock
    # 2. curl: Download zip
    # 3. tar: Extract (dia akan create folder 'mp4tomp3-main')
    # 4. xcopy: Ambil isi dalam 'mp4tomp3-main' tu, pindah ke SINI (Overwrite)
    # 5. rmdir & del: Buang fail zip dan folder temp
    
    update_cmd = (
        'start "MP3 Turbo Updater" cmd /c '
        '"timeout /t 3 >nul '
        '&& echo [INFO] Downloading Update... '
        '&& curl -k -L -o update.zip https://github.com/abdurrafiqz0304/mp4tomp3/archive/refs/heads/main.zip '
        '&& echo [INFO] Extracting... '
        '&& tar -xf update.zip '
        '&& echo [INFO] Overwriting old files... '
        '&& xcopy mp4tomp3-main\\* . /E /Y /Q '
        '&& rmdir /s /q mp4tomp3-main '
        '&& del update.zip '
        '&& echo [SUCCESS] Update Complete! Restarting... '
        '&& install.bat"'
    )
    
    os.system(update_cmd)
    
    print("👋 App closing in 3 seconds to allow file replacement...")
    sys.exit()

def delete_files_bulk(path):
    while True:
        files = [f for f in os.listdir(path) if f.endswith('.mp3')]
        if not files:
            print(f"\n⚠️ No MP3 files in '{path}'.")
            return
        print(f"\n--- DELETE FILES ({path}) ---")
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
    if os.path.basename(path) == 'downloads':
        print("\n❌ Cannot delete default 'downloads' folder.")
        return False
    if input(f"\n⚠️ DELETE FOLDER '{path}'? Type 'DELETE': ") == 'DELETE':
        shutil.rmtree(path)
        print("✅ Folder deleted.")
        return True
    return False

# --- CORE DOWNLOADER ---
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
        'quiet': False,
        'no_warnings': False,
        'noplaylist': True if download_mode == '1' else False,
        'outtmpl': f'{target_folder}/%(title)s.%(ext)s',
        'force_ipv4': True,
        'socket_timeout': 15,
        'nocheckcertificate': True,
    }

    print("\n[INFO] Connecting to YouTube...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in sources:
            try: ydl.download([url.strip()])
            except Exception as e: print(f"\n❌ FAILED: {e}")

# --- MENUS ---
def folder_menu():
    while True:
        print("\n--- FOLDER ---")
        print("1. Default ('downloads')")
        print("2. New Folder")
        print("3. Existing Folder")
        print("0. Back")
        c = input("Option: ").strip()
        if c == '0': return None
        if c == '1': return 'downloads'
        if c == '2': return input("Folder Name: ").strip() or 'downloads'
        if c == '3':
            folders = [f for f in os.listdir('.') if os.path.isdir(f) and not f.startswith('.')]
            for i, f in enumerate(folders, 1): print(f"{i}. {f}")
            try: return folders[int(input("Select: "))-1]
            except: pass

def main_menu():
    while True:
        print("\n" + "="*40)
        print("   MP3 TURBO V2.3 (IN-PLACE UPDATE)   ")
        print("="*40)
        print("1. Single Video")
        print("2. Playlist")
        print("3. Bulk (.txt)")
        print("4. File Manager")
        print("5. UPDATE SOFTWARE")
        print("6. Exit")
        
        mode = input("\nSelect (1-6): ").strip()
        if mode == '6': break
        if mode == '5': update_software()
        if mode == '4': 
            f = folder_menu()
            if f:
                while os.path.exists(f):
                    print(f"\nManage '{f}': 1.Open 2.Del Files 3.Del Folder 0.Back")
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