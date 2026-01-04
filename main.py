import yt_dlp
import os
import platform
import subprocess
import shutil

# --- FUNGSI BANTUAN ---
def open_folder_window(path):
    try:
        if platform.system() == "Windows": os.startfile(path)
        else: subprocess.call(["open" if platform.system() == "Darwin" else "xdg-open", path])
        print(f"📂 Folder '{path}' opened.")
    except Exception as e: print(f"❌ Error opening folder: {e}")

def get_ffmpeg_path():
    # Teknik 'GPS' cari lokasi script sebenar
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_path = os.path.join(script_dir, 'ffmpeg.exe')
    return ffmpeg_path

# --- CORE DOWNLOADER ---
def download_audio(sources, quality_choice, download_mode, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    kbps = '320' if quality_choice == '1' else '128'
    is_noplaylist = True if download_mode == '1' else False
    
    # 1. Cari FFmpeg guna 'GPS'
    ffmpeg_loc = get_ffmpeg_path()
    if not os.path.exists(ffmpeg_loc):
        print(f"\n❌ CRITICAL ERROR: FFmpeg not found!")
        print(f"   Looking at: {ffmpeg_loc}")
        print("   Please run 'install.bat' again to fix this.")
        return

    # 2. Progress Bar
    def progress_hook(d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%')
            print(f"\r[DOWNLOADING] {p}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\n[DONE] Processing Audio...")

    # 3. Setting yt-dlp (Debug Mode: ON)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': kbps,
        }],
        'ffmpeg_location': ffmpeg_loc, # Path yang betul
        'progress_hooks': [progress_hook],
        'quiet': False,     # Kita ON kan supaya nampak error kalau ada
        'no_warnings': False, # Kita nak tengok warning
        'noplaylist': is_noplaylist,
        'outtmpl': f'{target_folder}/%(title)s.%(ext)s',
    }

    print("\n[INFO] Connecting to YouTube... (Please wait)")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in sources:
            try:
                ydl.download([url.strip()])
            except Exception as e:
                print(f"\n❌ FAILED: {e}")

# --- MENU FUNCTIONS (Sama macam dulu) ---
def folder_menu():
    # (Simple version untuk jimat space, logic sama)
    print("\n--- SELECT FOLDER ---")
    print("1. 'downloads' (Default)")
    print("2. Create New Folder")
    choice = input("Option: ").strip()
    if choice == '2':
        name = input("Folder name: ").strip()
        return name if name else 'downloads'
    return 'downloads'

def main_menu():
    while True:
        print("\n" + "="*40)
        print("   MP3 TURBO V1.8 (STABLE EDITION)   ")
        print("="*40)
        print("1. Download Single Link")
        print("2. Download Playlist")
        print("3. Exit")
        
        mode = input("\nSelect (1-3): ").strip()
        if mode == '3': break
        
        if mode in ['1', '2']:
            folder = folder_menu()
            print("\nQuality: 1=320kbps, 2=128kbps")
            q = input("Select: ").strip()
            
            link = input("\nPaste Link: ").strip()
            if link:
                download_audio([link], q, mode, folder)
                input("\n[ENTER] to continue...")

if __name__ == "__main__":
    main_menu()
