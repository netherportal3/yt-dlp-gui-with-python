# YT-DLP GUI by netherportal3

This Python-based YouTube downloader utilizes the `youtube-dlp` library to provide a user-friendly interface for downloading YouTube videos and audio. The application is built using Tkinter for the GUI.

## Features:

1. **Graphical User Interface (GUI):**
   - Utilizes Tkinter for creating an intuitive and easy-to-use interface.
   - Provides options for selecting the desired output format and path.

2. **Format Selection:**
   - Fetches available formats for the provided YouTube URL using `youtube-dlp`.
   - Presents a dropdown menu with a list of available formats for the user to choose from.
   - Formats are categorized based on resolution
3. **Audio Download Options:**
   - When selecting a video format without audio, the application automatically extracts and downloads the audio in MP3 format. You can override this by downloading a video with the best audio quality listed for a different format.
   - Includes an option to download only the audio from a video.

4. **Output Path Configuration:**
   - By default, sets the output path to the current working directory. Change this at the bottom of the GUI.
   - 
7. **Audio Indicator Icon:**
   - Includes an audio indicator icon (🔇) next to format options that do not contain audio. Usually correct, but sometimes innacurate due to youtube's handling.


## Usage:

1. **YouTube URL Entry:**
   - Enter the YouTube URL of the video you wish to download in the designated text field.

2. **Format Selection:**
   - Choose the desired format from the dropdown menu based on available resolutions and audio options.

3. **Output Path Specification:**
   - Specify the directory where you want to save the downloaded video/audio.

4. **Audio Download Options:**
   - Check the "Download with Audio" checkbox to download videos with audio. Uncheck it to download video-only formats.

5. **Update Formats:**
   - Click the "Update Formats" button to refresh the list of available formats for the entered YouTube URL.

6. **Start Download:**
   - Click the "Download" button to initiate the download process based on the selected options.

## Requirements:

- Python 3.8 or later.
- `youtube-dlp` library in nightly mode.
- Tkinter library (usually included with Python distributions in the standard library)

## Getting Started:

1. Ensure you have Python installed on your system.
2. Install the required libraries by running:
    `pip3 install -U --pre yt-dlp`
    `sudo apt-get install ffmpeg` or however else you might install it. Use their nightly release if you can, avoids some common issues.
4. Copy the provided code into a Python file (e.g., `youtube_downloader.py`).
5. Run the Python script to launch the YouTube downloader application.

## Disclaimer:

This YouTube downloader is intended for personal and non-commercial use only. Ensure that you have the necessary rights or permissions before downloading any copyrighted content. The developer is not responsible for any misuse of this application.

## Sources:
YoutubeDLP: https://github.com/yt-dlp/yt-dlp
FFmpeg: https://www.ffmpeg.org/
