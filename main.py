import praw
import pandas as pd
import pydub
import re

import sottotitoli as st
import tiktok
import upload


def divide_text(text: str):
    char_to_split = "[({}).:;!?]"  # sono quelli interni alle []
    frasi = re.split(char_to_split, text.strip())  # divisione testo per punteggiatura

    frasi.append("Press the like button, comment with your opinion")
    frasi.append("Share the video and subscribe to the channel")

    sentences = []
    for block in frasi:
        blocks = block.split()  # divisione per parole
        if len(blocks) < 40:  # caso accettato da tiktok
            sentences.append(block)
            continue
        piece = len(blocks) // 40 + 1
        already_taken = 0
        for i in range(piece):
            if i == piece - 1:
                sentences.append(' '.join(
                    blocks[already_taken:]))  # l'ultimo blocco della frase è unito indipendentemente dalla lunghezza
            else:
                sentences.append(' '.join(blocks[already_taken: already_taken + len(
                    blocks) // piece]))  # unione parole in più pezzi accettati da tiktok
                already_taken += len(blocks) // piece
    return sentences


def from_reddit_to_posts(number_of_posts):
    reddit = praw.Reddit(
        client_id="HU4BpzSxzqNStBb3X-lfeQ",
        client_secret="l_-UaJpNj6BpTUyMm-8apYb9vC0fCg",
        user_agent="android:com.example.myredditapp:v1.2.3 (by u/PitifulBook4011)",
    )

    posts = []
    ml_subreddit = reddit.subreddit("offmychest+relationships+amitheasshole")
    for post in ml_subreddit.top(time_filter="day", limit=number_of_posts):
        posts.append(
            [post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posts = pd.DataFrame(posts, columns=["title", "score", "id", "subreddit", "url", "num_comments", "body", "created"])
    return posts


def from_posts_to_video(lista_posts):
    with open("numerazione_posts.txt", "r") as file:
        testo_file = file.readlines()
        parti = testo_file[0].split(":")

    parti[1] = parti[1].replace(" ", "")
    num_post = int(parti[1])
    chars_read_by_tiktok = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                            "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
                            "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    for t in range(len(lista_posts)):
        listastr = divide_text(lista_posts.iloc[t].loc['body'])  # listastr è il testo del post
        output = pydub.AudioSegment.empty()
        lista_str_and_dur = []  # considera tuple (str, float) = (schermata sottotitolo; durata sottotitolo)
        for block in listastr:
            if not set(block.lower()).intersection(chars_read_by_tiktok):  # controlla caratteri leggibili
                continue
            if block == '':  # controlla stringa vuota
                continue
            response = tiktok.tts("f133bd730fc2e44ad33cf5bda762c6fc", "en_us_006",
                                  block)  # ottiene dizionario con file audio
            if response["status_code"] == 5:  # se audio_segment non corretto passa al post successivo
                break

            # creazione di lista_str_and_dur dividendo la frase in più blocchi di 9 parole
            block = block.split()
            piece = len(block) // 9 + 1
            already_taken = 0
            for i in range(piece):
                if i == piece - 1:
                    subtitle = ' '.join(block[already_taken:])
                else:
                    subtitle = ' '.join(block[already_taken: already_taken + len(block) // piece])
                already_taken += len(block) // piece
                lista_str_and_dur.append((subtitle, response["audio_segment"].duration_seconds / piece / 1.15))

            output += response["audio_segment"]  # concatena i file audio
        else:  # eseguito se non sono stati prodotti audio_segment scorretti
            video_title = lista_posts.iloc[t].loc["title"]
            video_title = video_title.replace(".", "")
            output = output.speedup(playback_speed=1.15)
            output.export(f'./output/Post {num_post}.mp3', format="mp3")
            st.video_sottotitoli(f"./output/Post {num_post}.mp3", lista_str_and_dur, num_post, video_title)
            num_post += 1

    parti[1] = parti[1].replace(f"{parti[1]}", str(num_post), 1)
    with open("numerazione_posts.txt", "w") as file:
        parti[1] = f" {parti[1]}\n"
        first_line = ":".join(parti)
        testo_file[0] = first_line
        file.writelines(testo_file)


def main():
    number_of_posts = 1
    posts = from_reddit_to_posts(number_of_posts)
    posts.to_csv('file1.csv')
    from_posts_to_video(posts)


if __name__ == "__main__":
    main()
