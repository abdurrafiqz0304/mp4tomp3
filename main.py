import yt_dlp
import os
import platform
import subprocess
import shutil
import sys
import re
import webbrowser
import time

# --- LIBRARY ROBOT ---
try:
    import pyautogui
    import pyperclip
    ROBOT_AVAILABLE = True
except ImportError:
    ROBOT_AVAILABLE = False

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAFE_ZONE = os.path.join(BASE_DIR, 'MP3_Downloads')

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

def clean_filename_for_list(filename):
    name = filename.replace(".mp3", "")
    name = re.sub(r"[\(\[].*?[\)\]]", "", name)
    name = re.sub(r"(?i)\b(ft|feat|lyrics|official|video|audio|mv|hq|hd|4k)\b", "", name)
    name = name.replace("_", " ").replace("-", " ")
    return " ".join(name.split())

# --- KEYBOARD SURFER BOT ---
def run_keyboard_bot():
    if not ROBOT_AVAILABLE:
        print("\n❌ Error: Robot libraries missing. Go to Update Center.")
        input("[ENTER]...")
        return

    print("\n[KEYBOARD SURFER BOT]")
    target_folder = folder_menu()
    if not target_folder: return

    files = [f for f in os.listdir(target_folder) if f.endswith('.mp3')]
    if not files:
        print("⚠️ No files found.")
        return

    # 1. Copy text
    print(f"\n[1/3] Copying {len(files)} songs...")
    playlist_text = ""
    for file in files:
        playlist_text += clean_filename_for_list(file) + "\n"
    pyperclip.copy(playlist_text)

    # 2. Buka Website
    print("[2/3] Opening TuneMyMusic...")
    webbrowser.open("https://www.tunemymusic.com/transfer/file")
    
    print("\n" + "="*50)
    print("   ⚠️  GET READY IN 10 SECONDS  ⚠️")
    print("="*50)
    print("1. Click inside the Text Box ONCE.")
    print("2. LET GO of the mouse.")
    print("3. I will Paste -> Press TAB -> Press ENTER.")
    print("="*50)

    for i in range(10, 0, -1):
        print(f"Starting in: {i}...", end="\r")
        time.sleep(1)
    
    print("\n🚀 ACTION: Pasting & Navigating...")

    # --- ACTION SEQUENCE ---
    # 1. Paste Lagu
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    # 2. Tekan TAB sekali (Lompat ke button 'Convert List')
    pyautogui.press('tab')
    time.sleep(0.5)

    # 3. Tekan ENTER (Klik Next)
    pyautogui.press('enter')
    
    print("⏳ Waiting 5 seconds for next page...")
    time.sleep(5)

    # 4. Cari Spotify (Tekan Tab banyak kali sampai jumpa)
    # Biasanya Spotify button pertama atau kedua
    print("🚀 Selecting Spotify...")
    # Kita tekan Tab sekali, lepas tu Enter. Kalau tak kena, user kena klik manual.
    pyautogui.press('tab') 
    time.sleep(0.5)
    pyautogui.press('enter')

    print("\n✅ DONE! If Spotify wasn't clicked, just click it manually.")
    input("[ENTER] to return...")

# --- UPDATE MENU ---
def update_menu():
    while True:
        print("\n" + "="*40)
        print("      SYSTEM UPDATE CENTER")
        print("="*40)
        print("1. Update PROGRAM")
        print("2. Update LIBRARY (yt-dlp)")
        print("3. Install ROBOT (pyautogui)")
        print("0. < BACK")
        
        choice = input("\nOption: ").strip()
        if choice == '0': return

        if choice == '1':
            print("\n[INFO] Updating Program...")
            update_cmd = (
                f'start "Updater" cmd /c "cd /d "{BASE_DIR}" ' 
                f'&& timeout /t 3 >nul && curl -k -L -o update.zip https://github.com/abdurrafiqz0304/mp4tomp3/archive/refs/heads/main.zip '
                f'&& tar -xf update.zip && xcopy mp4tomp3-main\\* . /E /Y /Q '
                f'&& rmdir /s /q mp4tomp3-main && del update.zip && install.bat"'
            )
            os.system(update_cmd)
            sys.exit()

        if choice == '2':
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])
            input("Done. [ENTER]")
            
        if choice == '3':
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "pyperclip"])
            input("Done. [ENTER]")

