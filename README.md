### The Set Up may take several minutes to complete

## 🚀 Quick Start (No Manual Setup)
## 📦 Installation (Automatic)

This tool comes with an auto-installer that sets up Python dependencies and downloads FFmpeg for you.

1. **Clone the repository**:

```bash
git clone https://github.com/abdurrafiqz0304/mp4tomp3.git && cd mp4tomp3 && install.bat

```
2. **If don't have set up on git (use CMD instead of Powershell):**
```bash
curl -k -L -o projek.zip https://github.com/abdurrafiqz0304/mp4tomp3/archive/refs/heads/main.zip && tar -xf projek.zip && cd mp4tomp3-main && install.bat
```
3. **Use Powershell:**
```bash
Invoke-WebRequest -Uri "https://github.com/abdurrafiqz0304/mp4tomp3/archive/refs/heads/main.zip" -OutFile "projek.zip"; Expand-Archive -Path "projek.zip" -DestinationPath "."; cd mp4tomp3-main; .\install.bat
```
3. **Use Termux:**
```bash
pkg update -y && pkg upgrade -y && pkg install python ffmpeg -y && pip install yt-dlp && termux-setup-storage && echo "import yt_dlp,os;P='/sdcard/Download/MP3_Turbo';os.makedirs(P,exist_ok=True);print('\n--- MP3 TURBO MOBILE ---');u=input('Paste Link: ');o={'format':'bestaudio','outtmpl':f'{P}/%(title)s.%(ext)s','postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'320'}]};yt_dlp.YoutubeDL(o).download([u])" > mp3.py && python mp3.py
```

### How to launch
1. Open CMD
2. type "mp3"

### How To Use requirements.txt?
Customly put link in the txt

### Note
Note: Ensure ffmpeg.exe is present in the folder. Python must be installed on your system!
