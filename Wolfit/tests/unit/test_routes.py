import time
from datetime import datetime, timedelta

from flask import url_for

import pytest

from app import app, db
from app.models import ActivityLog, Category, Comment, Post, User

PASSWORD = "yoko"


def login(client, username, password):
    return client.post(
        url_for("login"),
        data=dict(username=username, password=password),
        follow_redirects=True,
    )


def logout(client):
    return client.get(url_for("logout"), follow_redirects=True)


def test_no_posts_no_user(client):
    """Start with a blank database."""

    response = client.get(url_for("index"))
    assert b"No entries" in response.data


def test_no_posts_logged_in_user(client, test_user):
    """
    Given a new system with just a registered user
    When the user logs in
    Then they should be greeted in person but see no posts
    """
    response = login(client, test_user.username, PASSWORD)
    assert response.status_code == 200
    assert b"No entries" in response.data
    assert b"john" in response.data


def test_index_should_have_link_to_more_when_beyond_post_limit(
    client, many_random_posts
):
    response = client.get(url_for("index"))
    assert b"index?page=2" in response.data


def test_should_be_anon_after_logout(client, test_user):
    """
    Given a new system with just a registered user
    When the user logs in then logs out
    Then the site should greet them as anonymous
    """
    response = login(client, test_user.username, PASSWORD)
    assert response.status_code == 200
    assert b"john" in response.data
    response = logout(client)
    assert b"Login" in response.data


def test_should_see_single_post(client, single_post):
    """
    Given there is a single post created
    When an anonymous user visits the site
    Then the user should see the post headline
    """
    response = client.get(url_for("index"))
    assert b"First post" in response.data
    assert b"Login" in response.data
    assert b"Older posts" not in response.data


def test_should_see_login_form_when_not_logged_in(client, single_post):
    response = client.get(url_for("login"))
    assert b"Sign In" in response.data
    assert b"Username" in response.data


def test_user_should_be_redirected_to_index_if_logged_in(client, test_user):
    login(client, test_user.username, PASSWORD)
    response = client.get(url_for("login"))
    assert response.status_code == 302
    assert "/index" in response.headers["Location"]


