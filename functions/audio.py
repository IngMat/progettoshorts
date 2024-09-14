import pydub

from functions import tiktok, text


def from_post_to_audio(post, voice, is_third_post=False):
    chars_read_by_tiktok = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                            "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
                            "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    strlist = string.divide_by_punctuation(post.loc["body"])  # strlist is the body of the post

    # call to undestand the sex of the speaker
    if is_third_post:
        strlist.append("Comment with your opinions")
        strlist.append("follow the channel")
        strlist.append("hit the like button ands share if you enjoyed the video")

    output = pydub.AudioSegment.empty()
    lista_str_and_dur = []  # (str, float) = (subtitle_text; subtitle_lenght)
    i = 1
    for block in strlist:
        if not set(block.lower()).intersection(chars_read_by_tiktok) or block == "":  # control unreadable blocks
            continue
        response = tiktok.tts("f133bd730fc2e44ad33cf5bda762c6fc", voice, block)  # dictionary with file audio
        print(f"Successfully generated block number {i}")
        i += 1

        # creazione di lista_str_and_dur dividendo la frase in più blocchi di 9 parole
        sentences = string.divide_by_words([block], 9)
        for sentence in sentences:
            if response["status_code"] == 6:
                continue
            lista_str_and_dur.append((sentence, response["audio_segment"].duration_seconds / len(sentences) / 1.15))

        output += response["audio_segment"]  # concatenate audio files

    output = output.speedup(playback_speed=1.15)
    output.export("Audio.wav", format="wav")

    return lista_str_and_dur


def title_audio(title, voice):
    response = tiktok.tts("f133bd730fc2e44ad33cf5bda762c6fc", voice, title)
    output = response["audio_segment"].speedup(playback_speed=1.15)
    output.export("Titolo.wav", format="wav")

    return output.duration_seconds


def concatenate_audio(postpath, titlepath):
    output = pydub.AudioSegment.from_wav(titlepath) + pydub.AudioSegment.from_wav(postpath)
    output.export("Risultato.wav", format="wav")
