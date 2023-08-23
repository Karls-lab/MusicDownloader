from pytube import Playlist
from pytube import YouTube
import os
import tkinter as tk
from tkinter import filedialog
import logging
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import numpy as np

# PYTUBE DOCS: https://pytube.io/en/latest/index.html
# Created by Karl :)
# Version 1.3

class Program:
    # ----- Init for gui -----
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Youtube Music Downloader")
        self.root.geometry('700x400')

        # Variables and their default values
        self.download_location = os.path.join(os.path.expanduser('~'),'Music')
        self.video_stream = True
        self.quality = "low"
        self.video_title = ""
        self.video_link = ""

        """Menu Labels""" 
        # row 0
        save_location_label = tk.Label(self.root, text="Save Location:")
        save_location_label.grid(row=0, column=0, sticky=tk.W)

        """Frame check buttons to control video/audio quality and audio/video only"""
        # row 1
        frame = tk.Frame(self.root, borderwidth=2, relief="ridge")  # You can customize borderwidth and relief
        frame.grid(row=1, column=0, columnspan=3, sticky='ew', padx=1)
        self.high_quallity_switch= tk.Checkbutton(frame, text="High Quality", onvalue="high", offvalue="low", command=lambda: self.change_Quality())
        self.high_quallity_switch.grid(row=1, column=0, sticky='ew')
        self.low_quallity_switch= tk.Checkbutton(frame, text="Low Quality", onvalue="low", offvalue="high", command=lambda: self.change_Quality())
        self.low_quallity_switch.grid(row=1, column=1, sticky='ew')
        self.audio_only_switch = tk.Checkbutton(frame, text="Audio Only", onvalue="audio", offvalue="video", command=lambda: self.change_audio_video())
        self.audio_only_switch.grid(row=1, column=2, sticky='n', padx=1)
        self.video_only_switch = tk.Checkbutton(frame, text="Video/Audio", onvalue="video", offvalue="audio", command=lambda: self.change_audio_video())
        self.video_only_switch.grid(row=1, column=3, sticky='e')

        # row 3
        url_label = tk.Label(self.root, text="Youtube URL:")
        url_label.grid(row=3, column=0, sticky=tk.W)
        
        # row 2
        dropMenuLabel = tk.Label(self.root, text="Recent URLs")
        dropMenuLabel.grid(row=2, column=0, sticky=tk.W)
        
        """Text Input and Output fields"""
        # Download Location text input, row 0
        self.downloadLocation = tk.Entry(self.root, width=50)
        self.downloadLocation.insert(0, self.download_location)
        self.downloadLocation.grid(row=0, column=1, columnspan=4, sticky=tk.W)

        # URL text input, row 3
        self.youtubeLink = tk.Entry(self.root, width=50)
        self.youtubeLink.grid(row=3, column=1, columnspan=2, sticky=tk.W)

        # Download Button, row 4
        btn = tk.Button(self.root, text = 'Download', fg = 'red', command=lambda: self.process(self.youtubeLink.get()))
        btn.grid(row=4, column=0, sticky=tk.W, padx=15)

        # Drop down menu for recent downloads, row 2
        recent = self.get_recent_playlists()
        default = "Recent Downloads"
        self.variable = tk.StringVar(self.root)
        self.variable.set(default) # default value
        w = tk.OptionMenu(self.root, self.variable, *recent, command=self.change_playlist_input)
        w.config(width=20)
        w.grid(row=2, column=1, columnspan=2, sticky='ew')    

        # Display Terminal
        self.display_terminal = ScrolledText(width=80, height=10, wrap='none')
        self.display_terminal.grid(row=5, columnspan=15, padx=10, sticky='ew')

        self.root.mainloop()   


    """
    Helper Methods
    """
    def disprint(self, text_to_display: str, separator = "\n"):
        """prints text to the screen, limit of 60 characters per line"""
        text = f"{text_to_display[:60]}{separator}" 
        self.display_terminal.insert(tk.INSERT, text)
        self.display_terminal.yview('end')
        if len(text_to_display) > 60: # Prevent Overflow
            second_line = f"             {text_to_display[60:106]}\n"
            self.display_terminal.insert(tk.INSERT, second_line)
        self.display_terminal.update_idletasks()


    def get_recent_playlists(self):
        """ Returns a list of 5 elements in the csv file
            if file doesn't exist, it creates a new one """
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
        if not df.isin([name]).any().any(): # if the entry is not in recent, add it
            df.loc[len(df)] = {"playlist_name": name, "link": link}
        df = df.tail(5) # trim to only last 5 entries
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


    def change_audio_video(self):
        """Deselects the other button and changes the value of video_stream"""
        if self.video_stream:
            self.video_stream = False
            self.video_only_switch.deselect()
        else:
            self.video_stream = True
            self.audio_only_switch.deselect()


    def change_Quality(self):
        """Changes the quality of the video/audio and updates the check button"""
        if self.quality == "low":
            self.quality = "high"
            self.low_quallity_switch.deselect()
        elif self.quality == "high":
            self.quality = "low"
            self.high_quallity_switch.deselect()


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
            if "playlist" in link: # if it's a playlist
                """ create a yt object, save name and link to recent downloads, download playlist"""
                print("Playlist Detected")
                yt = Playlist(link)
                # update save location to a folder with the playlist name:
                self.download_location = f"{self.download_location}/{yt.title}"
                # create a new folder if it doesn't exist
                if not os.path.exists(self.download_location):
                    os.mkdir(f"{self.download_location}")
                self.update_recent_downloads(yt.title, self.video_link)
                self.downloadYoutubeOjects(yt.videos) # pass a list of youtube video objects
            else: # if it's only one video
                """ create a yt object, save name and link to recent downloads, download video"""
                print("Video Detected")
                yt = YouTube(link)
                self.update_recent_downloads(yt.title, self.video_link)
                self.downloadYoutubeOjects([yt]) # pass a one element list of youtube video objects
        except Exception as e: # something went wrong
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
                print(f"video: {video}")
                try:
                    self.disprint("DOWNLOADING: " + video.title, separator="")
                    if self.video_stream: # Filter Video MP4 only
                        # Sort the streams from lowest quality to highest quality.
                        mp4_streams = video.streams.filter(progressive=True, mime_type='video/mp4')
                        sorted_video_streams = sorted(mp4_streams, key=lambda stream: int(stream.resolution[:-1]))
                        if self.quality == "high": 
                            selected_stream = sorted_video_streams[-1]
                        else:
                            selected_stream = sorted_video_streams[0]
                    else: # Filter Audio MP4 only
                        # Sort the streams from lowest quality to highest quality.
                        mp4_streams = video.streams.filter(mime_type="audio/mp4")
                        sorted_audio_streams = sorted(mp4_streams, key=lambda stream: int(stream.bitrate))
                        if self.quality == "high":
                            selected_stream = sorted_audio_streams[-1]
                        else:
                            selected_stream = sorted_audio_streams[0]
                        print(f"Selected stream: {selected_stream}")

                    # Now Attempt to download the selected user Stream to the download location
                    selected_stream.download(filename=f"{video.author} - {video.title}.{selected_stream.subtype}", output_path=f"{self.download_location}")

                    # Now download the image associataed with the song/video
                    #self.song_image_manager.download_image(f"https://www.youtube.com/watch?v={video.video_id}", 
                    #                                       self.get_download_location(), video.title)

                    # No exceptions were thrown! Yay!
                    self.disprint(" OK")
                    
                except Exception as e:
                    self.disprint(f"Error Downloading Title, Skipping...")
                    logging.error(f"Error Downloading Title, Skipping... {e}")
            self.disprint("Done")
        except Exception as e: 
            self.disprint(f"Error Downloading Video/Playlist")
            logging.error(f"Error Downloading Video/Playlist {e}")
            return

"""" Main LOOP """
if __name__ == "__main__":
        program = Program()