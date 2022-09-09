class DatabaseException(Exception):
      def __init__(self, status, message):            
        super().__init__("Database Error : " + message)