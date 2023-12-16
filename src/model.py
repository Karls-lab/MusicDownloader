from pytube import Playlist, YouTube
import os
import pandas as pd
import numpy as np
import logging
import tkinter as tk

class Model:
    def __init__(self):
        self.download_location = os.path.join(os.path.expanduser('~'),'Music')
        self.video_stream = True
        self.quality = "low"
        self.video_title = ""
        self.video_link = ""
        self.display_terminal_text = "here"


    def get_recent_playlists(self):
        """ Returns a dictionary of the 5 most recent videos/playlists
            In a dictionary. The key is the playlist name, and the value is the link"""
        if not os.path.exists('recent_playlists.txt'):
                os.mkdir('recent_playlists.txt')
        df = pd.read_csv('recent_playlists.txt')
        recent = df.tail(5) # will get the last 5 searched links
        recent_dict = dict(zip(recent['playlist_name'], recent['link']))
        return recent_dict


    def change_Quality(self):
        self.controller.change_Quality()


    def change_audio_video(self):
        self.controller.change_audio_video()


    def update_recent_downloads(self, name, link):
        # Resize the df to a length of 5 of most recent searches
        print(f"Saving new entry: {name} {link}")
        df = pd.read_csv('recent_playlists.txt')
        if not df.isin([name]).any().any(): # if the entry is not in recent, add it
            df.loc[len(df)] = {"playlist_name": name, "link": link}
        df = df.tail(5) # trim to only last 5 entries
        df.to_csv('recent_playlists.txt', index=False)


    """
    Pre-processing for the Video/Audio Download
    """
    def process(self, link):
        # Clear the display
        # self.display_terminal.delete("1.0", tk.END)
        self.video_link = link

        # self.disprint("processing...")
        # self.disprint(f"Saving music to: {self.download_location}\n")
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
                return yt.videos
                self.downloadYoutubeOjects(yt.videos) # pass a list of youtube video objects
            else: # if it's only one video
                """ create a yt object, save name and link to recent downloads, download video"""
                print("Video Detected")
                yt = YouTube(link)
                self.update_recent_downloads(yt.title, self.video_link)
                return [yt]
                self.downloadYoutubeOjects([yt]) # pass a one element list of youtube video objects
        except Exception as e: # something went wrong
            print(e)
            # self.disprint(f"Connection Error {e}")
            return



    """ 
    ----- Download List of Youtube Objects -----
    """
    def downloadYoutubeOjects(self, yt_objects: list):
        try: 
            for video in yt_objects:
                selected_stream = None
                print(f"video: {video}")
                self.video_title = video.title
                print(f"video title: {self.video_title}")
                try:
                    # self.disprint("DOWNLOADING: " + video.title, separator="")
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
                    # self.disprint(" OK")
                    
                except Exception as e:
                    # self.disprint(f"Error Downloading Title, Skipping...")
                    logging.error(f"Error Downloading Title, Skipping... {e}")
            # self.disprint("Done")
        except Exception as e: 
            # self.disprint(f"Error Downloading Video/Playlist")
            logging.error(f"Error Downloading Video/Playlist {e}")
            return
