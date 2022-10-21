import os


class Config:
    def __init__(self):
        """Base configuration variables."""

        self.SECRET_KEY = os.environ.get('SECRET_TODO')

        self.DB_CONNECTION_STRING = os.environ.get('TODO_CONNECTION_STRING')

        self.DB_NAME = os.environ.get('TODO_DB_NAME')

        self.CLIENT_ID = os.environ.get('GH_CLIENT_ID')

        self.CLIENT_SECRET = os.environ.get('GH_CLIENT_SECRET')

        self.LOGIN_DISABLED = os.environ.get('LOGIN_DISABLED') == 'True'

        self.LOG_LEVEL = os.environ.get("LOG_LEVEL")

        self.LOGGLY_TOKEN = os.environ.get("LOGGLY_TOKEN")

        if not (self.DB_CONNECTION_STRING):
            raise ValueError(
                "Database string not set up. Did you follow the setup instructions?")

        if not (self.DB_NAME):
            raise ValueError(
                "Database name not set up. Did you follow the setup instructions?")
