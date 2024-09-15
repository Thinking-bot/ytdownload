import tkinter as tk
from tkinter import ttk, messagebox
from pytubefix import YouTube
import threading

class YouTubeDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("400x200")
        
        # Variables
        self.download_format = tk.StringVar(value="mp3")  # Default format is mp3
        self.url_var = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        
        # Create GUI widgets
        self.create_widgets()
    
    def create_widgets(self):
        # URL Entry
        tk.Label(self, text="YouTube URL:").pack(pady=5)
        tk.Entry(self, textvariable=self.url_var, width=50).pack(pady=5)
        
        # Format Toggle Button
        self.toggle_button = tk.Button(self, text="Format: mp3", command=self.toggle_format)
        self.toggle_button.pack(pady=5)
        
        # Download Button
        tk.Button(self, text="Download", command=self.start_download).pack(pady=5)
        
        # Progress Bar
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=5, fill=tk.X, padx=20)
        
        # Status Label
        self.status_label = tk.Label(self, text="")
        self.status_label.pack(pady=5)
    def toggle_format(self):
        # Toggle between mp3 and mp4
        if self.download_format.get() == "mp3":
            self.download_format.set("mp4")
            self.toggle_button.config(text="Format: mp4")
        else:
            self.download_format.set("mp3")
            self.toggle_button.config(text="Format: mp3")
    def start_download(self):
        url = self.url_var.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        # Start the download in a new thread to prevent GUI freezing
        threading.Thread(target=self.download, args=(url,)).start()
    
    def download(self, url):
        try:
            yt = YouTube(url, on_progress_callback=self.on_progress)
            title = yt.title
            # Reset progress bar and update status
            self.after(0, self.progress_var.set, 0)
            self.after(0, self.update_status_label, f"Downloading: {title}")
            if self.download_format.get() == "mp3":
                ys = yt.streams.get_audio_only()
                ys.download(mp3=True)
            else:
                ys = yt.streams.get_highest_resolution()
                ys.download()
            self.after(0, self.update_status_label, "Download completed!")
        except Exception as e:
            self.after(0, self.update_status_label, f"Error: {str(e)}")

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        # Update progress bar and status label safely from the main thread
        self.after(0, self.progress_var.set, percentage_of_completion)
        self.after(0, self.update_status_label, f"Downloading... {percentage_of_completion:.2f}%")

    def update_status_label(self, text):
        self.status_label.config(text=text)

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop()