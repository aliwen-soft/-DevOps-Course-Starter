class ApiException(Exception):
      def __init__(self, status, message):            
        super().__init__("API Error : " + message + " with status " + str(status))