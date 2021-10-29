import os

class Config:
    def __init__(self):
        """Base configuration variables."""
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
       
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")

        self.TRELLO_BOARD_ID = os.environ.get('TRELLO_BOARD_ID')

        self.TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
     
        self.TRELLO_API_TOKEN = os.environ.get('TRELLO_API_TOKEN')
        
        if not (self.TRELLO_BOARD_ID and self.TRELLO_API_KEY and self.TRELLO_API_TOKEN) :
            raise ValueError("Trello secrets not set up. Did you follow the setup instructions?")


 
