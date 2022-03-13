import time

from flask import url_for

import pytest

from selenium.webdriver.common.keys import Keys

from test_live_server import TestLiveServer

from app import app, db
from app.models import Post, User

PASSWORD = "yoko"


class TestLoggedInUser(TestLiveServer):
    def login(self, client, test_user):
        client.browser.get(client.get_server_url())
        self.wait_for_element(client, "nav-login", "Login")
        login_link = client.browser.find_element_by_id("nav-login-link")
        login_link.click()
        self.wait_for_element(client, "remember_me", "")
        login_name = client.browser.find_element_by_id("username")
        login_name.send_keys(test_user.username)
        password = client.browser.find_element_by_id("password")
        password.send_keys("yoko")
        password.send_keys(Keys.ENTER)
        self.wait_for_element(client, "user-greeting", test_user.username)

    def test_create_new_post(self, client, test_user, default_category):
        body = ("Start of the body\n"
                "\n"
                "* Bullet 1\n"
                "* [Bullet 2](http://example.com)\n"
                "\n")
        self.login(client, test_user)
        create_post_link = client.browser.find_element_by_id("create-post-link")
        create_post_link.click()
        self.wait_for_element(client, "page-title", "Create Post")
        post_title = client.browser.find_element_by_id("title")
        post_title.send_keys("My Post Title")
        post_body = client.browser.find_element_by_id("body")
        post_body.send_keys(body)
        post_post = client.browser.find_element_by_id("submit")
        post_post.click()
