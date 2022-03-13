import argparse
from datetime import datetime
from random import randint

import praw

from app import app, config, db
from app.models import Category, Post, User

parser = argparse.ArgumentParser(description='Load posts from a subreddit.')
parser.add_argument('subreddit', metavar='subreddit', nargs='?', default='learnpython',
                    help='the subreddit to load (default is learnpython')
args = parser.parse_args()
subreddit = args.subreddit

app.config.from_object(config.Config)
app.config.from_envvar('WOLFIT_SETTINGS')


def create_user(subreddit):
    username = f"{subreddit}-{randint(0, 999999)}"
    u = User(username=username, email=f"{username}@example.com")
    u.set_password('wolfit')
    db.session.add(u)
    db.session.commit()
    return u


def create_category(subreddit):
    category = None
    category = Category.query.filter_by(title=subreddit).first()
    if category is None:
        category = Category(title=subreddit)
        db.session.add(category)
        db.session.commit()
    return category


reddit = praw.Reddit()

u = create_user(subreddit)
c = create_category(subreddit)

for submission in reddit.subreddit(subreddit).hot(limit=100):
    # We may have already loaded this post, so check title
    existing = Post.query.filter_by(title=submission.title).first()
    if existing is None:
        link = False
        url = None
        if ('reddit.com' not in submission.url):
            link = True
            url = submission.url

        p = Post(title=submission.title,
                 body=submission.selftext,
                 timestamp=datetime.utcfromtimestamp(submission.created_utc),
                 vote_count=0,
                 link=link,
                 url=url,
                 user_id=u.id,
                 category_id=c.id)
        print(f"Creating post: {p} with url {p.url} in {c.title}")
        db.session.add(p)
        db.session.commit()