def test_bad_password_should_be_redirected_to_login(client, test_user):
    response = client.post(
        url_for("login"),
        data=dict(username=test_user.username, password="paul"),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_empty_post_should_be_redirected_to_login(client, test_user):
    response = client.post(url_for("login"), follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_there_should_be_a_place_for_new_users_to_register(client):
    response = client.post(url_for("register"))
    assert response.status_code == 200
    assert b"Register" in response.data


def test_should_be_a_link_to_register_if_not_logged_in(client):
    response = client.get(url_for("login"))
    assert b"Register" in response.data


def test_register_should_create_a_new_user(client):
    response = client.post(
        url_for("register"),
        data=dict(
            username="john",
            email="john@beatles.com",
            password=PASSWORD,
            password2=PASSWORD,
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    u = db.session.query(User).filter_by(username="john").one()
    assert u.email == "john@beatles.com"


def test_user_should_have_a_profile_page(client, test_user):
    login(client, test_user.username, PASSWORD)
    response = client.get(url_for("user", username=test_user.username))
    assert response.status_code == 200
    assert test_user.username.encode() in response.data


def test_profile_should_show_posts_for_that_user(
    client, test_user, single_post, random_post
):
    login(client, test_user.username, PASSWORD)
    response = client.get(url_for("user", username=test_user.username))
    assert single_post.title.encode() in response.data
    assert random_post.title.encode() not in response.data
    assert (
        url_for("post", post_id=single_post.id, _external=False).encode()
        in response.data
    )


def test_last_seen_should_update_automatically_when_login(client, test_user):
    # Load the user up and force the last seen info to last week
    test_user.last_seen = test_user.last_seen - timedelta(days=7)
    db.session.add(test_user)
    db.session.commit()

    login(client, test_user.username, PASSWORD)
    response = client.get(url_for("user", username=test_user.username))
    assert b"Last seen" in response.data
    # And since we just logged in, it should reflect today
    assert datetime.utcnow().strftime("%Y-%m-%d").encode() in response.data


def test_index_with_posts_should_have_links_to_details(client, single_post):
    response = client.get(url_for("index"))
    assert (
        url_for("post", post_id=single_post.id, _external=False).encode()
        in response.data
    )


def test_post_should_have_detail_page_with_body(client, single_post):
    response = client.get(url_for("post", post_id=single_post.id))
    assert single_post.body.encode() in response.data


def test_home_page_should_have_a_link_to_create_a_new_post(client, test_user):
    response = login(client, test_user.username, PASSWORD)
    assert b"Create Post" in response.data


def test_single_post_should_have_link_to_voting(client, test_user, single_post):
    response = client.get(url_for("index"))
    assert (
        url_for("up_vote", post_id=single_post.id, _external=False).encode()
        in response.data
    )
    assert (
        url_for("down_vote", post_id=single_post.id, _external=False).encode()
        in response.data
    )


def test_should_be_a_category_page_that_shows_posts(
    client, test_user, single_post, default_category, random_post
):
    response = client.get(url_for("category", title=default_category.title))
    assert single_post.title.encode() in response.data
    assert random_post.title.encode() in response.data
    assert (
        url_for("post", post_id=single_post.id, _external=False).encode()
        in response.data
    )


def test_comments_are_shown_after_post(client, test_user, single_post_with_comment):
    response = client.get(url_for("post", post_id=single_post_with_comment.id))
    assert single_post_with_comment.comments[0].body.encode() in response.data


def test_number_of_comments_for_posts_shown_on_list(client, test_user, single_post):
    single_post.add_comment("Important insight!", test_user)
    single_post.add_comment("Another insight!", test_user)
    response = client.get(url_for("index"))
    assert b"2 Comments" in response.data


def test_if_logged_in_can_comment_on_post(client, test_user, single_post):
    login(client, test_user.username, PASSWORD)
    response = client.get(url_for("post", post_id=single_post.id))
    assert f"Comment as {test_user.username}".encode() in response.data


def test_single_comment_should_have_link_to_voting(
    client, test_user, single_post_with_comment
):
    response = client.get(url_for("post", post_id=single_post_with_comment.id))
    comment = single_post_with_comment.comments[0]
    assert (
        url_for("up_vote_comment", comment_id=comment.id, _external=False).encode()
        in response.data
    )
    assert (
        url_for("down_vote_comment", comment_id=comment.id, _external=False).encode()
        in response.data
    )


def test_should_see_category_created_with_new_post_and_no_categories(client, test_user):
    login(client, test_user.username, PASSWORD)
    response = client.get(url_for("create_post"))
    assert response.status_code == 200
    categories = Category.query.order_by("title")
    assert categories.count() == 1


def test_new_post_should_create_activity_log(client, test_user, default_category):
    login(client, test_user.username, PASSWORD)
    title = "Logged post title"
    response = client.post(
        url_for("create_post"),
        data=dict(
            title=title, body="", category_id=default_category.id, user_id=test_user.id
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    e = ActivityLog.latest_entry()
    assert e is not None
    assert title in e.details
    assert test_user.id == e.user_id


def test_login_and_logout_create_activity_log(client, test_user):
    login(client, test_user.username, PASSWORD)
    e = ActivityLog.latest_entry()
    assert e is not None
    assert "Login" in e.details
    assert test_user.id == e.user_id
    logout(client)
    e = ActivityLog.latest_entry()
    assert e is not None
    assert "Logout" in e.details
    assert test_user.id == e.user_id


def test_category_page_should_have_link_to_create_post(
    client, test_user, default_category
):
    response = client.get(url_for("category", title=default_category.title))
    assert b"Create Post" in response.data


def test_create_post_should_ask_for_category(client, test_user, default_category):
    login(client, test_user.username, PASSWORD)
    response = client.get(url_for("create_post"))
    assert b"Category" in response.data


def test_link_posts_should_have_link_to_url(client, test_user):
    link_post = Post(
        title="Interesting link I found", link=True, url="http://example.com"
    )
    db.session.add(link_post)
    db.session.commit()
    response = client.get(url_for("post", post_id=link_post.id))
    assert link_post.url.encode() in response.data
