class AppException(Exception):
    message = "Something went wrong"
    code = 500

    def __init__(self, **kwargs):
        self.message = kwargs.get("message", self.message)
        self.code = kwargs.get("code", self.code)
