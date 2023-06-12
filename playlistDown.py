import logging
from pytube import Playlist
from pytube import YouTube
import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import numpy as np

# PYTUBE DOCS: https://pytube.io/en/latest/index.html
# Created by Karl :)
# Version 1.0

class Program:
    # ----- Init for gui -----
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Youtube Music Downloader")
        self.root.geometry('800x400')

        # Variables
        self.download_location = os.path.join(os.path.expanduser('~'),'Music')
        self.video_stream = True
        self.quality = "low"
        self.video_title = ""
        self.video_link = ""

        # Menu Buttons
        menu = tk.Menu(self.root)
        menu.add_command(label='Save Destination', command=lambda: self.set_download_location())
        menu.add_radiobutton(label='Adudio Only', command=lambda: self.set_audio())
        menu.add_radiobutton(label='Video Only', command=lambda: self.set_video())
        self.root.config(menu=menu)

        # Quality Toggle Button
        quality_switch = tk.Checkbutton(self.root, text="High Quality", onvalue="high", offvalue="low", command=lambda: self.change_Quality())
        quality_switch.grid(row=0, column=0, sticky=tk.W)

        # Label Placement
        lbl_1 = tk.Label(self.root, text="Youtube URL:")
        lbl_1.grid(row=1, column=0, sticky=tk.W)
        dropMenuLabel = tk.Label(self.root, text="Download Recent Playlist")
        dropMenuLabel.grid(row=1, column=1, sticky=tk.W)

        # URL text input
        self.youtubeLink = tk.Entry(self.root, width=50)
        self.youtubeLink.grid(row=1, column=1)

        # Download Button
        btn = tk.Button(self.root, text = 'Download', fg = 'red', command=lambda: self.process(self.youtubeLink.get()))
        btn.grid(row=2, column=0, sticky=tk.N)

        # gets the index of the selected playlist in the drop down menu
        recent = self.get_recent_playlists()
        default = "Recent Downloads"
        self.variable = tk.StringVar(self.root)
        self.variable.set(default) # default value

        w = tk.OptionMenu(self.root, self.variable, *recent, command=self.change_playlist_input)
        w.grid(row=0, column=1, sticky=tk.W)    

        # Output text to tell the user what's going on
        self.display_terminal = ScrolledText(width=60, height=10, wrap='none')
        self.display_terminal.grid(row=3, columnspan=8, padx=0, sticky=tk.N)

        self.root.mainloop()   



    """
    Helper Methods
    """
    def disprint(self, text_to_display: str, separator = "\n"):
        # prints text to the screen, limit of 60 characters per line
        text = f"{text_to_display[:60]}{separator}" 
        self.display_terminal.insert(tk.INSERT, text)
        if len(text_to_display) > 60: # Prevent Overflow
            second_line = f"             {text_to_display[60:106]}\n"
            self.display_terminal.insert(tk.INSERT, second_line)
        self.display_terminal.update_idletasks()

    def get_recent_playlists(self):
        # Returns a list of 5 elements in the csv file
        # if file doesn't exist:
        if not os.path.exists('recent_playlists.txt'):
                os.mknod('recent_playlists.txt')
                with open('recent_playlists.txt', 'r+') as f:
                    f.write('playlist_name,link\n')
                    f.write('Example,https://www.youtube.com/watch?v=jNQXAC9IVRw')
        df = pd.read_csv('recent_playlists.txt')
        recent = df.tail(5) # will get the last 5 searched links
        list_of_recent = list(recent.iloc[0:5]['playlist_name'])
        return list_of_recent
    
    def update_recent_downloads(self, name, link):
        # Resize the df to a length of 5 of most recent searches
        print(f"Savingi new entry: {name} {link}")
        df = pd.read_csv('recent_playlists.txt')
        df.loc[len(df)] = {"playlist_name": name, "link": link}
        df = df.tail(5)
        df.to_csv('recent_playlists.txt', index=False)

    def change_playlist_input(self, video_name):
        # Queries the recent playlist df to find link, clears input and fills with link
        df = pd.read_csv('recent_playlists.txt')
        index = np.where((df['playlist_name'] == video_name))[0][0]
        link = df.at[index,'link']
        self.youtubeLink.delete(0, tk.END)
        self.youtubeLink.insert(0, link)

    def set_download_location(self):
        self.download_location = tk.filedialog.askdirectory()
        print(self.download_location)

    def get_download_location(self):
        return self.download_location

    def set_video(self):
        self.video_stream = True

    def set_audio(self):
        self.video_stream = False

    def change_Quality(self):
        if self.quality == "low":
            self.quality = "high"
        elif self.quality == "high":
            self.quality = "low"



    """
    Pre-processing for the Video/Audio Download
    """
    def process(self, link):
        # Clear the display
        self.display_terminal.delete("1.0", tk.END)
        self.video_link = link

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



    """ 
    ----- Download List of Youtube Objects -----
    """
    def downloadYoutubeOjects(self, yt_objects: list):
        try: 
            for video in yt_objects:
                selected_stream = None
                try:
                    self.disprint("DOWNLOADING: " + video.title, separator="")
                    ##########self.video_title = video.title
                    if self.video_stream: # Filter Video MP4 only
                        mp4_streams = video.streams.filter(progressive=True, mime_type='video/mp4')
                        sorted_video_streams = sorted(mp4_streams, key=lambda stream: int(stream.resolution[:-1]))
                        if self.quality == "high":
                            selected_stream = sorted_video_streams[-1]
                        else:
                            selected_stream = sorted_video_streams[0]
                    else: # Filter Audio MP4 only
                        mp4_streams = video.streams.filter(mime_type="audio/mp4")
                        sorted_audio_streams = sorted(mp4_streams, key=lambda stream: int(stream.bitrate))
                        print(sorted_audio_streams)
                        if self.quality == "high":
                            selected_stream = sorted_audio_streams[-1]
                        else:
                            selected_stream = sorted_audio_streams[0]
                        print(f"Selected stream: {selected_stream}")

                    # Now Attempt to download the selected user Stream to the download location
                    selected_stream.download(self.download_location)

                    # Now download the image associataed with the song/video
                    #self.song_image_manager.download_image(f"https://www.youtube.com/watch?v={video.video_id}", 
                    #                                       self.get_download_location(), video.title)

                    # Update recent playlists
                    self.update_recent_downloads(video.title, self.video_link)

                    # No exceptions were thrown! Yay!
                    self.disprint(" OK")
                    
                except Exception as e:
                    self.disprint(f"Error Downloading Title, Skipping...")
                    print(f"Error: {e}")
                    logging.exception("An exception was thrown!")
            self.disprint("Done")
        except Exception as e: 
            self.disprint(f"Error Downloading Video")
            self.disprint(f"{e}\n")


"""" Main LOOP """
if __name__ == "__main__":
        program = Program()