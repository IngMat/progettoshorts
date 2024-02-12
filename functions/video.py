import random
import moviepy.editor as mp
import os

from functions import string


def getDuration(path: str):
    video = mp.VideoFileClip(path)
    return video.duration


def from_audio_to_video(video_file_path, lista_str_and_dur, video_title, num_post):
    # ottieni percorso video
    parent_dir = os.path.dirname(os.getcwd())
    input_video_dir = os.path.join(parent_dir, "inputVideo")
    input_video_path = os.path.join(input_video_dir, "minecraft.mp4")

    # Carica il video
    audio_duration = sum(elem[1] for elem in lista_str_and_dur)
    starting_point = random.randint(15, 300)
    print(f"Video started at second {starting_point}")
    video = mp.VideoFileClip(input_video_path).subclip(starting_point)
    video = video.set_duration(audio_duration)
    video = video.crop(x1=442, x2=838, y1=8, y2=712)

    text_clips = []
    start_time = 0
    for elem in lista_str_and_dur:
        text_clips.append(
            mp.TextClip(string.multiline_string(elem[0], 3), fontsize=28, color='white', font='Impact',
                        size=(video.w, video.h))  # penso inutile: transparent=True
            .set_position(('center', 'bottom'))
            .set_start(start_time)
            .set_duration(elem[1]))

        start_time += elem[1]

    # Sovrapponi le clip di testo al video
    result = mp.CompositeVideoClip([video.set_duration(audio_duration)] + text_clips, size=(video.w, video.h))
    result = result.set_audio(mp.AudioFileClip("Audio.wav"))

    video_path = f"{video_file_path}/{num_post}-{video_title}.mp4"
    # Salva il video risultante
    result.write_videofile(video_path, codec="libx264", audio_codec="aac")

    video.reader.close()
    os.remove(f'Audio.wav')

    return video_path


def creaShort(video_path: str, directory_path: str, short_title: str):
    video = mp.VideoFileClip(video_path)

    if video.duration >= 50:
        short = video.subclip(0, 50)
    else:
        short = video

    """
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
    """

    short_path = f"{directory_path}/{short_title}.mp4"
    short.write_videofile(short_path, codec="libx264", audio_codec='aac')
    video.close()
    short.close()

    """
        try:
            os.remove(path)
        except PermissionError as e:
            print(f"Impossibile spostare il file: {e}")

    """

    return short_path


def video_merge(lista_percorsi, percorso_cartella, titolo):
    if titolo == "ERROR":
        exit("titolo == ERROR")

    # Crea una lista di clip video
    clip_video = [mp.VideoFileClip(percorso) for percorso in lista_percorsi]

    # Unisci le clip video
    video_finale = mp.concatenate_videoclips(clip_video)

    # Percorso del video finale
    percorso_finale = os.path.join(percorso_cartella, titolo + ".mp4")

    # Scrivi il video finale
    video_finale.write_videofile(percorso_finale, codec="libx264", audio_codec="aac")

    return percorso_finale


def video_title(title, audio_path, num, width, height):
    duration = 5

    title = string.multiline_string(title, 3)
    dictionary = {1: "First", 2: "Second", 3: "Third"}
    title = dictionary[num] + "\n" + title

    # Create a text clip with the provided text
    video = (mp.TextClip(title, fontsize=28, color='white', font='Impact', size=(width, height))
             .set_position(('center', 'bottom'))
             .set_duration(duration))

    # Create an audio clip from the provided file
    audio_clip = mp.AudioFileClip(audio_path).subclip(0, duration)

    # Add the audio to the video
    video = video.set_audio(audio_clip)

    # Output file path
    output_path = "output.mp4"

    # Save the video
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Return the path of the output file
    return output_path
