import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(os.path.dirname(__file__), 'dev.db')

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)
