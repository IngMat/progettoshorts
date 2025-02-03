import praw
import pandas as pd


def read_api_keys_from_file(file_path):
    # Reads the API keys from a text file and returns the client_id and client_secret
    with open(file_path, 'r') as keys_file:
        lines = keys_file.readlines()
        keys = [lines[0].rstrip(), lines[1].rstrip()]
    return keys


def from_reddit_to_posts(number_of_posts, csv_file=False, csv_file_name=None):
    # Fetches top posts from specific Reddit communities and returns them as a DataFrame
    # If csv_file is True a csv file is created with posts info

    keys = read_api_keys_from_file("keys.txt")

    # Create a Reddit instance with API credentials
    reddit = praw.Reddit(
        client_id=keys[0],
        client_secret=keys[1],
        user_agent="android:com.example.myredditapp:v1.2.3 (by u/PitifulBook4011)",
    )

    # Create a Pandas DataFrame with Reddit posts
    posts = []
    ml_subreddit = reddit.subreddit("offmychest%2Brelationships%2Bamitheasshole")
    for post in ml_subreddit.top(time_filter="week", limit=number_of_posts):
        posts.append(
            [post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posts = pd.DataFrame(posts, columns=["title", "score", "id", "subreddit", "url", "num_comments", "body", "created"])

    # Save DataFrame to CSV if requested
    if csv_file and csv_file_name:
        posts.to_csv(f'{csv_file_name}.csv')

    return posts