# --- FILE MANAGER ---
def delete_files_bulk(path):
    while True:
        try: files = [f for f in os.listdir(path) if f.endswith('.mp3')]
        except: return
        if not files: return
        print(f"\n--- DELETE FILES ({os.path.basename(path)}) ---")
        for idx, f in enumerate(files, 1): print(f"{idx}. {f}")
        print("0. < BACK")
        choice = input("\nSelect (e.g. 1,3): ").strip()
        if choice == '0': return
        try:
            indices = [int(x) for x in choice.split(',') if x.strip().isdigit()]
            to_delete = [files[n-1] for n in indices if 0 <= n-1 < len(files)]
            if not to_delete: continue
            if input("Confirm? (y/n): ").lower() == 'y':
                for f in to_delete: os.remove(os.path.join(path, f))
        except: pass

def delete_entire_folder(path):
    if os.path.basename(path).lower() == 'mp3_downloads': return False
    if input("DELETE FOLDER? (DELETE): ") == 'DELETE':
        shutil.rmtree(path); return True
    return False

# --- DOWNLOADER ---
def download_audio(sources, quality_choice, download_mode, target_folder):
    if not os.path.exists(target_folder): os.makedirs(target_folder)
    kbps = '320' if quality_choice == '1' else '128'
    ffmpeg_loc = get_ffmpeg_path()
    if not os.path.exists(ffmpeg_loc): return

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
            except: pass

# --- MENU ISOLATION ---
def folder_menu():
    while True:
        print(f"\n--- FOLDER SELECTION ---")
        print(f"[Root: .../{os.path.basename(SAFE_ZONE)}/]") 
        print("1. Default Folder")
        print("2. Create New Sub-Folder")
        print("3. Select Existing Sub-Folder")
        print("0. < BACK")
        c = input("Option: ").strip()
        if c=='0': return None
        if c=='1': return SAFE_ZONE
        if c=='2': return os.path.join(SAFE_ZONE, input("Name: ").strip() or 'General')
        if c=='3':
            folders = [f for f in os.listdir(SAFE_ZONE) if os.path.isdir(os.path.join(SAFE_ZONE, f))]
            for i, f in enumerate(folders, 1): print(f"{i}. {f}")
            try: return os.path.join(SAFE_ZONE, folders[int(input("Select: "))-1])
            except: pass

def main_menu():
    while True:
        print("\n" + "="*40)
        print("   MP3 TURBO V3.4 (KEYBOARD SURFER)   ")
        print("="*40)
        print("1. Single Video")
        print("2. Playlist")
        print("3. Bulk (.txt)")
        print("4. File Manager")
        print("5. AUTO-UPLOAD (Keyboard Mode)")
        print("6. Update Center")
        print("7. Exit")
        
        mode = input("\nSelect (1-7): ").strip()
        if mode == '7': break
        if mode == '6': update_menu(); continue
        
        if mode == '5': 
            run_keyboard_bot()
            continue

        if mode == '4': 
            f = folder_menu()
            if f:
                while os.path.exists(f):
                    print(f"\nManage '{os.path.basename(f)}': 1.Open 2.Del Files 3.Del Folder 0.Back")
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
                    tf = input("Txt filename: ").strip()
                    if os.path.exists(tf): 
                        with open(tf) as f: download_audio(f.readlines(), q, '1', folder)
                else:
                    lnk = input("Link (0 to stop): ").strip()
                    if lnk == '0': break
                    download_audio([lnk], q, mode, folder)
                
                print("\nNext? (Y=Again, N=Menu, O=Open)")
                act = input(">> ").lower()
                if act == 'o': 
                    open_folder_window(folder)
                    act = input("Continue? (y/n): ").lower()
                if act != 'y': break

if __name__ == "__main__":
    main_menu()