import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from pytube import Playlist, YouTube
import re
import requests
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC, TRCK, SYLT, COMM
from mutagen.mp3 import MP3
from pydub import AudioSegment
from moviepy.editor import *
import syncedlyrics

def download_video(url, output_path, Audio_Only=False):
    yt = YouTube(url)
    title = re.sub(r'[<>:"/\\|?*]', '', yt.title)  # Remove invalid characters
    if Audio_Only:
        stream = yt.streams.filter(only_audio=True).last() #first()
        progress_label.config(text=f"Downloading: {title}.mp3", fg="green")
        p = stream.download(output_path=output_path, filename=f"{title}.mp4")
        progress_label.config(text="Download completed.", fg="green")

        t = AudioFileClip(p)
        t.write_audiofile(p.replace("mp4", "wav"))
        aud = AudioSegment.from_wav(p.replace("mp4", "wav")) #from_file(p, format="wav")
        os.remove(p)
        mp=p.replace("mp4", "mp3")
        mp=mp.replace("\\", "/")
        aud.export(mp, format="mp3")
        audio = MP3(mp, ID3=ID3)
        os.remove(p.replace("mp4", "wav"))
        # Add ID3 tag if it doesn't exist
        try:
            audio.add_tags()
        except Exception:
            pass

        # Set the title, artist, and album
        audio["TIT2"] = TIT2(encoding=3, text=yt.title)
        audio["TPE1"] = TPE1(encoding=3, text=yt.author)  
        audio["TDRC"] = TDRC(encoding=3, text=str(yt.publish_date))
        audio["COMM"] = COMM(encoding=3, lang='eng', desc='description', text=str(yt.description if yt.description else None))
        r = requests.get(yt.thumbnail_url)
        with open(f"{output_path}/temp_cover.jpeg", "wb") as fh:
            fh.write(r.content)
            fh.close()
        with open(f"{output_path}/temp_cover.jpeg", "rb") as f:
            audio["APIC"] = APIC(data=f.read(),
                            type=3,
                            desc="cover",
                            mime="image/jpeg")
        os.remove(f"{output_path}/temp_cover.jpeg")
        audio.save()
        if 1+1==2:
            lrc = syncedlyrics.search(yt.title, lang="de")
            sync_lrc = []
            for line in lrc.split("\n"):
                parts = line.replace(".", ":")
                parts = parts.replace("[", "")
                parts = parts.replace("] ", ":")
                parts = parts.split(":")
                if len(parts) >= 3:
                    
                    min = int(parts[0])*60
                    sec = min + int(parts[1])
                    ms = sec*1000
                    ms = ms + int(parts[2])*10
                    sync_lrc += [parts[3], int(ms)],
                else:
                    continue
                    #sync_lrc += line + "\n"
            #print(sync_lrc)
            audio["SYLT"] = SYLT(encoding=3, format=2, type=1, text=sync_lrc if sync_lrc else None) #sync_lrc if transcript else 
            audio.save()
        else:
            pass

    else:
        stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
        progress_label.config(text=f"Downloading: {title}.mp4", fg="green")
        stream.download(output_path=output_path, filename=f"{title}.mp4")
        progress_label.config(text="Download completed.", fg="green")
    

def download_playlist(url, output_path, Audio_Only):
    playlist = Playlist(url)
    #pt= playlist.title
    progress_label.config(text=f"Downloading playlist {playlist.title}", fg="green")
    i=0
    for video in playlist.videos:
        out=len(playlist.videos)
        i+=1
        yt = YouTube(video.watch_url)
        title = re.sub(r'[<>:"/\\|?*]', '', yt.title)
        progress_label.config(text=f"Downloading {yt.title}.mp3", fg="green")
        download_video(video.watch_url, f"{output_path}/{playlist.title}", Audio_Only)
        if Audio_Only == True:
            audio = MP3(f"{output_path}/{playlist.title}/{title}.mp3", ID3=ID3)
            audio["TALB"] = TALB(encoding=3, text=playlist.title) 
            audio["TRCK"] = TRCK(encoding=3, text=str(i/out))
            audio.save()
    progress_label.config(text="Playlist download completed.", fg="green")
    

def browse_button():
    filename = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, filename)

def download():
    url = url_entry.get()
    output_path = path_entry.get()
    Audio_Only = video_audio_var.get()

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if "playlist" in url.lower():
        download_playlist(url, output_path, Audio_Only)
    else:
        download_video(url, output_path, Audio_Only)

# Create GUI
root = tk.Tk()
root.title("YouTube Downloader")

# URL entry
tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=5, pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Output directory selection
tk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=5, pady=5)
path_entry = tk.Entry(root, width=40)
path_entry.grid(row=1, column=1, padx=5, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_button)
browse_button.grid(row=1, column=2, padx=5, pady=5)

# Option to download video and audio
video_audio_var = tk.BooleanVar()
video_audio_var.set(False)
video_audio_checkbox = tk.Checkbutton(root, text="Download Audio Only", variable=video_audio_var)
video_audio_checkbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Download button
download_button = tk.Button(root, text="Download", command=download)
download_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Progress label
progress_label1 = tk.Label(root, text="Status:")
progress_label1.grid(row=4, column=0, columnspan=1, padx=5, pady=0)
progress_label = tk.Label(root, text="")
progress_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
