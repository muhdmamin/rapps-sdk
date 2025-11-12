class SDKError(Exception):
    """Base SDK error."""
    pass

class APIError(SDKError):
    """General API error with details."""
    def __init__(self, status: int, code: str | None, message: str, *, request_id: str | None):
        super().__init__(f"{status} {code or ''} {message}".strip())
        self.status, self.code, self.message, self.request_id = status, code, message, request_id

class RateLimitError(APIError):
    """when rate limiting occurs."""
    pass

class AuthError(APIError):
    """for authentication errors."""
    pass
