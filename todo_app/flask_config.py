import os
from re import S


class Config:
    def __init__(self):
        """Base configuration variables."""

        self.DB_CONNECTION_STRING = os.environ.get('TODO_CONNECTION_STRING')
     
        self.DB_NAME = os.environ.get('TODO_DB_NAME')
        
        self.CLIENT_ID = os.environ.get('GH_CLIENT_ID')

        if not (self.DB_CONNECTION_STRING and self.DB_NAME):
            raise ValueError(
                "Database secrets secrets not set up. Did you follow the setup instructions?")
