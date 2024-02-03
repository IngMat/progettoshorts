from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from pydub import AudioSegment
import subprocess
import whisper
import librosa


def sottotitoli(audio_file_path: str):
    # Definisci il percorso del modello di lingua italiano per Whisper

    audio = whisper.load_audio(audio_file_path)
    model = whisper.load_model("small")
    transcriptions = model.transcribe(audio)
    words = [entry["word"] for entry in transcriptions if "word" in entry]

    print(words)

    audio_duration = librosa.get_duration(filename=audio_file_path)
    # Carica il video
    video_path = "minecraft.mp4"
    video = VideoFileClip(video_path).set_duration(audio_duration)

    text_clips = [
        TextClip(word, fontsize=24, color='white', bg_color="", size=(video.w, video.h))
        .set_position(('center', 'bottom'))
        .set_duration(1)
        for word in words
    ]

    # Sovrapponi le clip di testo al video
    result = CompositeVideoClip([video.set_duration(audio_duration)] + text_clips, size=(video.w, video.h))

    # Salva il video risultante
    result.write_videofile("video_with_subtitles.mp4", codec="libx264", audio_codec="aac")

    video.reader.close()

if __name__ == "__main__":
    sottotitoli("./output/Post 0.mp3")
