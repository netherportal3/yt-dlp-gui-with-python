import tkinter as tk
from tkinter import messagebox
from yt_dlp import YoutubeDL
import os

class YoutubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader by netherportal3")

        self.url_label = tk.Label(root, text="YouTube URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        self.format_label = tk.Label(root, text="Select Format:") #build menu
        self.format_label.pack()

        self.format_frame = tk.Frame(root)
        self.format_frame.pack()

        self.format_listbox = tk.Listbox(self.format_frame, selectmode=tk.SINGLE, width=50)
        self.format_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.format_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.format_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.format_listbox.yview)

        self.output_label = tk.Label(root, text="Output Path:")
        self.output_label.pack()

        self.output_entry = tk.Entry(root, width=50)
        self.output_entry.pack()

        #current directory becomes the working dir
        self.output_entry.insert(0, os.getcwd())

        self.has_audio = tk.BooleanVar()
        self.has_audio.set(True)  #default to downloading audio.
        self.audio_checkbox = tk.Checkbutton(root, text="Download with Audio", variable=self.has_audio)
        self.audio_checkbox.pack()

        self.update_button = tk.Button(root, text="Update Formats", command=self.update_formats)
        self.update_button.pack()

        self.download_button = tk.Button(root, text="Download", command=self.start_download)
        self.download_button.pack()

    def fetch_formats(self, url): #get formatting for making the dropdown menu
        ydl_opts = {
            'quiet': True,
            'listformats': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
        formats = []
        for f in info_dict.get('formats', []):
            file_extension = f['ext']
            resolution = f.get('resolution', 'Unknown')
            has_audio = 'vcodec' in f and 'acodec' in f
            format_id = f['format_id']  
            formats.append({'format_id': format_id, 'file_extension': file_extension, 'resolution': resolution, 'has_audio': has_audio})
        return formats

    def download_video(self, url, format_id, output_path):
        ydl_opts = {
            'format': format_id,
            'outtmpl': output_path,
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def download_audio(self, url, output_path): #only audio was requested, so if the format is a video, remove the video and take audio.
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def download_with_audio(self, url, format_id, output_path, video_only):
        if video_only: #format only has video and audio was requested.
            print("File format is video only. Downloading best audio.")
            ydl_opts = {'format': 'bestaudio/best','postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],'postprocessor_args': ['-ar', '16000'],'prefer_ffmpeg': True,'keepvideo': False}
            print("Starting Audio Download")
            print(f"Audio Output Path: {output_path}")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("Audio Download Complete!")
            print("Starting Video Download")
            print(f"Video Output Path: {output_path}")
            ydl_opts1 = {
                'format': format_id,
            }
            with YoutubeDL(ydl_opts1) as ydl:
                ydl.download([url])
            print("Audio Download Complete")
        else: #already has vid and audio, don't need to do special handling.
            print("File format has audio and video. Downloading normally.")
            print("Starting Video+Audio Download")
            print(f"Video+Audio Output Path: {output_path}")
            ydl_opts1 = {
                'format': format_id,
            }
            with YoutubeDL(ydl_opts1) as ydl:
                ydl.download([url])
            print("Video+Audio Download Complete")
            
        



    def start_download(self):
        url = self.url_entry.get().strip()
        output_path = self.output_entry.get().strip()

        # Check if the output_path is a directory, if so, create the filename
        if os.path.isdir(output_path):
            format_index = self.format_listbox.curselection()
            if not format_index:
                messagebox.showerror("Error", "Please select a format")
                return
        selected_format_str = self.format_listbox.get(format_index)
        format_id = selected_format_str.split()[0]  # Assuming format ID is the first part of the string


        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
        if not output_path:
            messagebox.showerror("Error", "Please specify an output path")
            return

        if 'audio only' in selected_format_str and self.has_audio.get():
            messagebox.showerror("Error", "Selected format is audio only, cannot download without audio")
            return

        if self.has_audio.get():
            if 'video only' in selected_format_str:
                self.download_with_audio(url, format_id, output_path, True)
            else:
                self.download_with_audio(url, format_id, output_path, False)
        else:
            self.download_video_with_audio(url, format_id, output_path, False)

        messagebox.showinfo("Download Complete", "Video downloaded successfully!")


    def update_formats(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL") #if there is no url, pop up this message and go back to the main menu
            return
        self.format_listbox.delete(0, tk.END)
        formats = self.fetch_formats(url) #updates formats
    
        # Sort formats by resolution from highest to lowest
        formats.sort(key=lambda x: (x['resolution'] if x['resolution'] != 'audio only' else '0x0'), reverse=True) 
        #short lamda function to sort formats. I honestly don't particularly understand this, but it works, and thats what matters :D
     
        # groups formats by resolution 
        #todo: I need to make the resolution buttons not clickable, but for now, I don't see a way to do that. For example, I could
        grouped_formats = {}
        for f in formats:
            resolution = f['resolution']
            if resolution not in grouped_formats:
                grouped_formats[resolution] = []
            grouped_formats[resolution].append(f)
    
        # Display formats in listbox
        for resolution, formats in grouped_formats.items():
            self.format_listbox.insert(tk.END, f"Resolution: {resolution}")
            for f in formats:
                file_extension = f['file_extension']
                has_audio = f['has_audio']
                audio_icon = " " if has_audio else "🔇" #puts icon if no audio. Isn't 100% reliable because youtube lies sometimes. :D
                self.format_listbox.insert(tk.END, f"  {file_extension}  {audio_icon}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloader(root)
    root.mainloop()


