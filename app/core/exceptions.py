class AuthException(Exception):
    def __init__(self, message: str, status_code: int = 401, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class ValidationException(Exception):
    def __init__(self, message: str, errors: list = None):
        self.message = message
        self.errors = errors or []
        super().__init__(self.message)


class NotFoundException(Exception):
    def __init__(self, message: str, error_code: str = "NOT_FOUND"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ConflictException(Exception):
    def __init__(self, message: str, error_code: str = "CONFLICT"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class RateLimitException(Exception):
    def __init__(self, message: str, retry_after: int = 60):
        self.message = message
        self.retry_after = retry_after
        super().__init__(self.message)