import praw
import pandas

def read_api_keys_from_file(file_path):
    with open(file_path, 'r') as keys_file:
        lines = keys_file.readlines()
        keys = []
        keys[0] = lines[0].rstrip()
        keys[1] = lines[1].rstrip()
    return keys


def from_reddit_to_posts(number_of_posts, csv_file=False, csv_file_name=None):  # if csv_file is True a csv file is created with posts info
    keys = read_api_keys_from_file("keys.txt")
    reddit = praw.Reddit(
        client_id=keys[0],
        client_secret=keys[1],
        user_agent="android:com.example.myredditapp:v1.2.3 (by u/PitifulBook4011)",
    )

    posts = []
    ml_subreddit = reddit.subreddit("offmychest+relationships+amitheasshole")
    for post in ml_subreddit.top(time_filter="week", limit=number_of_posts):
        posts.append(
            [post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posts = pandas.DataFrame(posts, columns=["title", "score", "id", "subreddit", "url", "num_comments", "body", "created"])

    if csv_file and csv_file_name:
        posts.to_csv(f'{csv_file_name}.csv')

    return posts
