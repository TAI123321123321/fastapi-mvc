from app.utils.api_exception import ApiException


class AppException(ApiException):
    """Base class for all exceptions in the app."""

    def __init__(self, message: str, status_code: int = 500, payload=None):
        super().__init__(message=message, status_code=status_code, payload=payload)