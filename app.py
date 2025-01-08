import os
import praw
import datetime
import json
from pprint import pp
from dotenv import load_dotenv

load_dotenv()
    

reddit = praw.Reddit(
    client_id = os.getenv("PRAW_CLIENT_ID"),
    client_secret = os.getenv("PRAW_CLIENT_SECRET"),
    user_agent = os.getenv("PRAW_USER_AGENT"),
)


def get_chunk(last_elem):
    pass


def get_posts(date_from: datetime, date_to: datetime, limit: int = 100):
    total_posts = [
        post for post in reddit.subreddit("trees").new(limit=limit)
        if datetime.datetime.fromtimestamp(post.created_utc, datetime.UTC) > date_from
    ]

    while total_posts and not (len(total_posts) % limit):
        last_post_time = datetime.datetime.fromtimestamp(total_posts[-1].created_utc, datetime.UTC)
        print(f'len(total_posts) == {len(total_posts)}, last: {last_post_time}')

        next_posts = [
            post for post in reddit.subreddit("trees").new(limit=limit, params={'after': total_posts[-1].fullname})
            if datetime.datetime.fromtimestamp(post.created_utc, datetime.UTC) > date_from
        ]

        total_posts += next_posts

        if len(total_posts)%1000 == 0:
            index = len(total_posts)//1000
            with open(f'file{index}.json') as f:
                f.write(json.dumps(total_posts[index:index+1000]))

    posts = [
        {
            'url': post.url,
            'title': post.title,
            'author': f'/u/{post.author.name}',
            'score': post.score,
            'num_comments': post.num_comments,
        }
        for post in total_posts
    ]

    return posts


if __name__ == '__main__':
    posts = get_posts(
        date_from = datetime.datetime(2024, 12, 20, 0, 0, 0, 0, datetime.UTC), 
        date_to   = datetime.datetime(2024, 12, 30, 0, 0, 0, 0, datetime.UTC)
    )

    print(len(posts))

