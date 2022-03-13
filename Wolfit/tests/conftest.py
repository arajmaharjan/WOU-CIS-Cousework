from random import randint
from os import environ, getcwd

import pytest

if 'WOLFIT_SETTINGS' not in environ:
    environ["WOLFIT_SETTINGS"] = f"{getcwd()}/test.settings"


from app import db
from app.models import Category, Comment, Post, User

USERNAME = "john"
PASSWORD = "yoko"


def make_test_user():
    u = User(username=USERNAME, email="john@beatles.com")
    u.set_password(PASSWORD)
    db.session.add(u)
    db.session.commit()
    return u


def make_default_category():
    category = None
    category = Category.query.filter_by(title="learnpython").first()
    if category is None:
        category = Category(title="learnpython")
        db.session.add(category)
        db.session.commit()
    return category


def make_single_post():
    user = db.session.query(User).filter_by(username=USERNAME).first()
    if user is None:
        user = make_test_user()
    p = Post(title="First post",
             body="Something saucy",
             user_id=user.id,
             category_id=make_default_category().id)
    db.session.add(p)
    db.session.commit()
    return p


def make_random_post():
    username = f"user-{randint(0, 999999)}"
    u = User(username=username, email=f"{username}@python.org")
    u.set_password('rando')
    db.session.add(u)
    db.session.commit()
    p = Post(title=f"Random post #{randint(0, 999999)}",
             body="Something very random",
             user_id=u.id,
             category_id=make_default_category().id)
    db.session.add(p)
    db.session.commit()
    return p


@pytest.fixture
def test_user():
    return make_test_user()


@pytest.fixture
def default_category():
    return make_default_category()


@pytest.fixture
def single_post():
    return make_single_post()


@pytest.fixture
def single_post_with_comment():
    p = make_single_post()
    p.add_comment("Important insight!", p.author)
    return p


@pytest.fixture
def random_post():
    return make_random_post()


@pytest.fixture
def many_random_posts():
    for _ in range(100):
        make_random_post()
