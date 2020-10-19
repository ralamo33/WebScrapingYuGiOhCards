class ApiRequestError(Exception):
    def __init__(self, message=None):
        if not self.message:
            self.message = "The api request failed!"
        super().__init__(message)