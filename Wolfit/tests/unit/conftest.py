import os
import tempfile

import config

import pytest

from app import app, db


@pytest.fixture
def client():
    app.config.from_object(config.Config)
    app.config.from_envvar("WOLFIT_SETTINGS")
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SERVER_NAME"] = "test.local"
    client = app.test_client()
    db.session.close()
    db.drop_all()
    db.create_all()

    # Pushing the app context allows us to make calls to the app like url_for
    # as if we were the running Flask app. Makes testing routes more resiliant.
    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()
