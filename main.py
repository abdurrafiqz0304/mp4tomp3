import yt_dlp
import os
import platform
import subprocess
import shutil

def open_folder_window(path):
    """Opens the target folder in the system's file explorer."""
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        else:
            # Fallback for macOS/Linux
            opener = "open" if platform.system() == "Darwin" else "xdg-open"
            subprocess.call([opener, path])
        print(f"📂 Folder '{path}' opened successfully.")
    except Exception as e:
        print(f"❌ Failed to open folder: {e}")

def delete_files_bulk(path):
    """Menu to delete single or multiple files."""
    while True:
        # List all MP3 files
        files = [f for f in os.listdir(path) if f.endswith('.mp3')]
        
        if not files:
            print(f"\n⚠️ No MP3 files found in '{path}'.")
            return

        print(f"\n--- DELETE FILES (Folder: {path}) ---")
        for idx, f in enumerate(files, 1):
            print(f"{idx}. {f}")
        print("0. < BACK")

        print("\n[Tip] Enter a single number (e.g., 1)")
        print("      Or multiple numbers separated by commas (e.g., 1, 3, 5)")
        choice = input("Select file number(s): ").strip()
        
        if choice == '0':
            return
        
        try:
            # Parse input
            indices = [int(x.strip()) for x in choice.split(',') if x.strip().isdigit()]
            
            files_to_delete = []
            
            # Validate indices
            for n in indices:
                idx = n - 1
                if 0 <= idx < len(files):
                    files_to_delete.append(files[idx])
            
            if not files_to_delete:
                print("❌ No valid file numbers selected.")
                continue

            # Confirmation
            print(f"\nYou are about to DELETE {len(files_to_delete)} file(s):")
            for f in files_to_delete:
                print(f"- {f}")
            
            confirm = input("\n⚠️ Are you sure? (y/n): ").lower()
            if confirm == 'y':
                for f in files_to_delete:
                    full_path = os.path.join(path, f)
                    os.remove(full_path)
                    print(f"✅ Deleted: {f}")
            else:
                print("❌ Operation cancelled.")

        except ValueError:
            print("❌ Invalid input format.")

def delete_entire_folder(path):
    """Deletes the entire folder and its contents."""
    # Prevent deletion of the default folder
    if os.path.basename(path) == 'downloads':
        print("\n❌ The default 'downloads' folder cannot be deleted for safety.")
        return False

    print(f"\n⚠️ DANGER ZONE ⚠️")
    print(f"You are about to PERMANENTLY DELETE: {path}")
    print("All files inside will be lost.")
    
    confirm = input("Type 'DELETE' to confirm: ").strip()
    
    if confirm == 'DELETE':
        try:
            shutil.rmtree(path)
            print(f"✅ Folder '{path}' has been deleted successfully.")
            return True # Signal that folder is gone
        except Exception as e:
            print(f"❌ Failed to delete folder: {e}")
            return False
    else:
        print("❌ Cancelled. Input did not match 'DELETE'.")
        return False

def download_audio(sources, quality_choice, download_mode, target_folder):
    # Create folder if it doesn't exist
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"📁 Created new directory: {target_folder}")

    # Configuration
    kbps = '320' if quality_choice == '1' else '128'
    is_noplaylist = True if download_mode == '1' else False

    def progress_hook(d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%')
            s = d.get('_speed_str', 'N/A')
            print(f"\r[DOWNLOADING] {p} | Speed: {s}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\n[DONE] Download complete. Converting to MP3 ({kbps}kbps)...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'concurrent_fragment_downloads': 5,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': kbps,
        }],
        'ffmpeg_location': './ffmpeg.exe', 
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
        'noplaylist': is_noplaylist,
        'outtmpl': f'{target_folder}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in sources:
            url = url.strip()
            if url:
                try:
                    print(f"\n>>> PROCESSING: {url}")
                    ydl.download([url])
                except Exception as e:
                    print(f"\n❌ Error processing {url}: {e}")

