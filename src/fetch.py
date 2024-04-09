#!/usr/bin/env python3
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, UTC

app = Flask(__name__)
app.app_context().push()
app.config.from_prefixed_env()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///commits.sqlite3"

"""
Define the database model
that is used to store 
the github commits.
"""

db = SQLAlchemy(app)


def create_db():
    db.create_all()


class Commit(db.Model):
    __tablename__ = "commits"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sha = db.Column(db.String(40), nullable=False, unique=True)
    node_id = db.Column(db.Text, nullable=False)
    html_url = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    parent_sha = db.Column(db.String(40), nullable=True)
    commit_url = db.Column(db.Text, nullable=False)
    commit_author_name = db.Column(db.String(100), nullable=False)
    commit_author_email = db.Column(db.String(100), nullable=False)
    commit_author_datetime = db.Column(db.DateTime, nullable=False)
    commit_message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


"""
Helper function to save commits to the database
"""


def insert_commits(commits):
    commit_objects = []
    for commit in commits:
        c = Commit(
            sha=commit["sha"],
            node_id=commit["node_id"],
            url=commit["url"],
            parent_sha=commit["parents"][0]["sha"] if commit["parents"] else None,
            commit_url=commit["commit"]["url"],
            commit_author_name=commit["commit"]["author"]["name"],
            commit_author_email=commit["commit"]["author"]["email"],
            commit_author_datetime=datetime.strptime(
                commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ"
            ),
            commit_message=commit["commit"]["message"],
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        commit_objects.append(c)
    db.session.bulk_save_objects(commit_objects)
    db.session.commit()


"""
Helper function to get github commits
using API
"""


def get_github_commits():
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + app.config["GITHUB_API_TOKEN"],
        "X-GitHub-Api-Version": "2022-11-28",
    }
    # FIXME: hardcoded github repo `joshmedeski/dotfiles`
    response = requests.get(
        "https://api.github.com/repos/joshmedeski/dotfiles/commits", headers=headers
    )
    if response.status_code != 200:
        return None
    return response.json()


if __name__ == "__main__":
    create_db()
    recent_commits = get_github_commits()
    insert_commits(recent_commits)
    print("Commits saved to the database")
