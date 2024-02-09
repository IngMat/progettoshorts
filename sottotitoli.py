# from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
from moviepy.editor import *
import random
import os
import shutil

def format_string(s):
    words = s.split()
    formatted = '\n'.join([' '.join(words[i:i + 3]) for i in range(0, len(words), 3)])
    return formatted


def video_sottotitoli(audio_file_path: str, lista_str_and_dur: (str, int), num_post: int, video_title: str):
    # Carica il video
    audio_duration = sum(elem[1] for elem in lista_str_and_dur)
    starting_point = random.randint(15, 300)
    print(f"Video started at second {starting_point}")
    video = VideoFileClip("minecraft.mp4").subclip(starting_point)
    video = video.set_duration(audio_duration)
    video = video.crop(x1=442, x2=838, y1=8, y2=712)

    text_clips = []
    start_time = 0
    for elem in lista_str_and_dur:
        text_clips.append(
            TextClip(format_string(elem[0]), fontsize=36, color='white', font='Impact',
                     size=(video.w, video.h))  # penso inutile: transparent=True
            .set_position(('center', 'bottom'))
            .set_start(start_time)
            .set_duration(elem[1]))

        start_time += elem[1]

    # Sovrapponi le clip di testo al video
    result = CompositeVideoClip([video.set_duration(audio_duration)] + text_clips, size=(video.w, video.h))
    result = result.set_audio(AudioFileClip(audio_file_path))
    # Salva il video risultante
    result.write_videofile(f"./output/{num_post}, {video_title}.mp4", codec="libx264", audio_codec="aac")

    video.reader.close()
    os.remove(f'./output/Post {num_post}.wav')


def getDuration(path: str):
    video = VideoFileClip(path)
    return video.duration


def creaShort(path: str,npost : int):
    video = VideoFileClip(path)
    short = video.subclip(0, 60)

    # Ottieni il percorso della directory in cui si trova il file originale
    directory = os.path.dirname(path)

    # Crea una nuova directory all'interno della directory del file originale
    new_folder = os.path.join(directory, f"{npost}")
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    try:
        shutil.move(path, os.path.join(new_folder, "original_video.mp4"))
    except PermissionError as e:
        print(f"Impossibile spostare il file: {e}")

    short.write_videofile(os.path.join(new_folder, "short_video.mp4"), codec="libx264", audio_codec='aac')
    video.close()
    short.close()
    try:
        os.remove(path)
    except PermissionError as e:
        print(f"Impossibile spostare il file: {e}")


"""
if __name__ == "__main__":
    video_sottotitoli('./output/Post 1.wav',lista_str_and_dur=(),num_post=1,video_title='o cazz')
"""
