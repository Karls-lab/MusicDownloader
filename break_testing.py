import pytube
import re

# Playlist URL
playlist_url = "https://www.youtube.com/playlist?list=PLS_96ntbbZDH225rzjPEt5iNkmzbRVu7W"

# Extract the playlist ID from the URL
playlist_id = playlist_url.split("list=")[1]
print(playlist_id)
example = pytube.Playlist(playlist_url)
print(example)

# Create a YouTube object for the playlist
playlist = pytube.Playlist(f"https://www.youtube.com/playlist?list=PLS_96ntbbZDH225rzjPEt5iNkmzbRVu7W")
playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
print(len(playlist.video_urls))  # This will print 1...

# Iterate over the videos in the playlist
for video_url in playlist.video_urls:
    try:
        # Create a YouTube object for the video
        yt = pytube.YouTube(video_url)
        print('here')

        # Download the highest resolution video
        video = yt.streams.get_highest_resolution()
        video.download(output_path="/home/x1b3d3ad/Desktop")

        print(f"Downloaded: {yt.title}")
    except Exception as e:
        print(f"Error downloading video: {video_url}")
        print(str(e))
