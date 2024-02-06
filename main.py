import praw
import pandas as pd
import pydub
import re
import upload

import sottotitoli as st
import tiktok


def divide_text(text: str):
    char_to_split = "[({}).:;!?]"
    frasi = re.split(char_to_split, text.strip())

    # appena uno di noi trova un video di esempio mette le classiche frasi che vengono dette
    frasi.append("seguimi...")
    frasi.append("condivi...")
    frasi.append("like...")

    return frasi


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


def from_posts_to_mp3(lista_posts):
    num_post = 0
    chars_read_by_tiktok = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                            "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
                            "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    for t in range(len(lista_posts)):
        listastr = divide_text(lista_posts.iloc[t].loc['body'])
        output = pydub.AudioSegment.empty()
        lista_str_and_dur = []
        for block in listastr:
            if not set(block).intersection(chars_read_by_tiktok):
                continue
            response = tiktok.tts("f133bd730fc2e44ad33cf5bda762c6fc", "en_us_006", block)
            if response["status_code"] == 5:  # se audio_segment non corretto passa al post successivo
                break
            block = block.split()
            piece = len(block) // 9 + 1
            already_taken = 0
            for i in range(piece):
                if i == piece - 1:
                    subtitle = ' '.join(block[already_taken:])
                else:
                    subtitle = ' '.join(block[already_taken: already_taken + len(block) // piece])
                already_taken += len(block) // piece
                lista_str_and_dur.append((subtitle, response["audio_segment"].duration_seconds / piece))
            output += response["audio_segment"]
        else:  # eseguito se non sono stati prodotti audio_segment scorrett
            output.export(f'./output/Post {num_post}.mp3', format="mp3")
            st.video_sottotitoli(f"./output/Post {num_post}.mp3", lista_str_and_dur, num_post)
            num_post += 1


def main():
    number_of_posts = 1
    posts = from_reddit_to_posts(number_of_posts)
    posts.to_csv('file1.csv')
    from_posts_to_mp3(posts)


if __name__ == "__main__":
    main()
