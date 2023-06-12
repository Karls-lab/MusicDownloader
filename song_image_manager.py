import subprocess
from moviepy.editor import VideoFileClip
from moviepy.editor import ImageClip
from moviepy.editor import concatenate_videoclips
import pytube
import requests
import shutil
import os


class Image_manager():

    def download_image(self, youtube_link, saved_path, video_name):
        print(f"Saved path: {saved_path}")
        yt = pytube.YouTube(youtube_link)
        thumbnail_url = yt.thumbnail_url
        response = requests.get(thumbnail_url, stream=True)

        image_path = os.path.join(os.getcwd() + "/image.jpg")
        with open(image_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        response.close()

        # # Load the aduio clip
        audio_dir = os.path.join(saved_path, video_name + ".mp4")
        output_path = os.path.join(saved_path, video_name + "XXX.mp4")

        subprocess.run(['ffmpeg', '-i', audio_dir, '-i', image_path, '-map', '0', '-map', '1', '-c', 'copy', '-shortest', output_path])

        # audio_clip = VideoFileClip(audio_dir)
        # audio_clip = audio_clip.set_audio_channels(2)

        # # Load the image clip
        # image_clip = ImageClip(image_path)
        # image_clip = image_clip.set_duration(audio_clip.duration)
        # image_clip = image_clip.set_fps(audio_clip.fps)

        # print("HERE")

        # # # Combine the video clip and image clip
        # final_clip = concatenate_videoclips([image_clip.set_audio(audio_clip)])

        # # # Write the final combined video to a file
        # output_file_name = os.path.join(saved_path, video_name + ".mp4")
        # final_clip.write_videofile(output_file_name, codec="libx264", audio_codec="aac")
