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
    except Exception as e: print(f"❌ Error opening folder: {e}")

def get_ffmpeg_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'ffmpeg.exe')

def update_system():
    print("\n[SYSTEM UPDATE] Updating Core Engine (yt-dlp)...")
    print("Please wait...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
        print("\n✅ Update SUCCESS! System is now faster.")
        print("Please restart the app.")
        input("[Press Enter to Exit]")
        sys.exit()
    except Exception as e:
        print(f"❌ Update Failed: {e}")

# --- CORE DOWNLOADER ---
def download_audio(sources, quality_choice, download_mode, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    kbps = '320' if quality_choice == '1' else '128'
    is_noplaylist = True if download_mode == '1' else False
    
    ffmpeg_loc = get_ffmpeg_path()
    if not os.path.exists(ffmpeg_loc):
        print(f"\n❌ CRITICAL ERROR: FFmpeg not found at {ffmpeg_loc}")
        print("   Please run 'install.bat' again.")
        return

    # KITA BUANG 'progress_hook' SUPAYA KELUAR BAR ASAL
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': kbps,
        }],
        'ffmpeg_location': ffmpeg_loc,
        # 'quiet': False bermaksud: Tunjuk semua info (termasuk Bar, ETA, Speed)
        'quiet': False,     
        'no_warnings': True,
        'noplaylist': is_noplaylist,
        'outtmpl': f'{target_folder}/%(title)s.%(ext)s',
        # Ini penting supaya output nampak kemas sikit
        'noprogress': False, 
    }

    print("\n" + "="*50)
    print(f"   STARTING DOWNLOAD ({len(sources)} Items)   ")
    print("="*50)
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in sources:
            try:
                # Kita print tajuk sikit je, selebihnya biar yt-dlp buat bar dia
                print(f"\nTarget: {url}")
                ydl.download([url.strip()])
            except Exception as e:
                print(f"\n❌ FAILED: {e}")

# --- MENUS ---
def folder_menu():
    print("\n--- SELECT FOLDER ---")
    print("1. 'downloads' (Default)")
    print("2. Create New Folder")
    choice = input("Option: ").strip()
    if choice == '2':
        name = input("Folder name: ").strip()
        return name if name else 'downloads'
    return 'downloads'

def file_manager_menu():
    folder = folder_menu()
    if not os.path.exists(folder): return print("Folder not found.")
    
    print(f"\n--- MANAGER: {folder} ---")
    print("1. Open Folder")
    print("2. Delete Files")
    print("3. Delete Folder")
    c = input("Choice: ").strip()
    
    if c == '1': open_folder_window(folder)
    elif c == '2': # Simplified delete logic for brevity
        files = [f for f in os.listdir(folder) if f.endswith('.mp3')]
        for i, f in enumerate(files, 1): print(f"{i}. {f}")
        sel = input("File number to delete: ")
        if sel.isdigit() and 0 < int(sel) <= len(files):
            os.remove(os.path.join(folder, files[int(sel)-1]))
            print("Deleted.")
    elif c == '3':
        if input("Type 'DEL' to confirm: ") == 'DEL':
            shutil.rmtree(folder)
            print("Folder deleted.")

def main_menu():
    while True:
        print("\n" + "="*50)
        print("   MP3 TURBO V1.9 (LIVE UI + AUTO UPDATE)   ")
        print("="*50)
        print("1. Single Link")
        print("2. Playlist")
        print("3. Bulk (.txt)")
        print("4. File Manager")
        print("5. UPDATE SYSTEM (Fix Slow Speed)")
        print("6. Exit")
        
        mode = input("\nSelect (1-6): ").strip()

        if mode == '6': break
        if mode == '5': update_system(); continue
        if mode == '4': file_manager_menu(); continue
        
        if mode in ['1', '2', '3']:
            folder = folder_menu()
            print("\nQuality: 1=320kbps, 2=128kbps")
            q = input("Select: ").strip()
            
            links = []
            if mode == '3':
                fname = input("Txt filename: ").strip()
                if os.path.exists(fname): 
                    with open(fname) as f: links = f.readlines()
            else:
                l = input("Link: ").strip()
                if l: links = [l]
            
            if links:
                download_audio(links, q, mode, folder)
                if input("\nOpen folder? (y/n): ").lower() == 'y': open_folder_window(folder)

if __name__ == "__main__":
    main_menu()
