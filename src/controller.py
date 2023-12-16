import tkinter as tk
from tkinter import filedialog

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def set_download_location(self):
        self.model.download_location = filedialog.askdirectory()
        self.view.download_location_entry.delete(0, tk.END)
        self.view.download_location_entry.insert(0, self.model.download_location)
        print(self.model.download_location)

    def get_download_location(self):
        return self.model.download_location

    def get_recent_playlists(self):
        return self.model.get_recent_playlists()

    def change_audio_video(self):
        # Accessing the attribute from the model and updating its value
        if self.model.video_stream:
            self.model.video_stream = False
            self.view.video_only_switch.deselect()
        else:
            self.model.video_stream = True
            self.view.audio_only_switch.deselect()

    def change_Quality(self):
        # Accessing the attribute from the model and updating its value
        print(f'my view: {self.view}')
        if self.model.quality == "low":
            self.model.quality = "high"
            self.view.low_quallity_switch.deselect()
        elif self.model.quality == "high":
            self.model.quality = "low"
            self.view.high_quallity_switch.deselect()

    def process(self, link):
        ytObjects = self.model.process(link)
        self.view.display_terminal.insert(tk.END, self.model.display_terminal_text)
        self.view.display_terminal.update_idletasks()  
        
        self.view.display_terminal.insert(tk.END, f"\nDownloading: ...") 
        self.view.display_terminal.update_idletasks()  
        self.model.downloadYoutubeOjects(ytObjects)
        self.view.display_terminal.insert(tk.END, f" Saved {self.model.video_title} OK\n")
        self.view.display_terminal.see(tk.END)

    
    
    