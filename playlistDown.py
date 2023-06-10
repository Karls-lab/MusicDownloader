from tkinter import filedialog
from pytube import Playlist
from pytube import YouTube
import pytube
import os
import time
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import numpy as np

print(pytube.__file__)

# PYTUBE DOCS: https://pytube.io/en/latest/index.html
# Created by Karl :)
# Version 1.0

def main():
    start_time = time.time()
    program = Program()

class Program:
    # ----- Init for gui -----
    def __init__(self):
        self.root = Tk()
        self.root.title("Youtube Music Downloader")
        self.root.geometry('800x400')

        # Variables
        self.download_location = os.path.join(os.path.expanduser('~'),'Music')
        self.video_stream = True
        self.quality = "high"

        # Menu Buttons
        menu = Menu(self.root)
        menu.add_command(label='Save Destination', command=lambda: self.get_download_location())
        menu.add_radiobutton(label='Adudio Only', command=lambda: self.set_audio)
        menu.add_radiobutton(label='Video Only', command=lambda: self.set_video)
        self.root.config(menu=menu)

        # Quality Toggle Button
        quality_switch = Checkbutton(self.root, text="High Quality", onvalue="high", offvalue="low", command=self.change_Quality())
        quality_switch.grid(row=0, column=0, sticky=W)

        # Label Placement
        lbl_1 = Label(self.root, text="Youtube URL:")
        lbl_1.grid(row=1, column=0, sticky=W)
        dropMenuLabel = Label(self.root, text="Download Recent Playlist")
        dropMenuLabel.grid(row=1, column=1, sticky=W)

        # URL text input
        self.youtubeLink = Entry(self.root, width=50)
        self.youtubeLink.grid(row=1, column=1)

        # Download Button
        btn = Button(self.root, text = 'Download', fg = 'red', command=lambda:self.process(self.youtubeLink.get()))
        btn.grid(row=2, column=0, sticky=N)

        # gets the index of the selected playlist in the drop down menu
        self.df = pd.read_csv('recent_playlists.txt')
        recent = self.df.tail(5) # will get the last 5 searched links
        default = recent.iloc[0]['playlist_name']
        list_of_recent = list(recent.iloc[0:5]['playlist_name'])
        self.variable = StringVar(self.root)
        self.variable.set(default) # default value
        w = OptionMenu(self.root, self.variable, *list_of_recent, command=self.change_playlist_input)
        w.grid(row=0, column=1, sticky=W)    

        # Output text to tell the user what's going on
        self.display_terminal = ScrolledText(width=60, height=10)
        self.display_terminal.grid(row=3, columnspan=8, padx=0, sticky=N)

        self.root.mainloop()   


    # ----- Helper Methods -----
    def disprint(self, text_to_display: str):
        text = f"{text_to_display[:60]}\n"
        self.display_terminal.insert(INSERT, text)
        if len(text_to_display) > 60:
            second_line = f"             {text_to_display[60:106]}\n"
            self.display_terminal.insert(INSERT, second_line)
        self.display_terminal.update_idletasks()

    def get_recent_playlists(self):
        print("TODO")
        # df = pd.read_csv('recent_playlists.txt')
        # recent = df.tail(5) # will get the last 5 searched links
        # default = recent.iloc[0]['playlist_name']
        # list_of_recent = list(recent.iloc[0:5]['playlist_name'])
        # variable = StringVar(self.root)
        # variable.set(default) # default value

    """ 
    Queries the recent playlist df to find link
    updates Entry field with lin
    """
    def change_playlist_input(self, df):
        index = np.where((self.df['playlist_name'] == self.variable.get()))[0][0]
        link = self.df.at[index,'link']
        self.youtubeLink.delete(0, END)
        self.youtubeLink.insert(0, link)

    def get_download_location(self):
        self.download_location = filedialog.askdirectory()
        print(self.download_location)

    def set_video(self):
        self.video_stream = True

    def set_audio(self):
        self.video_stream = False

    def change_Quality(self):
        "high" if self.quality == "low" else "low"


    # ----- Pre-Processing -----
    def process(self, link):
        # Clear the display
        self.display_terminal.delete("1.0", END)

        self.disprint("processing...")
        self.disprint(f"Saving music to: {self.download_location}\n")
        print(f"link: {link}")
        try: 
            # Save the playlist to the Music folder, and create a new folder if it doesn't exist
            if not os.path.exists(self.download_location):
                os.mkdir(self.download_location)
            if "playlist" in link: # if it's a playlist
                print("Attempting playlist Download")
                yt = Playlist(link) 
                print(f"yt.videos: {yt.videos}")
                self.downloadYoutubeOjects(yt.videos) # changed yt to yt.videos
            else: # if it's only one video
                print("Not a playlist")
                yt = YouTube(link)
                print(yt)
                self.downloadYoutubeOjects([yt])
        except Exception as e:
            print(e)
            self.disprint(f"Connection Error {e}")
            return


    # ----- Download Playlist Logic -----
    def downloadYoutubeOjects(self, yt_objects: list):
        try: 
            for video in yt_objects:
                selected_stream = None
                try:
                    self.disprint("DOWNLOADING: " + video.title)
                    if self.video_stream: # if user requesets a video
                        video_streams = video.streams.filter(progressive=True).order_by('resolution').desc()
                        if self.quality == "high":
                            selected_stream = video_streams.first()
                        else:
                            selected_stream = video_streams.last()
                    else:
                        video_streams = video.streams.filter(only_audio=True)
                        if self.quality == "high":
                            selected_stream = video_streams.first()
                        else:
                            selected_stream = video_streams.last()
                    # Now Attempt to download the selected user Stream to the download location
                    selected_stream.download(self.download_location)
                except Exception as e:
                    self.disprint(f"Error Downloading Title, Skipping...")
                    self.disprint(f"{e}\n")
            self.disprint("Done")
        except Exception as e: 
            self.disprint(f"Error Downloading Video")
            self.disprint(f"{e}\n")


"""" Main LOOP """
if __name__ == "__main__":
        main()