import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import numpy as np

class View:
    def __init__(self, logger, controller):
        self.logger = logger
        self.root = tk.Tk()
        self.controller = controller
        self.root.title("Youtube Music Downloader")
        self.root.geometry('700x400')


    """ Sets up the GUI, is called from main"""
    def setupView(self):
        self.save_location_setup()
        self.setup_check_buttons()
        self.setup_text_input_fields()
        self.setup_download_button()
        self.setup_drop_down_menu()
        self.setup_display_terminal()
        self.root.mainloop()


    """ Sets up Save location entry """
    def save_location_setup(self):
        # Label
        save_location_label = tk.Label(self.root, text="Save Location:")
        save_location_label.grid(row=0, column=0, padx=10, sticky=tk.W)
        # Button 
        download_location_button = tk.Button(self.root, text="Browse", 
                                            command=self.controller.browse_download_location)
        download_location_button.grid(row=0, column=0, padx=0, pady=0, sticky=tk.E)
        # Text Entry
        self.download_location_entry = tk.Entry(self.root, width=50)
        self.download_location_entry.insert(0, os.path.join(os.path.expanduser('~'),'Music'))
        self.download_location_entry.grid(row=0, column=1, columnspan=4, padx=0, sticky=tk.W)


    """ Quality/Audio Only Check Buttons """
    def setup_check_buttons(self):
        frame = tk.Frame(self.root, borderwidth=2, relief="ridge")
        frame.grid(row=1, column=0, columnspan=3, sticky='ew', padx=10)
        # high quality toggle switch
        self.high_quality_switch = tk.Checkbutton(
            frame, text="High Quality", onvalue="high", offvalue="low", 
            command=self.controller.change_Quality)
        self.high_quality_switch.grid(row=1, column=0, sticky='ew')
        # Low quality toggle switch
        self.low_quality_switch = tk.Checkbutton(
            frame, text="Low Quality", onvalue="low", offvalue="high", 
            command=self.controller.change_Quality)
        self.low_quality_switch.select()
        self.low_quality_switch.grid(row=1, column=1, sticky='ew')
        # Audio only toggle switch
        self.audio_only_switch = tk.Checkbutton(
            frame, text="Audio Only", onvalue="audio", offvalue="video", 
            command=self.controller.change_audio_video)
        self.audio_only_switch.grid(row=1, column=2, sticky='n', padx=1)
        # Video only toggle switch
        self.video_only_switch = tk.Checkbutton(
            frame, text="Video/Audio", onvalue="video", offvalue="audio", 
            command=self.controller.change_audio_video)
        self.video_only_switch.grid(row=1, column=3, sticky='e')
        self.video_only_switch.select()


    def setup_text_input_fields(self):
        url_label = tk.Label(self.root, text="Youtube URL:")
        url_label.grid(row=3, column=0, padx=10, sticky=tk.W)
              # Youtube link entry
        self.youtube_link_entry = tk.Entry(self.root, width=50)
        self.youtube_link_entry.grid(row=3, column=1, columnspan=2, sticky=tk.W)


    """ Recent Playlists/Videos Drop Down Menu"""
    def setup_drop_down_menu(self):
        # Recent URLs label
        drop_menu_label = tk.Label(self.root, text="Recent URLs")
        drop_menu_label.grid(row=2, column=0, padx=10, sticky=tk.W)
        # Drop down menu for recent URLs
        recent = self.controller.get_recent_playlists()
        default = "Recent Downloads"
        self.variable = tk.StringVar(self.root)
        self.variable.set(default)
        w = tk.OptionMenu(self.root, self.variable, *recent, 
                          command=self.change_playlist_input)
        w.config(width=20)
        w.grid(row=2, column=1, columnspan=2, sticky='ew')


    """Grab the recent playlists to populate drop down menu"""
    def change_playlist_input(self, video_name):
        recentPlaylists = self.controller.get_recent_playlists()
        link = recentPlaylists[video_name]
        self.youtube_link_entry.delete(0, tk.END)
        self.youtube_link_entry.insert(0, link)


    """ Download Button """
    def setup_download_button(self):
        btn_label = tk.Label(self.root, text="Download:")
        btn_label.grid(row=4, column=0, padx=10, sticky=tk.W)
        btn = tk.Button(self.root, text='Download', font='bold', fg='red', width=30, 
                        command=lambda: 
                        self.process(self.youtube_link_entry.get()))
        btn.grid(row=4, column=1, columnspan=2, sticky=tk.W)


    """ Display Terminal """
    def setup_display_terminal(self):
        self.display_terminal = ScrolledText(width=80, height=10, wrap='none')
        self.display_terminal.grid(row=5, columnspan=15, padx=10, sticky='ew')


    """ Process the Link given by the user"""
    def process(self, link):
        self.controller.set_download_location()
        self.controller.process(link)
