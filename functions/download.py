from pytube import YouTube
import os
import ssl
from functions import directories
import yt_dlp


video_dict = {"satisfaction.mp4": "https://www.youtube.com/watch?v=olMxyuzxVDs",
              "minecraft.mp4": "https://www.youtube.com/watch?v=R0b-VFV8SJ8"}


def download_video(link, video_name):
    # Path to "inputVideo" folder
    current_dir = os.getcwd()
    input_video_dir = os.path.join(current_dir, "inputVideo")

    os.makedirs(input_video_dir, exist_ok=True)

    # Settings for yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(input_video_dir, video_name),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


def check_all_videos():
    # Check that all videos are present
    input_video_dir = directories.check_upper_directory("inputVideo")

    for video_name in video_dict.keys():
        file_path = os.path.join(input_video_dir, video_name)
        if not os.path.exists(file_path):
            print(video_name, "will be downloaded")
            download_video(video_dict[video_name], video_name)
        else:
            print(video_name, "already downloaded")
