from pytube import Playlist, YouTube
from moviepy.editor import AudioFileClip, ImageClip
import os
import pandas as pd
import numpy as np
import tkinter as tk
import requests

class Model:
    def __init__(self, logger):
        self.logger = logger
        print("LOGGER: ", logger)
        self.video_stream = True
        self.quality = "low"
        self.video_title = ""
        self.video_link = ""
        self.thumbnail_path = ""
        self.download_video_path = ""
        self.audio_file = False
        self.display_terminal_text = ""


    def get_recent_playlists(self):
        """ Returns a dictionary of the 5 most recent videos/playlists
            In a dictionary. The key is the playlist name, and the value is the link"""
        recentYTLinks = os.path.join(os.path.dirname(__file__), "data", "recent_playlists.csv")
        if not os.path.exists(recentYTLinks): # if recent doesn't exist, create it. 
            with open(recentYTLinks, 'w') as f:
                f.write("playlist_name,link\n")
                f.write("Me at the Zoo,https://www.youtube.com/watch?v=jNQXAC9IVRw")
        df = pd.read_csv(recentYTLinks)
        recent = df.tail(5) # will get the last 5 searched links
        reversed_recent = recent.iloc[::-1] # Reverse DF
        return_dict = dict(zip(reversed_recent['playlist_name'], reversed_recent['link']))
        return return_dict 


    def change_Quality(self):
        self.controller.change_Quality()


    def change_audio_video(self):
        self.controller.change_audio_video()


    def update_recent_downloads(self, name, link):
        # Resize the df to a length of 5 of most recent searches
        print(f"Saving new entry: {name} {link}")
        recent_playlists = os.path.join(os.path.dirname(__file__), "data", "recent_playlists.csv")
        df = pd.read_csv(recent_playlists)
        if not df.isin([name]).any().any(): # if the entry is not in recent, add it
            df.loc[len(df)] = {"playlist_name": name, "link": link}
        df = df.tail(5) # trim to only last 5 entries
        df.to_csv(recent_playlists, index=False)


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
            else: # if it's only one video
                """ create a yt object, save name and link to recent downloads, download video"""
                print("Found a YT object")
                yt = YouTube(link)
                self.update_recent_downloads(yt.title, self.video_link)
                return [yt]
        except Exception as e: # something went wrong
            print(e)
            # self.disprint(f"Connection Error {e}")
            return



    """ 
    ----- Download List of Youtube Objects -----
    """
    def downloadYoutubeObjects(self, yt_objects: list):
        try: 
            for video in yt_objects:
                selected_stream = None
                print(f"video: {video}")
                self.video_title = video.title
                print(f"video title: {self.video_title}")
                try:
                    if self.video_stream: # Filter VIDEO LOGIC MP4 only
                        # Sort the streams from lowest quality to highest quality.
                        # TODO let user choose stream video quality
                        print("Video Stream")
                        print(f"video.streams: {video.streams}")
                        mp4_streams = video.streams.filter(progressive=True, mime_type='video/mp4')
                        sorted_video_streams = sorted(mp4_streams, key=lambda stream: int(stream.resolution[:-1]))
                        print(f"sorted video streams: {sorted_video_streams}")
                        if self.quality == "high": 
                            selected_stream = sorted_video_streams[-1]
                        else:
                            selected_stream = sorted_video_streams[0]
                    else: # Filter AUDIO LOGIC MP3 only
                        """
                        Will prefer MP3 over MP4
                        Sort the streams from lowest quality to highest quality.
                        """

                        print("Audio Stream")
                        self.audio_file = True
                        mp_streams = video.streams.filter(mime_type="audio/mp3")
                        if len(mp_streams) == 0:
                            mp_streams= video.streams.filter(mime_type="audio/mp4")

                        # Sort the streams from lowest quality to highest quality.
                        for stream in mp_streams:
                            print(f"stream: {stream}")
                            stream.abr = int(stream.abr[:-4]) # removes kbps from end
                        sorted_audio_streams = sorted(mp_streams, key=lambda stream: stream.abr)
                        print(f"sorted audio streams: {sorted_audio_streams}")

                        if len(sorted_audio_streams) < 1:
                            raise Exception("Unable to find audio stream")
                        elif self.quality == "high":
                            selected_stream = sorted_audio_streams[-1]
                        elif self.quality == "low":
                            selected_stream = sorted_audio_streams[0]
                        print(f"Selected stream: {selected_stream}")

                    # Set the download path to the download location
                    video_name = f"{video.author} - {video.title}.{selected_stream.subtype}"
                    self.download_video_path = f"{self.download_location}/{video_name}"

                    # Now Attempt to download the selected user Stream to the download location
                    selected_stream.download(filename=f"{video.author} - {video.title}.{selected_stream.subtype}", output_path=f"{self.download_location}")

                    # Download the thumbnail
                    self.download_thumbnail()

                    # Combine the video and thumbnail if it's audio only 
                    if self.audio_file:
                        self.download_video_with_thumbnail()
                    
                except Exception as e:
                    self.logger.error(f"Error Downloading Title, Skipping... {e}")
        except Exception as e: 
            # self.disprint(f"Error Downloading Video/Playlist")
            self.logger.error(f"Error Downloading Video/Playlist {e}")
            return


    """
    Grabs the Thumbnail Image for Every Youtube Video 
    """
    def download_thumbnail(self):
        thumbnailLink = YouTube(self.video_link).thumbnail_url
        thumbnail = requests.get(thumbnailLink)
        saveLocation = os.path.join(os.path.dirname(__file__), 'data', 'video.png')
        with open(saveLocation, "wb") as img_file:
            img_file.write(thumbnail.content)
        self.thumbnail_path = saveLocation

    def delete_thumbnail(self):
        saveLocation = os.path.join(os.path.dirname(__file__), 'data')
        os.remove(f"{saveLocation}/video.png")


    """
    Downloads the Video, and combines it with the Thumbnail 
    """
    def download_video_with_thumbnail(self):
        self.logger.info(f'download video path: {self.download_video_path}')
        print(f'download video path: {self.download_video_path}')
        print(f'download thumbnail path: {self.thumbnail_path}')
        try:
            audio = AudioFileClip(self.download_video_path)
            thumbnail = ImageClip(self.thumbnail_path)
            resultAudio = thumbnail.set_audio(audio)
            resultAudio.duration = audio.duration
            resultAudio.fps = 1
            resultAudio.write_videofile(self.download_video_path, fps=1, codec='mpeg4')
        except Exception as e:
            print(f"Error combining video and thumbnail: {e}")
            return