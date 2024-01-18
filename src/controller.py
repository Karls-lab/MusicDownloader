import tkinter as tk
from tkinter import filedialog

class Controller:
    def __init__(self, logger, model, view):
        self.logger = logger
        self.model = model
        self.view = view

    def browse_download_location(self):
        curLocation = self.view.download_location_entry.get()
        self.model.download_location = filedialog.askdirectory(initialdir=curLocation)
        self.view.download_location_entry.delete(0, tk.END)
        self.view.download_location_entry.insert(0, self.model.download_location)

    def set_download_location(self):
        self.model.download_location = self.view.download_location_entry.get()
        self.view.download_location_entry.delete(0, tk.END)
        self.view.download_location_entry.insert(0, self.model.download_location)

    def get_download_location(self):
        return self.view.download_location_entry.get()

    def get_default_location(self):
        return self.model.download_location.get()

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
            self.view.low_quality_switch.deselect()
        elif self.model.quality == "high":
            self.model.quality = "low"
            self.view.high_quality_switch.deselect()

    """ Prints the download progress to the application terminal"""
    def process(self, link):
        ytObjects = self.model.process(link)
        # self.view.display_terminal.insert(tk.END, self.model.display_terminal_text)
        # self.view.display_terminal.update_idletasks()  
        
        self.view.display_terminal.insert(tk.END, f"Downloading: {self.model.video_title}\n") 
        self.view.display_terminal.insert(tk.END, "Please Wait...\n")
        self.view.display_terminal.update_idletasks()  
        self.model.downloadYoutubeObjects(ytObjects)
        # Return an error if something went wrong. 
        self.view.display_terminal.insert(tk.END, f" Saved OK")
        self.view.display_terminal.see(tk.END)

    
    
    