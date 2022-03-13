import os


class Config(object):

    @classmethod
    def DATABASE_URI(cls, app):
        db_path = os.path.join(os.path.dirname(__file__),
                               app.config['BLOG_DATABASE_NAME'])
        db_uri = f"sqlite:///{db_path}"
        return db_uri

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 10
