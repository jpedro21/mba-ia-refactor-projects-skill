import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///tasks.db')
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', '5000'))

VALID_STATUSES = ['pending', 'in_progress', 'done', 'cancelled']
VALID_ROLES = ['user', 'admin', 'manager']
MIN_TITLE_LENGTH = 3
MAX_TITLE_LENGTH = 200
MIN_PASSWORD_LENGTH = 4
DEFAULT_PRIORITY = 3
DEFAULT_COLOR = '#000000'
