import praw
import pandas as pd
import tiktok


def contatoreparole(string):
    string1 = string.strip()
    cont = 1
    for i in string1:
        if i == " ":
            cont += 1

    return cont


def main():
    reddit = praw.Reddit(
        client_id="HU4BpzSxzqNStBb3X-lfeQ",
        client_secret="l_-UaJpNj6BpTUyMm-8apYb9vC0fCg",
        user_agent="android:com.example.myredditapp:v1.2.3 (by u/PitifulBook4011)",
    )

    posts = []
    ml_subreddit = reddit.subreddit('offmychest+relationships+amitheasshole')
    for post in ml_subreddit.top(time_filter='week', limit=10):
        posts.append(
            [post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posts = pd.DataFrame(posts, columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

    posts.to_csv('file1.csv')

    # posts.iloc[i][6]

    for t in range(10):
        parole = contatoreparole(posts.iloc[t][6])
        n = 0
        car = 0
        listastr = []
        listacaratteri = []
        while parole - n > 0:
            i = 0
            temp = posts.iloc[t][6][car:]
            listacaratteri.clear()
            for k in temp:
                if k == ' ':
                    n += 1
                    i += 1
                    if i == 45:
                        break
                car += 1
                listacaratteri.append(k)
            listastr.append(listacaratteri.copy())

        w = 0

        for p in listastr:
            x = "".join(p)
            w += 1
            tiktok.tts("f133bd730fc2e44ad33cf5bda762c6fc", "en_us_006", x, f'Post {t} - {w} .mp3', False)
            x = 0


if __name__ == "__main__":
    main()

# tiktok.tts("f133bd730fc2e44ad33cf5bda762c6fc","en_us_006",stringa,f'Post - 1 .mp3',False)
