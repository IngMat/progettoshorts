import os
import random

import moviepy.editor as mp
from moviepy.video.fx import speedx as mpy

from functions import text, audio


def getDuration(path: str):
    # Returns the duration of a video file
    video = mp.VideoFileClip(path)
    return video.duration


def from_audio_to_video(video_file_path, lista_str_and_dur, video_title, num_post, posttitle, voice):
    # Creates a video using an audio file and overlays text

    # Get video path
    parent_dir = os.path.dirname(os.getcwd())
    input_video_dir = os.path.join(parent_dir, "inputVideo")
    input_video_path = os.path.join(input_video_dir, "minecraft.mp4")

    # Load video and set duration based on audio length
    audio_duration = sum(elem[1] for elem in lista_str_and_dur)
    starting_point = random.randint(15, 300)
    print(f"Video started at second {starting_point}")
    video = mp.VideoFileClip(input_video_path).subclip(starting_point)

    # Set video speed and dimension
    video = mpy.speedx(video, factor=1.15)
    video = video.set_duration(audio_duration)
    desired_width = 720
    desired_height = 1280
    video = video.crop(x1=(video.w - desired_width) / 2, x2=((video.w - desired_width) / 2) + desired_width,
                       y1=(video.h - desired_height) / 2, y2=(video.h - desired_height) / 2 + desired_height)

    # Generate title audio
    title_duration = audio.title_audio(posttitle, voice)

    # Create text clips for each text segment
    text_clips = []
    start_time = title_duration + 0.1
    for elem in lista_str_and_dur:
        text_clips.append(
            mp.TextClip(text.multiline_string(elem[0], 3), fontsize=60, color='white', font='Impact',
                        size=(video.w, video.h))  # penso inutile: transparent=True
            .set_position(('center', 'bottom'))
            .set_start(start_time)
            .set_duration(elem[1]))

        start_time += elem[1]

    # Overlay  a fake post image on the video
    image = mp.ImageClip("fakepost.png")
    image = image.set_duration(title_duration)
    image = image.set_position('center', 'bottom')

    # Create the title text clip
    title = (mp.TextClip(text.multiline_string(posttitle, 10), fontsize=18, color='black', font='Impact', align='West',
                         size=(video.w, video.h))
             .set_position(('center', 'bottom'))
             .set_duration(1.5))
    title = title.margin(bottom=50, left=100, opacity=0)

    # Combine all elements (video, text, title, image)
    result = mp.CompositeVideoClip([video.set_duration(audio_duration + title_duration)] + text_clips
                                   + [image.set_duration(title_duration)]
                                   + [title.set_duration(title_duration)], size=(video.w, video.h))
    audio.concatenate_audio("Audio.wav", "Titolo.wav")
    result = result.set_audio(mp.AudioFileClip("Risultato.wav"))

    # Save the final video file
    video_title = video_title.replace("?", "")
    video_path = f"{video_file_path}/{num_post}-{video_title}.mp4"
    result = result.set_duration(audio_duration + title_duration)
    result.write_videofile(filename=video_path, fps=24, codec="hevc_nvenc", audio_codec="aac", threads=64)

    # Close the video reader and remove temporary audio files
    video.reader.close()
    os.remove(f'Audio.wav')
    os.remove("Titolo.wav")
    os.remove("Risultato.wav")

    return video_path


def createShort(video_path: str, directory_path: str, short_title: str):
    # Creates a short version of a video (maximum 50 seconds)
    video = mp.VideoFileClip(video_path)

    if video.duration >= 50:
        short = video.subclip(0, 50)
    else:
        short = video

    # Save the short video
    short_path = f"{directory_path}/{short_title}.mp4"
    short.write_videofile(short_path, codec="libx264", audio_codec='aac')
    video.close()
    short.close()

    return short_path


def video_merge(path_list, folder_path, title):
    # Merges multiple video clips into a single final video
    if title == "ERROR":
        exit("Title == ERROR")

    # Load all video clips into a list
    clip_video = [mp.VideoFileClip(percorso) for percorso in path_list]

    # Concatenate all clips into a single video
    final_video = mp.concatenate_videoclips(clip_video)

    # Define the output path
    final_path = os.path.join(folder_path, title + ".mp4")

    # Save the final merged video
    final_video.write_videofile(final_path, codec="libx264", audio_codec="aac")

    return final_path


def video_title(title, audio_path, num, width, height):
    # reates a title animation video with text and audio
    duration = 5

    # Format title text
    title = text.multiline_string(title, 3)

    # Dictionary for numbering title sequences
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

    output_path = "output.mp4"

    # Save the video
    video.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=20)

    return output_path
