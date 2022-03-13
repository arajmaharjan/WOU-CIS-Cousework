import os

import config

from flask import Flask

from flask_bootstrap import Bootstrap

from flask_login import LoginManager

from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

from celery import Celery


app = Flask(__name__)
app.config.from_object(config.Config)
app.config.from_envvar('WOLFIT_SETTINGS')
app.config['SQLALCHEMY_DATABASE_URI'] = config.Config.DATABASE_URI(app)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

from app import models, routes
