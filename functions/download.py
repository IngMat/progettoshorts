from pytube import YouTube
import os

from functions import directories


video_dict = {"minecraft.mp4": "https://www.youtube.com/watch?v=R0b-VFV8SJ8",
              "satisfaction.mp4": "https://www.youtube.com/watch?v=olMxyuzxVDs"}


def download_video(link, video_name):

    # Ottieni il nome della cartella corrente
    current_folder = os.path.basename(os.getcwd())

    # Esegui il comando solo se la cartella corrente si chiama "progettoshort"
    if current_folder == "progettoshorts":
        os.environ['SSL_CERT_FILE'] = "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/certifi/cacert.pem"

    yt = YouTube(link)

    highresvideo = yt.streams.get_highest_resolution()

    # Ottieni il percorso alla cartella padre
    parent_dir = os.path.dirname(os.getcwd())

    # Percorso alla cartella "input_video" che è una sottocartella della cartella padre
    input_video_dir = os.path.join(parent_dir, "inputVideo")

    # Scarica il video nella cartella "input_video"
    highresvideo.download(input_video_dir, video_name)


def check_all_videos():

    input_video_dir = directories.check_upper_directory("inputVideo")

    for video_name in video_dict.keys():
        file_path = os.path.join(input_video_dir, video_name)
        if not os.path.exists(file_path):
            print(video_name, "will be downloaded")
            download_video(video_dict[video_name], video_name)
        else:
            print(video_name, "already downloaded")
