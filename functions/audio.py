import pydub
from functions import tiktok, text


def from_post_to_audio(post, voice, is_third_post=False):
    chars_read_by_tiktok = set("abcdefghijklmnopqrstuvwxyz1234567890")
    strlist = text.divide_by_punctuation(post.loc["body"])  # Split post body into smaller blocks by punctuation

    # Add promotional phrases in the last post
    if is_third_post:
        strlist.extend(["Comment with your opinions",
                        "follow the channel",
                        "hit the like button ands share if you enjoyed the video"])

    output = pydub.AudioSegment.empty()
    subtitles = []  # (str, float) = (subtitle_text; subtitle_lenght)
    i = 1
    for block in strlist:
        if not set(block.lower()).intersection(chars_read_by_tiktok) or block == "":  # control unreadable blocks
            continue
        response = tiktok.tts("f133bd730fc2e44ad33cf5bda762c6fc", voice, block)  # dictionary with file audio
        print(f"Successfully generated block number {i}")
        i += 1

        if response["status_code"] == 6: # skip if TTS response indicates an error
            continue

        # Divide the sentence into blocks of up to 9 words for subtitle creation
        sentences = text.divide_by_words([block], 9)
        for sentence in sentences:
            subtitles.append((sentence, response["audio_segment"].duration_seconds / len(sentences) / 1.15))

        output += response["audio_segment"]  # concatenate the audio segment

    output = output.speedup(playback_speed=1.15)
    output.export("Audio.wav", format="wav")

    return subtitles


def title_audio(title, voice):
    response = tiktok.tts("f133bd730fc2e44ad33cf5bda762c6fc", voice, title)
    output = response["audio_segment"].speedup(playback_speed=1.15)
    output.export("Title.wav", format="wav")

    return output.duration_seconds


def concatenate_audio(postpath, titlepath):
    output = pydub.AudioSegment.from_wav(titlepath) + pydub.AudioSegment.from_wav(postpath)
    output.export("Result.wav", format="wav")
