class CustomError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

    #def log_error(self):
    #    print(f"Error [{self.code}]: {self.args[0]}")