def folder_menu():
    while True:
        print("\n--- FOLDER MANAGEMENT ---")
        print("1. Use default 'downloads' folder")
        print("2. Create a NEW folder")
        print("3. Select an EXISTING folder")
        print("0. < BACK TO MAIN MENU")
        
        choice = input("Select option (0-3): ").strip()
        
        if choice == '0': return None
        elif choice == '1': return 'downloads'
        elif choice == '2':
            name = input("Enter new folder name: ").strip()
            return name if name else 'downloads'
        elif choice == '3':
            # List valid directories only
            all_items = os.listdir('.')
            folders = [f for f in all_items if os.path.isdir(f) and not f.startswith('.')]
            if not folders:
                print("⚠️ No existing folders found.")
                continue
            
            print("\nAvailable Folders:")
            for idx, f in enumerate(folders, 1):
                print(f"{idx}. {f}")
            print("0. < BACK")
            
            try:
                inp = input(f"Select number (0-{len(folders)}): ").strip()
                if inp == '0': continue
                
                idx = int(inp) - 1
                if 0 <= idx < len(folders):
                    return folders[idx]
                else:
                    print("❌ Invalid selection.")
            except ValueError: 
                print("❌ Invalid input.")
        else:
            print("❌ Invalid option.")

def file_manager_menu():
    print("\n[SELECT FOLDER TO MANAGE]")
    target_folder = folder_menu()
    if not target_folder: return

    if not os.path.exists(target_folder):
        print("⚠️ Folder does not exist.")
        return

    while True:
        if not os.path.exists(target_folder):
            print("⚠️ Folder no longer exists.")
            break

        print(f"\n--- FILE MANAGER: {target_folder} ---")
        print("1. OPEN Folder (Explorer)")
        print("2. DELETE Files (Single/Bulk)")
        print("3. DELETE THIS FOLDER")
        print("0. < BACK TO MAIN MENU")
        
        choice = input("Select option (0-3): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            open_folder_window(target_folder)
        elif choice == '2':
            delete_files_bulk(target_folder)
        elif choice == '3':
            success = delete_entire_folder(target_folder)
            if success: break 

def main_menu():
    while True:
        print("\n" + "="*50)
        print("   MP3 TURBO DOWNLOADER V1.7 (GITHUB EDITION)   ")
        print("="*50)
        print("1. Download Single Video")
        print("2. Download Playlist / Album")
        print("3. Bulk Download (from .txt)")
        print("4. File & Folder Manager")
        print("5. Exit")
        
        mode = input("\nSelect Menu (1-5): ").strip()

        if mode == '5':
            print("Exiting application. Goodbye!")
            break

        if mode == '4':
            file_manager_menu()
            continue

        if mode not in ['1', '2', '3']:
            print("❌ Invalid selection.")
            continue

        # Step 1: Choose Folder
        folder_target = folder_menu()
        if folder_target is None: continue

        # Step 2: Choose Quality
        print("\n--- AUDIO QUALITY ---")
        print("1. High Quality (320kbps)")
        print("2. Standard/Fast (128kbps)")
        print("0. < BACK")
        q = input("Select option: ").strip()
        if q == '0': continue

        # Step 3: Input Source
        if mode == '3':
            print("\n(Type '0' to cancel)")
            file_name = input("Enter .txt filename: ").strip()
            if file_name == '0': continue
            
            if os.path.exists(file_name):
                with open(file_name, 'r') as f:
                    links = f.readlines()
                download_audio(links, q, '1', folder_target)
                
                open_it = input("\nJob done! Open folder now? (y/n): ").lower()
                if open_it == 'y': open_folder_window(folder_target)
            else:
                print("❌ File not found.")
        else:
            print("\n(Type '0' to cancel)")
            link = input("Paste YouTube Link: ").strip()
            if link == '0': continue
            
            download_audio([link], q, mode, folder_target)
            
            open_it = input("\nJob done! Open folder now? (y/n): ").lower()
            if open_it == 'y': open_folder_window(folder_target)

if __name__ == "__main__":
    main_menu()