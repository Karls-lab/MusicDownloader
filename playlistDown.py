import threading
from tkinter import filedialog
from pytube import Playlist
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
# Version 1

def main():
    start_time = time.time()
    program = Program()

# COWBOW LINK: https://www.youtube.com/playlist?list=PLmh0YA3ZeaRgFv4dps_j_6tZXY5Tpamqg

class Program:


    def __init__(self):
        self.root = Tk()
        self.root.title("Youtube Music Downloader")
        self.root.geometry('500x250')

        menu = Menu(self.root)
        item = Menu(menu)
        self.download_location = os.path.join(os.path.expanduser('~'),'Music')
        menu.add_command(label='Save Where', command=lambda: self.get_download_location())
        self.root.config(menu=menu)

        # Label Placement
        lbl_1 = Label(self.root, text="Enter Youtube Playlist Link")
        lbl_1.grid(row=0, column=0, sticky=W)
        lbl_2 = Label(self.root, text="Recently downloaded Playlists")
        lbl_2.grid(row=1, column=0)

        playlistLink = Entry(self.root, width=20)
        playlistLink.grid(row=0, column=1)

        btn = Button(self.root, text = 'Download', fg = 'red', command=lambda:self.process(playlistLink.get()))
        btn.grid(row=0, column=2)

        # Add a drop down menu for recent downloaded playlists
        # add the link to recently downloaded playlists
        df = pd.read_csv('recent_playlists.txt')
        recent = df.tail(5) # will get the last 5 searched links
        default = recent.iloc[0]['playlist_name']
        list_of_recent = list(recent.iloc[0:5]['playlist_name'])
        variable = StringVar(self.root)
        variable.set(default) # default value
        print(list_of_recent)
        w = OptionMenu(self.root, variable, *list_of_recent)
        w.grid(row=1, column=1, sticky=W)    

        # gets the index of the selected playlist in the drop down menu
        index = np.where((df['playlist_name'] == variable.get()))[0][0]
        link = df.at[index,'link']
        print(index)
        print(link)

        btn_2 = Button(self.root, text = 'Download', fg = 'red', command=lambda:self.process(link))
        btn_2.grid(row=1, column=2)

        # Creates a scroll bar and fill it with text
        self.display_terminal = ScrolledText(width=60, height=10)
        self.display_terminal.grid(row=2, columnspan=3, padx=0, sticky=W)


        self.root.mainloop()   


    def disprint(self, text_to_display: str):
        text = f"{text_to_display[:60]}\n"
        self.display_terminal.insert(INSERT, text)
        if len(text_to_display) > 60:
            second_line = f"             {text_to_display[60:106]}\n"
            self.display_terminal.insert(INSERT, second_line)
        self.display_terminal.update_idletasks()

    def get_download_location(self):
        self.download_location = filedialog.askdirectory()
        print(self.download_location)
        

    def process(self, link):
        self.disprint("processing...")

        # Audio or Video?
        ONLYAUDIO = True
        try: 
            # Attempt to get youtube object, and conver title to alpha-numeric
            yt = Playlist(link) 
            cleaned_title="".join(ch for ch in yt.title if ch.isalnum()) 
        except: 
            self.disprint("Connection Error")
            return


        # Save the playlist to the Music folder, and create a new folder if it doesn't exist
        if not os.path.exists(self.download_location):
            os.mkdir(self.download_location)

        self.disprint(f"Saving music to: {self.download_location}\n")
        self.download(yt, self.download_location)



    def download(self, yt, downloadLocation):
        try: 
            for video in yt.videos:
                try:
                    self.disprint("DOWNLOADING: " + video.title)
                    streamQuery = video.streams.filter(only_audio=True)
                    stream = streamQuery.last()
                    stream.download(downloadLocation)
                except Exception as e:
                    self.disprint(f"Error Downloading Title, Skipping...")
                    self.disprint(f"{e}\n")
        except Exception as e: 
            self.disprint(e)
            self.disprint("Error... Exiting")


if __name__ == "__main__":
        main()