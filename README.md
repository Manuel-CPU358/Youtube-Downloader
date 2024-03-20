# Youtube-Downloader
This Python script allows users to download both individual YouTube videos and entire playlists as audio files (MP3 format) or video files (MP4 format). It utilizes the pytube library to fetch YouTube video information and download the content, tkinter for the graphical user interface (GUI), mutagen for audio metadata handling.

[Download EXE](https://drive.google.com/uc?export=download&id=1k-OrpFssYQk6Zccn3z8av_rJNE8_I0QP)

Features:
Download individual YouTube videos by providing the video URL.
Download entire YouTube playlists by providing the playlist URL.
Choose to download either audio-only or full video content.
Automatically fetches video metadata such as title, artist, album, and publication date.
Supports adding ID3 tags to downloaded audio files.
Offers an option to synchronize lyrics with downloaded audio files if available.

Instructions:

Enter the YouTube video or playlist URL in the designated field.
Choose the output directory for downloaded files.
Select whether to download audio-only or full video content.
Click the "Download" button to start the download process.
Track the download progress through the status updates.

Dependencies:

pytube: For fetching YouTube video information and downloading content.
tkinter: For building the graphical user interface.
mutagen: For handling audio metadata.
pydub: For audio conversion.
moviepy: For video processing.
