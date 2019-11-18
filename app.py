import praw
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config

APP = Flask(__name__)
APP.config["SQLALCHEMY_DATABASE_URI"] = config("DATABASE_URL")

DB = SQLAlchemy(APP)

class RedditPost(DB.Model):
    id = DB.Column(DB.String(10), primary_key=True)
    text = DB.Column(DB.Text(), nullable=False)
    subreddit = DB.Column(DB.Text(), nullable=False)

class SubReddit(DB.Model):
    id = DB.Column(DB.Text(), primary_key=True)
    name = DB.Column(DB.Text(), nullable=False)

DB.drop_all()
DB.create_all()

REDDIT = praw.Reddit(client_id=config("CLIENT_ID"),
                     client_secret=config("CLIENT_SECRET"),
                     user_agent=config("USER_AGENT"))
TOP_LIMIT=50

subreddits = REDDIT.subreddits.popular(limit=TOP_LIMIT)
for subreddit in subreddits.__iter__():
    print(subreddit.display_name)
    db_subreddit = SubReddit(id=subreddit.id, name=subreddit.display_name)
    DB.session.add(db_subreddit)
    hot_posts = subreddit.hot()
    for post in hot_posts.__iter__():
        db_post = RedditPost(id=post.id, text=post.title, subreddit=subreddit.id)
        DB.session.add(db_post)



DB.session.commit()


