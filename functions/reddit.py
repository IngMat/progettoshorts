import praw
import pandas


def from_reddit_to_posts(number_of_posts, csv_file=False, csv_file_name=None):  # if csv_file is True a csv file is created with posts info
    reddit = praw.Reddit(
        client_id="HU4BpzSxzqNStBb3X-lfeQ",
        client_secret="l_-UaJpNj6BpTUyMm-8apYb9vC0fCg",
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
