from datetime import timedelta

from flask import url_for

import pytest

from test_live_server import TestLiveServer

from app import app, db
from app.models import Post, User


class TestAnonymousUser(TestLiveServer):
    def test_no_posts_no_user(self, client):
        client.browser.get(client.get_server_url())
        self.wait_for_element(client, "nav-login-link", "Login")
        assert "Wolfit" in client.browser.title
        greeting = client.browser.find_element_by_id("nav-login-link").text
        assert "Login" in greeting

    def test_navigation_when_not_logged_in(self, client):
        client.browser.get(client.get_server_url())
        self.wait_for_element(client, "nav-login-link", "Login")
        nav = client.browser.find_element_by_id("nav-main").find_element_by_xpath(
            ".//a"
        )
        assert "index" in nav.get_attribute("href")
        nav = client.browser.find_element_by_id("nav-login").find_element_by_xpath(
            ".//a"
        )
        assert "login" in nav.get_attribute("href")

    def test_single_post_should_have_link_back_to_author(self, client, single_post):
        client.browser.get(client.get_server_url())
        self.wait_for_element(client, "post-0-link", single_post.title)
        post_link = client.browser.find_element_by_id("post-0-link")
        post_link.click()
        self.wait_for_element(client, "post-title", single_post.title)
        author_link = client.browser.find_element_by_id("author-link")
        assert single_post.author.username in author_link.text

    def test_posts_should_be_ordered_most_recent_first(
        self, client, test_user, single_post
    ):
        single_post.timestamp = single_post.timestamp - timedelta(days=1)
        db.session.add(single_post)
        db.session.commit()

        p = Post(title="Recent post", body="More current", user_id=test_user.id)
        db.session.add(p)
        db.session.commit()
        client.browser.get(client.get_server_url())
        self.wait_for_element(client, "nav-login-link", "Login")
        recent_post_link = client.browser.find_element_by_id("post-0-link")
        assert p.title in recent_post_link.text
