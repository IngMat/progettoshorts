from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import random
import os


def format_string(s):
    words = s.split()
    formatted = '\n'.join([' '.join(words[i:i + 3]) for i in range(0, len(words), 3)])
    return formatted


def video_sottotitoli(audio_file_path: str, lista_str_and_dur: (str, int), num_posts: int, video_title: str):
    # Carica il video
    audio_duration = sum(elem[1] for elem in lista_str_and_dur)
    starting_point = random.randint(15, 300)
    print(f"Video started at second {starting_point}")
    video = VideoFileClip("minecraft.mp4").subclip(starting_point)
    video = video.set_duration(audio_duration)
    # video = video.resize(height=1920)  # Ridimensiona l'altezza a 1920
    # video = video.crop(x_center=video.w / 2, width=1080)

    text_clips = []
    start_time = 0
    for elem in lista_str_and_dur:
        text_clips.append(
            TextClip(format_string(elem[0]), fontsize=30, color='white', font='Impact', size=(video.w, video.h)) # penso inutile: transparent=True
            .set_position(('center', 'bottom'))
            .set_start(start_time)
            .set_duration(elem[1]))

        start_time += elem[1]

    # Sovrapponi le clip di testo al video
    result = CompositeVideoClip([video.set_duration(audio_duration)] + text_clips, size=(video.w, video.h)) 
    result = result.set_audio(AudioFileClip(audio_file_path))
    # Salva il video risultante
    result.write_videofile(f"./output/{num_posts}, {video_title}.mp4", codec="libx264", audio_codec="aac")

    video.reader.close()
    os.remove(f'./output/Post {num_posts}.mp3')
