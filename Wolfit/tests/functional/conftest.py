import multiprocessing
import os
import tempfile
import threading
import time

import config

import pytest

from selenium import webdriver

from app import app, db

PORT = "8080"


class LiveClient(object):
    def __init__(self):
        app.config.from_object(config.Config)
        app.config.from_envvar("WOLFIT_SETTINGS")
        app.config["WTF_CSRF_ENABLED"] = False

    def get_server_url(self):
        """
        Return the url of the test server
        """
        return f"http://localhost:{PORT}"

    def begin(self):
        db.session.close()
        db.drop_all()
        db.create_all()
        self.ctx = app.app_context()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("headless")
        self.browser = webdriver.Chrome(options=chrome_options)

        # Start Flask server in a thread
        threading.Thread(target=app.run, kwargs={'port': PORT}).start()
        time.sleep(0.5)
        self.ctx.push()

    def end(self):
        # remove application context
        self.ctx.pop()
        self.browser.get(f"{(self.get_server_url())}/shutdown")
        self.browser.quit()


@pytest.fixture(scope="module")
def client():
    return LiveClient()
